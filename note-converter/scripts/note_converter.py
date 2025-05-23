#!/usr/bin/env python3
"""
note記事化システムのメインスクリプト

Markdown形式の入力ファイルを読み込み、フォーマット指示に基づいて
LLMを使用して記事を整形します。
"""
import os
import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 必要に応じてimportパスを設定
ROOT_DIR = Path(__file__).parent.parent.absolute()
sys.path.append(str(ROOT_DIR))

# OpenRouterクライアントをインポート
from scripts.openrouter_client import OpenRouterClient, OpenRouterAPIError

# LLMを使った処理関数
def process_with_llm(markdown_content, format_instructions):
    """LLMを使用してマークダウンコンテンツを処理する"""
    logger.info("LLM APIを使用してマークダウンを処理します")
    
    # 環境変数からAPIキーを取得
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        logger.warning("OPENROUTER_API_KEYが設定されていません。モック応答を返します。")
        return f"LLMで処理されたコンテンツ:\n\n{markdown_content}"
    
    try:
        # OpenRouterクライアントを初期化
        client = OpenRouterClient(
            api_key=api_key,
            model="anthropic/claude-3.5-sonnet",
            max_tokens=4096,
            temperature=0.7
        )
        
        # プロンプトをフォーマットして生成リクエスト
        prompt = client.format_prompt(markdown_content, format_instructions)
        response = client.generate_text(prompt)
        
        logger.info("LLM処理が完了しました")
        return response
        
    except OpenRouterAPIError as e:
        logger.error(f"LLM API呼び出しエラー: {str(e)}")
        # エラー時はモック応答を返す
        return f"APIエラーが発生しました。元のコンテンツ:\n\n{markdown_content}"
    except Exception as e:
        logger.error(f"予期せぬエラー: {str(e)}")
        # エラー時はモック応答を返す
        return f"エラーが発生しました。元のコンテンツ:\n\n{markdown_content}"

def parse_args():
    """コマンドライン引数をパースする"""
    parser = argparse.ArgumentParser(
        description="Markdown形式のファイルをnote記事形式に変換します"
    )
    
    # 必須の入力ファイル引数
    parser.add_argument(
        "input_file",
        help="変換するマークダウンファイルのパス"
    )
    
    # オプション引数
    parser.add_argument(
        "--output-dir",
        default="output",
        help="出力ディレクトリ（デフォルト: output）"
    )
    
    parser.add_argument(
        "--format-file",
        default=os.path.join(ROOT_DIR.parent, "templates", "note_format_prompt.md"),
        help="フォーマット指示ファイルのパス"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="ログレベル（デフォルト: INFO）"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="ドライラン（実際にはAPIを呼び出さない）"
    )
    
    return parser.parse_args()

def read_markdown_file(file_path):
    """マークダウンファイルを読み込む"""
    logger.info(f"マークダウンファイルを読み込み中: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"ファイルが見つかりません: {file_path}")
        raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")
    except Exception as e:
        logger.error(f"ファイル読み込み中にエラーが発生しました: {e}")
        raise

def read_format_instruction_file(file_path):
    """フォーマット指示ファイルを読み込む"""
    logger.info(f"フォーマット指示ファイルを読み込み中: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"ファイルが見つかりません: {file_path}")
        raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")
    except Exception as e:
        logger.error(f"ファイル読み込み中にエラーが発生しました: {e}")
        raise

def process_markdown(markdown_content, format_instructions):
    """マークダウンコンテンツをフォーマット指示に基づいて処理する"""
    logger.info("マークダウンコンテンツを処理中...")
    
    # LLMを使用してマークダウンを処理
    processed_content = process_with_llm(markdown_content, format_instructions)
    
    return processed_content

def generate_output_file(processed_content, input_filename, output_dir):
    """処理されたコンテンツを出力ファイルに書き込む"""
    # 出力ディレクトリが存在しない場合は作成
    os.makedirs(output_dir, exist_ok=True)
    
    # 入力ファイル名から出力ファイル名を生成（YYYYMMDD_title.md 形式）
    base_name = os.path.basename(input_filename)
    name_without_ext = os.path.splitext(base_name)[0]
    # 日付部分を取得（なければ今日の日付）
    today = datetime.now().strftime('%Y%m%d')
    output_filename = f"{today}_{name_without_ext}.md"
    output_path = os.path.join(output_dir, output_filename)
    
    logger.info(f"処理結果を出力中: {output_path}")
    
    # ファイルに書き込み
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(processed_content)
    
    return output_path

def main():
    """メイン実行関数"""
    try:
        # コマンドライン引数のパース
        args = parse_args()
        
        # ログレベルの設定
        logger.setLevel(getattr(logging, args.log_level))
        
        # 入力ファイルの読み込み
        markdown_content = read_markdown_file(args.input_file)
        
        # フォーマット指示ファイルの読み込み
        format_instructions = read_format_instruction_file(args.format_file)
        
        # ドライランモードのチェック
        if args.dry_run:
            logger.info("ドライランモードで実行中 - LLM APIは呼び出されません")
            logger.info(f"入力ファイル: {args.input_file}")
            logger.info(f"フォーマット指示ファイル: {args.format_file}")
            logger.info(f"出力ディレクトリ: {args.output_dir}")
            return
        
        # マークダウン処理
        processed_content = process_markdown(markdown_content, format_instructions)
        
        # 出力ファイル生成（保存先を note-articles/ に変更）
        output_dir = "note-articles"
        output_path = generate_output_file(processed_content, args.input_file, output_dir)
        
        logger.info(f"処理が完了しました。出力ファイル: {output_path}")
        
    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 