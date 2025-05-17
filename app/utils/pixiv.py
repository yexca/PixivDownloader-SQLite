from pixivpy3 import *
from app.utils.config_util import ConfigUtil
from app.utils.random_sleep import RandomSleep

class Pixiv():
    def __init__(self):
        self.api = AppPixivAPI()
        configUtil = ConfigUtil()
        settings = configUtil.getSettings()
        # self.refreshToken = settings.get("refresh_token", "")
        self.api.auth(refresh_token=settings.get("refresh_token", ""))
        # self.refreshToken = ""
        # self.__getToken()
        # self.api.auth(refresh_token=self.refreshToken)
        self.rand_sleep = RandomSleep()

    # def __getToken(self):
    #     # settings_path = os.path.join(os.getcwd(), "app", "resources", "conf", "settings.json")
    #     conf = Conf()
    #     self.refreshToken = conf.getRefreshRoken()

    def getInfoByIllustId(self, illustId):
        # self.api.auth(refresh_token=token)
        json_result = self.api.illust_detail(illustId)
        illust = json_result.illust
        return illust.user
    
    def getInfoByUserId(self, userID):
        # self.api.auth(refresh_token=token)
        json_result = self.api.user_detail(userID)
        return json_result.user

    # def getUserIDFromillustID(self, illustID: str) -> str:
    #     json_result = self.api.illust_detail(illustID)
    #     illust = json_result.illust
    #     userID = illust.user.id
        
    #     return userID
    
    # def getUsernameFromillustID(self, illustID: str) -> str:
    #     json_result = self.api.illust_detail(illustID)
    #     illust = json_result.illust
    #     username = illust.user.name
        
    #     return username
    
    # def getUsernameFromuserID(self, userID: str) -> str:
    #     json_result = self.api.user_detail(userID)
    #     # userInfo = json_result.user
    #     # username = userInfo.name
    #     logging.debug("Pixiv.getUsernameFromuserID: 获取用户名: %s", json_result.user.name)
    #     return json_result.user.name
    
    def getAllIllustFromUserID(self, userID: str):
        illusts = []
        # 参考: https://github.com/eggplants/pixiv-bulk-downloader/blob/eaf30d6f65fc2a1db7452e0cefee1c544e19bebe/pbd/base.py#L32-L85
        next_qs = {}
        while next_qs is not None:
            if next_qs == {}:
                json_result = self.api.user_illusts(userID)
            else:
                json_result = self.api.user_illusts(**next_qs)
            
            if "error" in json_result and "invalid_grant" in json_result["error"]["message"]:
                self.api.auth(refresh_token=self.refreshToken)
                continue

            for illust in json_result["illusts"]:
                illusts.append(illust)

            next_qs = self.api.parse_qs(json_result["next_url"])
            self.rand_sleep()
        return illusts
    
