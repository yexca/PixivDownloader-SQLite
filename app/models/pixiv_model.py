import logging
from datetime import datetime
from pathlib import Path

from app.utils.db import get_connection

logger = logging.getLogger(__name__)


class PixivModel:
    def __init__(self, db_path: Path | str | None = None):
        self.conn = get_connection(db_path)
        self._create_table()

    def _create_table(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                Create Table If Not Exists pic (
                    ID TEXT PRIMARY KEY,
                    name TEXT,
                    downloadedDate TEXT,
                    lastDownloadID TEXT,
                    url TEXT)
                """
            )
            self.conn.commit()

    def get_info_by_id(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM pic WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def insert_by_id(self, user_info):
        logger.debug("插入或替换数据: %s", user_info)
        user_id = user_info.get("ID")
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                    INSERT OR REPLACE INTO pic(ID, name, downloadedDate, lastDownloadID, url)
                    VALUES(?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    user_info.get("name"),
                    formatted_time,
                    user_info.get("lastDownloadID"),
                    f"https://www.pixiv.net/users/{user_id}",
                ),
            )

    def _createTable(self):
        self._create_table()

    def getInfoByID(self, user_id):
        return self.get_info_by_id(user_id)

    def insertById(self, user_info):
        self.insert_by_id(user_info)
