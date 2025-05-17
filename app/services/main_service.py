from app.utils.config_loader import load_app_config
from app.utils.config_util import ConfigUtil

class MainService:
    def __init__(self):
        self.config = load_app_config()
        self.configUtil = ConfigUtil()

    def get_app_name(self):
        return self.config["app"]["name"]

    def get_app_version(self):
        return self.config["app"]["version"]
    
    def get_background_image(self):
        return self.configUtil.getBackgroundImage()
