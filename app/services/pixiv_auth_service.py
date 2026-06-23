from app.utils.config_util import ConfigUtil


class PixivAuthService:
    def __init__(self):
        self.config = ConfigUtil()

    def get_pixiv_auth_token(self):
        settings = self.config.get_settings()
        return settings.get("refresh_token", "")

    def save_pixiv_auth_token(self, token):
        settings = self.config.get_settings()
        settings["refresh_token"] = token
        self.config.set_settings(settings)
