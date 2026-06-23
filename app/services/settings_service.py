from app.utils.config_util import ConfigUtil


class SettingsService:
    def __init__(self):
        self.config = ConfigUtil()

    def get_settings(self):
        return self.config.get_settings()

    def save_settings(self, settings):
        self.config.set_settings(settings)
