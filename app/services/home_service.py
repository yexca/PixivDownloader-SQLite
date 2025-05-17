from app.models.pixiv_model import PixivModel
from app.utils.pixiv import Pixiv
from app.utils.random_sleep import RandomSleep
from app.utils.single_download import SingleDownload
# from app.utils.config_util import ConfigUtil
import logging

class HomeService:
    def __init__(self):
        self.model = PixivModel()
        self.pixivUtil = Pixiv()
        # configUtil = ConfigUtil()
        # settings = configUtil.getSettings()
        # self.token = settings.get("refresh_token", "")
        self.rand_sleep = RandomSleep()
        self.single_download = SingleDownload()
        self.downloadLink = []

    def download(self, userId, illustId, reportProgress):
        # 获取画师信息
        reportProgress("获取画师信息中")

        try:
            if userId:
                # 如果是 userId 从数据库查找信息
                userInfo = self._fetch_userInfo_from_userId(userId)
            elif illustId:
                # 如果是 illustId 获取画师信息
                userInfo = self._fetch_userInfo_from_illustId(illustId)
        except RuntimeError as e:
            raise RuntimeError(f"获取信息出错: {e}")

        reportProgress("获取画师信息完成，获取作品信息中")

        # 下载
        illusts = self.pixivUtil.getAllIllustFromUserID(userInfo["ID"])

        # 获取下载链接
        reportProgress("获取作品信息完成，获取下载链接中")
        for illust in illusts:
            self._get_download_link(illust)

        # 下载
        lastDownloadID = self._download(userInfo, reportProgress)
        reportProgress("下载完成，插入数据库中")

        # 插入数据库
        userInfo["lastDownloadID"] = lastDownloadID
        self.model.insertById(userInfo)

        # 返回完成信号
        reportProgress("插入数据库完成")
        
    def _fetch_userInfo_from_userId(self, userId):
        userInfo = self.model.getInfoByID(userId)
        if userInfo:
            return userInfo
        else:
            info = self.pixivUtil.getInfoByUserId(userId)
            userInfo = {}
            userInfo["ID"] = userId
            userInfo["name"] = info.name
            return userInfo
    
    def _fetch_userInfo_from_illustId(self, illustId):
        illustInfo = self.pixivUtil.getInfoByIllustId(illustId)
        userInfo = self.model.getInfoByID(illustInfo.id)
        if userInfo:
            return userInfo
        else:
            userInfo = {}
            userInfo["ID"] = illustInfo.id
            userInfo["name"] = illustInfo.name
            return userInfo
        
    def _get_download_link(self, illust):
        if illust.meta_single_page.original_image_url:
            logging.debug("HomeService.getDownloadLink: 单个图片")
            self.downloadLink.append(illust.meta_single_page.original_image_url)
        elif illust.meta_pages:
            logging.debug("HomeService.getDownloadLink: 多个图片")
            for urls in illust.meta_pages:
                self.downloadLink.append(urls.image_urls.original)

    def _download(self, userInfo, reportProgress):
        # 报告进度
        total = len(self.downloadLink)
        i = 1
        lastDownloadID = 0

        if userInfo["lastDownloadID"]:
            lastDownloadID = userInfo["lastDownloadID"]
            logging.debug("Downloader.downloader: 数据库有记录")
            for url in self.downloadLink:
                # 报告进度
                reportProgress(f"正在下载第 {i} 张, 共 {total} 张")
                i += 1

                currentDownloadID = int(url.split("/")[-1].split("_")[0])
                if currentDownloadID <= int(userInfo["lastDownloadID"]):
                    logging.info("这张图片已经下载过了: %s", currentDownloadID)
                    continue
                self.rand_sleep()
                logging.info("正在下载: %s", currentDownloadID)
                self.single_download(userInfo["name"], userInfo["ID"], url)
                if lastDownloadID < currentDownloadID:
                    lastDownloadID = currentDownloadID
        else:
            logging.debug("Downloader.downloader: 数据库无记录")
            for url in self.downloadLink:
                # 报告进度
                reportProgress(f"正在下载 {i}, 一共 {total}")
                i += 1

                self.rand_sleep()
                currentDownloadID = int(url.split("/")[-1].split("_")[0])
                logging.info("正在下载: %s", currentDownloadID)
                self.single_download(userInfo["name"], userInfo["ID"], url)
                if lastDownloadID < currentDownloadID:
                    lastDownloadID = currentDownloadID
        return str(lastDownloadID)