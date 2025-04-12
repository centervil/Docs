"""
note_converter.pyに対するユニットテスト
"""
import os
import sys
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# プロジェクトルートへのパスを取得し、それをimportパスに追加
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

# 実装されるメインスクリプトのインポート
# まだ実装されていないため、インポートエラーとなる想定
# scripts.note_converter からのインポートになるはず
try:
    from scripts.note_converter import (
        parse_args,
        read_markdown_file,
        read_format_instruction_file,
        generate_output_file,
        process_markdown,
        main
    )
except ImportError:
    # テスト実行時にはまだインポートできないので、テストだけ記述
    pass


class TestNoteConverter:
    """note_converter.pyの機能をテストするクラス"""
    
    def test_parse_args(self):
        """コマンドライン引数パーサーのテスト"""
        # 正常系: 全て必須引数が指定された場合
        test_args = [
            "input.md",  # 入力ファイル
            "--output-dir", "output",  # 出力ディレクトリ
            "--format-file", "templates/note_format_prompt.md",  # フォーマット指示ファイル
            "--log-level", "INFO",  # ログレベル
            "--dry-run"  # ドライラン
        ]
        
        with patch("sys.argv", ["note_converter.py"] + test_args):
            args = parse_args()
            assert args.input_file == "input.md"
            assert args.output_dir == "output"
            assert args.format_file == "templates/note_format_prompt.md"
            assert args.log_level == "INFO"
            assert args.dry_run is True
        
        # 最小限の引数のみ（入力ファイルのみ）
        test_args_min = ["input.md"]
        with patch("sys.argv", ["note_converter.py"] + test_args_min):
            args = parse_args()
            assert args.input_file == "input.md"
            # デフォルト値のチェック
            assert args.output_dir  # デフォルト値があること
            assert args.format_file  # デフォルト値があること
            assert args.log_level == "INFO"  # デフォルト値
            assert args.dry_run is False  # デフォルト値
    
    def test_read_markdown_file(self):
        """マークダウンファイル読み込み機能のテスト"""
        # 一時ファイルを作成してテスト
        test_content = "# Test Markdown\n\nThis is a test."
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
            temp_file.write(test_content)
            temp_path = temp_file.name
        
        try:
            # ファイル読み込みのテスト
            content = read_markdown_file(temp_path)
            assert content == test_content
            
            # 存在しないファイルの読み込みテスト
            with pytest.raises(FileNotFoundError):
                read_markdown_file("non_existent_file.md")
        finally:
            # 一時ファイルの削除
            os.unlink(temp_path)
    
    def test_read_format_instruction_file(self):
        """フォーマット指示ファイル読み込み機能のテスト"""
        # 一時ファイルを作成してテスト
        test_content = "# Format Instructions\n\n## Style Guide\n- Use headers\n- Short paragraphs"
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
            temp_file.write(test_content)
            temp_path = temp_file.name
        
        try:
            # ファイル読み込みのテスト
            content = read_format_instruction_file(temp_path)
            assert content == test_content
            
            # 存在しないファイルの読み込みテスト
            with pytest.raises(FileNotFoundError):
                read_format_instruction_file("non_existent_file.md")
        finally:
            # 一時ファイルの削除
            os.unlink(temp_path)
    
    def test_process_markdown(self):
        """マークダウン処理機能のテスト"""
        # LLM APIを呼び出す関数なので、モックを使用
        markdown_content = "# Test Content\n\nThis is test content."
        format_instructions = "# Format Instructions\n\nUse proper headers."
        expected_output = "# Processed Test Content\n\nThis is formatted content."
        
        # APIクライアントのモック化
        with patch("scripts.note_converter.process_with_llm") as mock_process:
            mock_process.return_value = expected_output
            
            # 処理関数の呼び出し
            result = process_markdown(markdown_content, format_instructions)
            
            # 結果の検証
            assert result == expected_output
            mock_process.assert_called_once_with(markdown_content, format_instructions)
    
    def test_generate_output_file(self):
        """出力ファイル生成機能のテスト"""
        processed_content = "# Generated Content\n\nThis is processed content."
        input_filename = "test_input.md"
        output_dir = tempfile.mkdtemp()
        
        try:
            # 出力ファイル生成
            output_path = generate_output_file(processed_content, input_filename, output_dir)
            
            # 出力ファイルの存在確認
            assert os.path.exists(output_path)
            
            # 内容確認
            with open(output_path, "r", encoding="utf-8") as f:
                content = f.read()
                assert content == processed_content
            
            # 出力ファイル名が正しく生成されていることを確認
            expected_filename = f"processed_{os.path.splitext(input_filename)[0]}.md"
            assert os.path.basename(output_path) == expected_filename
            
        finally:
            # 一時ディレクトリの削除
            if os.path.exists(output_dir):
                import shutil
                shutil.rmtree(output_dir)
    
    def test_main_function(self):
        """メイン関数の統合テスト"""
        # モックを使用して統合テスト
        test_input = "# Test Input\n\nTest content."
        test_format = "# Format\n\nUse headers."
        processed_content = "# Processed Content\n\nFormatted content."
        
        # 一時ファイルとディレクトリの作成
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as input_file:
            input_file.write(test_input)
            input_path = input_file.name
        
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as format_file:
            format_file.write(test_format)
            format_path = format_file.name
        
        output_dir = tempfile.mkdtemp()
        
        try:
            # 各関数のモック化
            with patch("scripts.note_converter.read_markdown_file") as mock_read_md, \
                 patch("scripts.note_converter.read_format_instruction_file") as mock_read_format, \
                 patch("scripts.note_converter.process_markdown") as mock_process, \
                 patch("scripts.note_converter.generate_output_file") as mock_generate, \
                 patch("sys.argv", ["note_converter.py", input_path, 
                                     "--output-dir", output_dir, 
                                     "--format-file", format_path]):
                
                # モックの戻り値設定
                mock_read_md.return_value = test_input
                mock_read_format.return_value = test_format
                mock_process.return_value = processed_content
                mock_generate.return_value = os.path.join(output_dir, "processed_output.md")
                
                # メイン関数呼び出し
                main()
                
                # 各関数が正しく呼び出されたことを確認
                mock_read_md.assert_called_once_with(input_path)
                mock_read_format.assert_called_once_with(format_path)
                mock_process.assert_called_once_with(test_input, test_format)
                mock_generate.assert_called_once()
        
        finally:
            # 一時ファイルとディレクトリの削除
            for path in [input_path, format_path]:
                if os.path.exists(path):
                    os.unlink(path)
            
            if os.path.exists(output_dir):
                import shutil
                shutil.rmtree(output_dir) 