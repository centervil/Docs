# Pytestベストプラクティスガイド

このガイドでは、Pythonプロジェクトでのテスト駆動開発を効果的に行うための、Pytestの活用方法とベストプラクティスを解説します。

## 1. Pytestの基本

### 1.1 Pytestとは

Pytestは、Pythonのテストフレームワークで、シンプルな構文と強力な機能を組み合わせたテストツールです。以下の特徴があります：

- シンプルな構文：`assert`文を直接使用してテスト検証が可能
- 高度な検出機能：テストファイルとテスト関数を自動的に検出
- フィクスチャの柔軟な管理：テスト前後の環境セットアップと後処理
- プラグインエコシステム：拡張機能が豊富
- 詳細なエラーレポート：テスト失敗時の情報が充実

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

## 2. テスト構造とベストプラクティス

### 2.1 ディレクトリ構造

推奨されるテストディレクトリ構造：

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
│   └── fixtures/
│       └── test_data.json
└── pytest.ini
```

### 2.2 命名規則

- テストファイル：`test_<テスト対象>.py`
- テストクラス：`Test<テスト対象>`
- テスト関数：`test_<テストする機能>`

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

各テストは以下の3つのステップで構成することを推奨します：

1. **Arrange**：テストの前提条件を設定
2. **Act**：テスト対象の機能を実行
3. **Assert**：結果を検証

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

## 3. フィクスチャの効果的な活用

### 3.1 フィクスチャの基本

フィクスチャは、テスト実行前後の環境セットアップと後処理を行う仕組みです：

```python
import pytest

@pytest.fixture
def sample_data():
    """テスト用のサンプルデータを提供するフィクスチャ"""
    data = {"key1": "value1", "key2": "value2"}
    return data

def test_data_processing(sample_data):
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

`conftest.py`ファイルに共通のフィクスチャを定義すると、複数のテストファイルから参照できます：

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

異なる入力データで同じテストロジックを実行する場合、`@pytest.mark.parametrize`を使用します：

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

テストにマーカーを付けて、特定のテストのみを実行したり除外したりできます：

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

`pytest-xdist`プラグインを使用して、テストを並列実行できます：

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

`pytest-cov`を使用してカバレッジレポートを生成します：

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

- 一般的に80%以上のカバレッジを目指す
- 重要なビジネスロジックは90%以上を目標にする
- カバレッジ率だけでなく、テストの質も重要
- エッジケースやエラー処理のテストを優先
- CI/CDでカバレッジの低下をチェックし、目標未達の場合はビルドを失敗させる設定も有効

## 7. CI/CDパイプラインとの統合

### 7.1 GitHub Actionsでの統合例

```yaml
# .github/workflows/tests.yml
name: Python Tests

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
        pip install pytest pytest-cov pytest-xdist
        pip install -e .
    - name: Test with pytest
      run: |
        pytest --cov=src/ --cov-report=xml
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### 7.2 テスト実行の最適化

- 高速テストと低速テストを分離し、高速テストを先に実行
- テストの依存関係を最小化して並列実行を最大化
- キャッシュを活用して環境セットアップを高速化
- テスト失敗時のデバッグ情報を充実させる

## 8. テストデータ管理

### 8.1 テストデータの分類

- **固定テストデータ**: JSONやYAMLファイルに保存したテストケース
- **動的テストデータ**: テスト実行時に生成するデータ
- **ファクトリ**: モデルインスタンスの生成を簡素化するパターン

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

### 9.1 プロパティベーステスト

`hypothesis`ライブラリを使用したプロパティベーステスト：

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

`pytest-snapshot`を使用して出力の一貫性をテスト：

```bash
pip install pytest-snapshot
```

```python
def test_generate_report(snapshot):
    report = generate_complex_report()
    snapshot.assert_match(report, 'report.txt')
```

### 9.3 パフォーマンステスト

`pytest-benchmark`を使用してパフォーマンステスト：

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

## 10. トラブルシューティングとベストプラクティス

### 10.1 一般的な問題と解決策

- **テストの分離**: 各テストは独立して実行できることを確認
- **フィクスチャの適切な範囲**: スコープを適切に設定して実行効率を向上
- **テンポラリファイルの管理**: `tmp_path`フィクスチャを活用
- **環境変数の管理**: `monkeypatch`でテスト中の環境変数を制御
- **テストの順序依存性排除**: テスト順序に依存しないようにテストを設計

### 10.2 テストコードの品質維持

- テストコードも通常のコードと同様にレビュー対象とする
- 重複を避け、テストユーティリティやヘルパー関数を活用
- メンテナンス性を考慮したテスト設計
- 定期的なテストコードのリファクタリング

### 10.3 チーム内でのベストプラクティス確立

- テスト戦略とガイドラインのドキュメント化
- コードレビューでのテスト品質チェック
- テストファーストの文化醸成
- 継続的な学習と改善

## 11. 参考リソース

- [Pytest公式ドキュメント](https://docs.pytest.org/)
- [Python Testingの優れた実践](https://docs.python-guide.org/writing/tests/)
- [Pytestチュートリアル（Real Python）](https://realpython.com/pytest-python-testing/)
- [Effective Python Testing with Pytest](https://pragprog.com/titles/bopytest/python-testing-with-pytest/)
- [Factory Boy ドキュメント](https://factoryboy.readthedocs.io/) 