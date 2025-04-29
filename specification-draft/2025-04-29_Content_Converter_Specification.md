# Content-Converter プロジェクト仕様書

## 1. 概要

Content-Converterは、マークダウン形式のテキストファイルを様々な公開プラットフォーム用に最適化して変換するツールです。既存のDiary-ConverterとNote-Converterを統合し、拡張性と保守性を高めた統合ソリューションを提供します。LLM（大規模言語モデル）を活用して、テキスト変換の高度なカスタマイズと最適化を実現します。

本プロジェクトの開発は、`Docs/dev-docs/development_process_guide.md`に定義されている開発プロセスとベストプラクティスに従って実施します。また、既存の`Docs`リポジトリのCI/CDパイプラインに統合する形で開発を進めます。

## 2. 背景と目的

### 背景

- 既存の「Diary-Converter」はZennプラットフォーム向けの変換機能を提供
- 「Note-Converter」はnote.comプラットフォーム向けの変換機能を開発中
- 両ツールには多くの共通機能があり、別々に管理することで開発・保守の重複が発生
- サードパーティツール「OASIS」がnote.com等への投稿機能を提供しており、内部活用の検討が必要

### 目的

- 共通機能を統合し、プラットフォーム固有の機能を拡張可能なアーキテクチャで実装
- 複数のLLM APIをサポートし、ユーザーが選択できるようにする
- CI/CD環境を統合し、テスト・デプロイプロセスを効率化
- 将来的な新プラットフォーム対応を容易にする拡張性の高い設計を実現
- OASISツールとの連携により、note.comへの投稿機能を強化

## 3. 機能要件

### 3.1 コア機能

- マークダウンファイルの読み込みと解析
- フロントマター処理（メタデータ抽出・加工）
- LLMによるコンテンツ最適化処理
- 出力形式の生成（プラットフォーム固有フォーマット）
- テンプレート適用メカニズム

### 3.2 プラットフォーム対応

- Zennプラットフォーム向け変換機能
  - Zenn記事形式への最適化
  - Zenn固有メタデータ処理
  - 画像パス修正機能
- note.comプラットフォーム向け変換機能
  - note記事形式への最適化
  - note固有の埋め込みコンテンツ対応
  - OASIS連携によるnote.com投稿機能（オプション）

### 3.3 LLM機能

- 複数LLM APIサポート
  - Gemini API連携
  - OpenRouter API連携（Claude, GPT-4など）
- LLMプロンプトテンプレート管理
- LLM応答キャッシュ機能（オプション）
- エラーリトライ機能

### 3.4 ユーザーインターフェース

- コマンドラインインターフェース（CLI）
  - 変換元ファイル指定
  - 出力先指定
  - ターゲットプラットフォーム選択
  - LLM選択オプション
  - テンプレート選択オプション
  - OASIS連携オプション
- 設定ファイルによる環境設定
  - API認証情報
  - デフォルトオプション設定
  - カスタムテンプレートパス
  - OASIS設定

## 4. 非機能要件

### 4.1 パフォーマンス

- 単一ファイル変換は30秒以内に完了すること
- 複数ファイルの一括処理をサポート
- APIリクエスト最適化（必要最小限のトークン使用）

### 4.2 拡張性

- 新プラットフォーム追加が容易な設計
- 新LLMプロバイダー追加が容易な設計
- プラグインアーキテクチャの採用
- サードパーティツール連携インターフェース

### 4.3 保守性

- モジュール化された設計
- `development_process_guide.md`に従ったテスト駆動開発
- Docsリポジトリの既存CI/CDパイプラインとの統合

### 4.4 信頼性

- エラー発生時の適切なリカバリー
- タイムアウト処理
- APIダウン時の代替処理
- OASIS連携時の例外処理

### 4.5 セキュリティ

- API認証情報の安全な管理
- ユーザーデータの適切な取り扱い
- 安全な依存関係管理
- サードパーティツール連携時のセキュリティ考慮

## 5. アーキテクチャ設計

### 5.1 全体アーキテクチャ

本システムは下記のコンポーネントで構成されます：

```
Content-Converter/
├── src/
│   └── content_converter/
│       ├── __init__.py
│       ├── converter.py         # メインコンバーター
│       ├── document_processor.py
│       ├── template_manager.py
│       ├── platforms/
│       │   ├── __init__.py
│       │   ├── base.py          # 基底プラットフォームクラス
│       │   ├── zenn.py
│       │   └── note.py
│       ├── llm/
│       │   ├── __init__.py
│       │   ├── factory.py       # LLMクライアントファクトリー
│       │   ├── base.py          # 基底LLMクラス
│       │   ├── gemini_client.py
│       │   └── openrouter_client.py
│       └── integrations/
│           ├── __init__.py
│           └── oasis_integration.py  # OASIS連携モジュール
├── templates/
│   ├── zenn/
│   │   └── article_template.md
│   └── note/
│       └── article_template.md
├── tests/
    └── ...
```

### 5.2 コンポーネント詳細

#### 5.2.1 コアコンポーネント

- **converter.py**: メインの変換エンジン、プラットフォームとLLMの調整
- **document_processor.py**: マークダウン解析・加工機能
- **template_manager.py**: テンプレート読み込み・適用機能

#### 5.2.2 プラットフォームコンポーネント

- **platforms/base.py**: 全プラットフォーム共通の基底クラス
- **platforms/zenn.py**: Zenn固有の処理
- **platforms/note.py**: note.com固有の処理

#### 5.2.3 LLMコンポーネント

- **llm/factory.py**: LLMクライアント作成ファクトリー
- **llm/base.py**: LLMクライアントの基底クラス
- **llm/gemini_client.py**: Gemini API連携
- **llm/openrouter_client.py**: OpenRouter API連携

#### 5.2.4 外部連携コンポーネント
- **integrations/oasis_integration.py**: OASISツールとの連携インターフェース

### 5.3 データフロー

1. 入力ファイル読み込み
2. フロントマター解析・処理
3. テンプレート適用
4. LLM処理依頼
5. 応答処理
6. プラットフォーム固有フォーマットへの変換
7. 出力ファイル生成（または外部ツール連携）

## 6. インターフェース設計

### 6.1 コマンドラインインターフェース

```
content-convert [OPTIONS] INPUT_FILE [OUTPUT_FILE]

Options:
  --platform TEXT     変換先プラットフォーム (zenn, note) [required]
  --llm TEXT          使用するLLM (gemini, claude, gpt4) [default: gemini]
  --template TEXT     使用するテンプレート名
  --config FILE       設定ファイルパス
  --debug             デバッグモード有効化
  --dry-run           変換のみ行い、出力しない
  --use-oasis         OASISを使用してnote.comに投稿
  --help              ヘルプ表示
```

### 6.2 設定ファイル形式

```yaml
# config.yaml
general:
  default_platform: zenn
  default_llm: gemini
  template_dir: ./templates

platforms:
  zenn:
    template: default
    output_dir: ./articles
    
  note:
    template: default
    output_dir: ./note_articles
    use_oasis: false  # OASISを使用するかどうか

llm:
  gemini:
    api_key: ${GEMINI_API_KEY}
    
  openrouter:
    api_key: ${OPENROUTER_API_KEY}
    model: anthropic/claude-3-5-sonnet

integrations:
  oasis:
    enabled: false
    install_path: ${OASIS_PATH}
    config_path: ${OASIS_CONFIG}
```

### 6.3 OASIS連携インターフェース
```python
# OASIS連携の基本的な使用例
from content_converter.integrations.oasis_integration import OasisPublisher

publisher = OasisPublisher(config_path="path/to/oasis/config")
result = publisher.publish_to_note(markdown_file_path="path/to/processed/file.md")
```

## 7. CI/CD統合

Content-Converterは既存のDocsリポジトリのCI/CDパイプラインに統合されます。以下の点に特に注意します：

### 7.1 統合方法
- 既存のGitHub Actionsワークフローに新しいジョブを追加
- Dockerコンテナベースのビルド・テスト環境
- テスト自動化とカバレッジレポート

### 7.2 デプロイ戦略
- マスターブランチへのマージ時に自動テスト実行
- テスト成功時に自動的にリリースタグ付け
- PyPIへの自動パッケージ公開（オプション）

### 7.3 CI/CDパイプラインフロー
1. コードプッシュ/PRイベント検知
2. 依存関係インストール
3. 静的解析（Flake8, MyPy）
4. ユニットテスト実行
5. 統合テスト実行
6. テストカバレッジレポート生成
7. Docsリポジトリの他のコンポーネントとの統合テスト
8. (マスターブランチのみ) リリース手順実行

## 8. 開発ロードマップ

### フェーズ1: 基盤構築

- プロジェクト構造作成
- コアコンポーネント実装
- 基本テスト実装
- CI/CD初期統合

### フェーズ2: プラットフォーム統合

- Zenn対応の移行実装
- note.com基本対応の移行実装
- 統合テスト

### フェーズ3: LLM統合

- LLMファクトリー実装
- Gemini API実装
- OpenRouter API実装
- LLMテスト

### フェーズ4: OASIS連携実装

- OASISインテグレーションモジュール開発
- OASIS APIラッパー機能
- note.com拡張機能の実装
- 連携テスト

### フェーズ5: テスト・ドキュメント

- 徹底的なテスト実施
- ドキュメント整備
- 利用ガイド作成

## 9. リスクと考慮事項

### 9.1 潜在的なリスク

- LLM API仕様の変更・非互換性
- プラットフォーム固有の要件変更
- 依存ライブラリの互換性問題
- OASISの仕様変更・サポート停止リスク

### 9.2 対策

- API抽象化レイヤーの徹底
- プラットフォーム要件の定期確認
- バージョン固定とアップデート戦略の確立
- 十分なエラーハンドリングの実装
- OASIS依存部分のモジュール化と代替戦略検討

## 10. 依存関係

### 必須依存パッケージ

```
# requirements.txt
pyyaml>=6.0
python-frontmatter>=1.0.0
requests>=2.28.0
python-dotenv>=1.0.0
markdown>=3.4.0
pydantic>=2.5.2
```

### オプション依存パッケージ

```
# requirements-optional.txt
oasis-article>=0.8.0  # OASIS連携用
```

### 開発・テスト依存パッケージ
開発およびテスト関連の依存関係は`development_process_guide.md`に従って設定します。

## 11. ライセンス

MIT License

## 12. 参考資料

- Diary-Converter GitHub リポジトリ
- Note-Converter GitHub リポジトリ
- Zenn API ドキュメント
- note API ドキュメント
- Gemini API ドキュメント
- OpenRouter API ドキュメント
- OASIS GitHub リポジトリおよびドキュメント
- `Docs/dev-docs/development_process_guide.md` (開発プロセスガイド)
