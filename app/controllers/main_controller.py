from app.services.main_service import MainService

class MainController:
    def __init__(self):
        self.service = MainService()
    def get_app_name(self):
        return self.service.get_app_name()
    def get_app_version(self):
        return self.service.get_app_version()
    def get_background_image(self):
        return self.service.get_background_image()