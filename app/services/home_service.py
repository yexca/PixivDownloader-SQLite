import logging

from app.models.pixiv_model import PixivModel
from app.utils.pixiv import Pixiv
from app.utils.random_sleep import RandomSleep
from app.utils.single_download import SingleDownload

# from app.utils.config_util import ConfigUtil

logger = logging.getLogger(__name__)


class HomeService:
    def __init__(self):
        self.model = PixivModel()
        self.pixiv_util = Pixiv()
        # configUtil = ConfigUtil()
        # settings = configUtil.getSettings()
        # self.token = settings.get("refresh_token", "")
        self.rand_sleep = RandomSleep()
        self.single_download = SingleDownload()
        self.download_link = []

    def download(self, user_id, illust_id, report_progress):
        # 获取画师信息
        report_progress("Getting user info...")

        try:
            if user_id:
                # 如果是 userId 从数据库查找信息
                user_info = self._fetch_user_info_from_user_id(user_id)
            elif illust_id:
                # 如果是 illustId 获取画师信息
                user_info = self._fetch_user_info_from_illust_id(illust_id)
        except RuntimeError as e:
            raise RuntimeError(f"获取信息出错: {e}") from e

        report_progress("Got user info. Getting artworks info...")

        # 下载
        illusts = self.pixiv_util.get_all_illust_from_user_id(user_info["ID"])

        # 获取下载链接
        report_progress("Got artworks info. Getting download links...")
        for illust in illusts:
            self._get_download_link(illust)

        # 下载
        last_download_id = self._download(user_info, report_progress)
        report_progress("Download completed, Inserting database...")

        # 插入数据库
        user_info["lastDownloadID"] = last_download_id
        self.model.insert_by_id(user_info)

        # 返回完成信号
        report_progress("Inserted database")

    def _fetch_user_info_from_user_id(self, user_id):
        user_info = self.model.get_info_by_id(user_id)
        if user_info:
            return user_info
        info = self.pixiv_util.get_info_by_user_id(user_id)
        user_info = {}
        user_info["ID"] = user_id
        user_info["name"] = info.name
        return user_info

    def _fetch_user_info_from_illust_id(self, illust_id):
        illust_info = self.pixiv_util.get_info_by_illust_id(illust_id)
        user_info = self.model.get_info_by_id(illust_info.id)
        if user_info:
            return user_info
        user_info = {}
        user_info["ID"] = illust_info.id
        user_info["name"] = illust_info.name
        return user_info

    def _get_download_link(self, illust):
        if illust.meta_single_page.original_image_url:
            logger.debug("HomeService.getDownloadLink: 单个图片")
            self.download_link.append(illust.meta_single_page.original_image_url)
        elif illust.meta_pages:
            logger.debug("HomeService.getDownloadLink: 多个图片")
            for urls in illust.meta_pages:
                self.download_link.append(urls.image_urls.original)

    def _download(self, user_info, report_progress):
        # 报告进度
        total = len(self.download_link)
        i = 1
        last_download_id = 0

        if "lastDownloadID" in user_info:
            last_download_id = int(user_info["lastDownloadID"])
            logger.debug("Downloader.downloader: 数据库有记录")
            for url in self.download_link:
                # 报告进度
                report_progress(f"Downloading NO. {i}, Total: {total}")
                i += 1

                current_download_id = int(url.split("/")[-1].split("_")[0].split("-")[0])
                if current_download_id <= int(user_info["lastDownloadID"]):
                    logger.info("这张图片已经下载过了: %s", current_download_id)
                    continue
                self.rand_sleep()
                logger.info("正在下载: %s", current_download_id)
                self.single_download(user_info["name"], user_info["ID"], url)
                if last_download_id < current_download_id:
                    last_download_id = current_download_id
        else:
            logger.debug("Downloader.downloader: 数据库无记录")
            for url in self.download_link:
                # 报告进度
                report_progress(f"Downloading NO. {i}, Total: {total}")
                i += 1

                self.rand_sleep()
                current_download_id = int(url.split("/")[-1].split("_")[0].split("-")[0])
                logger.info("正在下载: %s", current_download_id)
                self.single_download(user_info["name"], user_info["ID"], url)
                if last_download_id < current_download_id:
                    last_download_id = current_download_id
        return str(last_download_id)

    @property
    def pixivUtil(self):
        return self.pixiv_util

    @pixivUtil.setter
    def pixivUtil(self, value):
        self.pixiv_util = value

    @property
    def downloadLink(self):
        return self.download_link

    @downloadLink.setter
    def downloadLink(self, value):
        self.download_link = value
