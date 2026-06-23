import logging
from pathlib import Path

import yaml

CONFIG_PATH = (
    Path(__file__).resolve().parent.parent.parent / "resources" / "conf" / "app_config.yml"
)

logger = logging.getLogger(__name__)


def load_app_config():
    try:
        return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        logger.error("配置文件找不到: %s", CONFIG_PATH)
        raise RuntimeError(f"配置文件找不到: {CONFIG_PATH}") from None
    except yaml.YAMLError as e:
        logger.error("配置文件解析错误：%s", e)
        raise RuntimeError(f"配置文件解析错误：{e}") from e
