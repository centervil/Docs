# 品質管理ダッシュボードガイド (AIエージェント主導開発向け)

このガイドでは、AIコーディングエージェント (Cursor, Cline, MCPなど) が主体となって開発を進め、人間がプロジェクトマネージャー (PM) として監視・レビュー・承認を行う開発体制において、品質管理ダッシュボードを構築・運用する方法を説明します。ダッシュボードはAIエージェントが自律的に品質とセキュリティを監視・改善するためのツールであると同時に、PMがAIエージェントの成果物の品質とセキュリティ体制を客観的に評価し、必要な場合にのみ介入するための重要な指標となります。

## 1. ダッシュボードの目的と価値 (AIエージェント自律監視 & PM戦略的監視)

### 1.1 品質管理ダッシュボードの目的

- **透明性の確保**: プロジェクト全体の健全性、コード品質、セキュリティ体制、AIエージェントの活動状況と成果を可視化。AIエージェント自身が品質とセキュリティを継続的に監視し、PMは全体傾向を把握できるようにする。
- **早期問題検出**: AIエージェントが自律的に品質やセキュリティ問題を早期発見し、対応。深刻な問題や対応が難しい問題のみをPMに報告。
- **自律的改善**: AIエージェントが客観的なデータ（品質・セキュリティ指標）に基づき、自律的に改善活動（テスト追加、リファクタリング、脆弱性修正等）を行う。
- **継続的改善**: AIエージェントとPMが共同でダッシュボードを通じて開発プロセス全体の改善効果を確認し、次のアクションを決定。
- **戦略的判断基準**: PMがデータに基づきプロジェクト全体の方向性とセキュリティリスクを評価し、アーキテクチャレベルの決定や投資判断を行う。

### 1.2 主要な品質指標 (AIエージェント自律監視 & PM戦略的判断)

AIエージェントは日々の開発活動において以下の指標を自律的に監視し、PMはより長期的な傾向とプロジェクト全体の健全性とセキュリティ体制を評価します。

#### コード品質指標
- コードカバレッジ率（AIが自律的に目標達成を監視）
- 静的解析の警告・エラー数（AIが自律的に検出・修正）
- コード複雑度メトリクス（AIが自律的に複雑なコードを検出・リファクタリング）
- 技術的負債（AIによる継続的な検出・解消）

#### セキュリティ指標 (`devsecops_guide.md`参照)
- **SAST結果**: 検出された脆弱性の数（深刻度別）、修正状況
- **DAST結果**: 検出された脆弱性の数（深刻度別）、修正状況
- **SCA結果**: 依存関係に含まれる既知の脆弱性(CVE)の数、修正状況 (Dependabotアラート数など)
- **シークレット検知結果**: コード内に検出されたシークレット数
- **コンテナスキャン結果**: イメージに含まれる脆弱性の数（深刻度別）

#### プロセス品質指標 (GitHub Flow関連)
- ブランチのライフタイム（機能ブランチがマージされるまでの平均時間）
- PRのサイズ（変更行数、変更ファイル数）
- ビルド成功率（特にフィーチャーブランチでのCI実行結果、セキュリティチェック失敗含む）
- テスト実行時間（最適化の必要性を検出）
- **AIエージェントの自律性指標**（PMによる介入回数・介入度の推移）
- **PR承認速度**（PMによるレビュー・承認に要する時間）

#### 成果品質指標
- バグ発生率・解決率（AIが自律的に検出・修正）
- 機能完了率（計画通りに進捗しているか）
- パフォーマンス指標（AIが継続的に監視・最適化）
- **セキュリティインシデント数**: 発生したインシデントの数と対応状況 (PMが手動入力または別システム連携)

## 2. ダッシュボード構築ガイド

### 2.1 基本アーキテクチャ

```
[GitHub Flow & CI/CDパイプライン (Security Tools含む)] → [データ収集スクリプト] → [データストレージ (DB/ファイル)] → [可視化ツール (Grafana/静的HTML)]
```
AIエージェントの活動ログ (開発日記など) もデータソースとして活用します。

#### 実装オプション

1. **軽量アプローチ**:
   - データ収集: GitHub Actions (mainブランチマージ時およびPR作成時)
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

#### **セキュリティスキャンデータ**

CI/CDパイプラインで実行される各セキュリティツールの結果 (JSON, XML, CSV形式など) を収集・解析します。

- **Bandit**: JSONレポート (`bandit -f json -o bandit-report.json`)
- **Semgrep**: JSONレポート (`semgrep scan --json > semgrep-report.json`)
- **OWASP ZAP**: XMLまたはJSONレポート (スキャン設定による)
- **pip-audit**: JSONレポート (`pip-audit --format json > pip-audit-report.json`)
- **Trivy**: JSONレポート (`trivy image --format json -o trivy-report.json <イメージ名>`)
- **detect-secrets**: JSONレポート (`detect-secrets scan --all > detect-secrets-report.json`)

**データ抽出スクリプト例 (概念)**:
```python
import json

def extract_security_scan_data():
    scan_results = {
        'sast_bandit': {'high': 0, 'medium': 0, 'low': 0},
        'sast_semgrep': {'error': 0, 'warning': 0, 'info': 0},
        'dast_zap': {'high': 0, 'medium': 0, 'low': 0},
        'sca_pip_audit': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0},
        'sca_trivy': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0},
        'secrets': 0
    }
    
    # Banditレポート解析
    try:
        with open('bandit-report.json', 'r') as f:
            bandit_data = json.load(f)
            for result in bandit_data.get('results', []):
                severity = result.get('issue_severity', 'low').lower()
                if severity in scan_results['sast_bandit']:
                    scan_results['sast_bandit'][severity] += 1
    except FileNotFoundError:
        pass # レポートがない場合はスキップ
        
    # Semgrepレポート解析
    try:
        with open('semgrep-report.json', 'r') as f:
            semgrep_data = json.load(f)
            for result in semgrep_data.get('results', []):
                severity = result.get('extra', {}).get('severity', 'info').lower()
                if severity in scan_results['sast_semgrep']:
                    scan_results['sast_semgrep'][severity] += 1
    except FileNotFoundError:
        pass
        
    # pip-auditレポート解析
    try:
        with open('pip-audit-report.json', 'r') as f:
             pip_audit_data = json.load(f)
             # 脆弱性が見つかった依存関係の数をカウントするなどの処理
             # pip-auditのJSON構造に合わせて脆弱性レベルを集計
             vulnerability_count = len(pip_audit_data)
             # 仮に深刻度highとしてカウント
             if vulnerability_count > 0:
                 scan_results['sca_pip_audit']['high'] = vulnerability_count 
    except FileNotFoundError:
        pass
        
    # Trivyレポート解析 (TrivyのJSON構造に合わせて処理)
    # OWASP ZAPレポート解析 (ZAPのレポート形式に合わせて処理)
    # detect-secretsレポート解析 (detect-secretsのレポート形式に合わせて処理)
        
    return scan_results
```

#### GitHub Flow関連メトリクス

GitHub APIを利用して、ブランチ寿命、PR統計などを収集:

```python
import requests
from datetime import datetime

def get_github_flow_metrics(repo, token):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # PRの統計情報収集
    pr_url = f'https://api.github.com/repos/{repo}/pulls?state=all&per_page=100'
    response = requests.get(pr_url, headers=headers)
    prs = response.json()
    
    # 分析データ
    pr_stats = {
        'avg_lifetime': 0,  # PRがオープンからマージまでの平均時間（時間）
        'avg_size': 0,      # 変更行数の平均
        'review_time': 0,   # レビューにかかる平均時間（時間）
        'approval_rate': 0, # 承認されたPRの割合（%）
    }
    
    total_prs = len(prs)
    if total_prs == 0:
        return pr_stats
    
    total_lifetime = 0
    total_changes = 0
    total_review_time = 0
    approved_prs = 0
    
    for pr in prs:
        # マージされたPRのみ分析
        if pr['merged_at']:
            created_at = datetime.strptime(pr['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            merged_at = datetime.strptime(pr['merged_at'], '%Y-%m-%dT%H:%M:%SZ')
            lifetime = (merged_at - created_at).total_seconds() / 3600  # 時間単位
            total_lifetime += lifetime
            
            # PRの変更サイズ取得
            pr_detail_url = pr['url']
            detail_resp = requests.get(pr_detail_url, headers=headers)
            pr_detail = detail_resp.json()
            changes = pr_detail.get('additions', 0) + pr_detail.get('deletions', 0)
            total_changes += changes
            
            # レビュー時間の計算（最初のレビューまたはコメントから）
            reviews_url = f"{pr['url']}/reviews"
            reviews_resp = requests.get(reviews_url, headers=headers)
            reviews = reviews_resp.json()
            
            if reviews:
                first_review_time = min([datetime.strptime(r['submitted_at'], '%Y-%m-%dT%H:%M:%SZ') for r in reviews])
                review_time = (first_review_time - created_at).total_seconds() / 3600
                total_review_time += review_time
            
            approved_prs += 1
    
    if approved_prs > 0:
        pr_stats['avg_lifetime'] = total_lifetime / approved_prs
        pr_stats['avg_size'] = total_changes / approved_prs
        pr_stats['review_time'] = total_review_time / approved_prs
        pr_stats['approval_rate'] = (approved_prs / total_prs) * 100
    
    return pr_stats
```

#### AIエージェント活動メトリクス

開発日記 (`Docs/dev-records/`) のログとGitHub活動から、AIエージェントの自律性や効率性に関する指標を収集:

```python
import re
from pathlib import Path
import json

def analyze_ai_autonomy(log_dir="Docs/dev-records/", metrics_file="ai_metrics.json"):
    """AIエージェントの自律性と効率性を分析"""
    # 以前のメトリクスがあれば読み込む
    try:
        with open(metrics_file, 'r') as f:
            historical_metrics = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        historical_metrics = []
    
    # 新しいメトリクスを計算
    current_metrics = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'pm_interventions': 0,  # PMの介入回数
        'ai_initiatives': 0,    # AIの自発的な提案・行動
        'ai_questions': 0,      # AIが自ら質問した回数
        'completed_tasks': 0,   # 完了したタスク数
        'autonomy_score': 0     # 自律性スコア（0-100）
    }
    
    # 開発日記ファイルを分析
    log_files = sorted(Path(log_dir).glob("*.md"))
    # 最新の数ファイル（例えば過去7日分）のみ分析
    recent_logs = log_files[-7:] if len(log_files) > 7 else log_files
    
    for log_file in recent_logs:
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # PMの介入回数を計測（「PMが指示」「修正を依頼」などのキーワード）
            pm_interventions = len(re.findall(r"ユーザー:.*(修正|変更|やり直し|指示)して", content, re.MULTILINE))
            current_metrics['pm_interventions'] += pm_interventions
            
            # AIの自発的な提案数を計測
            ai_initiatives = len(re.findall(r"LLM:.*(提案します|改善できます|最適化できます)", content, re.MULTILINE))
            current_metrics['ai_initiatives'] += ai_initiatives
            
            # AIの質問数を計測
            ai_questions = len(re.findall(r"LLM:.*(\?|でしょうか\?|いかがでしょう|確認したいです)", content, re.MULTILINE))
            current_metrics['ai_questions'] += ai_questions
            
            # 完了タスク数を計測（「完了しました」「実装しました」などのキーワード）
            completed_tasks = len(re.findall(r"LLM:.*(完了しました|実装しました|終了しました)", content, re.MULTILINE))
            current_metrics['completed_tasks'] += completed_tasks
    
    # 自律性スコアの計算（例：自発的行動と介入回数のバランスに基づく）
    if current_metrics['pm_interventions'] + current_metrics['ai_initiatives'] > 0:
        autonomy_ratio = current_metrics['ai_initiatives'] / (current_metrics['pm_interventions'] + current_metrics['ai_initiatives'])
        current_metrics['autonomy_score'] = min(100, autonomy_ratio * 100)
    
    # メトリクスを履歴に追加
    historical_metrics.append(current_metrics)
    
    # 保存
    with open(metrics_file, 'w') as f:
        json.dump(historical_metrics, f, indent=2)
    
    return current_metrics, historical_metrics
```

### 2.3 データ保存と履歴管理

#### ファイルベースのアプローチ

日付ベースのJSONファイル (セキュリティ結果も含む):

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
├── security/
│   ├── sast-bandit/ ...
│   ├── sast-semgrep/ ...
│   ├── sca-pip-audit/ ...
│   └── ...
└── process/
    ├── 2025-04-01.json
    ├── 2025-04-02.json
    └── ...
```

サンプルJSON構造 (一部抜粋):

```json
{
  "timestamp": "2025-04-30T10:45:00Z",
  "build_id": "github-actions-123456",
  // ... coverage, static_analysis ...
  "security_scans": {
    "sast_bandit": {"high": 1, "medium": 3, "low": 10},
    "sast_semgrep": {"error": 0, "warning": 5, "info": 2},
    "sca_pip_audit": {"critical": 0, "high": 2, "medium": 1, "low": 0},
    // ... 他のスキャン結果 ...
  }
}
```

#### データベースアプローチ

SQLiteスキーマ例 (`metrics`テーブルにセキュリティ指標を追加):

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

-- metric_types テーブルにセキュリティ関連のタイプを追加
INSERT INTO metric_types (name, description) VALUES
('sast_high', 'SAST High Severity Issues'),
('dast_medium', 'DAST Medium Severity Issues'),
('sca_critical', 'SCA Critical CVEs');

-- metrics テーブルへの挿入例
INSERT INTO metrics (build_id, metric_type_id, value)
VALUES (123, (SELECT id FROM metric_types WHERE name='sast_high'), 1);
```

### 2.4 可視化実装

#### 静的HTMLダッシュボード

既存のダッシュボードにセキュリティ指標のセクションを追加します。

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
    
    <!-- セキュリティ指標セクション -->
    <div class="card">
      <h2>セキュリティ脆弱性</h2>
      <div>SAST (Bandit): <span id="sast-bandit-high">-</span> High, <span id="sast-bandit-medium">-</span> Med</div>
      <div>SCA (pip-audit): <span id="sca-pip-audit-critical">-</span> Crit, <span id="sca-pip-audit-high">-</span> High</div>
      <div class="chart-container">
        <canvas id="vulnerability-trend-chart"></canvas>
      </div>
    </div>
  </div>
  
  <script src="dashboard.js"></script>
</body>
</html>
```

JavaScriptでデータを取得し、チャートを描画します。

#### Grafanaを用いた動的ダッシュボード

- **セキュリティ専用ダッシュボード**: SAST, DAST, SCAなどの結果を詳細に表示するダッシュボードを作成。
- **概要ダッシュボードへの組み込み**: 主要なセキュリティ指標（例: High以上の脆弱性数）を既存の品質ダッシュボードに追加。
- **アラート設定**: 
    - 新たなCritical/High脆弱性が検出された場合に通知。
    - 修正されていない既知の脆弱性が一定期間存在する場合に通知。
    - シークレットが検出された場合に即時通知。

## 3. CI/CDパイプラインとの統合

### 3.1 GitHub Actions統合

CI/CDパイプラインは、AIエージェントが生成したコードの品質とセキュリティを自動チェックする上で極めて重要です。

```yaml
# .github/workflows/quality-dashboard.yml
name: Quality & Security Dashboard Update

on:
  push:
    branches: [ main, develop ]
  schedule:
    - cron: '0 1 * * *'  # 毎日1時に実行

jobs:
  update_dashboard:
    runs-on: ubuntu-latest
    permissions:
      contents: read # コードのチェックアウトに必要
      # security-events: write # GitHub Securityへの結果書き込みに必要 (将来的に検討)
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          # requirements-dev.txt で管理
          pip install -r requirements-dev.txt 
          
      - name: Run tests with coverage
        run: pytest --cov=src/ --cov-report=xml
        
      - name: Run Static Analysis & SAST (Bandit, Semgrep)
        run: |
          pylint src/ --output-format=json --exit-zero > pylint-report.json
          flake8 src/ --output-file=flake8-report.txt --exit-zero
          mypy src/ --txt-report mypy-report --ignore-missing-imports
          bandit -r src/ -f json -o bandit-report.json --exit-zero
          semgrep scan --config auto --json > semgrep-report.json --error # エラーが見つかったら失敗させる
          
      - name: Run SCA (pip-audit, Trivy-fs)
        run: |
          pip-audit --format json > pip-audit-report.json || echo "pip-audit found issues"
          # ファイルシステムのスキャン例 (必要に応じて調整)
          trivy fs --format json -o trivy-fs-report.json . || echo "Trivy found issues"
          
      - name: Run Secret Detection
        run: detect-secrets scan --all > detect-secrets-report.json || echo "Secrets detected"
        
      - name: Collect AI Agent Metrics (Optional)
        run: python scripts/collect_agent_metrics.py
        
      - name: Process quality & security data
        # 各レポートファイルを読み込み、DBやJSONに保存するスクリプト
        run: python scripts/process_scan_data.py 
        
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

- **トレンド分析**: AIエージェントの導入・活用方針変更後の品質・セキュリティ体制の変化を評価。
- **コンポーネント分析**: AIエージェントが品質・セキュリティを維持しやすい/低下させやすいコード領域を特定。
- **相関分析**: AIへの指示内容や頻度と、コード品質・生産性、セキュリティ脆弱性の発生状況の関係性を分析。
- **異常検出**: AIによる予期せぬ品質劣化やビルド失敗、セキュリティ脆弱性の急増を早期に発見。
- **リスク評価**: 検出された脆弱性の深刻度と影響範囲を評価し、対応の優先順位を決定。

### 4.2 意思決定フレームワーク (PMによるAIへの指示改善)

PMはダッシュボードのデータを基に、AIエージェントへの指示内容や連携方法、およびセキュリティ対策を改善します。

1.  **閾値ベースの判断**: 品質・セキュリティ指標が設定した閾値を逸脱した場合、PMは原因を調査し、AIエージェントに具体的な改善タスク（テスト追加、リファクタリング、脆弱性修正、規約遵守など）を指示します。
    *   例: AI生成コードのカバレッジが80%未満 → 「カバレッジレポートを確認し、`module_x.py` の未テスト行に対するテストを追加してください」
    *   例: **HighのSAST脆弱性が検出された** → 「Bandit/Semgrepのレポートを確認し、`module_y.py` の脆弱性を修正するPRを作成してください」
2.  **トレンドベースの判断**: 品質・セキュリティ指標の悪化傾向が見られる場合、PMはAIへの指示方法やプロンプト、利用するツール（MCPサーバー等）、セキュリティチェックの強化などを検討します。
    *   例: PMからの修正指示回数が増加傾向 → 指示の具体性を高める、参考情報を追加する、タスクをより小さく分割する。
    *   例: 特定領域でAIによるバグや脆弱性発生が多い → その領域はAIに任せずPMが担当する、またはより詳細な仕様とテストケース、セキュリティ要件を指示する。
3.  **品質・セキュリティゲート**: PMはPRマージの最終承認者として、ダッシュボードで示される品質・セキュリティ基準（カバレッジ、静的解析結果、脆弱性スキャン結果など）を満たしていることを確認します。

## 5. 実装例とベストプラクティス (PM主導のAIエージェント開発)

### 5.1 小規模プロジェクト向け最小構成

1. **GitHub Actionsワークフロー**: 
   - pytest-covでカバレッジ計測
   - **基本的なSAST (Bandit) と SCA (pip-audit) を実行**
   - レポートをGitHub Pagesに公開

2. **最小限のレポート構成**: 
   - 全体カバレッジ率と推移
   - 静的解析の警告数とその推移
   - **SAST/SCAで検出されたHigh以上の脆弱性数**

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

- **継続的な改善目標設定**: PMはAIエージェントのパフォーマンスとセキュリティ体制に関する具体的な目標を設定し、ダッシュボードで進捗を追跡します。
- **人間(PM)とAIの役割分担**: PMはダッシュボードを参考に、AIに任せるべきタスクと、PM自身が介入・判断すべきポイント（レビュー、承認、複雑な意思決定、高度なセキュリティ判断）を明確にします。
- **AIへのフィードバックループ**: PMはダッシュボードの情報を定期的に確認し、それを基にAIエージェントへの指示プロンプト、利用ツール、開発プロセス自体、セキュリティ対策を継続的に改善します。
- **ダッシュボードの活用**: PMはダッシュボードを日々のAIエージェント管理とセキュリティ監視の中心に据え、客観的なデータに基づいた意思決定を行います。

## 6. 参考リソースとツール

### 6.1 推奨ツール

- **テスト＆カバレッジ**: pytest, pytest-cov, coverage
- **静的解析**: pylint, flake8, mypy, bandit
- **セキュリティ**: `devsecops_guide.md` 参照 (Bandit, Semgrep, OWASP ZAP, pip-audit, Trivy, detect-secrets, Hadolint等)
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
- **OWASP Top 10**: [https://owasp.org/www-project-top-ten/](https://owasp.org/www-project-top-ten/)
- **`devsecops_guide.md` (本プロジェクト内)** 