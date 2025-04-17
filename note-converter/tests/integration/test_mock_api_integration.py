"""
モックサーバーを使用した統合テスト

OpenRouterとnote.comのモックAPIを使用して、変換処理とアップロード機能をテストします。
"""
import os
import sys
import json
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

# プロジェクトルートへのパスを取得し、それをimportパスに追加
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

# 必要なモジュールをインポート
from scripts.clients.openrouter_client import OpenRouterClient
from scripts.clients.note_client import NoteClient
from scripts.note_converter import read_markdown_file, process_markdown, convert_and_publish

# テスト用データの準備
TEST_MARKDOWN_FILE = os.path.join(ROOT_DIR, "tests", "fixtures", "test_article.md")
TEST_FORMAT_FILE = os.path.join(ROOT_DIR, "templates", "note_format_prompt.md")

class TestMockAPIIntegration:
    """モックAPIサーバーを使用した統合テスト"""
    
    @pytest.fixture
    def test_markdown_content(self):
        """テスト用のマークダウンコンテンツを読み込む"""
        if not os.path.exists(TEST_MARKDOWN_FILE):
            return """# テスト記事

## はじめに
これはモックAPIテスト用のサンプル記事です。

## サンプルコード
```python
def hello():
    print("Hello")
```

## まとめ
テスト用のシンプルな記事です。
"""
        return read_markdown_file(TEST_MARKDOWN_FILE)
    
    @pytest.fixture
    def format_instructions(self):
        """フォーマット指示を読み込む"""
        if not os.path.exists(TEST_FORMAT_FILE):
            return """# note記事フォーマット指示

## 記事構成
- 導入部: 読者の興味を引く一文
- 目次
- 本文
- まとめ

## 執筆スタイル
- 読みやすく
- 簡潔に
- 専門用語は解説
"""
        return read_markdown_file(TEST_FORMAT_FILE)
    
    @pytest.fixture
    def mock_openrouter_client(self):
        """OpenRouter APIクライアントのモック"""
        mock_client = MagicMock(spec=OpenRouterClient)
        
        # process_with_llmメソッドのモック
        def mock_process_with_llm(prompt, system_prompt=None):
            # 簡易的な応答を返す
            return """# 整形後のテスト記事

## はじめに

このテスト記事は、モックAPIを使用した統合テストのために整形されたものです。

## 目次

1. テストの目的
2. サンプルコード
3. まとめ

## テストの目的

この記事はAPIモックを使用した統合テストの動作確認に使用されます。

## サンプルコード

以下は簡単なPythonのサンプルコードです：

```python
def hello():
    print("Hello")
```

## まとめ

モックAPIを使用して文章が適切に整形されていることを確認しました。
"""
        
        mock_client.process_with_llm.side_effect = mock_process_with_llm
        mock_client.test_connection.return_value = True
        return mock_client
    
    @pytest.fixture
    def mock_note_client(self):
        """Note.com APIクライアントのモック"""
        mock_client = MagicMock(spec=NoteClient)
        
        # loginメソッドのモック
        mock_client.login.return_value = True
        
        # create_noteメソッドのモック
        mock_client.create_note.return_value = "test_note_12345"
        
        # get_user_notesメソッドのモック
        mock_client.get_user_notes.return_value = [
            {"id": "test_note_12345", "name": "テスト記事", "status": "draft"}
        ]
        
        mock_client.test_connection.return_value = True
        return mock_client
    
    def test_markdown_processing(self, mock_openrouter_client, test_markdown_content, format_instructions):
        """マークダウン処理のテスト"""
        # process_with_llm関数をモックで置き換え
        with patch('scripts.note_converter.process_with_llm', mock_openrouter_client.process_with_llm):
            # マークダウン処理を実行
            processed_content = process_markdown(test_markdown_content, format_instructions)
            
            # 処理結果の検証
            assert processed_content
            assert len(processed_content) > 0
            assert isinstance(processed_content, str)
            assert "# 整形後のテスト記事" in processed_content
            assert "## まとめ" in processed_content
            
            # モックが呼び出されたことを確認
            mock_openrouter_client.process_with_llm.assert_called_once()
    
    def test_end_to_end_conversion(self, mock_openrouter_client, mock_note_client, test_markdown_content, format_instructions):
        """エンドツーエンドのマークダウン変換と投稿テスト"""
        # パッチを適用
        with patch('scripts.note_converter.get_openrouter_client', return_value=mock_openrouter_client), \
             patch('scripts.note_converter.get_note_client', return_value=mock_note_client), \
             patch('scripts.note_converter.process_with_llm', mock_openrouter_client.process_with_llm):
            
            # マークダウンファイルのパス
            mock_file_path = TEST_MARKDOWN_FILE
            
            # 変換と投稿を実行
            result = convert_and_publish(mock_file_path, format_instructions, draft_mode=True)
            
            # 結果の検証
            assert result.get("success") is True
            assert "note_id" in result
            assert result["note_id"] == "test_note_12345"
            
            # 各モックが適切に呼び出されたことを確認
            mock_openrouter_client.process_with_llm.assert_called_once()
            mock_note_client.login.assert_called_once()
            mock_note_client.create_note.assert_called_once()
    
    def test_error_handling(self, mock_openrouter_client, mock_note_client, test_markdown_content):
        """エラーハンドリングのテスト"""
        # OpenRouterのエラーをシミュレート
        mock_openrouter_client.process_with_llm.side_effect = Exception("API呼び出しエラー")
        
        # パッチを適用
        with patch('scripts.note_converter.get_openrouter_client', return_value=mock_openrouter_client), \
             patch('scripts.note_converter.get_note_client', return_value=mock_note_client), \
             patch('scripts.note_converter.process_with_llm', mock_openrouter_client.process_with_llm):
            
            # 変換と投稿を実行
            result = convert_and_publish(TEST_MARKDOWN_FILE, "テスト指示", draft_mode=True)
            
            # 失敗結果の検証
            assert result.get("success") is False
            assert "error" in result
            assert "API呼び出しエラー" in result["error"]
    
    def test_network_error_handling(self, mock_openrouter_client, mock_note_client):
        """ネットワークエラーハンドリングのテスト"""
        # note.comの接続エラーをシミュレート
        mock_note_client.login.side_effect = Exception("ネットワーク接続エラー")
        
        # パッチを適用
        with patch('scripts.note_converter.get_openrouter_client', return_value=mock_openrouter_client), \
             patch('scripts.note_converter.get_note_client', return_value=mock_note_client):
            
            # 変換と投稿を実行
            result = convert_and_publish(TEST_MARKDOWN_FILE, "テスト指示", draft_mode=True)
            
            # 失敗結果の検証
            assert result.get("success") is False
            assert "error" in result
            assert "ネットワーク接続エラー" in result["error"] 