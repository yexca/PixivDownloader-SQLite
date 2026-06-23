import json
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

RESOURCES_DIR = BASE_DIR / "resources"
SETTINGS_PATH = RESOURCES_DIR / "conf" / "settings.json"
BACKGROUND_IMAGE_PATH = RESOURCES_DIR / "images" / "background.png"
ICON_PATH = RESOURCES_DIR / "icon.ico"


class ConfigUtil:
    def __init__(self, settings_path: Path | str | None = None):
        # Example: Define application settings
        # self.APP_NAME = "PixivDwonloader"
        # self.VERSION = "1.3"
        self.settings_path = Path(settings_path) if settings_path is not None else SETTINGS_PATH
        self.background_image_path = BACKGROUND_IMAGE_PATH
        self.icon_path = ICON_PATH

    def get_settings(self):
        try:
            return json.loads(self.settings_path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            logger.debug("Setting file not found at %s", self.settings_path)
            return {}
        except json.JSONDecodeError:
            logger.debug("Error decoding the settings file.")
            return {}

    def get_background_image(self):
        return str(self.background_image_path)

    def get_icon(self):
        return str(self.icon_path)

    # def getDownloadPath(self):
    #     settings = self.getSettings()
    #     return settings.get("download_path", "")

    def set_settings(self, settings):
        try:
            self.settings_path.parent.mkdir(parents=True, exist_ok=True)
            self.settings_path.write_text(
                json.dumps(settings, indent=4, ensure_ascii=False),
                encoding="utf-8",
            )
        except OSError:
            logger.exception("Error saving settings file")

    def getSettings(self):
        return self.get_settings()

    def getBackgroundImage(self):
        return self.get_background_image()

    def getIcon(self):
        return self.get_icon()

    def setSettings(self, settings):
        self.set_settings(settings)
