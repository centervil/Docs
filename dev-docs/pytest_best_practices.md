# Pytestベストプラクティスガイド (AIエージェント主導開発向け)

このガイドでは、Pythonプロジェクトにおいて、AIコーディングエージェント (Cursor, Cline, MCPなど) が自律的にテストコード生成やテスト実行を行い、人間がPMとして重要な方向性の確認とレビューを行う開発体制における、Pytestの活用方法とベストプラクティスを解説します。
**`devsecops_guide.md` で定義されたセキュリティテスト戦略も考慮してください。**

## 1. Pytestの基本

### 1.1 Pytestとは

Pytestは、Pythonのテストフレームワークで、シンプルな構文と強力な機能を組み合わせたテストツールです。以下の特徴があります：

- シンプルな構文：`assert`文を直接使用してテスト検証が可能
- 高度な検出機能：テストファイルとテスト関数を自動的に検出
- フィクスチャの柔軟な管理：テスト前後の環境セットアップと後処理
- プラグインエコシステム：拡張機能が豊富
- 詳細なエラーレポート：テスト失敗時の情報が充実

AIエージェントはこれらの特徴を活かし、最小限の指示でも効果的なテストを自律的に設計・実装できます。

### 1.2 インストールと基本設定

```bash
pip install pytest pytest-cov pytest-xdist
```

プロジェクトのルートディレクトリに`pytest.ini`ファイルを作成：

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
addopts = --strict-markers
```

AIエージェントはこの設定ファイルを参照し、プロジェクト規約に沿ったテストを自律的に生成します。

## 2. テスト構造とベストプラクティス

### 2.1 ディレクトリ構造

AIエージェントが従うべき推奨テストディレクトリ構造：

```
myproject/
├── src/
│   └── mymodule/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_core.py
│   │   └── test_utils.py
│   ├── integration/
│   │   └── test_end_to_end.py
│   ├── security/            # セキュリティテスト (オプション)
│   │   └── test_security_vulnerabilities.py # 特定の脆弱性再現テストなど
│   └── fixtures/
│       └── test_data.json
└── pytest.ini
```

AIエージェントは既存のディレクトリ構造を尊重し、新しいテストファイルを適切な場所に自律的に配置します。
**特定の脆弱性に対するテストは `tests/security/` ディレクトリに配置することを検討してください。**

### 2.2 命名規則

AIエージェントは以下の命名規則に従ってテストコードを生成します：

- テストファイル：`test_<テスト対象>.py`
- テストクラス：`Test<テスト対象>`
- テスト関数：`test_<テストする機能>`
- **セキュリティテスト関数**: `test_security_<脆弱性やシナリオ>` (例: `test_security_sql_injection`)

例：
```python
# src/mymodule/utils.py
def add_numbers(a, b):
    return a + b

# tests/unit/test_utils.py
from mymodule.utils import add_numbers

def test_add_numbers():
    assert add_numbers(1, 2) == 3
    assert add_numbers(-1, 1) == 0
    assert add_numbers(0, 0) == 0
```

### 2.3 AAA（Arrange-Act-Assert）パターン

AIエージェントは自律的にテスト生成する際、AAA（Arrange-Act-Assert）パターンを使用します：

1.  **Arrange**: テストの前提条件を設定（必要なデータ、モック化する対象など）
2.  **Act**: テスト対象の機能を実行
3.  **Assert**: 期待される結果や状態変化を検証

例：
```python
def test_user_registration():
    # Arrange
    user_data = {"username": "testuser", "email": "test@example.com"}
    db = MockDatabase()
    
    # Act
    result = register_user(user_data, db)
    
    # Assert
    assert result.success is True
    assert db.get_user("testuser") is not None
    assert len(db.sent_emails) == 1
```

PMはレビュー時に、AIが生成したテストがAAAパターンに従っているか、テストが機能の境界条件や異常系、**および想定されるセキュリティ攻撃パターン**を適切にカバーしているかを確認します。

## 3. フィクスチャの効果的な活用

### 3.1 フィクスチャの基本

AIエージェントは、`conftest.py` などで定義された既存のフィクスチャを検出し、テスト生成時に自律的に活用します。

```python
import pytest

@pytest.fixture
def sample_data():
    """テスト用のサンプルデータを提供するフィクスチャ"""
    data = {"key1": "value1", "key2": "value2"}
    return data

def test_data_processing(sample_data): # AIエージェントが自律的に適切なフィクスチャを選択
    result = process_data(sample_data)
    assert "key1" in result
    assert result["key1"] == "processed_value1"
```

### 3.2 フィクスチャのスコープ

フィクスチャのスコープを適切に設定することで、テストの効率を向上させることができます：

```python
@pytest.fixture(scope="function")  # デフォルト：各テスト関数ごとに実行
def db_connection():
    conn = create_db_connection()
    yield conn
    conn.close()

@pytest.fixture(scope="module")  # モジュール内の全テストで共有
def expensive_computation():
    result = perform_expensive_computation()
    return result

@pytest.fixture(scope="session")  # テストセッション全体で共有
def app_client():
    app = create_app("testing")
    client = app.test_client()
    return client
```

スコープの種類：
- `function`: 各テスト関数ごとに実行（デフォルト）
- `class`: クラス内の全テストで共有
- `module`: モジュール内の全テストで共有
- `package`: パッケージ内の全テストで共有
- `session`: テストセッション全体で共有

### 3.3 フィクスチャの依存関係

フィクスチャは他のフィクスチャに依存することができます：

```python
@pytest.fixture
def user():
    return {"id": 1, "name": "Test User"}

@pytest.fixture
def authenticated_client(app_client, user):
    app_client.login(user)
    yield app_client
    app_client.logout()
```

### 3.4 conftest.py の活用

`conftest.py` に共通フィクスチャを定義することで、AIエージェントはプロジェクト全体で利用可能なセットアップコードを容易に発見・利用できます。

```python
# tests/conftest.py
import pytest
import json
from pathlib import Path

@pytest.fixture(scope="session")
def test_data():
    data_file = Path(__file__).parent / "fixtures" / "test_data.json"
    with open(data_file, "r") as f:
        return json.load(f)
```

異なるディレクトリレベルで`conftest.py`を配置することで、スコープを調整できます。

## 4. パラメータ化とテストの効率化

### 4.1 パラメータ化テスト

PMはAIエージェントに対し、`@pytest.mark.parametrize` を用いて、境界値、代表値、異常値などを考慮したテストケースを網羅的に生成するように指示できます。

```python
@pytest.mark.parametrize("input_value,expected", [
    (1, 1),
    (2, 4),
    (3, 9),
    (4, 16),
    (-1, 1),  # 絶対値を返す場合
])
def test_square_function(input_value, expected):
    assert square(input_value) == expected
```

複数のパラメータセットを使用する場合：

```python
@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_multiple_parameters(x, y):
    # x=0,y=2 / x=0,y=3 / x=1,y=2 / x=1,y=3 の4パターンでテスト実行
    assert x < y
```

### 4.2 マーカーの活用

PMはAIエージェントに対し、特定のマーカー（例: `-m "not slow"`, `-m integration`）を指定してテストを実行させることで、テストスイートの実行を制御できます。

```python
@pytest.mark.slow
def test_slow_operation():
    # 時間のかかる処理
    result = perform_slow_operation()
    assert result is not None

@pytest.mark.integration
def test_database_integration():
    # 実際のデータベースを使ったテスト
    db = get_real_database()
    assert db.is_connected()
```

マーカーを使ったテスト実行：

```bash
# 遅いテストを除外
pytest -m "not slow"

# 統合テストのみ実行
pytest -m "integration"

# 複雑な条件
pytest -m "integration and not slow"
```

### 4.3 並列実行によるテスト高速化

PMはAIエージェントに対し、`pytest-xdist` を利用した並列実行（例: `pytest -n auto`）を指示することで、CI/CDパイプラインなどでのテスト時間を短縮できます。ただし、AIが生成するテストが独立していることの重要性を認識しておく必要があります。

```bash
# CPUコア数に基づいて自動的に並列実行
pytest -n auto

# 指定した数のプロセスで並列実行
pytest -n 4
```

注意点：
- 並列実行では、テスト間の独立性が重要
- 共有リソース（データベース、ファイルなど）へのアクセスには注意が必要
- 順序依存のテストは問題が発生する可能性がある

## 5. モックとスタブ

PMはAIエージェントに対し、テスト対象の外部依存性（API、DBなど）を特定し、`monkeypatch` や `pytest-mock` を用いて適切にモック化するよう指示します。

### 5.1 MonkeyPatchの活用

`monkeypatch`フィクスチャを使用して、関数やオブジェクトを一時的に置き換えることができます：

```python
def test_api_request(monkeypatch):
    # 外部APIへの実際のリクエストを送信しないようにモック化
    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self):
                self.status_code = 200
                self.json_data = {"key": "value"}
                
            def json(self):
                return self.json_data
                
        return MockResponse()
    
    # requestsライブラリのget関数をモック化
    monkeypatch.setattr("requests.get", mock_get)
    
    # テスト対象の関数を実行（内部でrequests.getを使用）
    result = fetch_data_from_api("https://api.example.com/data")
    
    # モック化された結果を検証
    assert result == {"key": "value"}
```

### 5.2 pytest-mockの活用

`pytest-mock`プラグインを使用すると、より高度なモックが可能になります：

```bash
pip install pytest-mock
```

使用例：
```python
def test_function_with_mock(mocker):
    # spy：元の関数を呼び出しつつ、呼び出し情報を記録
    spy = mocker.spy(math, 'sqrt')
    
    # 関数の戻り値をモック化
    mocker.patch('module.submodule.function', return_value=10)
    
    # 例外を発生させるモック
    mocker.patch('module.submodule.function', side_effect=ValueError)
    
    # 呼び出し確認
    result = function_under_test()
    spy.assert_called_once_with(4)
```

### 5.3 モックを使用する際の注意点

- モックは必要最小限にとどめる
- 可能な限り実際の依存関係を使用したテストも行う
- 外部システムとの統合部分をモック化するのが最も効果的
- モックが本物の動作を正確に再現していることを確認する

## 6. コードカバレッジの最適化

### 6.1 カバレッジレポートの生成

CI/CDパイプラインで生成されたカバレッジレポートをPMが確認し、カバレッジが低い箇所についてAIエージェントにテストケースの追加を指示します。
**ただし、カバレッジ率だけを追求するのではなく、重要な機能やセキュリティに関連するコードパスがテストされていることを重視します。**

```bash
# 基本的なカバレッジレポート
pytest --cov=src/mymodule

# HTML形式の詳細レポート
pytest --cov=src/mymodule --cov-report=html

# XMLレポート（CI/CDツールとの統合用）
pytest --cov=src/mymodule --cov-report=xml
```

### 6.2 カバレッジ計測の設定

`.coveragerc`ファイルを使用して、カバレッジ計測の詳細を設定できます：

```ini
[run]
source = src/mymodule
omit =
    */tests/*
    */migrations/*
    */__init__.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__.:
    pass
    raise ImportError
```

### 6.3 カバレッジ目標と戦略

PMはプロジェクトのカバレッジ目標を設定し、AIエージェントにその目標達成に向けたテスト生成を指示します。CI/CDでのカバレッジチェックは品質維持に不可欠です。

## 7. CI/CDパイプラインとの統合

### 7.1 GitHub Actionsでの統合例

CI/CDパイプラインは、AIエージェントによるコード変更に対する自動的な品質・**セキュリティ**チェック機構として機能します。テスト失敗時には、PMがログを確認し、AIエージェントに修正を指示します。

```yaml
# .github/workflows/tests.yml
name: Python Tests & Security Checks

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10']

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        # requirements-dev.txt などで pytest, pytest-cov, SAST/SCAツールなどを管理
        pip install -r requirements-dev.txt 
        pip install -e . 
    - name: Run SAST (Bandit)
      run: bandit -r src/ -f json -o bandit-report.json || echo "Bandit found issues"
    - name: Run SAST (Semgrep)
      run: semgrep scan --config auto --json > semgrep-report.json || echo "Semgrep found issues"
    - name: Run SCA (pip-audit)
      run: pip-audit || echo "pip-audit found issues"
    - name: Test with pytest
      run: |
        pytest --cov=src/ --cov-report=xml
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
    # 必要に応じて、レポートをアーティファクトとして保存するステップを追加
    # - name: Archive reports
    #   uses: actions/upload-artifact@v3
    #   with:
    #     name: security-reports
    #     path: |
    #       bandit-report.json
    #       semgrep-report.json
```

### 7.2 テスト実行の最適化

PMはAIエージェント（またはCI/CD設定）に対し、マーカーや並列実行を活用して効率的なテスト実行を指示できます。
**セキュリティテスト (`@pytest.mark.security`) を定義し、必要に応じて選択的に実行することも検討します。**

## 8. テストデータ管理

### 8.1 テストデータの分類

PMはAIエージェントに対し、テストデータの種類（固定、動的、ファクトリ）に応じて、適切な管理・利用方法（ファイル参照、フィクスチャ利用、Factory Boy利用など）を指示します。

### 8.2 Factory Boyパターン

```python
# tests/factories.py
import factory
from myapp.models import User, Post

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    id = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda o: f'{o.username}@example.com')
    is_active = True

class PostFactory(factory.Factory):
    class Meta:
        model = Post
    
    id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: f'Post Title {n}')
    content = factory.Faker('text', max_nb_chars=200)
    author = factory.SubFactory(UserFactory)
```

使用例：
```python
def test_post_creation():
    # 特定のユーザーを作成
    user = UserFactory(username="testuser")
    
    # そのユーザーの投稿を作成
    post = PostFactory(author=user)
    
    assert post.author.username == "testuser"
    
    # バッチ作成
    posts = PostFactory.create_batch(5, author=user)
    assert len(posts) == 5
    assert all(p.author == user for p in posts)
```

## 9. 高度なテストテクニック

PMはAIエージェントに対し、必要に応じてこれらの高度なテスト手法（プロパティベーステスト、スナップショットテスト、パフォーマンステスト）の利用を指示できます。

### 9.1 プロパティベーステスト

`hypothesis` を利用して、AIエージェントに多様な入力パターンを自動生成させ、予期せぬバグを発見させることを試みます。

```bash
pip install hypothesis
```

```python
from hypothesis import given
from hypothesis import strategies as st

@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    assert a + b == b + a

@given(st.lists(st.integers()))
def test_sorted_result_has_same_elements(lst):
    sorted_lst = sorted(lst)
    assert len(sorted_lst) == len(lst)
    assert set(sorted_lst) == set(lst)
```

### 9.2 スナップショットテスト

`pytest-snapshot` を利用して、複雑な出力（例: 生成されたファイル、APIレスポンス）の一貫性をAIエージェントに検証させます。

```bash
pip install pytest-snapshot
```

```python
def test_generate_report(snapshot):
    report = generate_complex_report()
    snapshot.assert_match(report, 'report.txt')
```

### 9.3 パフォーマンステスト

`pytest-benchmark` を利用して、特定のコードブロックのパフォーマンスをAIエージェントに測定させ、リファクタリングの効果を確認させます。

```bash
pip install pytest-benchmark
```

```python
def test_algorithm_performance(benchmark):
    # ベンチマーク実行
    result = benchmark(sort_algorithm, large_data_set)
    
    # 結果検証
    assert benchmark.stats.stats.mean < 0.001  # 平均実行時間
```

## 10. トラブルシューティングとベストプラクティス (AIエージェント連携 & Human-In-The-Loop)

### 10.1 AIエージェントによるテストの問題

- **不適切なテスト生成**: AIが意図しないテストを生成する場合があるため、PMによるレビューが不可欠です。
- **既存コードへの影響**: PMはAIの変更が既存コードに悪影響を与えないか確認する必要があります。
- **テストの独立性**: PMはAIに対し、独立したテストを生成するように指示します。
- **セキュリティテストの不足**: AIは機能テストに偏る可能性があるため、PMはセキュリティテストの観点からもレビューし、必要に応じて追加・修正を指示します。

### 10.2 テストコードの品質維持 (AIエージェント連携)

- AI生成コードもPM（またはレビュアー）がレビューし、品質 (**およびセキュリティ観点**) を担保します。
- PMはAIに対し、テストユーティリティの活用やリファクタリングを指示できます。

### 10.3 AIエージェント開発におけるベストプラクティス (PM視点)

- **明確な指示**: PMはテストの目的、対象、期待結果、利用すべき技術（フィクスチャ、モック）、**考慮すべきセキュリティシナリオ**を具体的に指示します。
- **段階的な生成と確認 (Human-In-The-Loop)**: PMはAIに段階的にテストを生成させ、各ステップで結果を確認・フィードバックします。
- **結果の検証**: PMはAIが生成したテストが意図通り機能し、品質・**セキュリティ**向上に貢献しているかを最終的に判断します。
- **TDDサイクルの実践**: PMが指示を出し、AIが実行し、PMが確認するという対話ループを通じて、TDDサイクル（Red→Green→Refactor）を回します。

## 11. 参考リソース

- [Pytest公式ドキュメント](https://docs.pytest.org/)
- [Python Testingの優れた実践](https://docs.python-guide.org/writing/tests/)
- [Pytestチュートリアル（Real Python）](https://realpython.com/pytest-python-testing/)
- [Effective Python Testing with Pytest](https://pragprog.com/titles/bopytest/python-testing-with-pytest/)
- [Factory Boy ドキュメント](https://factoryboy.readthedocs.io/)
- **`devsecops_guide.md` (本プロジェクト内)** 