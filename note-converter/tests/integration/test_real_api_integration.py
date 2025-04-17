"""
実際のAPIを使用した統合テスト

環境変数TEST_USE_REAL_API=trueの場合のみ実行される
.envファイルに実際のAPIキーとnote.com認証情報が必要
"""
import os
import sys
import pytest
from pathlib import Path

# プロジェクトルートへのパスを取得し、それをimportパスに追加
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

# 設定をインポート
from scripts.config import is_config_valid, TEST_USE_REAL_API, TEST_MARKDOWN_FILE
from scripts.config import get_openrouter_config, get_note_api_config

# 必要なモジュールをインポート
from scripts.openrouter_client import OpenRouterClient
from scripts.note_converter import read_markdown_file, process_markdown

# TEST_USE_REAL_APIがTrueの場合のみテストを実行
pytestmark = pytest.mark.skipif(
    not TEST_USE_REAL_API,
    reason="環境変数TEST_USE_REAL_API=trueが設定されていないため、実API連携テストをスキップします"
)

class TestRealAPIIntegration:
    """実際のAPIを使用した統合テスト"""
    
    @pytest.fixture(scope="class")
    def check_config(self):
        """設定が有効かどうかをチェック"""
        if not is_config_valid():
            pytest.skip("APIキーまたは認証情報が設定されていないため、テストをスキップします")
    
    @pytest.fixture
    def openrouter_client(self, check_config):
        """OpenRouterクライアントのインスタンスを作成"""
        config = get_openrouter_config()
        client = OpenRouterClient(
            api_key=config["api_key"],
            model=config["model"],
            max_tokens=config["max_tokens"],
            temperature=config["temperature"],
            http_proxy=config["http_proxy"],
            https_proxy=config["https_proxy"]
        )
        return client
    
    @pytest.fixture
    def test_markdown_content(self):
        """テスト用のマークダウンコンテンツを読み込む"""
        # TEST_MARKDOWN_FILEが設定されていない場合のデフォルト値
        if not os.path.exists(TEST_MARKDOWN_FILE):
            pytest.skip(f"テスト用マークダウンファイル {TEST_MARKDOWN_FILE} が見つかりません")
        
        return read_markdown_file(TEST_MARKDOWN_FILE)
    
    @pytest.fixture
    def format_instructions(self):
        """フォーマット指示を読み込む"""
        format_file = os.path.join(ROOT_DIR, "templates", "note_format_prompt.md")
        if not os.path.exists(format_file):
            # テスト用の簡易フォーマット指示
            return """# note記事フォーマット指示

## 記事構成
- 導入部: 読者の興味を引く一文
- 目次: 3～5個の大項目
- 本文: 各セクションは簡潔に
- まとめ: 主要ポイントのまとめ

## 執筆スタイル
- 専門用語を分かりやすく説明
- 論理的な構成
- 読みやすい文章
"""
        return read_markdown_file(format_file)
    
    def test_openrouter_api_connection(self, openrouter_client):
        """OpenRouter APIへの接続テスト"""
        # シンプルなプロンプトでテスト
        prompt = "Hello, this is a test prompt. Please respond with a short greeting."
        
        # APIを呼び出し
        response = openrouter_client.generate_text(prompt)
        
        # レスポンスの検証
        assert response
        assert len(response) > 0
        assert isinstance(response, str)
    
    def test_markdown_processing_with_real_api(self, openrouter_client, test_markdown_content, format_instructions):
        """実際のAPIを使用したマークダウン処理テスト"""
        # OpenRouterクライアントを使用してマークダウンを処理
        formatted_prompt = openrouter_client.format_prompt(test_markdown_content, format_instructions)
        
        # テスト用のモックprocess_with_llm関数を定義
        def test_process_with_llm(markdown_content, format_instructions):
            return openrouter_client.generate_text(formatted_prompt)
        
        # process_markdownをパッチしてテスト
        with pytest.MonkeyPatch.context() as mp:
            # process_with_llm関数をモックで置き換え
            from scripts import note_converter
            mp.setattr(note_converter, "process_with_llm", test_process_with_llm)
            
            # マークダウン処理を実行
            processed_content = process_markdown(test_markdown_content, format_instructions)
            
            # 処理結果の検証
            assert processed_content
            assert len(processed_content) > 0
            assert isinstance(processed_content, str)
            
            # マークダウン形式かどうかを簡易チェック
            assert "#" in processed_content  # 見出しを含む
            assert processed_content != test_markdown_content  # 元のコンテンツと異なる 