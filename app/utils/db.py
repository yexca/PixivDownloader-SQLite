import sys
from pathlib import Path
import sqlite3

if getattr(sys, 'frozen', False):
    # 如果是打包后，放在和可执行文件同目录
    BASE_DIR = Path(sys.executable).parent
else:
    # 如果是开发环境，放在主入口
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

DB_PATH = BASE_DIR / "resources" / "pixiv.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    # 将返回风格从元组改为字典风格
    conn.row_factory = sqlite3.Row
    return conn
