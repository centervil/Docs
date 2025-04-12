FROM python:3.11-slim

WORKDIR /app

# 依存関係ファイルのコピー
COPY requirements.txt .

# 依存関係のインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードのコピー
COPY . .

# エントリーポイント設定
ENTRYPOINT ["/bin/bash", "/app/docker/entrypoint.sh"] 