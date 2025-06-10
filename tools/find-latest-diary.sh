#!/bin/bash
# 最新の開発日記ファイルとZenn用ファイル名を出力

LATEST_DIARY=$(find dev-records -type f -name "*.md" | sort -r | head -n 1)
if [ -z "$LATEST_DIARY" ]; then
  echo "diary_file="
  echo "output_file="
  exit 0
fi

OUTPUT_FILENAME=$(./tools/diary-filename-processor.sh "$LATEST_DIARY")
echo "diary_file=$LATEST_DIARY"
echo "output_file=articles/$OUTPUT_FILENAME" 