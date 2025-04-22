"""
note.comのAPI接続テスト

note.comのAPIに実際に接続し、認証やコンテンツのやりとりをテストします。
環境変数TEST_USE_REAL_API=trueの場合のみ実行されます。
"""
import os
import sys
import pytest
from pathlib import Path
import logging

# ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# プロジェクトルートへのパスを取得し、それをimportパスに追加
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

# 設定をインポート
from scripts.config import (
    is_config_valid, TEST_USE_REAL_API, NOTE_AUTH_TOKEN, NOTE_SESSION_V5,
    NOTE_EMAIL, NOTE_PASSWORD, get_note_api_config
)
from scripts.clients.note_client import NoteClient

# テスト実行の条件：実APIテストが有効で、note.comの認証情報が設定されていること
has_cookie_auth = NOTE_AUTH_TOKEN and NOTE_SESSION_V5
has_password_auth = NOTE_EMAIL and NOTE_PASSWORD

has_note_auth = has_cookie_auth or has_password_auth

# 条件を満たさない場合はスキップ
pytestmark = pytest.mark.skipif(
    not TEST_USE_REAL_API or not has_note_auth,
    reason="環境変数TEST_USE_REAL_API=trueが設定されていないか、note.com認証情報が設定されていないため、テストをスキップします"
)

# デバッグ情報
if TEST_USE_REAL_API:
    logger.info(f"Note.com認証情報: Cookie認証={has_cookie_auth}, パスワード認証={has_password_auth}")
else:
    logger.info("実APIテストが無効です")

class TestNoteAPIPosting:
    """note.comのAPI接続と投稿機能のテスト"""
    
    @pytest.fixture(scope="class")
    def note_client(self):
        """note.comクライアントのインスタンスを作成"""
        config = get_note_api_config()
        return NoteClient(config)
    
    def test_api_availability(self, note_client):
        """APIの可用性テスト（認証情報の確認）"""
        result = note_client.test_connection()
        assert result, "note.com APIへの接続に失敗しました。認証情報を確認してください。"
        
        # 認証方法のログ出力
        if has_cookie_auth:
            logger.info("Cookie認証でnote.com APIに接続しました")
        else:
            logger.info("メール/パスワード認証でnote.com APIに接続しました")
    
    def test_user_notes_retrieval(self, note_client):
        """ユーザーの記事一覧取得テスト"""
        # ログイン状態を確認・設定
        if not note_client.is_logged_in:
            assert note_client.login(), "note.comへのログインに失敗しました"
        
        # 記事一覧を取得（指定なしの場合は自分の記事）
        notes = note_client.get_user_notes()
        assert isinstance(notes, list), "記事一覧の取得に失敗しました"
        
        # 記事情報のログ出力
        logger.info(f"{len(notes)}件の記事が見つかりました")
        if notes:
            logger.info(f"最新の記事: {notes[0].get('name', 'タイトルなし')}")
    
    def test_create_draft(self, note_client):
        """下書き記事の作成テスト"""
        # ログイン状態を確認・設定
        if not note_client.is_logged_in:
            assert note_client.login(), "note.comへのログインに失敗しました"
        
        # テスト用の記事内容
        title = "APIテスト用記事（自動テスト）"
        content = """<p>これはnote-converterのAPIテストによって自動的に作成された記事です。</p>
<p>このテストは、note.comのAPIが正常に機能していることを確認するために実行されました。</p>
<p>テストが完了しましたら、この記事は削除される予定です。</p>"""
        
        # 下書き記事を作成
        note_id = note_client.create_note(title, content, status="draft")
        
        # 作成結果の確認
        assert note_id, "下書き記事の作成に失敗しました"
        logger.info(f"下書き記事が作成されました（ID: {note_id}）")
        
        # 作成した記事の内容を取得して検証
        note_data = note_client.get_note_content(note_id)
        assert note_data, "作成した記事の取得に失敗しました"
        assert note_data.get("name") == title, "記事のタイトルが一致しません"
        logger.info("作成した記事の内容が正しく取得できました")
        
        # 後続のテストのために記事IDを返す
        return note_id
    
    def test_update_draft(self, note_client):
        """下書き記事の更新テスト"""
        # まず記事を作成
        note_id = self.test_create_draft(note_client)
        
        # 更新内容
        updated_title = "更新されたAPIテスト用記事（自動テスト）"
        updated_content = """<p>これはnote-converterのAPIテストによって自動的に作成され、更新された記事です。</p>
<p>このテストは、note.comのAPIが正常に機能していることを確認するために実行されました。</p>
<p>テストが完了しましたら、この記事は削除される予定です。</p>
<p><strong>この行は更新によって追加されました。</strong></p>"""
        
        # 記事を更新
        update_result = note_client.update_note(note_id, updated_title, updated_content)
        assert update_result, "記事の更新に失敗しました"
        logger.info(f"記事（ID: {note_id}）が正常に更新されました")
        
        # 更新された記事の内容を取得して検証
        updated_note = note_client.get_note_content(note_id)
        assert updated_note, "更新された記事の取得に失敗しました"
        assert updated_note.get("name") == updated_title, "更新後の記事タイトルが一致しません"
        logger.info("更新した記事の内容が正しく取得できました") 