"""
OpenRouter APIクライアント

OpenRouter APIとの通信を行い、LLMによるテキスト生成を行うモジュール
"""
import os
import requests
import json
import time
import logging
from typing import Dict, List, Any, Optional, Union

# ロガーの設定
logger = logging.getLogger(__name__)

class OpenRouterAPIError(Exception):
    """OpenRouter API呼び出し時の一般的なエラー"""
    pass

class OpenRouterRateLimitError(OpenRouterAPIError):
    """レートリミット超過エラー"""
    pass

class OpenRouterAuthError(OpenRouterAPIError):
    """認証エラー"""
    pass

class OpenRouterClient:
    """
    OpenRouter APIクライアント
    
    OpenRouter APIを使用してLLMによるテキスト生成を行うクラス
    """
    
    # OpenRouter APIエンドポイント
    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    
    def __init__(
        self, 
        api_key: str,
        model: str = "anthropic/claude-3.5-sonnet",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        top_p: float = 0.9,
        http_proxy: Optional[str] = None,
        https_proxy: Optional[str] = None,
        retry_count: int = 3,
        retry_delay: int = 2
    ):
        """
        初期化
        
        Args:
            api_key: OpenRouter API キー
            model: 使用するモデル名
            max_tokens: 最大トークン数
            temperature: 生成の温度（高いほどランダム性が増す）
            top_p: 使用する確率分布の上位割合
            http_proxy: HTTPプロキシ
            https_proxy: HTTPSプロキシ
            retry_count: リトライ回数
            retry_delay: リトライ間隔（秒）
        
        Raises:
            ValueError: APIキーが指定されていない場合
        """
        if not api_key:
            raise ValueError("API key is required")
        
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.http_proxy = http_proxy
        self.https_proxy = https_proxy
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        
        # プロキシ設定
        self.proxies = {}
        if http_proxy:
            self.proxies['http'] = http_proxy
        if https_proxy:
            self.proxies['https'] = https_proxy
    
    def generate_text(self, prompt: str) -> str:
        """
        テキストを生成
        
        Args:
            prompt: 生成のためのプロンプト
        
        Returns:
            生成されたテキスト
        
        Raises:
            OpenRouterAuthError: 認証エラーが発生した場合
            OpenRouterRateLimitError: レートリミットを超過した場合
            OpenRouterAPIError: その他のAPIエラーが発生した場合
        """
        # トークン制限のチェック
        self.check_token_limit(prompt)
        
        # リクエストヘッダー
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://note.com"  # リファラー設定
        }
        
        # リクエストボディ
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p
        }
        
        # リトライを含めたリクエスト処理
        response_data = None
        retry_count = 0
        
        while retry_count <= self.retry_count:
            try:
                logger.debug(f"Sending request to OpenRouter API (attempt {retry_count + 1})")
                response = requests.post(
                    self.API_URL,
                    headers=headers,
                    data=json.dumps(payload),
                    proxies=self.proxies if self.proxies else None
                )
                
                # ステータスコードの処理
                if response.status_code == 200:
                    response_data = response.json()
                    break
                elif response.status_code == 401:
                    raise OpenRouterAuthError(f"Authentication failed: {response.text}")
                elif response.status_code == 429:
                    raise OpenRouterRateLimitError(f"Rate limit exceeded: {response.text}")
                else:
                    # サーバーエラーなどのリトライ可能なエラー
                    if retry_count < self.retry_count:
                        retry_count += 1
                        logger.warning(f"API error (status {response.status_code}), retrying in {self.retry_delay} seconds")
                        time.sleep(self.retry_delay)
                    else:
                        raise OpenRouterAPIError(f"API error (status {response.status_code}): {response.text}")
            
            except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
                # ネットワークエラーやJSONデコードエラー
                if retry_count < self.retry_count:
                    retry_count += 1
                    logger.warning(f"Request error: {str(e)}, retrying in {self.retry_delay} seconds")
                    time.sleep(self.retry_delay)
                else:
                    raise OpenRouterAPIError(f"Failed to connect to OpenRouter API: {str(e)}")
        
        if not response_data:
            raise OpenRouterAPIError("No response data received after retries")
        
        # レスポンスからコンテンツを抽出
        return self.extract_content_from_response(response_data)
    
    def format_prompt(self, markdown_content: str, template: str) -> str:
        """
        プロンプトをフォーマット
        
        マークダウンコンテンツとテンプレートを組み合わせてLLM用のプロンプトを生成
        
        Args:
            markdown_content: マークダウンコンテンツ
            template: プロンプトテンプレート
        
        Returns:
            フォーマットされたプロンプト
        """
        formatted_prompt = f"{template}\n\n以下の研究資料をもとに記事を作成してください:\n\n```markdown\n{markdown_content}\n```"
        return formatted_prompt
    
    def check_token_limit(self, content: str) -> None:
        """
        コンテンツのトークン制限をチェック
        
        Args:
            content: チェックするコンテンツ
        
        Raises:
            ValueError: トークン制限を超えた場合
        """
        # 簡易的なトークン数の見積もり（実際はもっと複雑だが、ここでは簡略化）
        estimated_tokens = len(content) // 4  # 大まかに4文字で1トークンと仮定
        
        # APIリクエストにおける最大トークン数制限（入力＋出力合計）
        max_allowed_tokens = 32000  # テスト用に小さい値に設定
        
        if estimated_tokens > max_allowed_tokens:
            raise ValueError(f"Input content exceeds token limit ({estimated_tokens} > {max_allowed_tokens})")
    
    def extract_content_from_response(self, response: Dict[str, Any]) -> str:
        """
        レスポンスからコンテンツを抽出
        
        Args:
            response: APIレスポンス
        
        Returns:
            抽出されたコンテンツ
        
        Raises:
            KeyError: レスポンス形式が不明な場合
        """
        # レスポンス形式のチェック
        if "choices" in response and len(response["choices"]) > 0:
            choice = response["choices"][0]
            
            # Claude形式（OpenRouterで実際に返される形式）
            if "text" in choice:
                return choice["text"]
            
            # GPT形式
            elif "message" in choice and "content" in choice["message"]:
                return choice["message"]["content"]
        
        # 未知の形式
        raise KeyError(f"Unable to extract content from response: {response}") 