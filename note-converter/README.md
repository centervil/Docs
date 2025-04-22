# Note Converter

LLM調査結果をnote記事形式に自動変換し、note.comに投稿するシステム

## 背景と目的

### 背景
日々の情報収集に複数のLLMサービス（ChatGPT, Perplexity, Grok, Claudeなど）を利用しているが、調査結果が各プラットフォームに分散し、後で参照しにくい。また、対話形式の調査では、会話スレッドを追わないと流れが分かりにくい場合がある。

### 目的
`Docs/research/` ディレクトリに保存されたMarkdown形式のLLM調査結果を、LLMを利用して分かりやすいnote記事形式に自動変換し、note.comに自動公開する仕組みを構築する。これにより、情報の一元管理と参照性の向上、および知識共有の効率化を目指す。

## 機能

- LLM調査結果（Markdown）の自動変換
- note.comへの下書き投稿
- フォーマットの自動調整
- エラーハンドリングとログ記録

## 必要条件

- Docker
- Docker Compose
- GitHubアカウント（CI/CD利用時）

## セットアップ

1. リポジトリをクローン
```bash
git clone <repository-url>
cd Docs/note-converter
```

2. 環境変数の設定
```bash
cp .env.example .env
# .envファイルを編集して必要な環境変数を設定
```

3. Dockerイメージのビルド
```bash
docker-compose build
```

### note.com認証設定

note.comへの投稿には認証が必要です。以下の認証方法がサポートされています：

#### 1. Cookie認証（推奨）

1. ブラウザでnote.comにログインします
2. 開発者ツール（F12）を開き、「Application」タブ → 「Cookies」 → 「https://note.com」を選択
3. 以下の値をコピーして`.env`ファイルに設定します：
   - `note_gql_auth_token` → `NOTE_AUTH_TOKEN=値`
   - `_note_session_v5` → `NOTE_SESSION_V5=値`


**注意**: Cookieの有効期限は限られているため、一定期間後に再取得が必要になります。

## 使用方法

### ローカル開発

1. 開発コンテナの起動
```bash
docker-compose up -d
```

2. テストの実行
```bash
# すべてのテスト
docker-compose run --rm test

# 特定のテスト
docker-compose run --rm test pytest tests/unit/test_note_converter.py

# note.comのAPI接続テスト（実際のAPIを使用）
# .envファイルでTEST_USE_REAL_API=trueに設定した上で実行
docker-compose run --rm test pytest tests/integration/test_note_api_posting.py -v
```

3. スクリプトの実行
```bash
docker-compose run --rm converter python scripts/note_converter.py
```

### CI/CD

- プッシュまたはプルリクエスト時に自動的にテストが実行されます
- テスト結果はGitHub Actionsのアーティファクトとして保存されます

## システム構成

### ディレクトリ構造
```
Docs/
├── research/                  # 入力となるLLM調査結果
├── templates/                 # テンプレートファイル
│   └── note_format_prompt.md  # note記事フォーマット指示
└── note-converter/           # 変換・投稿システム
    ├── scripts/              # 変換・投稿スクリプト
    │   ├── note_converter.py      # メインスクリプト
    │   ├── clients/               # APIクライアント
    │   │   ├── note_client.py     # note.com APIクライアント
    │   │   └── openrouter_client.py # OpenRouter APIクライアント
    │   ├── config.py              # 設定管理
    │   └── utils/                 # ユーティリティ
    │       ├── markdown_utils.py  # Markdown処理
    │       └── error_handler.py   # エラーハンドリング
    ├── tests/                 # テストコード
    │   ├── unit/              # ユニットテスト
    │   └── integration/       # 統合テスト
    │       ├── test_note_api_posting.py # note.comのAPI連携テスト
    │       └── test_real_api_integration.py # 実APIテスト
    ├── docker/               # Docker関連ファイル
    │   ├── Dockerfile        # 開発・テスト用Dockerfile
    │   ├── docker-compose.yml # ローカル開発環境用
    │   └── entrypoint.sh     # コンテナ起動スクリプト
    ├── .github/              # GitHub Actions設定
    │   └── workflows/        # CI/CDワークフロー
    │       ├── test.yml      # テスト自動化
    │       └── deploy.yml    # デプロイ
    ├── requirements.txt      # Python依存関係
    └── README.md            # プロジェクト説明
```

### 処理フロー
1. **トリガー**: 開発者が `Docs` リポジトリにコミットし、プッシュする。
2. **CI/CDパイプライン起動**: GitHub ActionsなどのCI/CDサービスがプッシュイベントを検知し、ワークフローを開始する。
3. **変更ファイル特定**: ワークフロー内で、コミットによって追加・変更されたファイルのうち、`Docs/research/` ディレクトリ配下のMarkdownファイル（`.md`）を特定する。
4. **記事変換処理**: 特定された各Markdownファイルに対して、以下の処理を実行する。
    a.  **ファイル読み込み**: Markdownファイルの内容を読み込む。
    b.  **フォーマット指示読み込み**: 事前に定義されたnote記事用フォーマット指示Markdownファイル (`Docs/templates/note_format_prompt.md` とする) の内容を読み込む。
    c.  **OpenRouter API呼び出し**: 読み込んだ調査結果Markdownとフォーマット指示Markdownを組み合わせたプロンプトを作成し、OpenRouter APIに送信してnote記事形式のMarkdown生成を依頼する。
    d.  **変換結果取得**: OpenRouter APIから変換後のMarkdownコンテンツを取得する。
5.  **note.com下書き投稿**: 変換されたMarkdownコンテンツを、note.comの非公式APIを使用して下書きとして投稿する。
6.  **結果通知**: 処理結果（成功・失敗、投稿された下書きURLなど）をワークフローのログに出力する。

## 開発ガイド

### コード規約

- PEP 8に準拠
- 型ヒントの使用
- ドキュメント文字列の記述

### テスト

- ユニットテスト: `tests/unit/`
- 統合テスト: `tests/integration/`
- カバレッジ目標: 80%以上

### コミットメッセージ

- プレフィックス: `feat:`, `fix:`, `docs:`, `test:`, `chore:`
- 英語で記述
- 変更内容を簡潔に説明

## トラブルシューティング

### よくある問題

1. **Docker起動エラー**
   - ポートの競合を確認
   - イメージを再ビルド

2. **認証エラー**
   - 環境変数の設定を確認
   - セッションの有効期限を確認
   - Cookie認証の場合、Cookieの有効期限が切れていないか確認（再取得が必要な場合あり）
   - CSRFトークン取得の問題が発生する場合は、Cookie認証に切り替えることで解決できる可能性があります

3. **テスト失敗**
   - テスト環境の設定を確認
   - モックの設定を確認

## ライセンス

MIT License

## 貢献

1. イシューの作成
2. ブランチの作成
3. 変更の実装
4. テストの追加
5. プルリクエストの作成 