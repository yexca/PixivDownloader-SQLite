from app.services.home_service import HomeService


class HomeController:
    def __init__(self):
        self.service = HomeService()

    def download(self, user_id, illust_id, report_progress):
        self.service.download(user_id, illust_id, report_progress)
