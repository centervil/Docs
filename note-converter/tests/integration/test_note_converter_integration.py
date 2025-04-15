"""
note_converter.pyに対する統合テスト
"""
import os
import sys
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, call

# プロジェクトルートへのパスを取得し、それをimportパスに追加
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

# 実装されるメインスクリプトのインポート
# まだ実装されていないため、インポートエラーとなる想定
try:
    from scripts.note_converter import main
except ImportError:
    # テスト実行時にはまだインポートできないので、テストだけ記述
    pass


class TestNoteConverterIntegration:
    """note_converter.pyの統合テスト"""
    
    @pytest.fixture
    def setup_test_files(self):
        """テスト用の一時ファイルとディレクトリをセットアップする"""
        # テスト用マークダウンファイル
        test_markdown = """# サンプル記事

## はじめに
これはテスト用のマークダウンです。

## 本文
マークダウンの処理をテストします。
- リスト項目1
- リスト項目2

## まとめ
テストマークダウンの終わりです。
"""
        # テスト用フォーマット指示ファイル
        test_format = """# note記事フォーマット指示

## 記事構成
- 導入部: 読者の興味を引く一文
- 目次: 3〜5個の大項目
- 本文: 段落は3〜4行
- まとめ: 主要ポイントのまとめ

## スタイルガイド
- 見出し: H2, H3を効果的に使用
- 段落: 適度な空白を設ける
- 強調: 太字を適切に使用
"""
        
        # 一時ファイル作成
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, encoding="utf-8") as md_file:
            md_file.write(test_markdown)
            md_path = md_file.name
        
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, encoding="utf-8") as format_file:
            format_file.write(test_format)
            format_path = format_file.name
        
        # 一時出力ディレクトリ
        output_dir = tempfile.mkdtemp()
        
        # フィクスチャ戻り値
        fixture_data = {
            "markdown_path": md_path,
            "format_path": format_path,
            "output_dir": output_dir,
            "markdown_content": test_markdown,
            "format_content": test_format
        }
        
        yield fixture_data
        
        # クリーンアップ
        for path in [md_path, format_path]:
            if os.path.exists(path):
                os.unlink(path)
        
        if os.path.exists(output_dir):
            import shutil
            shutil.rmtree(output_dir)
    
    def test_end_to_end_with_mock_llm(self, setup_test_files):
        """LLM APIをモックしたエンドツーエンドテスト"""
        files = setup_test_files
        
        # LLM処理の結果をモック
        expected_output = """# 改善されたサンプル記事

## はじめに
マークダウン処理の効果的な方法を探求する旅に出かけましょう。

## 目次
- マークダウンとは
- 処理の基本
- テスト手法
- 実践的応用

## マークダウンとは
マークダウンは軽量マークアップ言語で、シンプルな文法で文書を構造化できます。
多くの開発者やライターに愛用されている理由は、その直感的な書き方にあります。
特別なツールなしでも読みやすく書けることが最大の特徴です。

## 処理の基本
マークダウンの処理には様々なアプローチがあります：
- パーサーによる構文解析
- ASTへの変換
- HTML等への出力生成

## テスト手法
マークダウン処理のテストは重要です。単体テストから統合テストまで、
適切なカバレッジを確保しましょう。

## まとめ
マークダウン処理は、適切なツールと方法論を選ぶことで効率化できます。
本記事の手法を活用して、あなたのマークダウン処理を改善してください。
"""
        
        # コマンドライン引数と必要なモックをセットアップ
        with patch("sys.argv", ["note_converter.py", 
                               files["markdown_path"],
                               "--output-dir", files["output_dir"],
                               "--format-file", files["format_path"]]), \
             patch("scripts.note_converter.process_with_llm") as mock_llm:
            
            # LLM処理の結果を設定
            mock_llm.return_value = expected_output
            
            # メイン関数を実行
            main()
            
            # 出力ファイルの検証
            expected_output_filename = f"processed_{os.path.basename(files['markdown_path']).split('.')[0]}.md"
            output_path = os.path.join(files["output_dir"], expected_output_filename)
            
            # ファイルが存在することを確認
            assert os.path.exists(output_path)
            
            # ファイル内容を確認
            with open(output_path, "r", encoding="utf-8") as f:
                content = f.read()
                assert content == expected_output
            
            # LLM処理が正しく呼び出されたことを確認
            mock_llm.assert_called_once()
    
    def test_error_handling(self, setup_test_files):
        """エラーハンドリングのテスト"""
        files = setup_test_files
        
        # 存在しないファイルを指定
        non_existent_file = "non_existent_file.md"
        
        # コマンドライン引数をセットアップ
        with patch("sys.argv", ["note_converter.py", 
                               non_existent_file,
                               "--output-dir", files["output_dir"],
                               "--format-file", files["format_path"]]), \
             patch("sys.exit") as mock_exit, \
             patch("scripts.note_converter.logger.error") as mock_log_error:
            
            # メイン関数を実行（例外が発生する想定）
            main()
            
            # エラーログが記録されたことを確認
            mock_log_error.assert_called()
            
            # プログラムが終了したことを確認
            mock_exit.assert_called()
    
    def test_dry_run_mode(self, setup_test_files):
        """ドライランモードのテスト"""
        files = setup_test_files
        
        # ドライランモードを指定
        with patch("sys.argv", ["note_converter.py", 
                               files["markdown_path"],
                               "--output-dir", files["output_dir"],
                               "--format-file", files["format_path"],
                               "--dry-run"]), \
             patch("scripts.note_converter.process_with_llm") as mock_llm:
            
            # ドライランにより、LLM APIは呼ばれないはず
            mock_llm.return_value = "これは呼ばれないはず"
            
            # メイン関数を実行
            main()
            
            # LLM処理が呼ばれていないことを確認
            mock_llm.assert_not_called()
            
            # 出力ファイルが生成されていないことを確認
            output_files = os.listdir(files["output_dir"])
            assert len(output_files) == 0 