#!/bin/bash

# 開発日記ファイルのパスを受け取り、Zennの記事用ファイル名を生成するスクリプト

# 引数の確認
if [ "$#" -ne 1 ]; then
  echo "使用方法: $0 <開発日記ファイルパス>"
  exit 1
fi

DIARY_FILE=$1

# ベースファイル名を取得
DIARY_FILENAME=$(basename "$DIARY_FILE")

# 日付部分を抽出
DATE_PART=$(echo "$DIARY_FILENAME" | grep -oP '\d{4}-\d{2}-\d{2}')

# テーマ部分を抽出
THEME_PART=$(echo "$DIARY_FILENAME" | sed "s/${DATE_PART}-//g" | sed "s/.md$//g")

# Zennのslugルールに従って調整
# 1. 大文字を小文字に変換
SLUG_THEME=$(echo "$THEME_PART" | tr '[:upper:]' '[:lower:]')

# 2. 先頭に日付を追加
SLUG="${DATE_PART}-${SLUG_THEME}"

# 3. 文字数をチェック（拡張子を除いて12〜50字）
SLUG_LENGTH=${#SLUG}
if [ $SLUG_LENGTH -lt 12 ]; then
  # 12文字未満の場合、接尾辞を追加
  ADDITIONAL_CHARS=$((12 - SLUG_LENGTH))
  SUFFIX="-zenn-article"
  SLUG="${SLUG}${SUFFIX}"
  echo "slugが短すぎるため接尾辞を追加: $SLUG" >&2
elif [ $SLUG_LENGTH -gt 50 ]; then
  # 50文字を超える場合、切り詰め
  SLUG="${SLUG:0:50}"
  echo "slugが長すぎるため切り詰め: $SLUG" >&2
fi

# 最終的な出力ファイル名
OUTPUT_FILENAME="${SLUG}.md"

# 出力
echo "$OUTPUT_FILENAME" 