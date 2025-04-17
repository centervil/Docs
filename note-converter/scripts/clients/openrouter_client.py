"""
OpenRouter APIクライアント

OpenRouter APIと通信するためのクライアントクラスを提供します。
"""
import json
import logging
import requests
from typing import Dict, Any, List, Optional

# ロガーの設定
logger = logging.getLogger(__name__)

class OpenRouterClient:
    """OpenRouter APIとの通信を行うクライアントクラス"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初期化

        Args:
            config: APIの設定情報
                - api_key: OpenRouter APIキー
                - model: 使用するモデル名
                - max_tokens: 生成する最大トークン数
                - temperature: 生成の温度
                - http_proxy: HTTPプロキシ (任意)
                - https_proxy: HTTPSプロキシ (任意)
        """
        self.api_key = config.get("api_key")
        self.model = config.get("model", "openai/gpt-3.5-turbo")
        self.max_tokens = config.get("max_tokens", 1500)
        self.temperature = config.get("temperature", 0.7)
        
        # プロキシの設定
        self.proxies = {}
        if config.get("http_proxy"):
            self.proxies["http"] = config["http_proxy"]
        if config.get("https_proxy"):
            self.proxies["https"] = config["https_proxy"]
        
        # APIのエンドポイント
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # ヘッダーの設定
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://note-converter.example.com",  # あなたのウェブサイトURLに変更してください
            "X-Title": "Note Converter"  # あなたのアプリケーション名
        }
        
        logger.info(f"OpenRouterClient initialized with model: {self.model}")
    
    def chat_completion(self, messages: List[Dict[str, str]], 
                        max_tokens: Optional[int] = None, 
                        temperature: Optional[float] = None) -> Dict[str, Any]:
        """
        チャット完了APIを呼び出す

        Args:
            messages: メッセージのリスト (例: [{"role": "user", "content": "こんにちは"}])
            max_tokens: 生成する最大トークン数 (指定しない場合はコンストラクタで設定した値を使用)
            temperature: 生成の温度 (指定しない場合はコンストラクタで設定した値を使用)

        Returns:
            APIレスポンス
            
        Raises:
            Exception: API呼び出しに失敗した場合
        """
        try:
            # リクエストパラメータの設定
            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens if max_tokens is not None else self.max_tokens,
                "temperature": temperature if temperature is not None else self.temperature
            }
            
            logger.debug(f"Sending request to OpenRouter API: {json.dumps(payload, ensure_ascii=False)}")
            
            # APIリクエスト
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                proxies=self.proxies if self.proxies else None
            )
            
            # レスポンスの確認
            response.raise_for_status()
            result = response.json()
            
            logger.debug(f"Received response from OpenRouter API: {json.dumps(result, ensure_ascii=False)}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling OpenRouter API: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response: {e.response.text}")
            raise Exception(f"OpenRouter API呼び出しエラー: {str(e)}")
    
    def process_with_llm(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        LLMを使用してテキストを処理する

        Args:
            prompt: ユーザープロンプト
            system_prompt: システムプロンプト (指定しない場合はデフォルトのものを使用)

        Returns:
            LLMからの応答テキスト
            
        Raises:
            Exception: API呼び出しに失敗した場合
        """
        if not system_prompt:
            system_prompt = "あなたは役立つAIアシスタントです。与えられたテキストを適切に処理してください。"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        result = self.chat_completion(messages)
        
        try:
            # 応答テキストの抽出
            response_text = result["choices"][0]["message"]["content"]
            return response_text
        except (KeyError, IndexError) as e:
            logger.error(f"Error parsing OpenRouter API response: {str(e)}")
            logger.error(f"Response: {json.dumps(result, ensure_ascii=False)}")
            raise Exception("OpenRouter APIレスポンスの解析エラー")
    
    def test_connection(self) -> bool:
        """
        API接続テスト

        Returns:
            接続成功の場合はTrue、失敗の場合はFalse
        """
        try:
            result = self.process_with_llm("こんにちは。簡単な接続テストです。「接続OK」と返してください。")
            logger.info(f"OpenRouter API connection test result: {result}")
            return "接続OK" in result
        except Exception as e:
            logger.error(f"OpenRouter API connection test failed: {str(e)}")
            return False 