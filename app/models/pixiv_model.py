from datetime import datetime
from app.utils.db import get_connection
import logging

class PixivModel:
    def __init__(self):
        self.conn = get_connection()
        self._createTable()

    def _createTable(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                Create Table If Not Exists pic (
                    ID TEXT PRIMARY KEY,
                    name TEXT,
                    downloadedDate TEXT,
                    lastDownloadID TEXT,
                    url TEXT)
                """)
            self.conn.commit()

    def getInfoByID(self, userId):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM pic WHERE id =  ?", (userId,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def insertById(self, userInfo):
        logging.debug(f"插入或替换数据: {userInfo}")
        userId = userInfo.get("ID")
        # existFlag = self.getInfoByID(userId)
        current_time = datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        with self.conn:
            cursor = self.conn.cursor()
            # if existFlag:
            #     cursor.execute("""
            #         UPDATE pic SET
            #         name = ?, downloadedDate = ?, lastdownloadID = ?
            #         WHERE ID = ?;
            #     """, (userInfo.get("name"), formatted_time, userInfo.get("lastdownloadID"), userId, ))
            # else:
            #     cursor.execute("""
            #         INSERT INTO pic VALUES
            #         (?, ?, ?, ?, ?)
            #     """, (userId, userInfo.get("name"), formatted_time, userInfo.get("lastdownloadID"), "https://www.pixiv.net/users/" + userId, ))
            cursor.execute("""
                    INSERT OR REPLACE INTO pic(ID, name, downloadedDate, lastDownloadID, url)
                    VALUES(?, ?, ?, ?, ?)
                """, (userId, userInfo.get("name"), formatted_time, userInfo.get("lastDownloadID"), f"https://www.pixiv.net/users/{userId}", ))
