from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl
from api.utils import JwtFactory, Const, Dao
import requests
import json

user_router = APIRouter(
    prefix='/api/user'
)


class LoginPostBody(BaseModel):
    js_code: str
    avatar_url: HttpUrl
    nickname: str


class VerifyBody(BaseModel):
    js_code: str
    appid: str = Const.APPID
    secret: str = Const.APPSECRET
    grant_type: str = 'authorization_code'


@user_router.post('/login')
async def user_login(login_body: LoginPostBody):
    vb = VerifyBody(js_code=login_body.js_code)
    response = requests.get(url=Const.verify_url, params=vb.dict())
    content: dict = json.loads(response.content.decode())
    if 'errcode' in content:
        return {'errcode': content.get('errcode'), 'errmsg': content.get('errmsg')}
    else:
        Dao.update_user(content.get('openid'), login_body.avatar_url, login_body.nickname)
        return {'errcode': 0, 'token': JwtFactory.generate_token_openid(content.get('openid'))}
