import yaml, logging
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "resources" / "conf" / "app_config.yml"

def load_app_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logging.error(f"配置文件找不到: {CONFIG_PATH}")
        raise RuntimeError(f"配置文件找不到: {CONFIG_PATH}")
    except yaml.YAMLError as e:
        logging.error(f"配置文件解析错误：{e}")
        raise RuntimeError(f"配置文件解析错误：{e}")