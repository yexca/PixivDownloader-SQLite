from app.services.settings_service import SettingsService

class SettingsController:
    def __init__(self):
        self.service = SettingsService()

    def get_settings(self):
        return self.service.get_settings()

    def save_settings(self, settings):
        self.service.save_settings(settings)