"""
OpenRouter APIクライアントモジュールのユニットテスト
"""
import os
import sys
import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock

# プロジェクトルートへのパスを取得し、それをimportパスに追加
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

# まだ実装されていないモジュールをインポート
try:
    from scripts.openrouter_client import (
        OpenRouterClient,
        OpenRouterAPIError,
        OpenRouterRateLimitError,
        OpenRouterAuthError
    )
except ImportError:
    # テスト実行時にはまだインポートできないので、テストだけ記述
    pass


class TestOpenRouterClient:
    """OpenRouter APIクライアントのテストクラス"""
    
    @pytest.fixture
    def sample_api_key(self):
        """テスト用のAPIキー"""
        return "test_api_key_123456789"
    
    @pytest.fixture
    def sample_prompt(self):
        """テスト用のプロンプト"""
        return "研究資料をnote記事に変換してください"
    
    @pytest.fixture
    def sample_config(self):
        """テスト用の設定"""
        return {
            "model": "anthropic/claude-3.5-sonnet",
            "max_tokens": 4096,
            "temperature": 0.7,
            "top_p": 0.9,
            "http_proxy": None,
            "https_proxy": None,
            "retry_count": 3,
            "retry_delay": 2
        }
    
    @pytest.fixture
    def sample_response(self):
        """テスト用のレスポンス"""
        return {
            "id": "gen-abc123xyz456",
            "object": "completion",
            "created": 1683920500,
            "model": "anthropic/claude-3.5-sonnet",
            "choices": [
                {
                    "text": "# タイトル\n\n## はじめに\nこれはLLMが生成したnote記事のサンプルです。\n\n## 本文\nここに本文が入ります。\n\n## まとめ\n要点をまとめました。",
                    "index": 0,
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 150,
                "completion_tokens": 100,
                "total_tokens": 250
            }
        }
    
    @pytest.fixture
    def client(self, sample_api_key, sample_config):
        """テスト用のクライアントインスタンス"""
        return OpenRouterClient(api_key=sample_api_key, **sample_config)
    
    def test_init(self, sample_api_key, sample_config):
        """初期化のテスト"""
        client = OpenRouterClient(api_key=sample_api_key, **sample_config)
        
        # 属性が正しく設定されていることを確認
        assert client.api_key == sample_api_key
        assert client.model == sample_config["model"]
        assert client.max_tokens == sample_config["max_tokens"]
        assert client.temperature == sample_config["temperature"]
        assert client.top_p == sample_config["top_p"]
        assert client.retry_count == sample_config["retry_count"]
        assert client.retry_delay == sample_config["retry_delay"]
    
    def test_init_default_values(self, sample_api_key):
        """デフォルト値での初期化テスト"""
        client = OpenRouterClient(api_key=sample_api_key)
        
        # デフォルト値が設定されていることを確認
        assert client.api_key == sample_api_key
        assert client.model == "anthropic/claude-3.5-sonnet"  # デフォルトモデル
        assert client.max_tokens == 4096  # デフォルトトークン数
        assert client.temperature == 0.7  # デフォルト温度
        assert client.retry_count == 3  # デフォルトリトライ回数
    
    def test_init_missing_api_key(self):
        """APIキーなしでの初期化テスト"""
        with pytest.raises(ValueError) as excinfo:
            OpenRouterClient(api_key=None)
        
        assert "API key is required" in str(excinfo.value)
    
    @patch("requests.post")
    def test_generate_text(self, mock_post, client, sample_prompt, sample_response):
        """テキスト生成のテスト"""
        # リクエストのモック設定
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_response
        mock_post.return_value = mock_response
        
        # メソッド呼び出し
        result = client.generate_text(sample_prompt)
        
        # 正しいエンドポイントにリクエストが送信されたか確認
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert args[0] == "https://openrouter.ai/api/v1/chat/completions"
        
        # ヘッダーに認証情報が含まれているか確認
        headers = kwargs["headers"]
        assert "Authorization" in headers
        assert headers["Authorization"] == f"Bearer {client.api_key}"
        
        # リクエストボディが正しいか確認
        body = json.loads(kwargs["data"])
        assert "model" in body
        assert body["model"] == client.model
        assert "messages" in body
        assert len(body["messages"]) == 1
        assert body["messages"][0]["role"] == "user"
        assert body["messages"][0]["content"] == sample_prompt
        
        # レスポンスが正しく解析されているか確認
        assert result == sample_response["choices"][0]["text"]
    
    @patch("requests.post")
    def test_generate_text_rate_limit_error(self, mock_post, client, sample_prompt):
        """レートリミットエラーのテスト"""
        # レートリミットエラーのモック設定
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.json.return_value = {"error": "Too many requests"}
        mock_post.return_value = mock_response
        
        # エラーが発生することを確認
        with pytest.raises(OpenRouterRateLimitError) as excinfo:
            client.generate_text(sample_prompt)
        
        assert "Rate limit exceeded" in str(excinfo.value)
    
    @patch("requests.post")
    def test_generate_text_auth_error(self, mock_post, client, sample_prompt):
        """認証エラーのテスト"""
        # 認証エラーのモック設定
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Invalid API key"}
        mock_post.return_value = mock_response
        
        # エラーが発生することを確認
        with pytest.raises(OpenRouterAuthError) as excinfo:
            client.generate_text(sample_prompt)
        
        assert "Authentication failed" in str(excinfo.value)
    
    @patch("requests.post")
    def test_generate_text_server_error(self, mock_post, client, sample_prompt):
        """サーバーエラーのテスト"""
        # サーバーエラーのモック設定
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "Server error"}
        mock_post.return_value = mock_response
        
        # エラーが発生することを確認
        with pytest.raises(OpenRouterAPIError) as excinfo:
            client.generate_text(sample_prompt)
        
        assert "API error" in str(excinfo.value)
    
    @patch("requests.post")
    def test_generate_text_retry_success(self, mock_post, client, sample_prompt, sample_response):
        """リトライ成功のテスト"""
        # 最初は失敗、2回目は成功するレスポンスのモック設定
        error_response = MagicMock()
        error_response.status_code = 500
        error_response.json.return_value = {"error": "Server error"}
        
        success_response = MagicMock()
        success_response.status_code = 200
        success_response.json.return_value = sample_response
        
        mock_post.side_effect = [error_response, success_response]
        
        # テスト実行（2回目のリクエストで成功することを期待）
        with patch("time.sleep", return_value=None):  # sleep関数をモック化
            result = client.generate_text(sample_prompt)
        
        # 2回呼び出されたことを確認
        assert mock_post.call_count == 2
        
        # レスポンスが正しく解析されているか確認
        assert result == sample_response["choices"][0]["text"]
    
    def test_format_prompt(self, client):
        """プロンプトフォーマットのテスト"""
        markdown_content = "# タイトル\n\n## セクション1\nこれは内容です。"
        template = "研究資料を元にnote記事を作成してください。"
        
        result = client.format_prompt(markdown_content, template)
        
        # テンプレートと内容が含まれているか確認
        assert template in result
        assert markdown_content in result
        assert "以下の研究資料" in result or "研究資料:" in result
    
    def test_check_token_limit(self, client):
        """トークン制限チェックのテスト"""
        # 長すぎるコンテンツ（実際には文字数ではなくトークン数をチェックする）
        long_content = "a" * 150000  # 十分に長いコンテンツ
        
        with pytest.raises(ValueError) as excinfo:
            client.check_token_limit(long_content)
        
        assert "exceeds token limit" in str(excinfo.value)
    
    def test_extract_content_from_response(self, client, sample_response):
        """レスポンスからコンテンツを抽出するテスト"""
        # 様々なレスポンス形式をテスト
        
        # Claude形式
        claude_response = {
            "choices": [{"text": "生成されたテキスト"}]
        }
        
        assert client.extract_content_from_response(claude_response) == "生成されたテキスト"
        
        # GPT形式
        gpt_response = {
            "choices": [{"message": {"content": "生成されたテキスト"}}]
        }
        
        assert client.extract_content_from_response(gpt_response) == "生成されたテキスト"
        
        # 未知の形式
        unknown_response = {"result": "生成されたテキスト"}
        
        with pytest.raises(KeyError) as excinfo:
            client.extract_content_from_response(unknown_response)
        
        assert "Unable to extract content" in str(excinfo.value) 