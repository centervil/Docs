#!/bin/bash
# 最新のZenn記事スラッグを出力

LATEST_ARTICLE=$(find articles -type f -name "*.md" | sort -r | head -n 1)
if [ -n "$LATEST_ARTICLE" ]; then
  PREV_ARTICLE_SLUG=$(basename "$LATEST_ARTICLE" .md)
  echo "prev_article_slug=$PREV_ARTICLE_SLUG"
else
  echo "prev_article_slug="
fi 