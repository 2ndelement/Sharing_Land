from fastapi import APIRouter, Depends
from pydantic import BaseModel, HttpUrl
from typing import List, Tuple, Optional
from api.utils import JwtFactory, Const, Dao
from api.depends import token_is_valid
import requests
import json

user_router = APIRouter(
    prefix='/api/user'
)


class LoginPostBody(BaseModel):
    """
    登录请求体模型
    """
    js_code: str
    avatar_url: HttpUrl
    nickname: str


class VerifyBody(BaseModel):
    """
    登录验证模型
    """
    js_code: str
    appid: str = Const.APPID
    secret: str = Const.APPSECRET
    grant_type: str = 'authorization_code'


class LandBody(BaseModel):
    """
    土地信息模型
    """
    description: str
    image_urls: Optional[List[HttpUrl]] = None
    positon: Tuple[float, float]


@user_router.post('/login')
async def user_login(login_body: LoginPostBody):
    """
    用户登录接口处理
    :param login_body:登录体
    :return:
    """
    vb = VerifyBody(js_code=login_body.js_code)
    response = requests.get(url=Const.verify_url, params=vb.dict())
    content: dict = json.loads(response.content.decode())
    if 'errcode' in content:
        return {'errcode': content.get('errcode'), 'errmsg': content.get('errmsg')}
    else:
        try:
            Dao.update_user(content.get('openid'), login_body.avatar_url, login_body.nickname)
        except Exception as e:
            return {'errcode': 500, 'errmsg': '服务器内部错误'}
        return {'errcode': 0, 'token': JwtFactory.generate_token_openid(content.get('openid'))}


@user_router.post('/postland')
async def post_land(land_body: LandBody, openid=Depends(token_is_valid)):
    description = land_body.description
    lng, lat = land_body.positon
    position = f'{lng};{lat}'
    image_urls = ''
    if land_body.image_urls:
        for url in land_body.image_urls:
            image_urls += url + ';'
        image_urls = image_urls[:-1]
    try:
        Dao.user_post_land(openid, description, position, image_urls)
        return {'errcode': 0}
    except Exception:
        return {'errcode': 500, 'errmsg': '服务器内部故障'}
