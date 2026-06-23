import logging
import re
from pathlib import Path

import requests

from app.utils.config_util import ConfigUtil

logger = logging.getLogger(__name__)


class SingleDownload:
    def __init__(self, download_path: Path | str | None = None):
        self.download_path = Path(download_path) if download_path is not None else Path()
        if download_path is None:
            self.load_settings()
        self.download_path.mkdir(parents=True, exist_ok=True)

    def __call__(self, user_name: str, user_id: str, url: str):
        return self.single_download(user_name, user_id, url)

    def single_download(self, user_name: str, user_id: str, url: str) -> bool:
        # 清理文件夹路径
        user_name = self.clean_path(user_name)
        # 判断画师文件夹是否存在
        # save_dir = os.path.join(self.downloadPath, userName + " - " + userID)
        save_dir = self.download_path / f"{user_name} - {user_id}"
        save_dir.mkdir(parents=True, exist_ok=True)

        file_name = url.split("/")[-1]  # 从 URL 中提取文件名
        # save_path = os.path.join(self.downloadPath, userName ,file_name)
        save_path = save_dir / file_name
        try:
            # 设置 HTTP 请求头（例如，对于 Pixiv 需要 Referer）
            headers = {
                "Referer": "https://www.pixiv.net/",
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                ),
            }

            # 发起 GET 请求
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()  # 检查是否请求成功

            # 保存文件
            with save_path.open("wb") as file:
                for chunk in response.iter_content(chunk_size=8192):  # 分块下载
                    file.write(chunk)
            logger.info("File saved to %s", save_path)
            return True

        except requests.exceptions.RequestException as e:
            logger.error("An error occurred while downloading %s: %s", url, e)
            return False

    def load_settings(self):
        config_util = ConfigUtil()
        settings = config_util.get_settings()
        self.download_path = Path(settings.get("download_path", ""))

    @property
    def downloadPath(self):
        return str(self.download_path)

    @downloadPath.setter
    def downloadPath(self, value):
        self.download_path = Path(value)

    def clean_path(self, path: str) -> str:
        # 移除非法字符
        return re.sub(r'[<>:"/\\|?*]', "", path)
