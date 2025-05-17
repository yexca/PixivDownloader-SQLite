from app.services.pixiv_auth_service import PixivAuthService

class PixivAuthController:
    def __init__(self):
        self.service = PixivAuthService()
    
    def get_pixiv_auth_token(self):
        return self.service.get_pixiv_auth_token()
    
    def save_pixiv_auth_token(self, token):
        self.service.save_pixiv_auth_token(token)