from app.services.home_service import HomeService

class HomeController:
    def __init__(self):
        self.service = HomeService()
    
    def download(self, userId, illustId, reportProgress):
        self.service.download(userId, illustId, reportProgress)