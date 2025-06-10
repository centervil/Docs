#!/bin/bash
# Usage: ./replace_template_placeholders.sh <MODEL_NAME> <PREV_ARTICLE_SLUG> <TEMPLATE_PATH> <OUTPUT_PATH>

if [ "$#" -ne 4 ]; then
  echo "Usage: $0 <MODEL_NAME> <PREV_ARTICLE_SLUG> <TEMPLATE_PATH> <OUTPUT_PATH>" >&2
  exit 1
fi

MODEL_NAME="$1"
PREV_ARTICLE_SLUG="$2"
TEMPLATE_PATH="$3"
OUTPUT_PATH="$4"

sed -e "s/\[LLM Model名\]/${MODEL_NAME}/g" \
    -e "s/\[前回の記事スラッグ\]/${PREV_ARTICLE_SLUG}/g" \
    "$TEMPLATE_PATH" > "$OUTPUT_PATH" 