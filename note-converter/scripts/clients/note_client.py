"""
note.com APIクライアント

note.comのAPIとの通信を行うためのクライアントクラスを提供します。
"""
import json
import logging
import requests
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup
import re

# ロガーの設定
logger = logging.getLogger(__name__)

class NoteClient:
    """note.com APIとの通信を行うクライアントクラス"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初期化

        Args:
            config: APIの設定情報
                - auth_token: note.comのauth_token (Cookie: note_gql_auth_token)
                - session_v5: note.comのセッション (Cookie: _note_session_v5)
                - http_proxy: HTTPプロキシ (任意)
                - https_proxy: HTTPSプロキシ (任意)
        """
        self.auth_token = config.get("auth_token")
        self.session_v5 = config.get("session_v5")
        
        # 旧認証情報（後方互換のため）
        self.email = config.get("email")
        self.password = config.get("password")
        
        # プロキシの設定
        self.proxies = {}
        if config.get("http_proxy"):
            self.proxies["http"] = config["http_proxy"]
        if config.get("https_proxy"):
            self.proxies["https"] = config["https_proxy"]
        
        # セッション作成
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        
        # Cookie認証がある場合はセットアップ
        if self.auth_token and self.session_v5:
            self.setup_cookie_auth()
            self.is_logged_in = True
        else:
            self.is_logged_in = False
        
        logger.info("NoteClient initialized")
    
    def setup_cookie_auth(self):
        """
        Cookie認証の設定
        """
        # Cookieを設定（ドメイン指定なし）
        self.session.cookies.set("note_gql_auth_token", self.auth_token)
        self.session.cookies.set("_note_session_v5", self.session_v5)
        logger.info("Cookie authentication setup completed")
    
    def login(self) -> bool:
        """
        note.comにログインする

        Cookie認証情報がある場合はそれを使用
        ない場合は従来のメール/パスワード認証を試行
        
        Returns:
            ログイン成功の場合はTrue、失敗の場合はFalse
        """
        # すでにCookie認証済み
        if self.is_logged_in:
            logger.info("Already authenticated with cookies")
            return True
            
        # Cookie認証情報がある場合
        if self.auth_token and self.session_v5:
            self.setup_cookie_auth()
            self.is_logged_in = True
            logger.info("Logged in with cookie authentication")
            return True
            
        # 以下は従来のログイン方法（後方互換のため維持）
        if not self.email or not self.password:
            logger.error("Neither cookie authentication nor email/password provided")
            return False
            
        try:
            # note.comのログインページを取得
            login_url = "https://note.com/login"
            response = self.session.get(login_url, proxies=self.proxies if self.proxies else None)
            response.raise_for_status()
            
            # CSRFトークンを取得
            soup = BeautifulSoup(response.text, "html.parser")
            csrf_meta = soup.find("meta", {"name": "csrf-token"})
            
            if not csrf_meta:
                logger.error("CSRF token not found in login page")
                return False
                
            csrf_token = csrf_meta["content"]
            
            # ログイン情報を送信
            login_api_url = "https://note.com/api/v1/login"
            login_data = {
                "login": self.email,
                "password": self.password
            }
            headers = {
                "X-CSRF-Token": csrf_token
            }
            
            login_response = self.session.post(
                login_api_url,
                headers=headers,
                json=login_data,
                proxies=self.proxies if self.proxies else None
            )
            login_response.raise_for_status()
            
            # ログイン結果を確認
            result = login_response.json()
            if result.get("is_success", False):
                self.is_logged_in = True
                logger.info("Successfully logged in to note.com with email/password")
                
                # Cookie情報を取得
                cookies = self.session.cookies
                self.auth_token = cookies.get("note_gql_auth_token")
                self.session_v5 = cookies.get("_note_session_v5")
                
                logger.info("Retrieved authentication cookies from login")
                return True
            else:
                logger.error(f"Failed to login to note.com: {json.dumps(result, ensure_ascii=False)}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error during note.com login: {str(e)}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response: {e.response.text}")
            return False
    
    def get_user_notes(self, username: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        ユーザーの記事一覧を取得する

        Args:
            username: 記事を取得するユーザー名（指定なしの場合はログインユーザー）

        Returns:
            記事情報のリスト
        """
        if not self.is_logged_in and not self.login():
            logger.error("Failed to get user notes: not logged in")
            return []
            
        try:
            # ユーザー名を取得（指定がない場合はプロフィールページから取得）
            if not username:
                profile_url = "https://note.com/settings/profile"
                profile_response = self.session.get(profile_url, proxies=self.proxies if self.proxies else None)
                profile_response.raise_for_status()
                
                # ユーザー名を抽出
                soup = BeautifulSoup(profile_response.text, "html.parser")
                username_elem = soup.find("input", {"name": "urlname"})
                if username_elem and username_elem.get("value"):
                    username = username_elem["value"]
                else:
                    logger.error("Failed to retrieve username from profile")
                    return []
            
            # ユーザーの記事一覧を取得
            notes_url = f"https://note.com/api/v2/creators/{username}/contents"
            params = {
                "kind": "note",
                "page": 1
            }
            
            notes_response = self.session.get(
                notes_url,
                params=params,
                proxies=self.proxies if self.proxies else None
            )
            notes_response.raise_for_status()
            
            result = notes_response.json()
            notes = result.get("data", {}).get("contents", [])
            
            logger.info(f"Retrieved {len(notes)} notes from user {username}")
            return notes
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving notes: {str(e)}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response: {e.response.text}")
            return []
    
    def get_note_content(self, note_id: str) -> Optional[Dict[str, Any]]:
        """
        記事の内容を取得する

        Args:
            note_id: 記事ID

        Returns:
            記事の内容情報
        """
        if not self.is_logged_in and not self.login():
            logger.error(f"Failed to get note content for {note_id}: not logged in")
            return None
            
        try:
            # 記事の内容を取得
            note_url = f"https://note.com/api/v3/notes/{note_id}"
            
            note_response = self.session.get(
                note_url,
                proxies=self.proxies if self.proxies else None
            )
            note_response.raise_for_status()
            
            result = note_response.json()
            note_data = result.get("data")
            
            if note_data:
                logger.info(f"Successfully retrieved content for note {note_id}")
                return note_data
            else:
                logger.error(f"Failed to retrieve content for note {note_id}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving note content: {str(e)}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response: {e.response.text}")
            return None
    
    def create_note(self, title: str, content: str, status: str = "draft") -> Optional[str]:
        """
        記事を作成する

        Args:
            title: 記事のタイトル
            content: 記事の内容（HTML形式）
            status: 公開ステータス（"draft"または"published"）

        Returns:
            作成された記事のID、失敗した場合はNone
        """
        if not self.is_logged_in and not self.login():
            logger.error("Failed to create note: not logged in")
            return None
            
        try:
            # トップページのCSRFトークンを使用
            response = self.session.get("https://note.com", proxies=self.proxies if self.proxies else None)
            response.raise_for_status()
            
            # HTMLからCSRFトークンを抽出する
            html_content = response.text
            
            # デバッグ情報出力
            logger.info(f"Response status code: {response.status_code}")
            
            # CSRFトークンを検索
            soup = BeautifulSoup(html_content, "html.parser")
            csrf_token = soup.find("meta", {"name": "csrf-token"})
            
            # CSRFトークンが見つからない場合、正規表現で検索
            if not csrf_token:
                logger.warning("CSRF token not found using BeautifulSoup, trying regex")
                match = re.search(r'<meta name="csrf-token" content="([^"]+)"', html_content)
                if match:
                    csrf_token_value = match.group(1)
                    logger.info(f"CSRF token found using regex: {csrf_token_value[:10]}...")
                else:
                    # 記事作成APIを別の形式で呼び出す（CSRFなし）
                    logger.warning("CSRF token not found, trying without CSRF token")
                    
                    # v1 APIに戻す
                    create_url = "https://note.com/api/v1/notes"
                    headers = {
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        # Cookieは自動的に送信される
                    }
                    
                    data = {
                        "note": {
                            "name": title,
                            "body": content,
                            "status": status,
                            "publish_at": None,
                            "price": 0,
                            "is_time_limited_to_members": False
                        }
                    }
                    
                    create_response = self.session.post(
                        create_url,
                        headers=headers,
                        json=data,
                        proxies=self.proxies if self.proxies else None
                    )
                    create_response.raise_for_status()
                    
                    result = create_response.json()
                    note_id = result.get("data", {}).get("id")
                    
                    if note_id:
                        logger.info(f"Successfully created note with ID {note_id} (without CSRF token)")
                        return note_id
                    else:
                        logger.error(f"Failed to create note: {json.dumps(result, ensure_ascii=False)}")
                        return None
                    
            else:
                csrf_token_value = csrf_token["content"]
                logger.info(f"CSRF token found: {csrf_token_value[:10]}...")
            
            # 記事作成APIを呼び出す (v1に戻す)
            create_url = "https://note.com/api/v1/notes"
            headers = {
                "X-CSRF-Token": csrf_token_value,
                "Content-Type": "application/json",
                "Accept": "application/json",
                # 追加のヘッダー
                "Origin": "https://note.com",
                "Referer": "https://note.com/new"
            }
            
            # v1 APIのデータ形式に戻す
            data = {
                "note": {
                    "name": title,
                    "body": content,
                    "status": status,
                    "publish_at": None,
                    "price": 0,
                    "is_time_limited_to_members": False
                }
            }
            
            create_response = self.session.post(
                create_url,
                headers=headers,
                json=data,
                proxies=self.proxies if self.proxies else None
            )
            create_response.raise_for_status()
            
            result = create_response.json()
            note_id = result.get("data", {}).get("id")
            
            if note_id:
                logger.info(f"Successfully created note with ID {note_id}")
                return note_id
            else:
                logger.error(f"Failed to create note: {json.dumps(result, ensure_ascii=False)}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating note: {str(e)}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response headers: {e.response.headers}")
                try:
                    error_content = e.response.json()
                    logger.error(f"Error response: {json.dumps(error_content, ensure_ascii=False)}")
                except:
                    logger.error(f"Response text: {e.response.text[:500]}")
            return None
    
    def update_note(self, note_id: str, title: str, content: str, status: Optional[str] = None) -> bool:
        """
        記事を更新する

        Args:
            note_id: 記事ID
            title: 記事のタイトル
            content: 記事の内容（HTML形式）
            status: 公開ステータス（"draft"または"published"）

        Returns:
            更新成功の場合はTrue、失敗の場合はFalse
        """
        if not self.is_logged_in and not self.login():
            logger.error(f"Failed to update note {note_id}: not logged in")
            return False
            
        try:
            # 現在の記事情報を取得
            current_note = self.get_note_content(note_id)
            if not current_note:
                logger.error(f"Failed to update note {note_id}: could not retrieve current note data")
                return False
            
            # トップページのCSRFトークンを使用
            response = self.session.get("https://note.com", proxies=self.proxies if self.proxies else None)
            response.raise_for_status()
            
            # HTMLからCSRFトークンを抽出する
            html_content = response.text
            
            # デバッグ情報出力
            logger.info(f"Response status code: {response.status_code}")
            
            # CSRFトークンを検索
            soup = BeautifulSoup(html_content, "html.parser")
            csrf_token = soup.find("meta", {"name": "csrf-token"})
            
            # CSRFトークンが見つからない場合、正規表現で検索
            if not csrf_token:
                logger.warning("CSRF token not found using BeautifulSoup, trying regex")
                match = re.search(r'<meta name="csrf-token" content="([^"]+)"', html_content)
                if match:
                    csrf_token_value = match.group(1)
                    logger.info(f"CSRF token found using regex: {csrf_token_value[:10]}...")
                else:
                    # 記事更新APIを別の形式で呼び出す（CSRFなし）
                    logger.warning("CSRF token not found, trying without CSRF token")
                    
                    # 更新するデータ（現在の設定を維持するために現在の記事情報をマージ）
                    current_status = status if status is not None else current_note.get("status", "draft")
                    
                    # APIを呼び出す
                    update_url = f"https://note.com/api/v1/notes/{note_id}"
                    headers = {
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        # Cookieは自動的に送信される
                    }
                    
                    data = {
                        "note": {
                            "name": title,
                            "body": content,
                            "status": current_status,
                            "price": current_note.get("price", 0),
                            "is_time_limited_to_members": current_note.get("is_time_limited_to_members", False)
                        }
                    }
                    
                    update_response = self.session.put(
                        update_url,
                        headers=headers,
                        json=data,
                        proxies=self.proxies if self.proxies else None
                    )
                    update_response.raise_for_status()
                    
                    result = update_response.json()
                    success = result.get("is_success", False)
                    
                    if success:
                        logger.info(f"Successfully updated note {note_id} (without CSRF token)")
                        return True
                    else:
                        logger.error(f"Failed to update note {note_id}: {json.dumps(result, ensure_ascii=False)}")
                        return False
            else:
                csrf_token_value = csrf_token["content"]
                logger.info(f"CSRF token found: {csrf_token_value[:10]}...")
            
            # 更新APIを呼び出す (v1 API)
            update_url = f"https://note.com/api/v1/notes/{note_id}"
            headers = {
                "X-CSRF-Token": csrf_token_value,
                "Content-Type": "application/json",
                "Accept": "application/json",
                # 追加のヘッダー
                "Origin": "https://note.com",
                "Referer": f"https://note.com/edit/{note_id}"
            }
            
            # 更新するデータ（現在の設定を維持するために現在の記事情報をマージ）
            current_status = status if status is not None else current_note.get("status", "draft")
            
            # v1 APIのデータ形式を使用
            data = {
                "note": {
                    "name": title,
                    "body": content,
                    "status": current_status,
                    "price": current_note.get("price", 0),
                    "is_time_limited_to_members": current_note.get("is_time_limited_to_members", False)
                }
            }
            
            update_response = self.session.put(
                update_url,
                headers=headers,
                json=data,
                proxies=self.proxies if self.proxies else None
            )
            update_response.raise_for_status()
            
            result = update_response.json()
            success = result.get("is_success", False)
            
            if success:
                logger.info(f"Successfully updated note {note_id}")
                return True
            else:
                logger.error(f"Failed to update note {note_id}: {json.dumps(result, ensure_ascii=False)}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error updating note {note_id}: {str(e)}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response headers: {e.response.headers}")
                try:
                    error_content = e.response.json()
                    logger.error(f"Error response: {json.dumps(error_content, ensure_ascii=False)}")
                except:
                    logger.error(f"Response text: {e.response.text[:500]}")
            return False
    
    def test_connection(self) -> bool:
        """
        API接続テスト

        Returns:
            接続成功の場合はTrue、失敗の場合はFalse
        """
        try:
            # まずCookie認証をチェック
            if self.auth_token and self.session_v5:
                self.setup_cookie_auth()
                
                # Cookie情報をログ出力（デバッグ用）
                cookies_dict = {c.name: c.value for c in self.session.cookies}
                logger.info(f"Cookies before request: {cookies_dict}")
                
                # リクエストにCookieを直接含める
                headers = {
                    'Cookie': f'note_gql_auth_token={self.auth_token}; _note_session_v5={self.session_v5}'
                }
                self.session.headers.update(headers)
                
                # 簡易的な接続テスト（トップページにアクセス）
                response = self.session.get("https://note.com/", proxies=self.proxies if self.proxies else None)
                response.raise_for_status()
                
                logger.info(f"Response status code: {response.status_code}")
                
                # レスポンスからユーザー名を抽出してみる（ログイン状態の確認）
                html_content = response.text
                
                # ログイン状態を確認（ログイン済みならマイページへのリンクがある）
                soup = BeautifulSoup(html_content, "html.parser")
                
                # デバッグ: レスポンスHTMLの一部をログに出力
                if len(html_content) > 1000:
                    logger.info(f"Response HTML (first 1000 chars): {html_content[:1000]}...")
                else:
                    logger.info(f"Response HTML: {html_content}")
                
                # マイページリンクの検索方法を改善
                profile_link = soup.find("a", href=lambda href: href and "/mypage" in href)
                login_button = soup.find("a", href=lambda href: href and "/login" in href)
                
                if profile_link:
                    logger.info("Note.com API connection test successful with cookie authentication")
                    self.is_logged_in = True
                    return True
                elif login_button:
                    logger.info("Login button found - not logged in")
                    # Cookie認証情報は設定されているが、ログインできていない
                    logger.error("Cookie authentication failed: Valid tokens needed")
                    return False
                else:
                    logger.warning("Could not determine login state from HTML")
                    # ページ構造が変わった可能性があるが、エラーではない
                    self.is_logged_in = True  # APIリクエストは通っているのでTrueとする
                    return True
            
            # Cookie認証に失敗したらメール/パスワード認証を試行
            if self.email and self.password:
                login_success = self.login()
                logger.info(f"Note.com API connection test with email/password: {'Success' if login_success else 'Failed'}")
                return login_success
            
            logger.error("Note.com API connection test failed: No valid authentication method")
            return False
            
        except Exception as e:
            import traceback
            logger.error(f"Note.com API connection test failed: {str(e)}")
            logger.error(f"Error details: {type(e).__name__}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            return False 