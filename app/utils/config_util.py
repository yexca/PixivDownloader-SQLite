import os
import json
import logging

class ConfigUtil:
    def __init__(self):
        # Example: Define application settings
        # self.APP_NAME = "PixivDwonloader"
        # self.VERSION = "1.3"

        # Paths
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        RESOURCES_DIR = os.path.join(BASE_DIR, "..", "..", "resources")

        self.SETTING_PATH = os.path.join(RESOURCES_DIR, 'conf', 'settings.json')
        # self.QSS_PATH = os.path.join(RESOURCES_DIR, 'stylesheets', 'main.qss')

        self.BGIMG = os.path.join(RESOURCES_DIR, 'images', 'background.png')
        self.ICON = os.path.join(RESOURCES_DIR, 'icon.ico')
        
    def getSettings(self):
        try:
            with open(self.SETTING_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            logging.debug(f"Setting file not found at {self.SETTING_PATH}")
        except json.JSONDecodeError:
            logging.debug("Error decoding the settings file.")

    def getBackgroundImage(self):
        return self.BGIMG
    def getIcon(self):
        return self.ICON

    # def getDownloadPath(self):
    #     settings = self.getSettings()
    #     return settings.get("download_path", "")

    def setSettings(self, settings):
        try:
            with open(self.SETTING_PATH, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logging.debug(f"Error savinf file: {e}")