from fastapi import Header, HTTPException
from api.utils import JwtFactory, Const


async def token_is_valid(token: str = Header(...)):
    if Const.debug:
        return 'debug'
    status, payload = JwtFactory.parse_token(token)
    if status:
        return {'openid': payload.get('openid')}
    else:
        raise HTTPException(
            status_code=401,
            detail='token is invalid',
        )
