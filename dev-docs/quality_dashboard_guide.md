# 品質管理ダッシュボードガイド (AIエージェント開発向け: PM主導)

このガイドでは、人間がPMとしてAIコーディングエージェント (Cursor, Cline, MCPなど) に指示を出す開発体制において、品質管理ダッシュボードを構築・運用する方法を説明します。ダッシュボードはPMがAIエージェントの活動と成果物の品質を客観的に評価し、適切な指示やフィードバックを与えるための重要なツールとなります。

## 1. ダッシュボードの目的と価値 (PMによるAIエージェント管理)

### 1.1 品質管理ダッシュボードの目的

- **透明性の確保**: プロジェクト全体の健全性、コード品質、AIエージェントの活動状況と成果をPMが把握可能にする。
- **早期問題検出**: AIエージェントの作業に起因する品質低下や問題をPMが早期に発見し、対応指示を出す。
- **AIエージェントへのフィードバック**: PMが客観的なデータ（品質指標）に基づき、AIエージェントへ具体的な改善指示（テスト追加、リファクタリング等）を行う。
- **継続的改善**: PMがダッシュボードを通じて開発プロセス（人間とAIの連携含む）全体の改善効果を確認し、次のアクションを決定する。
- **客観的な判断基準**: PMがデータに基づきAIエージェントのパフォーマンス（生産性、品質）を評価し、タスク割り当てや指示方法を最適化する。

### 1.2 主要な品質指標 (PMによる評価のため)

PMがAIエージェントの作業品質を評価するために、以下の指標に注目します。

#### コード品質指標
- コードカバレッジ率（目標達成度、AIによる増減）
- 静的解析の警告・エラー数（AIによる増減、深刻度）
- コード複雑度メトリクス（AIによる過度な複雑化の有無）
- 技術的負債（AIによる新規発生・解消状況）

#### プロセス品質指標 (Human-In-The-Loop 関連)
- ビルド成功率（AIコミット起因の失敗頻度）
- テスト実行時間（AIによる影響）
- AIエージェントによるチケット解決速度
- **PMによるレビュー時間・頻度**（AI生成コードに対するボトルネック特定）
- **PMからAIへの修正指示回数・内容**（AIの理解度、指示の明確さの指標）

#### 成果品質指標
- バグ発生率・解決率（AI生成コード起因のバグ特定）
- 機能完了率（計画通りに進捗しているか）
- パフォーマンス指標（AIによるリグレッション有無）
- セキュリティ脆弱性数（AI生成コードのスキャン結果）

## 2. ダッシュボード構築ガイド

### 2.1 基本アーキテクチャ

```
[CI/CDパイプライン (GitHub Actions)] → [データ収集スクリプト] → [データストレージ (DB/ファイル)] → [可視化ツール (Grafana/静的HTML)]
```
AIエージェントの活動ログ (開発日記など) もデータソースとして検討可能です。

#### 実装オプション

1. **軽量アプローチ**:
   - データ収集: GitHub Actions
   - データストレージ: JSON/CSV ファイル（GitHub Pages）
   - 可視化: 静的HTML + JavaScript（Chart.js）

2. **フル機能アプローチ**:
   - データ収集: Jenkins/GitHub Actions
   - データストレージ: データベース（SQLite/PostgreSQL）
   - 可視化: Grafana / カスタムウェブアプリ

### 2.2 データ収集方法

#### テストカバレッジデータ

pytest-covを使用したカバレッジデータ収集:

```bash
pytest --cov=src --cov-report=xml
```

生成されるcoverage.xmlを解析してデータを抽出:

```python
import xml.etree.ElementTree as ET

def extract_coverage_data(xml_path='coverage.xml'):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # 全体カバレッジ
    total_coverage = float(root.attrib.get('line-rate', 0)) * 100
    
    # モジュール別カバレッジ
    module_coverage = {}
    for package in root.findall('.//package'):
        pkg_name = package.attrib.get('name', 'unknown')
        pkg_rate = float(package.attrib.get('line-rate', 0)) * 100
        module_coverage[pkg_name] = pkg_rate
    
    return {
        'total': total_coverage,
        'modules': module_coverage
    }
```

#### 静的解析データ

flake8の結果を構造化データとして収集:

```bash
flake8 src --output-file=flake8-report.txt
```

pylintのJSON形式の出力を利用:

```bash
pylint src --output-format=json > pylint-report.json
```

デコード例:
```python
import json

def extract_pylint_data(json_path='pylint-report.json'):
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # メッセージタイプごとの集計
    message_counts = {
        'error': 0,
        'warning': 0,
        'convention': 0,
        'refactor': 0
    }
    
    for message in data:
        msg_type = message.get('type', '')
        if msg_type in message_counts:
            message_counts[msg_type] += 1
    
    # スコア計算（pylintの評価は10点満点）
    if 'score' in data[-1]:
        score = data[-1]['score']
    else:
        score = 0
    
    return {
        'message_counts': message_counts,
        'score': score
    }
```

#### プロセスメトリクスデータ (AIエージェント関連)

GitHub APIに加え、開発日記 (`Docs/dev-records/`) のログを解析することで、AIエージェント関連の指標を収集することも可能です。

- **開発日記ログ解析スクリプト例 (概念)**:
  ```python
  import re
  from pathlib import Path
  
  def analyze_dev_logs(log_dir="Docs/dev-records/"):
      agent_metrics = {
          'total_interactions': 0,
          'agent_commits': 0, # Git連携が必要
          'correction_requests': 0,
          # 他の指標...
      }
      log_files = Path(log_dir).glob("*.md")
      
      for log_file in log_files:
          with open(log_file, 'r', encoding='utf-8') as f:
              content = f.read()
              # 正規表現などでログから情報を抽出
              agent_metrics['total_interactions'] += len(re.findall(r"^- LLM:", content, re.MULTILINE))
              # 例: 修正依頼を示す特定のキーワードをカウント
              agent_metrics['correction_requests'] += len(re.findall(r"ユーザー:.*(修正|変更|やり直し)してください", content))
              # Git連携でコミット数をカウントする処理を追加...
              
      return agent_metrics
  ```

### 2.3 データ保存と履歴管理

#### ファイルベースのアプローチ

日付ベースのJSONファイル:

```
reports/
├── coverage/
│   ├── 2025-04-01.json
│   ├── 2025-04-02.json
│   └── ...
├── static-analysis/
│   ├── 2025-04-01.json
│   ├── 2025-04-02.json
│   └── ...
└── process/
    ├── 2025-04-01.json
    ├── 2025-04-02.json
    └── ...
```

サンプルJSON構造:

```json
{
  "timestamp": "2025-04-30T10:45:00Z",
  "build_id": "github-actions-123456",
  "coverage": {
    "total": 87.5,
    "modules": {
      "src/core": 92.3,
      "src/utils": 85.1,
      "src/api": 79.8
    }
  },
  "static_analysis": {
    "pylint_score": 8.7,
    "flake8_violations": 12,
    "mypy_errors": 3
  }
}
```

#### データベースアプローチ

SQLiteスキーマ例:

```sql
-- メトリクスの種類
CREATE TABLE metric_types (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT
);

-- ビルド/実行情報
CREATE TABLE builds (
  id INTEGER PRIMARY KEY,
  build_id TEXT NOT NULL,
  timestamp DATETIME NOT NULL,
  branch TEXT,
  commit_hash TEXT
);

-- メトリクス値
CREATE TABLE metrics (
  id INTEGER PRIMARY KEY,
  build_id INTEGER REFERENCES builds(id),
  metric_type_id INTEGER REFERENCES metric_types(id),
  value REAL NOT NULL,
  component TEXT,  -- optional for component-specific metrics
  extra JSON       -- additional structured data
);
```

### 2.4 可視化実装

#### 静的HTMLダッシュボード

基本構造:

```html
<!DOCTYPE html>
<html>
<head>
  <title>プロジェクト品質ダッシュボード</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/luxon@2.0.2"></script>
  <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-luxon@1.0.0"></script>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header>
    <h1>プロジェクト品質ダッシュボード</h1>
    <p>最終更新: <span id="last-updated">Loading...</span></p>
  </header>
  
  <div class="dashboard-grid">
    <!-- カバレッジセクション -->
    <div class="card">
      <h2>コードカバレッジ</h2>
      <div class="metric-big">
        <span id="total-coverage">--.-%</span><span class="unit">%</span>
      </div>
      <div class="chart-container">
        <canvas id="coverage-trend-chart"></canvas>
      </div>
    </div>
    
    <!-- 静的解析セクション -->
    <div class="card">
      <h2>コード品質スコア</h2>
      <div class="metric-big">
        <span id="code-quality-score">-.--</span><span class="unit">/10</span>
      </div>
      <div class="chart-container">
        <canvas id="code-quality-chart"></canvas>
      </div>
    </div>
    
    <!-- その他のチャートとメトリクス -->
  </div>
  
  <script src="dashboard.js"></script>
</body>
</html>
```

JavaScript実装例:

```javascript
// dashboard.js
document.addEventListener('DOMContentLoaded', async () => {
  // データ読み込み
  const coverageData = await fetch('./data/coverage-history.json').then(r => r.json());
  const codeQualityData = await fetch('./data/code-quality-history.json').then(r => r.json());
  
  // 最新値の表示
  const latestCoverage = coverageData[coverageData.length - 1];
  document.getElementById('total-coverage').textContent = 
    latestCoverage.total.toFixed(1);
  document.getElementById('last-updated').textContent = 
    new Date(latestCoverage.timestamp).toLocaleString();
  
  // トレンドチャート描画
  const coverageTrendChart = new Chart(
    document.getElementById('coverage-trend-chart'),
    {
      type: 'line',
      data: {
        datasets: [{
          label: 'コードカバレッジ',
          data: coverageData.map(d => ({
            x: new Date(d.timestamp),
            y: d.total
          })),
          borderColor: '#4CAF50',
          tension: 0.1
        }]
      },
      options: {
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'day'
            }
          },
          y: {
            min: 0,
            max: 100,
            title: {
              display: true,
              text: 'カバレッジ (%)'
            }
          }
        }
      }
    }
  );
  
  // その他のチャート描画
});
```

#### Grafanaを用いた動的ダッシュボード

1. **データソース設定**:
   - SQLiteまたはPostgreSQLをデータソースとして設定
   - JSONファイルの場合はJSON APIデータソースプラグインを活用

2. **ダッシュボード構成**:
   - 概要パネル: 主要な品質指標を一覧表示
   - トレンドパネル: 時系列でのメトリクス変化
   - コンポーネントパネル: モジュール/コンポーネント別の詳細
   - アラートパネル: 閾値を下回った指標の警告表示

3. **アラート設定**: 
   - AI生成コードのカバレッジが特定の閾値を下回った場合に通知
   - AI生成コードに対する静的解析エラーが急増した場合に通知
   - AIエージェントによるビルド失敗が連続した場合に通知

## 3. CI/CDパイプラインとの統合

### 3.1 GitHub Actions統合

CI/CDパイプラインは、AIエージェントが生成したコードの品質を自動チェックする上で極めて重要です。

```yaml
# .github/workflows/quality-dashboard.yml
name: Quality Dashboard Update

on:
  push:
    branches: [ main, develop ]
  schedule:
    - cron: '0 0 * * *'  # 毎日実行

jobs:
  update_dashboard:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt
          pip install pytest pytest-cov pylint flake8 mypy
          
      - name: Run tests with coverage
        run: pytest --cov=src/ --cov-report=xml
        
      - name: Run static analysis
        run: |
          pylint src/ --output-format=json > pylint-report.json
          flake8 src/ --output-file=flake8-report.txt
          mypy src/ --txt-report mypy-report
          
      - name: Collect AI Agent Metrics (Optional)
        # 開発日記ログなどを解析して指標を収集するスクリプトを実行
        run: python scripts/collect_agent_metrics.py
        
      - name: Process quality data (including agent metrics)
        run: python scripts/process_quality_data.py
        
      - name: Generate dashboard
        run: python scripts/generate_dashboard.py
        
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dashboard
```

### 3.2 Jenkins統合

```groovy
// Jenkinsfile
pipeline {
    agent {
        docker {
            image 'python:3.10'
        }
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install -r requirements-dev.txt'
                sh 'pip install pytest pytest-cov pylint flake8 mypy'
            }
        }
        
        stage('Test') {
            steps {
                sh 'pytest --cov=src/ --cov-report=xml'
                junit 'test-results.xml'
            }
        }
        
        stage('Static Analysis') {
            parallel {
                stage('Pylint') {
                    steps {
                        sh 'pylint src/ --output-format=json > pylint-report.json'
                    }
                }
                stage('Flake8') {
                    steps {
                        sh 'flake8 src/ --output-file=flake8-report.txt'
                    }
                }
                stage('MyPy') {
                    steps {
                        sh 'mypy src/ --txt-report mypy-report'
                    }
                }
            }
        }
        
        stage('Process Quality Data') {
            steps {
                sh 'python scripts/process_quality_data.py'
            }
        }
        
        stage('Update Dashboard') {
            steps {
                sh 'python scripts/generate_dashboard.py'
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'dashboard',
                    reportFiles: 'index.html',
                    reportName: 'Quality Dashboard'
                ])
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'quality-data/*.json', fingerprint: true
        }
    }
}
```

## 4. データ解析と意思決定 (PM主導 & Human-In-The-Loop)

### 4.1 主要な分析視点 (PM向け)

PMはダッシュボードから以下の視点でデータを分析し、アクションに繋げます。

- **トレンド分析**: AIエージェントの導入・活用方針変更後の品質変化を評価。
- **コンポーネント分析**: AIエージェントが品質を維持しやすい/低下させやすいコード領域を特定。
- **相関分析**: AIへの指示内容や頻度と、コード品質・生産性の関係性を分析。
- **異常検出**: AIによる予期せぬ品質劣化やビルド失敗を早期に発見。

### 4.2 意思決定フレームワーク (PMによるAIへの指示改善)

PMはダッシュボードのデータを基に、AIエージェントへの指示内容や連携方法を改善します。

1.  **閾値ベースの判断**: 品質指標が設定した閾値を逸脱した場合、PMは原因を調査し、AIエージェントに具体的な改善タスク（テスト追加、リファクタリング、規約遵守など）を指示します。
    *   例: AI生成コードのカバレッジが80%未満 → 「カバレッジレポートを確認し、`module_x.py` の未テスト行に対するテストを追加してください」
2.  **トレンドベースの判断**: 品質指標の悪化傾向が見られる場合、PMはAIへの指示方法やプロンプト、利用するツール（MCPサーバー等）の見直しを検討します。
    *   例: PMからの修正指示回数が増加傾向 → 指示の具体性を高める、参考情報を追加する、タスクをより小さく分割する。
    *   例: 特定領域でAIによるバグ発生が多い → その領域はAIに任せずPMが担当する、またはより詳細な仕様とテストケースを指示する。
3.  **品質ゲート**: PMはPRマージの最終承認者として、ダッシュボードで示される品質基準（カバレッジ、静的解析結果など）を満たしていることを確認します。

## 5. 実装例とベストプラクティス (PM主導のAIエージェント開発)

### 5.1 小規模プロジェクト向け最小構成

1. **GitHub Actionsワークフロー**:
   - pytest-covでカバレッジ計測
   - レポートをGitHub Pagesに公開

2. **最小限のレポート構成**:
   - 全体カバレッジ率と推移
   - 静的解析の警告数とその推移

### 5.2 中・大規模プロジェクト向け構成

1. **専用データベース**:
   - 時系列データの継続的蓄積
   - 複雑なクエリと多角的分析

2. **Grafanaダッシュボード**:
   - リアルタイムモニタリング
   - ドリルダウン分析機能
   - チーム別・コンポーネント別ビュー

3. **アラート連携**:
   - Slack/Teamsへの通知
   - 品質低下時の自動Issue作成

### 5.3 ベストプラクティス (PM主導のAIエージェント開発)

- **継続的な改善目標設定**: PMはAIエージェントのパフォーマンスに関する具体的な目標を設定し、ダッシュボードで進捗を追跡します。
- **人間(PM)とAIの役割分担**: PMはダッシュボードを参考に、AIに任せるべきタスクと、PM自身が介入・判断すべきポイント（レビュー、承認、複雑な意思決定）を明確にします。
- **AIへのフィードバックループ**: PMはダッシュボードの情報を定期的に確認し、それを基にAIエージェントへの指示プロンプト、利用ツール、開発プロセス自体を継続的に改善します。
- **ダッシュボードの活用**: PMはダッシュボードを日々のAIエージェント管理の中心に据え、客観的なデータに基づいた意思決定を行います。

## 6. 参考リソースとツール

### 6.1 推奨ツール

- **テスト＆カバレッジ**: pytest, pytest-cov, coverage
- **静的解析**: pylint, flake8, mypy, bandit
- **可視化**: Chart.js, Grafana, Metabase
- **CI/CD連携**: GitHub Actions
- **データ保存**: SQLite, PostgreSQL, InfluxDB, JSON/CSV (GitHub Pages)
- **AIエージェント**: Cursor, Roo Code (Cline), etc.
- **ログ解析**: Python (re, pandas), etc.

### 6.2 参考リソース

- [Google エンジニアリングプラクティス - 品質指標](https://google.github.io/eng-practices/)
- [Grafana Labs - メトリクスダッシュボード構築ガイド](https://grafana.com/docs/grafana/latest/)
- [The Joel Test: 12 Steps to Better Code](https://www.joelonsoftware.com/2000/08/09/the-joel-test-12-steps-to-better-code/)
- [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
- [Software Quality Metrics](https://en.wikipedia.org/wiki/Software_quality) 