"""
エラーハンドリングユーティリティモジュールのユニットテスト
"""
import os
import sys
import pytest
import json
import logging
import time
from pathlib import Path
from unittest.mock import patch, MagicMock, call

# プロジェクトルートへのパスを取得し、それをimportパスに追加
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

from scripts.utils.error_handler import (
    BaseError, APIError, AuthError, RateLimitError, NetworkError,
    ValidationError, FileError, ConfigError, log_error, retry,
    safe_operation, configure_logging
)


class TestBaseError:
    """BaseErrorクラスのテスト"""
    
    def test_init(self):
        """初期化のテスト"""
        error = BaseError("Test error message")
        
        assert error.message == "Test error message"
        assert isinstance(error.context, dict)
        assert error.context == {}
        assert error.timestamp is not None
    
    def test_init_with_context(self):
        """コンテキスト付きの初期化のテスト"""
        context = {"key": "value", "number": 42}
        error = BaseError("Test error message", context)
        
        assert error.message == "Test error message"
        assert error.context == context
    
    def test_to_dict(self):
        """to_dictメソッドのテスト"""
        context = {"key": "value"}
        error = BaseError("Test error message", context)
        
        error_dict = error.to_dict()
        
        assert error_dict["error_type"] == "BaseError"
        assert error_dict["message"] == "Test error message"
        assert error_dict["context"] == context
        assert "timestamp" in error_dict
    
    def test_to_json(self):
        """to_jsonメソッドのテスト"""
        context = {"key": "value"}
        error = BaseError("Test error message", context)
        
        error_json = error.to_json()
        
        # JSONとして解析可能かを確認
        error_dict = json.loads(error_json)
        
        assert error_dict["error_type"] == "BaseError"
        assert error_dict["message"] == "Test error message"
        assert error_dict["context"] == context


class TestAPIError:
    """APIErrorクラスのテスト"""
    
    def test_init(self):
        """初期化のテスト"""
        error = APIError("API error")
        
        assert error.message == "API error"
        assert error.context == {}
    
    def test_init_with_status_code(self):
        """ステータスコード付きの初期化のテスト"""
        error = APIError("API error", status_code=404)
        
        assert error.message == "API error"
        assert error.context["status_code"] == 404
    
    def test_init_with_response_body(self):
        """レスポンスボディ付きの初期化のテスト"""
        error = APIError("API error", response_body='{"error": "Not found"}')
        
        assert error.message == "API error"
        assert error.context["response_body"] == '{"error": "Not found"}'
    
    def test_init_with_context(self):
        """コンテキスト付きの初期化のテスト"""
        context = {"endpoint": "/api/test"}
        error = APIError("API error", context=context)
        
        assert error.message == "API error"
        assert error.context["endpoint"] == "/api/test"
    
    def test_init_with_all_params(self):
        """全パラメータ付きの初期化のテスト"""
        context = {"endpoint": "/api/test"}
        error = APIError(
            "API error",
            status_code=500,
            response_body='{"error": "Server error"}',
            context=context
        )
        
        assert error.message == "API error"
        assert error.context["status_code"] == 500
        assert error.context["response_body"] == '{"error": "Server error"}'
        assert error.context["endpoint"] == "/api/test"


class TestErrorSubclasses:
    """エラーサブクラスのテスト"""
    
    def test_auth_error(self):
        """AuthErrorクラスのテスト"""
        error = AuthError("Auth failed")
        
        assert isinstance(error, APIError)
        assert isinstance(error, BaseError)
        assert error.message == "Auth failed"
    
    def test_rate_limit_error(self):
        """RateLimitErrorクラスのテスト"""
        error = RateLimitError("Rate limit exceeded")
        
        assert isinstance(error, APIError)
        assert isinstance(error, BaseError)
        assert error.message == "Rate limit exceeded"
    
    def test_network_error(self):
        """NetworkErrorクラスのテスト"""
        error = NetworkError("Connection failed")
        
        assert isinstance(error, BaseError)
        assert error.message == "Connection failed"
    
    def test_validation_error(self):
        """ValidationErrorクラスのテスト"""
        error = ValidationError("Invalid input")
        
        assert isinstance(error, BaseError)
        assert error.message == "Invalid input"
    
    def test_file_error(self):
        """FileErrorクラスのテスト"""
        error = FileError("File not found")
        
        assert isinstance(error, BaseError)
        assert error.message == "File not found"
    
    def test_config_error(self):
        """ConfigErrorクラスのテスト"""
        error = ConfigError("Missing configuration")
        
        assert isinstance(error, BaseError)
        assert error.message == "Missing configuration"


class TestLogError:
    """log_error関数のテスト"""
    
    @patch("logging.Logger.log")
    def test_log_base_error(self, mock_log):
        """BaseErrorのログ出力テスト"""
        error = BaseError("Test error")
        
        log_error(error, level=logging.WARNING)
        
        # ログが呼ばれたことを確認
        mock_log.assert_called_once()
        
        # 呼び出し時の引数を確認
        args, kwargs = mock_log.call_args
        
        assert args[0] == logging.WARNING
        
        # JSONとして解析可能なログメッセージかを確認
        error_dict = json.loads(args[1])
        
        assert error_dict["error_type"] == "BaseError"
        assert error_dict["message"] == "Test error"
    
    @patch("logging.Logger.log")
    def test_log_standard_exception(self, mock_log):
        """標準例外のログ出力テスト"""
        error = ValueError("Invalid value")
        
        log_error(error, level=logging.ERROR, include_traceback=False)
        
        # ログが呼ばれたことを確認
        mock_log.assert_called_once()
        
        # 呼び出し時の引数を確認
        args, kwargs = mock_log.call_args
        
        assert args[0] == logging.ERROR
        assert "ValueError: Invalid value" in args[1]
        assert kwargs == {}  # include_traceback=Falseなのでexc_infoは含まれない
    
    @patch("logging.Logger.log")
    def test_log_standard_exception_with_traceback(self, mock_log):
        """トレースバック付きの標準例外のログ出力テスト"""
        error = ValueError("Invalid value")
        
        log_error(error, include_traceback=True)
        
        # ログが呼ばれたことを確認
        mock_log.assert_called_once()
        
        # 呼び出し時の引数を確認
        args, kwargs = mock_log.call_args
        
        assert args[0] == logging.ERROR
        assert "ValueError: Invalid value" in args[1]
        assert kwargs["exc_info"] is True


class TestRetry:
    """retry関数のテスト"""
    
    def test_successful_execution(self):
        """成功するケースのテスト"""
        mock_func = MagicMock(return_value="success")
        
        # リトライデコレータを適用
        decorated_func = retry(max_attempts=3)(mock_func)
        
        # 実行
        result = decorated_func("arg1", "arg2", key="value")
        
        # 結果を確認
        assert result == "success"
        
        # 関数が1回だけ呼ばれたことを確認
        mock_func.assert_called_once_with("arg1", "arg2", key="value")
    
    def test_retry_and_success(self):
        """失敗後に成功するケースのテスト"""
        # 最初の2回は例外を発生させ、3回目で成功する関数をモック
        mock_func = MagicMock(side_effect=[ValueError("Fail 1"), ValueError("Fail 2"), "success"])
        
        # リトライデコレータを適用（短い待機時間で設定）
        decorated_func = retry(max_attempts=3, delay=0.01)(mock_func)
        
        # 実行
        result = decorated_func()
        
        # 結果を確認
        assert result == "success"
        
        # 関数が3回呼ばれたことを確認
        assert mock_func.call_count == 3
    
    def test_retry_and_failure(self):
        """リトライ後も失敗するケースのテスト"""
        # すべての呼び出しで例外を発生させる関数をモック
        mock_func = MagicMock(side_effect=ValueError("Persistent failure"))
        
        # リトライデコレータを適用（短い待機時間で設定）
        decorated_func = retry(max_attempts=3, delay=0.01)(mock_func)
        
        # 例外が発生することを確認
        with pytest.raises(ValueError) as excinfo:
            decorated_func()
        
        assert "Persistent failure" in str(excinfo.value)
        
        # 関数が3回呼ばれたことを確認
        assert mock_func.call_count == 3
    
    def test_retry_specific_exceptions(self):
        """特定の例外のみをリトライするケースのテスト"""
        # 異なる種類の例外を発生させる関数をモック
        mock_func = MagicMock(side_effect=[ValueError("Value error"), TypeError("Type error"), "success"])
        
        # ValueErrorのみをリトライ対象とするデコレータを適用
        decorated_func = retry(max_attempts=3, delay=0.01, exceptions=[ValueError])(mock_func)
        
        # TypeErrorは対象外なので、例外が発生することを確認
        with pytest.raises(TypeError) as excinfo:
            decorated_func()
        
        assert "Type error" in str(excinfo.value)
        
        # 関数が2回呼ばれたことを確認（ValueErrorのリトライ1回と、TypeErrorの発生1回）
        assert mock_func.call_count == 2


class TestSafeOperation:
    """safe_operation関数のテスト"""
    
    def test_successful_execution(self):
        """成功するケースのテスト"""
        mock_func = MagicMock(return_value="success")
        
        # safe_operationデコレータを適用
        decorated_func = safe_operation(default_return="default")(mock_func)
        
        # 実行
        result = decorated_func("arg1", key="value")
        
        # 結果を確認
        assert result == "success"
        
        # 関数が1回だけ呼ばれたことを確認
        mock_func.assert_called_once_with("arg1", key="value")
    
    def test_failure_with_default_return(self):
        """失敗時のデフォルト値返却のテスト"""
        # 例外を発生させる関数をモック
        mock_func = MagicMock(side_effect=ValueError("Error"))
        
        # safe_operationデコレータを適用
        decorated_func = safe_operation(default_return="default")(mock_func)
        
        # 実行
        with patch("scripts.utils.error_handler.log_error") as mock_log_error:
            result = decorated_func()
        
        # 結果を確認
        assert result == "default"
        
        # log_errorが呼ばれたことを確認
        mock_log_error.assert_called_once()
    
    def test_failure_with_error_handler(self):
        """エラーハンドラ付きの失敗時のテスト"""
        # 例外を発生させる関数をモック
        mock_func = MagicMock(side_effect=ValueError("Error"))
        
        # エラーハンドラをモック
        mock_error_handler = MagicMock()
        
        # safe_operationデコレータを適用
        decorated_func = safe_operation(
            default_return="default",
            error_handler=mock_error_handler
        )(mock_func)
        
        # 実行
        with patch("scripts.utils.error_handler.log_error"):
            result = decorated_func()
        
        # 結果を確認
        assert result == "default"
        
        # エラーハンドラが呼ばれたことを確認
        mock_error_handler.assert_called_once()
        
        # エラーハンドラに正しい例外が渡されたことを確認
        args, kwargs = mock_error_handler.call_args
        assert isinstance(args[0], ValueError)
        assert str(args[0]) == "Error"


class TestConfigureLogging:
    """configure_logging関数のテスト"""
    
    @patch("logging.getLogger")
    @patch("logging.StreamHandler")
    @patch("logging.FileHandler")
    def test_configure_logging_with_file(self, mock_file_handler, mock_stream_handler, mock_get_logger):
        """ファイルハンドラ付きのロギング設定テスト"""
        # モックの設定
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        mock_stream_handler_instance = MagicMock()
        mock_stream_handler.return_value = mock_stream_handler_instance
        
        mock_file_handler_instance = MagicMock()
        mock_file_handler.return_value = mock_file_handler_instance
        
        # 実行
        configure_logging(log_level=logging.DEBUG, log_file="test.log")
        
        # ロガーのレベルが設定されたことを確認
        mock_logger.setLevel.assert_called_once_with(logging.DEBUG)
        
        # ハンドラが追加されたことを確認
        mock_logger.addHandler.assert_has_calls([
            call(mock_stream_handler_instance),
            call(mock_file_handler_instance)
        ])
        
        # プロパゲーションが無効化されたことを確認
        assert mock_logger.propagate is False
    
    @patch("logging.getLogger")
    @patch("logging.StreamHandler")
    @patch("logging.FileHandler")
    def test_configure_logging_without_file(self, mock_file_handler, mock_stream_handler, mock_get_logger):
        """ファイルハンドラなしのロギング設定テスト"""
        # モックの設定
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        mock_stream_handler_instance = MagicMock()
        mock_stream_handler.return_value = mock_stream_handler_instance
        
        # 実行
        configure_logging()
        
        # ロガーのレベルが設定されたことを確認
        mock_logger.setLevel.assert_called_once_with(logging.INFO)
        
        # ストリームハンドラのみが追加されたことを確認
        mock_logger.addHandler.assert_called_once_with(mock_stream_handler_instance)
        
        # ファイルハンドラが作成されなかったことを確認
        mock_file_handler.assert_not_called() 