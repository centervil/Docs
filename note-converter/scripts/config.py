"""
設定と環境変数の管理モジュール

アプリケーションで使用される環境変数の読み込みと提供を行います。
"""
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# プロジェクトルートディレクトリを取得
ROOT_DIR = Path(__file__).parent.parent

# 環境変数の読み込み
load_dotenv(os.path.join(ROOT_DIR, '.env'))

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# OpenRouter API設定
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")
OPENROUTER_MAX_TOKENS = int(os.getenv("OPENROUTER_MAX_TOKENS", "1500"))
OPENROUTER_TEMPERATURE = float(os.getenv("OPENROUTER_TEMPERATURE", "0.7"))
HTTP_PROXY = os.getenv("HTTP_PROXY", "")
HTTPS_PROXY = os.getenv("HTTPS_PROXY", "")

# note.com API設定 (Cookie認証)
NOTE_AUTH_TOKEN = os.getenv("NOTE_AUTH_TOKEN", "")
NOTE_SESSION_V5 = os.getenv("NOTE_SESSION_V5", "")

# note.com API設定 (従来の認証方法 - 後方互換のため)
NOTE_EMAIL = os.getenv("NOTE_EMAIL", "")
NOTE_PASSWORD = os.getenv("NOTE_PASSWORD", "")
NOTE_USERNAME = os.getenv("NOTE_USERNAME", "")

# テスト設定
TEST_USE_REAL_API = os.getenv("TEST_USE_REAL_API", "").lower() == "true"
TEST_MARKDOWN_FILE = os.getenv("TEST_MARKDOWN_FILE", os.path.join(ROOT_DIR, "tests", "fixtures", "test_article.md"))

def get_openrouter_config():
    """OpenRouter API設定を取得する"""
    return {
        "api_key": OPENROUTER_API_KEY,
        "model": OPENROUTER_MODEL,
        "max_tokens": OPENROUTER_MAX_TOKENS,
        "temperature": OPENROUTER_TEMPERATURE,
        "http_proxy": HTTP_PROXY,
        "https_proxy": HTTPS_PROXY,
    }

def get_note_api_config():
    """note.com API設定を取得する"""
    config = {
        "http_proxy": HTTP_PROXY,
        "https_proxy": HTTPS_PROXY,
    }
    
    # Cookie認証情報の設定（優先）
    if NOTE_AUTH_TOKEN and NOTE_SESSION_V5:
        config.update({
            "auth_token": NOTE_AUTH_TOKEN,
            "session_v5": NOTE_SESSION_V5,
        })
    
    # 従来の認証情報も追加（後方互換用）
    if NOTE_EMAIL and NOTE_PASSWORD:
        config.update({
            "email": NOTE_EMAIL,
            "password": NOTE_PASSWORD,
            "username": NOTE_USERNAME,
        })
    
    return config

def is_config_valid():
    """設定が有効かどうかを確認する"""
    # OpenRouter APIキーの確認
    if not OPENROUTER_API_KEY:
        logger.warning("OPENROUTER_API_KEYが設定されていません")
        return False
    
    # note.com認証情報の確認
    has_cookie_auth = NOTE_AUTH_TOKEN and NOTE_SESSION_V5
    has_password_auth = NOTE_EMAIL and NOTE_PASSWORD
    
    if not (has_cookie_auth or has_password_auth):
        logger.warning("note.com認証情報が設定されていません (Cookie認証またはパスワード認証)")
        # APIテストのみの場合はnote.com認証情報は必須ではない
        pass
    
    return True

def log_config_status(include_secrets=False):
    """現在の設定状態をログに出力する"""
    logger.info("=== 設定状態 ===")
    
    # OpenRouter設定
    logger.info(f"OpenRouter Model: {OPENROUTER_MODEL}")
    logger.info(f"OpenRouter Max Tokens: {OPENROUTER_MAX_TOKENS}")
    logger.info(f"OpenRouter Temperature: {OPENROUTER_TEMPERATURE}")
    
    # note.com認証設定
    has_cookie_auth = NOTE_AUTH_TOKEN and NOTE_SESSION_V5
    has_password_auth = NOTE_EMAIL and NOTE_PASSWORD
    
    if include_secrets:
        # 注意：本番環境では秘密情報をログに出力しないこと
        logger.info(f"OpenRouter API Key: {OPENROUTER_API_KEY or 'Not Set'}")
        
        if has_cookie_auth:
            logger.info(f"note.com Cookie Auth: Set (Token length: {len(NOTE_AUTH_TOKEN)})")
        else:
            logger.info("note.com Cookie Auth: Not Set")
            
        if has_password_auth:
            logger.info(f"note.com Email: {NOTE_EMAIL}")
            logger.info(f"note.com Username: {NOTE_USERNAME or 'Not Set'}")
    else:
        logger.info(f"OpenRouter API Key: {'Set' if OPENROUTER_API_KEY else 'Not Set'}")
        logger.info(f"note.com Cookie Auth: {'Set' if has_cookie_auth else 'Not Set'}")
        logger.info(f"note.com Password Auth: {'Set' if has_password_auth else 'Not Set'}")
    
    # プロキシ設定
    logger.info(f"HTTP Proxy: {HTTP_PROXY or 'Not Set'}")
    logger.info(f"HTTPS Proxy: {HTTPS_PROXY or 'Not Set'}")
    
    # テスト設定
    logger.info(f"Test Use Real API: {TEST_USE_REAL_API}")
    logger.info(f"Test Markdown File: {TEST_MARKDOWN_FILE}")
    
    logger.info("================")

# モジュール読み込み時に設定有効性を確認
if not is_config_valid():
    logger.warning("一部の設定が無効です。必要な環境変数を確認してください。") 