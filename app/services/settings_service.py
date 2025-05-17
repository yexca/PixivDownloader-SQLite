from app.utils.config_util import ConfigUtil

class SettingsService:
    def __init__(self):
        self.config = ConfigUtil()

    def get_settings(self):
        return self.config.getSettings()
    
    def save_settings(self, settings):
        self.config.setSettings(settings)