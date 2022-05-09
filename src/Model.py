from pydantic import BaseModel
import Const


class VerifyBody(BaseModel):
    js_code: str
    appid: str = Const.APPID
    secret: str = Const.APPSECRET
    grant_type: str = 'authorization_code'
