# 品質管理ダッシュボードガイド

このガイドでは、Pythonプロジェクト向けの包括的な品質管理ダッシュボードの構築と運用方法について説明します。品質指標の可視化を通じて、開発プロセスの透明性を高め、継続的な改善を促進することを目的としています。

## 1. ダッシュボードの目的と価値

### 1.1 品質管理ダッシュボードの目的

- **透明性の確保**: プロジェクトの健全性と問題点を可視化
- **早期問題検出**: 開発初期段階での問題の特定と対応
- **チーム意識の向上**: 品質指標の共有によるチーム全体の品質意識向上
- **継続的改善**: トレンド分析による改善効果の確認
- **客観的な判断基準**: 感覚ではなくデータに基づく意思決定

### 1.2 主要な品質指標

#### コード品質指標
- コードカバレッジ率（全体・コンポーネント別）
- 静的解析の警告数・エラー数
- コード複雑度メトリクス
- 技術的負債の定量評価

#### プロセス品質指標
- ビルド成功率
- テスト実行時間
- Issue・PR解決速度
- レビュー率・フィードバック対応率

#### 成果品質指標
- バグ発生率・解決率
- 機能完了率
- パフォーマンス指標
- セキュリティ脆弱性数

## 2. ダッシュボード構築ガイド

### 2.1 基本アーキテクチャ

```
[CI/CDパイプライン] → [データ収集スクリプト] → [データストレージ] → [可視化ツール]
```

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

#### プロセスメトリクスデータ

GitHub APIを活用したデータ収集:

```python
import requests

def fetch_github_metrics(repo, token):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # PRデータ取得
    pr_url = f'https://api.github.com/repos/{repo}/pulls?state=all'
    pr_response = requests.get(pr_url, headers=headers)
    pr_data = pr_response.json()
    
    # Issue データ取得
    issues_url = f'https://api.github.com/repos/{repo}/issues?state=all'
    issues_response = requests.get(issues_url, headers=headers)
    issues_data = issues_response.json()
    
    # データ解析・集計処理
    # ...
    
    return {
        'pr_metrics': pr_metrics,
        'issue_metrics': issue_metrics
    }
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
   - カバレッジが80%を下回った場合に通知
   - 静的解析エラーが10件を超えた場合に通知
   - ビルド失敗が2回連続した場合に通知

## 3. CI/CDパイプラインとの統合

### 3.1 GitHub Actions統合

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
          
      - name: Collect GitHub metrics
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python scripts/collect_github_metrics.py
        
      - name: Process quality data
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

## 4. データ解析と意思決定

### 4.1 主要な分析視点

- **トレンド分析**: 時間経過に伴う品質指標の変化
- **コンポーネント分析**: モジュール/ファイルごとの品質差異
- **相関分析**: 異なる指標間の相関関係
- **異常検出**: 通常パターンからの逸脱の特定

### 4.2 意思決定フレームワーク

1. **閾値ベースの判断**:
   - カバレッジ: 80%以上を維持
   - 静的解析: 重大な警告0件
   - ビルド成功率: 95%以上

2. **トレンドベースの判断**:
   - 3日連続でカバレッジ低下: 調査実施
   - 静的解析警告の継続的増加: リファクタリング検討
   - ビルド時間の増加傾向: パフォーマンス最適化

3. **品質ゲート**:
   - PRマージ条件: カバレッジ低下なし、静的解析エラーなし
   - リリース条件: 全テスト通過、カバレッジ目標達成、セキュリティスキャンパス

### 4.3 自動レポート生成

週次品質レポートの自動生成:

```python
# scripts/generate_weekly_report.py
import json
import datetime
from pathlib import Path
import matplotlib.pyplot as plt

def generate_weekly_report():
    # 日付範囲の決定
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=7)
    
    # データ収集
    coverage_data = []
    for day in range(7):
        date = start_date + datetime.timedelta(days=day)
        date_str = date.strftime('%Y-%m-%d')
        data_path = Path(f'reports/coverage/{date_str}.json')
        
        if data_path.exists():
            with open(data_path, 'r') as f:
                coverage_data.append(json.load(f))
    
    # グラフ生成
    dates = [d['timestamp'][:10] for d in coverage_data]
    values = [d['coverage']['total'] for d in coverage_data]
    
    plt.figure(figsize=(10, 6))
    plt.plot(dates, values, marker='o')
    plt.title('週間コードカバレッジ推移')
    plt.xlabel('日付')
    plt.ylabel('カバレッジ率 (%)')
    plt.grid(True)
    plt.savefig('reports/weekly/coverage_trend.png')
    
    # HTML レポート生成
    html = f"""
    <html>
    <head><title>週間品質レポート</title></head>
    <body>
        <h1>週間品質レポート ({start_date} ～ {today})</h1>
        
        <h2>カバレッジ推移</h2>
        <img src="coverage_trend.png" alt="カバレッジ推移">
        
        <h2>主要指標サマリー</h2>
        <table border="1">
            <tr><th>指標</th><th>現在値</th><th>先週比</th><th>状態</th></tr>
            <tr>
                <td>コードカバレッジ</td>
                <td>{values[-1]}%</td>
                <td>{values[-1] - values[0]:.1f}%</td>
                <td>{'🟢' if values[-1] >= 80 else '🔴'}</td>
            </tr>
            <!-- その他の指標 -->
        </table>
    </body>
    </html>
    """
    
    Path('reports/weekly').mkdir(exist_ok=True, parents=True)
    with open('reports/weekly/index.html', 'w') as f:
        f.write(html)

if __name__ == '__main__':
    generate_weekly_report()
```

## 5. 実装例とベストプラクティス

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

### 5.3 ベストプラクティス

- **継続的な改善目標設定**:
  - 達成可能な段階的な目標設定
  - 品質指標の優先順位付け

- **チーム文化との統合**:
  - 朝会でのダッシュボード確認ルーチン
  - 品質改善の取り組みを評価する文化醸成

- **メンテナンス計画**:
  - 古いデータのアーカイブ戦略
  - ダッシュボード自体のテストと品質確保

## 6. 参考リソースとツール

### 6.1 推奨ツール

- **テスト＆カバレッジ**: pytest, pytest-cov, coverage
- **静的解析**: pylint, flake8, mypy, bandit
- **可視化**: Chart.js, Grafana, Metabase
- **CI/CD連携**: GitHub Actions, Jenkins, CircleCI
- **データ保存**: SQLite, PostgreSQL, InfluxDB

### 6.2 参考リソース

- [Google エンジニアリングプラクティス - 品質指標](https://google.github.io/eng-practices/)
- [Grafana Labs - メトリクスダッシュボード構築ガイド](https://grafana.com/docs/grafana/latest/)
- [The Joel Test: 12 Steps to Better Code](https://www.joelonsoftware.com/2000/08/09/the-joel-test-12-steps-to-better-code/)
- [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
- [Software Quality Metrics](https://en.wikipedia.org/wiki/Software_quality) 