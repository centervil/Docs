"""
CI/CDパイプラインが正常に動作することを確認するための単純なサンプルテスト
"""
import pytest


def add(a, b):
    """2つの数値を加算する単純な関数"""
    return a + b


class TestSample:
    """基本的なテスト機能の確認用クラス"""
    
    def test_addition(self):
        """加算関数のテスト"""
        assert add(1, 2) == 3
        assert add(-1, 1) == 0
        assert add(0, 0) == 0
    
    def test_truthiness(self):
        """基本的な真偽値のテスト"""
        assert True
        assert not False
        assert 1
        assert not 0
    
    @pytest.mark.parametrize("input_val,expected", [
        (1, 1),
        ("string", "string"),
        ([1, 2], [1, 2]),
        (None, None)
    ])
    def test_identity(self, input_val, expected):
        """パラメータ化されたテストの例"""
        assert input_val == expected 