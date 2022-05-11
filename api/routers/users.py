from fastapi import APIRouter, Depends
from api.models import LoginPostBody, VerifyBody
from api.utils import JwtFactory, Const, Dao, ResponseDict, ErrorCode
import requests
import json

user_router = APIRouter(
    prefix='/api/user'
)


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
        return ResponseDict(ErrorCode.login_failure)
    else:
        try:
            openid = content.get('openid')
            Dao.update_user(openid, login_body.avatar_url, login_body.nickname)
            uid = Dao.get_uid_by_openid(openid)
            return ResponseDict(ErrorCode.success, token=JwtFactory.generate_token_openid_uid(openid, uid))
        except Exception as e:
            return ResponseDict(ErrorCode.internal_errors)
