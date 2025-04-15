#!/bin/bash
set -e

# コマンドライン引数に基づいて実行する動作を決定
if [ "$1" = "test" ]; then
    echo "テストを実行します..."
    
    # テストカバレッジ付きでテストを実行
    if [ "$2" = "coverage" ]; then
        pytest --cov=scripts --cov-report=term --cov-report=html:reports/coverage "${@:3}"
    else
        pytest "${@:2}"
    fi

elif [ "$1" = "lint" ]; then
    echo "リンターを実行します..."
    flake8 scripts tests

elif [ "$1" = "run" ]; then
    echo "アプリケーションを実行します..."
    python -m scripts.note_converter "${@:2}"

else
    # デフォルトでは対話的なシェルを提供
    exec "$@"
fi
