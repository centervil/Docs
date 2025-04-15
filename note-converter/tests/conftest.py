"""
pytestのための共通フィクスチャと設定を定義するモジュール
"""
import os
import sys
import pytest
from pathlib import Path

# プロジェクトルートへのパスを取得し、それをimportパスに追加
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))


@pytest.fixture
def sample_markdown_text():
    """マークダウンテスト用のサンプルテキストを提供するフィクスチャ"""
    return """# サンプル記事

## はじめに
これはテスト用のマークダウンです。

## 本文
マークダウンの処理をテストします。
- リスト項目1
- リスト項目2

## まとめ
テストマークダウンの終わりです。
"""


@pytest.fixture
def mock_env_vars(monkeypatch):
    """環境変数をモックするためのフィクスチャ"""
    test_env_vars = {
        "OPENROUTER_API_KEY": "test_api_key",
        "NOTE_SESSION_TOKEN": "test_session_token",
        "NOTE_CSRF_TOKEN": "test_csrf_token",
    }
    
    for key, value in test_env_vars.items():
        monkeypatch.setenv(key, value)
    
    return test_env_vars 