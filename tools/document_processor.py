#!/usr/bin/env python3
"""
ドキュメント処理モジュール

Diary-Converterで生成されたドキュメントの後処理を行うモジュール。
LLMによって生成されたドキュメントの一般的な問題を修正します。
"""

import os
import sys
import re
import argparse
import logging
from typing import List, Callable, Dict, Any, Optional


class DocumentProcessor:
    """ドキュメント処理クラス"""

    def __init__(self, debug: bool = False):
        """初期化"""
        self.debug = debug
        self.setup_logging()
        # 処理関数のリスト（順番に実行される）
        self.processors: List[Callable[[str], str]] = [
            self.remove_markdown_code_block,
            # 将来的に他の処理関数を追加可能
            # self.fix_frontmatter_format,
            # self.normalize_headings,
            # self.fix_image_paths,
            # など
        ]

    def setup_logging(self):
        """ロギングの設定"""
        level = logging.DEBUG if self.debug else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('DocumentProcessor')

    def remove_markdown_code_block(self, content: str) -> str:
        """
        マークダウンファイル全体を囲むコードブロックを削除する
        """
        self.logger.debug("remove_markdown_code_blockを開始します。")

        # コンテンツの先頭と末尾の空白をトリム
        trimmed_content = content.strip()

        # 先頭がコードブロックマーカーで始まり、末尾がコードブロックマーカーで終わるかチェック
        # ここで、言語指定の有無も考慮する
        starts_with_code_block_match = re.match(r"^```(?:[a-zA-Z]+\s*)?", trimmed_content)

        if starts_with_code_block_match:
            self.logger.debug("ドキュメント冒頭にコードブロックマーカーを検出しました。")
            
            content_after_start = trimmed_content[starts_with_code_block_match.end():]
            
            # 末尾にもコードブロックマーカーがあるかチェック
            ends_with_code_block = content_after_start.rstrip().endswith('```')

            if ends_with_code_block:
                self.logger.debug("ドキュメント全体がコードブロックで囲まれています。削除を試みます。")
                # 末尾のコードブロックマーカーを削除
                content_without_end = content_after_start.rstrip()[:-3].rstrip()
                self.logger.debug("囲むコードブロックを削除しました。")
                return content_without_end
            else:
                self.logger.debug("冒頭のコードブロックマーカーのみを削除します。")
                # 末尾のコードブロックマーカーがない場合、先頭のマーカーのみを削除
                return content_after_start.lstrip() # 先頭の空白も削除
        else:
            self.logger.debug("ドキュメント冒頭にコードブロックマーカーは見つかりませんでした。")
            return content # 変更なし

    def process(self, input_file: str, output_file: Optional[str] = None) -> bool:
        """
        ドキュメントを処理する
        
        Args:
            input_file: 入力ファイルのパス
            output_file: 出力ファイルのパス（Noneの場合は入力ファイルを上書き）
            
        Returns:
            処理が成功したかどうか
        """
        try:
            # 入力ファイルを読み込む
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            self.logger.debug(f"ファイル読み込み: {input_file}")
            
            # 各処理関数を順番に適用
            original_content = content
            for processor in self.processors:
                content = processor(content)
                
            # 変更があったかチェック
            if content == original_content:
                self.logger.info("ドキュメントに変更はありませんでした。")
            else:
                self.logger.info("ドキュメントを修正しました。")
                
            # 出力ファイルに書き込む
            output_path = output_file if output_file else input_file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            self.logger.debug(f"ファイル書き込み: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"処理中にエラーが発生しました: {e}")
            return False


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description="ドキュメント処理ツール")
    parser.add_argument("input", help="入力ファイルのパス")
    parser.add_argument("-o", "--output", help="出力ファイルのパス（指定しない場合は入力ファイルを上書き）")
    parser.add_argument("--debug", action="store_true", help="デバッグモードを有効にする")
    args = parser.parse_args()
    
    processor = DocumentProcessor(debug=args.debug)
    success = processor.process(args.input, args.output)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
