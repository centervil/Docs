"""
マークダウン処理ユーティリティモジュールのユニットテスト
"""
import os
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# プロジェクトルートへのパスを取得し、それをimportパスに追加
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

# まだ実装されていないモジュールをインポート
try:
    from scripts.utils.markdown_utils import (
        parse_markdown,
        extract_headers,
        extract_lists,
        extract_code_blocks,
        format_markdown_for_note,
        clean_markdown
    )
except ImportError:
    # テスト実行時にはまだインポートできないので、テストだけ記述
    pass


class TestMarkdownUtils:
    """マークダウン処理ユーティリティのテストクラス"""
    
    @pytest.fixture
    def sample_markdown(self):
        """テスト用のサンプルマークダウン"""
        return """# サンプルマークダウン

## 見出し1
これは本文です。

## 見出し2
- リスト項目1
- リスト項目2
  - ネストされた項目

### 見出し2-1
```python
def hello():
    print("Hello, world!")
```

## 見出し3
これは**強調**された文字を含む文章です。
"""
    
    def test_parse_markdown(self, sample_markdown):
        """マークダウンのパース機能をテスト"""
        result = parse_markdown(sample_markdown)
        
        # 結果が辞書であることを確認
        assert isinstance(result, dict)
        
        # 必要なキーが含まれていることを確認
        assert "headers" in result
        assert "lists" in result
        assert "code_blocks" in result
        assert "paragraphs" in result
        
        # 内容の確認
        assert len(result["headers"]) > 0
        assert "サンプルマークダウン" in str(result["headers"])
    
    def test_extract_headers(self, sample_markdown):
        """見出しの抽出機能をテスト"""
        headers = extract_headers(sample_markdown)
        
        # 見出しの数が正しいことを確認
        assert len(headers) == 5
        
        # 見出しの内容と階層が正しいことを確認
        assert headers[0]["level"] == 1
        assert headers[0]["text"] == "サンプルマークダウン"
        assert headers[1]["level"] == 2
        assert headers[1]["text"] == "見出し1"
        assert headers[2]["level"] == 2
        assert headers[2]["text"] == "見出し2"
        assert headers[3]["level"] == 3
        assert headers[3]["text"] == "見出し2-1"
        assert headers[4]["level"] == 2
        assert headers[4]["text"] == "見出し3"
    
    def test_extract_lists(self, sample_markdown):
        """リストの抽出機能をテスト"""
        lists = extract_lists(sample_markdown)
        
        # リストが抽出されていることを確認
        assert len(lists) == 1
        
        # リスト項目の数と内容が正しいことを確認
        list_items = lists[0]["items"]
        assert len(list_items) == 2
        assert list_items[0]["text"] == "リスト項目1"
        assert list_items[0]["level"] == 1
        assert list_items[1]["text"] == "リスト項目2"
        assert list_items[1]["level"] == 1
        
        # ネストされたリスト項目が正しく抽出されていることを確認
        nested_items = lists[0]["nested_items"]
        assert len(nested_items) == 1
        assert nested_items[0]["text"] == "ネストされた項目"
        assert nested_items[0]["level"] == 2
        assert nested_items[0]["parent_index"] == 1  # 2番目の項目の子
    
    def test_extract_code_blocks(self, sample_markdown):
        """コードブロックの抽出機能をテスト"""
        code_blocks = extract_code_blocks(sample_markdown)
        
        # コードブロックが抽出されていることを確認
        assert len(code_blocks) == 1
        
        # コードブロックの言語と内容が正しいことを確認
        assert code_blocks[0]["language"] == "python"
        assert "def hello():" in code_blocks[0]["code"]
        assert "print(\"Hello, world!\")" in code_blocks[0]["code"]
    
    def test_format_markdown_for_note(self, sample_markdown):
        """note用のマークダウンフォーマット機能をテスト"""
        formatted = format_markdown_for_note(sample_markdown)
        
        # 結果がstring型であることを確認
        assert isinstance(formatted, str)
        
        # note特有の装飾が適用されていることを確認
        assert "# サンプルマークダウン" in formatted
        assert "## 見出し1" in formatted
        assert "**強調**" in formatted
        
        # コードブロックが適切にフォーマットされていることを確認
        assert "```python" in formatted
        assert "def hello():" in formatted
    
    def test_clean_markdown(self):
        """マークダウンのクリーニング機能をテスト"""
        # 不要な空白行を含むマークダウン
        dirty_markdown = """# タイトル

        
## セクション1

これは段落です。


- 項目1

- 項目2



## セクション2
"""
        
        cleaned = clean_markdown(dirty_markdown)
        
        # デバッグ用の出力
        print("\n--- 実際の結果 ---")
        print(repr(cleaned))
        
        expected = """# タイトル

## セクション1

これは段落です。

- 項目1
- 項目2

## セクション2"""
        
        print("\n--- 期待値 ---")
        print(repr(expected))
        
        # 空白行が適切に処理されていることを確認
        assert cleaned == expected
    
    def test_clean_markdown_preserves_code_blocks(self):
        """コードブロック内の空白行が保持されることをテスト"""
        markdown_with_code = """# コードブロック例

```python
def example():
    
    # 空行を含む
    return True

# もう一つの空行

```
"""
        cleaned = clean_markdown(markdown_with_code)
        
        # コードブロック内の空白行が保持されていることを確認
        assert "def example():" in cleaned
        assert "\n    \n" in cleaned  # コードブロック内の空行
        assert "\n# もう一つの空行\n" in cleaned 