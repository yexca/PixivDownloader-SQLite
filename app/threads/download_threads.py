from PyQt6.QtCore import QThread, pyqtSignal
from app.controllers.home_controller import HomeController

class DownloadThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()    # 信号，表示任务完成

    def __init__(self, user_id, illust_id):
        super().__init__()
        self.user_id = user_id
        self.illust_id = illust_id
        self.controller = HomeController()

    def run(self):
        # try:
        #     # ⬅ Controller → Service → 传入 self.report_progress 回调
        #     self.controller.download(self.user_id, self.illust_id, self.report_progress)
        # except Exception as e:
        #     self.progress.emit(f"下载失败: {e}")
        #     raise RuntimeError
        self.controller.download(self.user_id, self.illust_id, self.report_progress)
        self.finished.emit()

    def report_progress(self, msg):
        self.progress.emit(msg)

    # def run(self):
    #     self.progress.emit("查询数据库中")
    #     get_info = GetInfo()
    #     userInfo = get_info(self.userID, self.illustID)
    #     logging.debug("DownloadThread: 获取信息: %s", userInfo)
    #     self.progress.emit("获取信息完成")

    #     # 下载
    #     downloader = Downloader()
    #     logging.debug("DownloadThread: 下载图片")
    #     self.progress.emit("准备下载图片")
    #     lastDownloadID = downloader.start(self.downloadProgess, userInfo)
    #     self.progress.emit("下载完成")

    #     # 插入数据库
    #     logging.debug("DownloadThread: 开始插入数据库")
    #     self.progress.emit("开始插入数据库")
    #     userInfo["lastDownloadID"] = lastDownloadID
    #     sqlConnector = SQLConnector()
    #     sqlConnector.insertByID(userInfo)
    #     self.progress.emit("插入数据库完成")

    #     # 返回信号
    #     logging.debug("DownloadThread: 返回信号")
    #     self.finished.emit()

    # def downloadProgess(self, value):
    #     self.progress.emit(value)