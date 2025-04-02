#!/bin/bash

# 開発日記ファイルのパスを受け取り、Zennの記事用ファイル名を生成するスクリプト

# 引数の確認
if [ "$#" -ne 1 ]; then
  echo "使用方法: $0 <開発日記ファイルパス>" >&2
  exit 1
fi

DIARY_FILE=$1

# ベースファイル名を取得
DIARY_FILENAME=$(basename "$DIARY_FILE")

# 日付部分を抽出 (YYYY-MM-DD)
DATE_PART=$(echo "$DIARY_FILENAME" | grep -oP '^\d{4}-\d{2}-\d{2}')
if [ -z "$DATE_PART" ]; then
  echo "エラー: ファイル名から日付を抽出できませんでした: $DIARY_FILENAME" >&2
  exit 1
fi

# 通し番号を抽出 (例: 033)
SERIAL_NUMBER=$(echo "$DIARY_FILENAME" | grep -oP '(?<=^\d{4}-\d{2}-\d{2}_)\d+(?=_development\.md$)')
if [ -z "$SERIAL_NUMBER" ]; then
  echo "エラー: ファイル名から通し番号を抽出できませんでした: $DIARY_FILENAME" >&2
  exit 1
fi

# 固定のSLUGを生成
SLUG="${DATE_PART}_${SERIAL_NUMBER}_dev-diary"

# 最終的な出力ファイル名
OUTPUT_FILENAME="${SLUG}.md"

# 出力
echo "$OUTPUT_FILENAME"
