from fastapi import Header, HTTPException
from api.utils import JwtFactory, Const

example_token = "eyJ0eXAiOiJqd3QiLCJhbGciOiJIUzI1NiJ9" \
                ".eyJvcGVuaWQiOiJvR1JMMTRvQ0dpamZsb1BmaXdBRl9DQmlXRnJRIiwidWlkIjoxLCJleHAiOjE2NTI5MDc1OTJ9" \
                ".LmlpStnI2QTu70P-mSJGi4GDETjkOwBgXfnBwkndaLY "


async def token_is_valid(token: str = Header(..., example=example_token)):
    """
    判断token是否有效的依赖,debug状态不进行验证
    :param token: jwt_token
    :return:
    """
    if Const.debug:
        return {'openid': 'debug', 'uid': 'debug'}

    status, payload = JwtFactory.parse_token(token)

    if status:
        return dict(openid=payload.get('openid'), uid=payload.get('uid'))
    else:
        raise HTTPException(
            status_code=401,
            detail='token is invalid',
        )
