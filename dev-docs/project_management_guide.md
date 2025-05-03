# プロジェクト管理ガイド（AIエージェント開発向け）

このドキュメントは、AIコーディングエージェント（Cursor, Cline, MCPなど）が主体となって開発を進め、人間がプロジェクトマネージャー（PM）として監視・レビュー・承認を行う開発体制における管理手法とツールについて解説します。AIエージェントは自律的にコード記述やテスト実行を行い、PMは方向性の指示、進捗確認、レビュー、承認を通じて品質とセキュリティを保証します。`devsecops_guide.md` と合わせて参照してください。本ガイドは特にPythonプロジェクトを念頭に置いていますが、多くの原則は他の言語やフレームワークにも適用できます。

## 1. プロジェクト管理のフレームワーク (チケット駆動 & Human-In-The-Loop)

### 1.1 Githubを活用した進捗管理

開発の中心はGitHub Issue（チケット）とし、AIエージェントの自律的な開発活動の管理にGitHubを最大限活用します。

#### プロジェクトボード

- **プロジェクトボードの作成**: 各プロジェクトごとにGitHubプロジェクトボードを作成
- **カンバン方式の採用**: 「Todo」「In Progress」「Review」「Done」のカラムを設定。AIエージェントは自律的にチケットを「In Progress」に移動し、作業完了時に「Review」に移動します。
- **自動化ルールの設定**:
  - AIがブランチを作成したら自動的に「Todo」から「In Progress」に移動
  - AIがPRをオープンしたら自動的に「In Progress」から「Review」に移動
  - PRがマージされたら（PMが承認後）自動的に「Review」から「Done」に移動
  - Issue がクローズされたら自動的に「Done」に移動

#### Issue管理 (チケット駆動開発)

- **チケット駆動**: すべての開発作業はGitHub Issue（チケット）を起点とします。PMはチケットを作成し、開発のゴールと背景、達成基準 (Acceptance Criteria) を記述します。セキュリティ要件や脅威モデルの結果も必要に応じて含めます。 AIエージェントはチケットの内容を理解し、自律的に開発を進めます。
- **タスクの粒度**: 
  - AIエージェントが自律的に1-2日程度で完了できる、明確で独立した作業単位を目安とします。
  - 大きな機能は複数のチケットに分割し、チケット間の依存関係を明示します。
  - 例: ユーザー管理システム → (1)ユーザーモデル設計・データベーススキーマ作成、(2)ユーザー登録APIエンドポイント実装(入力バリデーション強化)、(3)認証機能実装(セキュアなセッション管理含む)、(4)ユーザープロフィール管理機能実装、(5)ユーザー権限管理機能実装、といった粒度。
  - チケットの記述では具体的な実装手法ではなく「何を」達成すべきかを明確にし、「どのように」実装するかはAIエージェントの裁量に任せます。
- **テンプレートの活用**: 機能開発、バグ修正、リファクタリングなど、チケットの種類に応じたテンプレートを用意し、必要な情報（目的、期待される結果、制約、参照ファイル、関連するセキュリティ要件）を構造化します。AIエージェントが自律的に判断できるよう、実装方法の詳細は指定せず、達成すべき目標を明確にします。
- **ラベルの体系化**: 
  - 優先度: `priority:high`, `priority:medium`, `priority:low`
  - 種類: `type:feature`, `type:bug`, `type:docs`, `type:refactor`, `type:security`
  - 状態: `status:blocked`, `status:needs-discussion`, `status:agent-working`, `status:human-review`
- **マイルストーン**: 開発フェーズや期間ごとにマイルストーンを設定し、チケットを紐付け、進捗を管理します。

#### プルリクエスト (PMによる品質保証)

- **PRテンプレートの活用**: AIエージェントが作成したPRには、関連するIssue番号、変更の概要、実装アプローチ、テスト結果（CI/CDによる）、実施したセキュリティチェック（SAST結果など）の要約などを記載するようにテンプレートで定めます。
- **レビュープロセス (Human-In-The-Loop)**: AIエージェントが作成したコードは、PMがレビューします。細かな実装ではなく、全体的なアーキテクチャ、方向性、セキュリティ（CI/CDのセキュリティチェック結果含む）などの重要な側面に焦点を当てます。
- **修正指示**: レビューで問題が見つかった場合、PMは高レベルな修正方針をコメントし、AIエージェントが自律的に修正方法を決定して実装します。
- **自動テスト**: CI/CDパイプラインによる自動テスト (およびセキュリティスキャン) は必須です。テスト結果はPRに表示され、レビューの判断材料となります。
- **最終承認**: すべてのレビューコメントが解決され、CIテストとセキュリティチェックがパスした後、PMが最終的にPRを承認し、マージします。

### 1.2 AIエージェントへの指示と連携 (PMの役割)

PMはAIエージェントの効果的な「ガイド」および「レビュアー」としての役割を担い、AIの自律性を尊重します。

- **高レベルな目標設定**: チケットを通じて、目的、期待成果、制約、参照情報（`@`メンション活用）を提供しますが、実装の詳細はAIに委ねます。
- **必要最小限のコンテキスト提供**: AIが自律的に判断するために必要な背景情報のみを提供し、過度な干渉は避けます。
- **重要判断点でのレビュー (Human-In-The-Loop)**: すべての段階ではなく、重要な判断ポイントでのみPMがレビューフィードバックを行い、AIの創造性と自律性を最大化します。
- **対話ログの活用**: 開発日記に対話ログを記録し、PMとAIの決定事項や方向性の変更を明確に残します。

### 1.3 Model Context Protocol (MCP) の活用

MCPは、AIエージェントが外部ツールやリソース（ファイルシステム、Web、APIなど）と対話するための標準プロトコルです。AIエージェントの能力を拡張するために活用します。

#### MCPの役割と利用シーン
- **ファイルシステムアクセス**: コードの読み書き、ファイル生成・削除
- **Web情報取得**: ドキュメント参照、ライブラリ調査、Webスクレイピング
- **外部API連携**: GitHub操作、Slack通知、データベースアクセスなど
- **その他**: AIエージェントが単独で実行できないタスク全般

#### MCPサーバーの選択と設定
- **サーバー選択**: タスクに必要な機能を持つMCPサーバーを選択します。コミュニティ製サーバーの利用時は信頼性を確認します。
- **設定**: 利用するMCPサーバーのコマンドや引数を設定ファイル (`mcp_agent.config.yaml` など) に定義します。
- **認証**: APIキーなどが必要なサーバーは、`.env` やシークレット管理ツールを用いて安全に設定します。
- **注意**: MCPサーバーの実行には `npx` や `uvx` などのランタイムが必要な場合があります。リモートサーバー接続は標準化が進行中です。

#### AIエージェントへのMCP利用指示
- AIエージェントに対し、どのMCPサーバー（またはツール）を利用するかを明確に指示します。
- 例：「`filesystem`サーバーを使って`README.md`を読み込んでください」
- 例：「`fetch`サーバーを使ってこのURLの内容を取得し、要約してください」

### 1.4 振り返りと改善活動 (チケット完了時)

チケットが「Done」になった際、AIエージェントとPMは共同で振り返りを行い、得られた学びを次に活かします。この活動はAIエージェント開発プロセスの継続的な改善に不可欠です。

- **振り返りの観点**:
  - **目標達成度**: チケットの達成基準は満たされたか？期待通りの成果が得られたか？
  - **プロセス効率**: AIの自律的な判断は適切だったか？PMの介入は必要最小限だったか？手戻りは発生しなかったか？
  - **AIのパフォーマンス**: AIは期待される品質のコードを生成したか？アーキテクチャや設計判断は適切だったか？
  - **コミュニケーション**: PMとAI間の認識齟齬はなかったか？チケットの記述に改善の余地はあるか？
  - **技術的負債**: 実装過程で新たな技術的負債が発生していないか？既存の負債に対処できたか？
  - **セキュリティ**: 開発中にセキュリティ上の懸念は発生しなかったか？CI/CDでのセキュリティチェックは有効だったか？新たな脅威は考慮すべきか？
  - **開発ドキュメント**: 今回の作業を通じて、既存ドキュメント (`devsecops_guide.md`含む) に不足や改善点は見つからなかったか？
- **改善アクション**:
  - **チケット改善**: より効果的なチケット記述方法を特定し、テンプレートやガイドラインを更新します。
  - **AIの自律性向上**: AIエージェントがより自律的に判断できる領域を特定し、PMの介入を減らす方策を検討します。
  - **ドキュメント修正/追記**: 開発プロセスガイド、テスト戦略、プロジェクト管理ガイド、DevSecOpsガイドなどの関連ドキュメントを更新し、今回の学びを反映させます。
  - **AI設定調整**: 利用するAIモデルやツールの設定を見直します。
  - **アーキテクチャ改善**: 実装を通じて明らかになったアーキテクチャの弱点や改善点を特定し、今後のチケットに反映します。
  - **セキュリティプラクティスの改善**: 脅威モデルの見直し、セキュリティテストの追加・改善、CI/CDへのセキュリティチェック強化などを検討します。
- **実施プロセス**:
  1. チケットが「Done」になった後、AIエージェントが振り返りを提案し、主な観点に基づく自己評価を行います。
  2. PMはAIの自己評価に対してフィードバックを提供し、追加の観点や改善点を指摘します。
  3. AIとPMは共同で具体的な改善アクションを決定し、それを実行するための新たなチケットを作成するか、既存のプロセスやドキュメントを更新します。
  4. 振り返りの内容と決定した改善アクションは、開発日記や別途管理する改善ログに記録します。

## 2. テスト戦略

### 2.1 Pytestを活用したテスト駆動開発

#### テスト構造

- **階層的テスト構造**:
  ```
  tests/
  ├── conftest.py        # 共通フィクスチャ
  ├── unit/              # ユニットテスト
  │   └── test_*.py      
  ├── integration/       # 統合テスト
  │   └── test_*_integration.py
  └── e2e/               # エンドツーエンドテスト
      └── test_*_e2e.py
  ```

#### Pytestの拡張機能活用

- **pytest-cov**: コードカバレッジレポート生成
  ```bash
  pytest --cov=src/ --cov-report=html
  ```
- **pytest-xdist**: 並列テスト実行によるテスト高速化
  ```bash
  pytest -n auto
  ```
- **pytest-benchmark**: パフォーマンステスト
  ```bash
  pytest --benchmark-json=results.json
  ```

#### フィクスチャの効果的な利用

```python
# conftest.py
@pytest.fixture(scope="session")
def api_client():
    client = ApiClient()
    yield client
    client.close()

# test_api.py
def test_api_request(api_client):
    response = api_client.get("/endpoint")
    assert response.status_code == 200
```

### 2.2 自動テスト戦略

#### テストピラミッド

- **単体テスト(70%)**: 関数やメソッドレベルの小さなテスト（高速で数が多い）
- **統合テスト(20%)**: 複数コンポーネントの連携テスト
- **E2Eテスト(10%)**: システム全体の動作確認（低速で数は少ない）

#### モックとスタブの活用

```python
# 外部APIのモック例
@pytest.fixture
def mock_api_response(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse({"key": "value"}, 200)
    
    monkeypatch.setattr(requests, "get", mock_get)
    
def test_external_api(mock_api_response):
    result = my_function_that_calls_api()
    assert result["key"] == "value"
```

#### パラメータ化テスト

```python
@pytest.mark.parametrize("input,expected", [
    ("text1", "RESULT1"),
    ("text2", "RESULT2"),
    ("text3", "RESULT3"),
])
def test_converter(input, expected):
    assert convert_text(input) == expected
```

## 3. 品質管理ダッシュボード

### 3.1 GitHub Actionsによる自動化と連携

- **コントリビューション分析**: AIエージェントの活動を含むコミット履歴やPR統計を分析します（GitHub Insightsやカスタムスクリプトで）。
- **コードレビュー統計**: 人間によるレビューの頻度や時間、AIエージェントによる修正PRなどを分析します。
- **PRとIssue統計**: AIエージェントが関与したIssueやPRの解決時間、自動クローズ率などを追跡します。

### 3.2 独自ダッシュボードの構築

#### テストカバレッジダッシュボード

- **日次カバレッジレポート**: CIパイプラインでカバレッジ情報を収集し、ウェブページとして公開
- **トレンド分析**: 時間経過に伴うカバレッジ率の変化をグラフ化
- **コンポーネント別分析**: モジュールごとのカバレッジ率比較

#### コード品質ダッシュボード

- **静的解析レポート**: flake8, pylint, mypy等の結果を集約
- **複雑度分析**: 循環的複雑度の高い関数やクラスを特定
- **技術的負債**: コードスメル、TODO/FIXME数、重複コードなどを可視化

### 3.3 CI/CDパイプラインとの統合

#### 自動レポート生成

```yaml
# .github/workflows/quality-report.yml
name: Quality Report
on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * *'  # 毎日実行

jobs:
  quality_report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - name: Install dependencies
        run: pip install -r requirements-dev.txt
      - name: Run tests with coverage
        run: pytest --cov=src/ --cov-report=xml
      - name: Run static analysis
        run: pylint src/ --exit-zero --output-format=json > pylint-report.json
      - name: Generate dashboard
        run: python scripts/generate_dashboard.py
      - name: Deploy report
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./reports
```

#### ダッシュボード生成スクリプト例

```python
# scripts/generate_dashboard.py
import json
import xml.etree.ElementTree as ET
from pathlib import Path

def generate_coverage_report():
    # coverage.xmlの解析とHTMLレポート生成
    tree = ET.parse('coverage.xml')
    root = tree.getroot()
    total_coverage = float(root.attrib['line-rate']) * 100
    
    # コンポーネント別カバレッジの計算
    packages = {}
    for package in root.findall('.//package'):
        pkg_name = package.attrib['name']
        pkg_coverage = float(package.attrib['line-rate']) * 100
        packages[pkg_name] = pkg_coverage
    
    # HTMLレポート生成
    html = f"""
    <html>
    <head><title>Coverage Report</title></head>
    <body>
        <h1>Coverage Report</h1>
        <h2>Total Coverage: {total_coverage:.2f}%</h2>
        <h3>Component Coverage:</h3>
        <ul>
    """
    
    for pkg, cov in packages.items():
        html += f"<li>{pkg}: {cov:.2f}%</li>\n"
    
    html += """
        </ul>
    </body>
    </html>
    """
    
    Path('reports').mkdir(exist_ok=True)
    with open('reports/coverage.html', 'w') as f:
        f.write(html)

if __name__ == '__main__':
    generate_coverage_report()
    # その他のレポート生成関数を追加
```

## 4. ドキュメント管理

### 4.1 ドキュメント構造

#### 推奨ディレクトリ構造

```
docs/
├── project/              # プロジェクト管理ドキュメント
│   ├── roadmap.md        # ロードマップ
│   ├── architecture.md   # アーキテクチャ概要
│   └── process.md        # 開発プロセス (このファイルなど)
├── dev/                  # 開発者向けドキュメント (AIエージェントも参照)
│   ├── setup.md          # 環境構築
│   ├── contributing.md   # (削除またはAI向けに修正)
│   └── api/              # API仕様
├── guides/               # ユーザーガイド
│   ├── quickstart.md     # クイックスタート
│   └── tutorials/        # チュートリアル
└── reference/            # リファレンス資料
    ├── configuration.md  # 設定リファレンス
    └── cli.md            # コマンドラインツール
```

#### ドキュメント生成の自動化

- **Sphinx**: Pythonプロジェクト向けドキュメント生成ツール
- **mkdocs-material**: マークダウンベースのモダンなドキュメントサイト生成
- **docstringsからの自動生成**: 
  ```python
  def process_text(text: str) -> str:
      """テキストを処理する関数
      
      Args:
          text: 処理対象のテキスト
          
      Returns:
          処理後のテキスト
          
      Raises:
          ValueError: テキストが空の場合
      """
  ```

### 4.2 ドキュメントのレビュープロセス

- **ドキュメント専用PR**: コード変更とドキュメント変更を分離します。
- **AIエージェントによる更新**: コード変更時に、関連ドキュメントの更新もAIエージェントに指示します。
- **人間によるレビュー**: AIエージェントが更新したドキュメントの内容を確認・修正します。
- **ユーザビリティ**: ドキュメントがAIエージェントにとっても理解しやすいか（例: `@`メンションしやすい構造か）を考慮します。

## 5. 開発イテレーションの進め方 (AIエージェント中心 & Human-In-The-Loop)

### 5.1 イテレーションサイクル (チケット駆動)

AIエージェントを活用した開発サイクルは、チケット駆動とHuman-In-The-Loop、およびDevSecOpsプラクティスを基本とします。

#### 計画フェーズ (PM)
- **タスク定義**: PMはGitHub Issue（チケット）を作成し、開発目標、背景、受け入れ基準を明確に定義します。セキュリティ要件も明記します。
- **指示の準備**: チケットに基づき、AIエージェントへの具体的な指示内容（コンテキスト、制約含む）を準備します。

#### 開発フェーズ (AI ↔ PM)
- **指示と実行**: PMがAIエージェントにチケットの内容に基づいた指示を与え、AIがコーディング、テスト、ファイル操作などを実行します。AIは`devsecops_guide.md`に基づき、セキュリティチェック（SAST等）も実施します。
- **進捗確認とフィードバック (Human-In-The-Loop)**: PMはAIエージェントの進捗（生成コード、テスト結果、セキュリティチェック結果、ログ）を確認し、必要に応じて軌道修正の指示や追加情報を提供します。
- **対話ログ記録**: 開発日記に記録します。

#### レビューフェーズ (PM + AI)
- **成果物の確認**: AIエージェントがタスク完了を報告（例: PR作成）。PMは生成されたコード、ドキュメント、テスト結果、CI/CDでのセキュリティチェック結果をレビューします。
- **修正指示ループ (Human-In-The-Loop)**: 問題点があればPMが具体的な修正指示を出し、AIが修正。PMが再度レビュー。このサイクルを問題が解消されるまで繰り返します。

#### 統合フェーズ (PM承認)
- **PR承認とマージ**: PMが最終レビューを行い、問題がなければ**PRを承認し、マージします。**
- **デプロイ**: CI/CDパイプラインを通じてステージング環境や本番環境へデプロイします（デプロイ承認も人間が行う場合があります）。このパイプラインにはDASTやコンテナスキャン等のセキュリティチェックが含まれます。

### 5.2 リリース管理

#### セマンティックバージョニング

- **バージョン形式**: `MAJOR.MINOR.PATCH`
  - MAJOR: 後方互換性のない変更
  - MINOR: 後方互換性のある機能追加
  - PATCH: 後方互換性のあるバグ修正

#### リリースノート作成

- **変更ログの自動生成**: コミットメッセージやPRタイトルから変更ログを自動生成
- **ユーザー向け説明**: 技術的変更をユーザー向けに分かりやすく説明
- **アップグレードガイド**: メジャーバージョンアップ時には移行ガイドを提供

#### リリースプロセス

1. **リリースブランチ作成**: `release/v1.2.0` のような名前でブランチを作成
2. **最終テスト**: リリースブランチ上でテストを実行
3. **バージョン番号更新**: パッケージのバージョン情報を更新
4. **タグ付け**: `git tag v1.2.0`
5. **リリース作成**: GitHub Releasesでリリースノートと共に公開 (PMが最終確認・実行)
6. **デプロイ**: PyPI等へのパッケージ公開 (PMが最終確認・実行)

## 6. ツールとリソース (AIエージェント開発向け)

### 7.1 推奨ツール一覧

- **プロジェクト管理**: GitHub (Projects, Issues, PRs)
- **CI/CD**: GitHub Actions
- **テスト**: pytest, pytest-cov, pytest-xdist
- **静的解析**: flake8, pylint, mypy
- **セキュリティ**: `devsecops_guide.md` に記載のツール (Bandit, Semgrep, OWASP ZAP, pip-audit, Trivy, detect-secrets, Hadolintなど)
- **ドキュメント**: Sphinx, MkDocs, Read the Docs
- **コード品質**: SonarQube, Codacy (CI/CD連携)
- **パッケージ管理**: Poetry, Pip-tools
- **AIコーディングエージェント**: Cursor, Roo Code (Cline), その他MCP対応ツール
- **MCPサーバー**: 各種コミュニティ製サーバー (ファイルシステム, Fetch, Git, etc.)

### 7.2 ツール連携設定例

#### GitHub + GitHub Actions + pytest の連携例

```yaml
# .github/workflows/test.yml
name: Test

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
    - name: Run tests
      run: |
        pytest --cov=src/ --cov-report=xml
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### 7.3 参考リソース

- [GitHub Guides](https://guides.github.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [The Twelve-Factor App](https://12factor.net/) - モダンアプリケーション開発の原則
- [Semantic Versioning](https://semver.org/) - バージョニングの標準
- [Keep a Changelog](https://keepachangelog.com/) - 効果的な変更ログの書き方
- **`devsecops_guide.md` (本プロジェクト内)** 