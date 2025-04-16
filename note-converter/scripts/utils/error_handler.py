"""
エラーハンドリングユーティリティモジュール

一貫したエラー処理とロギングの仕組みを提供する
"""
import logging
import json
import time
import traceback
import sys
from typing import Callable, Any, Dict, Optional, Union, TypeVar, List, Tuple
from datetime import datetime
from functools import wraps

# ロガーの設定
logger = logging.getLogger(__name__)

# リトライ可能な関数の戻り値の型
T = TypeVar('T')

class BaseError(Exception):
    """基本エラークラス"""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        """
        初期化
        
        Args:
            message: エラーメッセージ
            context: エラーのコンテキスト情報
        """
        self.message = message
        self.context = context or {}
        self.timestamp = datetime.now().isoformat()
        
        # 親クラスの初期化
        super().__init__(message)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        エラー情報を辞書形式に変換
        
        Returns:
            エラー情報の辞書
        """
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "timestamp": self.timestamp,
            "context": self.context
        }
    
    def to_json(self) -> str:
        """
        エラー情報をJSON形式に変換
        
        Returns:
            JSON形式のエラー情報
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class APIError(BaseError):
    """API呼び出し時のエラー"""
    
    def __init__(
        self, 
        message: str, 
        status_code: Optional[int] = None, 
        response_body: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        初期化
        
        Args:
            message: エラーメッセージ
            status_code: HTTPステータスコード
            response_body: レスポンスボディ
            context: エラーのコンテキスト情報
        """
        # コンテキスト情報の準備
        ctx = context or {}
        
        if status_code is not None:
            ctx["status_code"] = status_code
        
        if response_body is not None:
            ctx["response_body"] = response_body
        
        # 親クラスの初期化
        super().__init__(message, ctx)


class AuthError(APIError):
    """認証エラー"""
    pass


class RateLimitError(APIError):
    """レートリミットエラー"""
    pass


class NetworkError(BaseError):
    """ネットワークエラー"""
    pass


class ValidationError(BaseError):
    """入力検証エラー"""
    pass


class FileError(BaseError):
    """ファイル操作のエラー"""
    pass


class ConfigError(BaseError):
    """設定関連のエラー"""
    pass


def log_error(
    error: Union[BaseError, Exception], 
    level: int = logging.ERROR, 
    include_traceback: bool = True
) -> None:
    """
    エラーをログに記録
    
    Args:
        error: エラーオブジェクト
        level: ログレベル
        include_traceback: トレースバックを含めるかどうか
    """
    # BaseErrorの場合は構造化されたログを出力
    if isinstance(error, BaseError):
        log_data = error.to_dict()
        
        if include_traceback:
            log_data["traceback"] = traceback.format_exc()
        
        logger.log(level, json.dumps(log_data, ensure_ascii=False))
    
    # 標準の例外の場合は通常のログを出力
    else:
        if include_traceback:
            logger.log(level, f"{error.__class__.__name__}: {str(error)}", exc_info=True)
        else:
            logger.log(level, f"{error.__class__.__name__}: {str(error)}")


def retry(
    max_attempts: int = 3, 
    delay: float = 1.0, 
    backoff_factor: float = 2.0,
    exceptions: List[type] = None
) -> Callable:
    """
    リトライデコレータ
    
    Args:
        max_attempts: 最大リトライ回数
        delay: 初期遅延（秒）
        backoff_factor: バックオフ係数
        exceptions: リトライ対象の例外クラスのリスト
        
    Returns:
        デコレータ関数
    """
    if exceptions is None:
        exceptions = [Exception]
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            attempt = 0
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except tuple(exceptions) as e:
                    attempt += 1
                    
                    # 最後の試行で失敗した場合は例外を再発生
                    if attempt == max_attempts:
                        raise
                    
                    # 遅延時間の計算（指数バックオフ）
                    wait_time = delay * (backoff_factor ** (attempt - 1))
                    
                    # エラーをログに記録
                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed: {str(e)}. "
                        f"Retrying in {wait_time:.2f} seconds..."
                    )
                    
                    # 待機
                    time.sleep(wait_time)
            
            # ここには到達しないはずだが、型チェックのために必要
            raise RuntimeError("Unexpected error in retry logic")
        
        return wrapper
    
    return decorator


def safe_operation(
    default_return: Any = None, 
    error_handler: Optional[Callable[[Exception], None]] = None
) -> Callable:
    """
    安全に操作を実行するデコレータ
    
    Args:
        default_return: エラー時のデフォルト戻り値
        error_handler: エラーハンドラ関数
        
    Returns:
        デコレータ関数
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # エラーをログに記録
                log_error(e)
                
                # カスタムエラーハンドラがあれば実行
                if error_handler:
                    error_handler(e)
                
                # デフォルト値を返す
                return default_return
        
        return wrapper
    
    return decorator


def configure_logging(
    log_level: int = logging.INFO,
    log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    log_file: Optional[str] = None
) -> None:
    """
    ロギングの設定
    
    Args:
        log_level: ログレベル
        log_format: ログフォーマット
        log_file: ログファイルのパス
    """
    # ロガーの設定
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # フォーマッタの作成
    formatter = logging.Formatter(log_format)
    
    # コンソールハンドラの設定
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # ファイルハンドラの設定（指定された場合）
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # デフォルトのロガーが重複して出力するのを防ぐ
    root_logger.propagate = False 