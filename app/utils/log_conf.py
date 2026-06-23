import logging
import logging.config
import sys
import traceback
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class LogConf:
    def __init__(self):
        # 如果是打包后的可执行文件，获取其目录；否则获取源代码目录
        base_dir = (
            Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
        )
        # 获取当天日期
        log_date = datetime.now().strftime("%Y-%m-%d")
        # 设置日志文件路径
        log_dir = base_dir / "logs"
        log_file_path = log_dir / f"app_{log_date}.log"

        # 确保日志目录存在
        log_dir.mkdir(parents=True, exist_ok=True)
        self.logging_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
            },
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                },
                "file": {
                    "level": "INFO",
                    "class": "logging.FileHandler",
                    "formatter": "standard",
                    "filename": log_file_path,
                    "encoding": "utf-8",  # 确保文件以 UTF-8 编码写入
                },
            },
            "root": {
                "level": "DEBUG",
                "handlers": ["console", "file"],
            },
            "loggers": {
                "sql_logger": {
                    "level": "INFO",
                    "handlers": ["file"],
                    "propagate": False,
                },
            },
        }

    def setup_logging(self):
        logging.config.dictConfig(self.logging_config)

        # 设置全局异常处理
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                # Ctrl+C 不处理
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            logger.critical("未捕获异常: \n%s", error_msg)

        sys.excepthook = handle_exception


# 记录不同级别的日志
# logging.debug("This is a debug message.")
# logging.info("This is an info message.")
# logging.warning("This is a warning message.")
# logging.error("This is an error message.")
# logging.critical("This is a critical message.")
