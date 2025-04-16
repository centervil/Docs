"""
note.com APIクライアントモジュールのユニットテスト
"""
import os
import sys
import pytest
import json
import re
from pathlib import Path
from unittest.mock import patch, MagicMock, Mock

# プロジェクトルートへのパスを取得し、それをimportパスに追加
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

# まだ実装されていないモジュールをインポート
try:
    from scripts.note_api_client import (
        NoteApiClient,
        NoteApiError,
        NoteApiAuthError,
        NoteApiRateLimitError
    )
except ImportError:
    # テスト実行時にはまだインポートできないので、テストだけ記述
    pass


class TestNoteApiClient:
    """note.com APIクライアントのテストクラス"""
    
    @pytest.fixture
    def sample_username(self):
        """テスト用のユーザー名"""
        return "test_user"
    
    @pytest.fixture
    def sample_password(self):
        """テスト用のパスワード"""
        return "test_password"
    
    @pytest.fixture
    def sample_config(self):
        """テスト用の設定"""
        return {
            "http_proxy": None,
            "https_proxy": None,
            "retry_count": 3,
            "retry_delay": 2,
            "session_timeout": 86400  # 24時間（秒）
        }
    
    @pytest.fixture
    def sample_session(self):
        """テスト用のセッション情報"""
        return {
            "session_id": "test_session_123456789",
            "csrf_token": "test_csrf_token_123456789",
            "expires_at": 1683920500 + 86400  # 現在時刻 + 24時間
        }
    
    @pytest.fixture
    def sample_post_data(self):
        """テスト用の投稿データ"""
        return {
            "title": "テスト記事",
            "body": "<h1>テスト記事</h1><p>これはテスト記事です。</p>",
            "tags": ["テスト", "API"],
            "status": "draft"
        }
    
    @pytest.fixture
    def sample_post_response(self):
        """テスト用の投稿レスポンス"""
        return {
            "id": "note123456789",
            "status": "draft",
            "url": "https://note.com/test_user/n/note123456789",
            "title": "テスト記事",
            "body": "<h1>テスト記事</h1><p>これはテスト記事です。</p>",
            "created_at": "2025-04-15T12:00:00+09:00"
        }
    
    @pytest.fixture
    def client(self, sample_username, sample_password, sample_config):
        """テスト用のクライアントインスタンス"""
        return NoteApiClient(username=sample_username, password=sample_password, **sample_config)
    
    def test_init(self, sample_username, sample_password, sample_config):
        """初期化のテスト"""
        client = NoteApiClient(username=sample_username, password=sample_password, **sample_config)
        
        # 属性が正しく設定されていることを確認
        assert client.username == sample_username
        assert client.password == sample_password
        assert client.retry_count == sample_config["retry_count"]
        assert client.retry_delay == sample_config["retry_delay"]
        assert client.session_timeout == sample_config["session_timeout"]
        assert client.session is None
        assert client.csrf_token is None
        assert client.session_expires_at is None
    
    def test_init_missing_credentials(self):
        """認証情報なしでの初期化テスト"""
        with pytest.raises(ValueError) as excinfo:
            NoteApiClient(username=None, password="test")
        
        assert "Username is required" in str(excinfo.value)
        
        with pytest.raises(ValueError) as excinfo:
            NoteApiClient(username="test", password=None)
        
        assert "Password is required" in str(excinfo.value)
    
    @patch("requests.Session")
    def test_login(self, mock_session, client):
        """ログインのテスト"""
        # セッションのモック
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance
        
        # CSRFトークン取得ページのレスポンス
        mock_get_response = MagicMock()
        mock_get_response.text = '<meta name="csrf-token" content="test_csrf_token_123456789">'
        mock_session_instance.get.return_value = mock_get_response
        
        # ログインAPIのレスポンス
        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {"user": {"id": "user123"}}
        mock_session_instance.post.return_value = mock_post_response
        
        # クッキー設定のモック
        mock_session_instance.cookies = {"note_session": "test_session_cookie"}
        
        # ログイン実行
        client.login()
        
        # セッションが作成されたか確認
        assert client.session is not None
        # CSRFトークンが取得されたか確認
        assert client.csrf_token == "test_csrf_token_123456789"
        # セッション有効期限が設定されたか確認
        assert client.session_expires_at is not None
        
        # ログインAPIが呼ばれたか確認
        mock_session_instance.post.assert_called_once()
        args, kwargs = mock_session_instance.post.call_args
        assert args[0] == "https://note.com/api/v1/login"
        
        # リクエストボディに認証情報が含まれているか確認
        body = kwargs["json"]
        assert body["login_id"] == client.username
        assert body["password"] == client.password
    
    @patch("requests.Session")
    def test_login_failure(self, mock_session, client):
        """ログイン失敗のテスト"""
        # セッションのモック
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance
        
        # CSRFトークン取得ページのレスポンス
        mock_get_response = MagicMock()
        mock_get_response.text = '<meta name="csrf-token" content="test_csrf_token_123456789">'
        mock_session_instance.get.return_value = mock_get_response
        
        # ログイン失敗のレスポンス
        mock_post_response = MagicMock()
        mock_post_response.status_code = 401
        mock_post_response.json.return_value = {"error": "Invalid credentials"}
        mock_session_instance.post.return_value = mock_post_response
        
        # ログイン失敗のテスト
        with pytest.raises(NoteApiAuthError) as excinfo:
            client.login()
        
        assert "Login failed" in str(excinfo.value)
    
    @patch("requests.Session")
    def test_login_csrf_token_not_found(self, mock_session, client):
        """CSRFトークンが見つからない場合のテスト"""
        # セッションのモック
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance
        
        # CSRFトークンが含まれないレスポンス
        mock_get_response = MagicMock()
        mock_get_response.text = '<html><body>No CSRF token here</body></html>'
        mock_session_instance.get.return_value = mock_get_response
        
        # CSRFトークンが見つからないエラーのテスト
        with pytest.raises(NoteApiError) as excinfo:
            client.login()
        
        assert "Could not extract CSRF token" in str(excinfo.value)
    
    @patch.object(NoteApiClient, "ensure_login")
    def test_create_draft(self, mock_ensure_login, client, sample_post_data, sample_post_response):
        """下書き作成のテスト"""
        # ログイン確認をモック
        mock_ensure_login.return_value = True
        
        # セッションをモック
        client.session = MagicMock()
        client.csrf_token = "test_csrf_token_123456789"
        
        # 投稿APIのレスポンスをモック
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_post_response
        client.session.post.return_value = mock_response
        
        # 下書き作成を実行
        result = client.create_draft(
            title=sample_post_data["title"],
            body=sample_post_data["body"],
            tags=sample_post_data["tags"]
        )
        
        # APIが呼ばれたか確認
        client.session.post.assert_called_once()
        args, kwargs = client.session.post.call_args
        assert args[0] == "https://note.com/api/v1/notes/draft"
        
        # ヘッダーにCSRFトークンが含まれているか確認
        headers = kwargs["headers"]
        assert "X-CSRF-Token" in headers
        assert headers["X-CSRF-Token"] == client.csrf_token
        
        # リクエストボディが正しいか確認
        body = kwargs["json"]
        assert body["title"] == sample_post_data["title"]
        assert body["body"] == sample_post_data["body"]
        assert body["tags"] == sample_post_data["tags"]
        assert body["status"] == "draft"
        
        # 結果が正しいか確認
        assert result == sample_post_response
    
    @patch.object(NoteApiClient, "ensure_login")
    def test_create_draft_failure(self, mock_ensure_login, client, sample_post_data):
        """下書き作成失敗のテスト"""
        # ログイン確認をモック
        mock_ensure_login.return_value = True
        
        # セッションをモック
        client.session = MagicMock()
        client.csrf_token = "test_csrf_token_123456789"
        
        # 投稿失敗のレスポンスをモック
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "Server error"}
        client.session.post.return_value = mock_response
        
        # 下書き作成失敗のテスト
        with pytest.raises(NoteApiError) as excinfo:
            client.create_draft(
                title=sample_post_data["title"],
                body=sample_post_data["body"],
                tags=sample_post_data["tags"]
            )
        
        assert "Failed to create draft" in str(excinfo.value)
    
    @patch.object(NoteApiClient, "login")
    def test_ensure_login_not_logged_in(self, mock_login, client):
        """ログインしていない場合の自動ログインテスト"""
        # ログインメソッドをモック
        mock_login.return_value = None
        
        # セッションがない状態
        client.session = None
        
        # 自動ログインのテスト
        client.ensure_login()
        
        # loginが呼ばれたことを確認
        mock_login.assert_called_once()
    
    @patch.object(NoteApiClient, "login")
    def test_ensure_login_session_expired(self, mock_login, client):
        """セッション期限切れの場合の自動ログインテスト"""
        # ログインメソッドをモック
        mock_login.return_value = None
        
        # セッションはあるが期限切れの状態
        client.session = MagicMock()
        client.session_expires_at = 1000  # 過去の時間
        
        # 自動ログインのテスト
        client.ensure_login()
        
        # loginが呼ばれたことを確認
        mock_login.assert_called_once()
    
    def test_ensure_login_already_logged_in(self, client):
        """すでにログイン済みの場合のテスト"""
        # ログイン状態を設定
        client.session = MagicMock()
        client.csrf_token = "test_csrf_token"
        client.session_expires_at = 9999999999  # 未来の時間
        
        # ログインメソッドをモック
        with patch.object(NoteApiClient, "login") as mock_login:
            # 自動ログインのテスト
            client.ensure_login()
            
            # loginが呼ばれていないことを確認
            mock_login.assert_not_called()
    
    def test_format_markdown_to_html(self, client):
        """マークダウンからHTMLへの変換テスト"""
        markdown = """
# タイトル

これは**太字**のテキストです。

- リスト項目1
- リスト項目2

```python
print("Hello, World!")
```
"""
        # モック関数を使ってHTMLを直接返す
        expected_html = """<h1>タイトル</h1>
<p>これは<strong>太字</strong>のテキストです。</p>
<ul>
<li>リスト項目1</li>
<li>リスト項目2</li>
</ul>
<pre><code class="language-python">print("Hello, World!")</code></pre>"""
        
        with patch('markdown.markdown', return_value=expected_html):
            # HTMLへの変換
            html = client.format_markdown_to_html(markdown)
            
            # 基本的な変換が行われているか確認
            assert "<h1>タイトル</h1>" in html
            assert "<strong>太字</strong>" in html
            assert "<ul>" in html and "<li>リスト項目1</li>" in html
            assert '<pre><code class="language-python">' in html
            assert 'print("Hello, World!")' in html
    
    def test_extract_csrf_token(self, client):
        """CSRFトークン抽出のテスト"""
        html = '<html><head><meta name="csrf-token" content="abc123xyz"></head><body></body></html>'
        token = client._extract_csrf_token(html)
        assert token == "abc123xyz"
        
        # トークンが見つからない場合
        html_no_token = '<html><head></head><body></body></html>'
        with pytest.raises(ValueError) as excinfo:
            client._extract_csrf_token(html_no_token)
        
        assert "Could not extract CSRF token" in str(excinfo.value) 