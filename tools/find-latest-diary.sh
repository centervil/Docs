#!/bin/bash
# 最新の開発日記ファイルとZenn用ファイル名を出力

# Usage:
#   eval $(./tools/find-latest-diary.sh [optional_diary_file_path])
#
# Output variables:
#   diary_file: 変換対象の開発日記ファイルのパス
#   output_file: 変換後のZenn記事の出力パス

TARGET_DIARY_FILE=""

if [ -n "$1" ]; then
  # 引数があれば、そのファイルを変換対象とする
  TARGET_DIARY_FILE="$1"
  if [ ! -f "$TARGET_DIARY_FILE" ]; then
    echo "エラー: 指定されたファイルが見つかりません: $TARGET_DIARY_FILE" >&2
    exit 1
  fi
else
  # 引数がない場合、通常のロジックで最新のファイルを検索
  LATEST_MODIFIED_DIARY=$(git diff --name-only HEAD~1 HEAD | grep 'dev-records/.*\.md$' | sort -r | head -n 1)

  if [ -z "$LATEST_MODIFIED_DIARY" ]; then
    echo "変更された開発日記ファイルが見つかりませんでした。最新のファイルを使用します。" >&2
    # 変更されたファイルがない場合、dev-records/ディレクトリ内の最新のファイルを検索
    # 日付と連番でソートする方が確実だが、ls -t で十分なケースも多い
    LATEST_MODIFIED_DIARY=$(find dev-records -name "*.md" | sort -r | head -n 1) # 日付順のファイル名ならこれでOK
    if [ -z "$LATEST_MODIFIED_DIARY" ]; then
      echo "エラー: 開発日記ファイルが見つかりません。" >&2
      exit 1
    fi
  fi
  TARGET_DIARY_FILE="$LATEST_MODIFIED_DIARY"
fi

# ファイル名からZenn記事のファイル名を生成
DIARY_FILENAME=$(basename "$TARGET_DIARY_FILE")
# 拡張子を除去
BASE_FILENAME="${DIARY_FILENAME%.*}"
# output_fileのフォーマットに変換
OUTPUT_FILENAME="${BASE_FILENAME/_development/_dev-diary}" # .mdは既に除去済み
OUTPUT_FILE="articles/${OUTPUT_FILENAME}.md" # 確実に.mdをつける

echo "diary_file=$TARGET_DIARY_FILE"
echo "output_file=$OUTPUT_FILE" 