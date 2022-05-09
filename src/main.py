from fastapi import FastAPI

import requests as rq
import json
from JwtToken import JwtFactory
import Const
from Model import VerifyBody

app = FastAPI()


@app.get('/api/login')
async def user_login(js_code: str):
    vb = VerifyBody(js_code=js_code)
    response = rq.get(url=Const.verify_url, params=vb.dict())
    content: dict = json.loads(response.content.decode())
    print(content)
    if 'errcode' in content:
        return {'errcode': content.get('errcode'), 'errmsg': content.get('errmsg')}
    else:
        return {'errcode': 0, 'token': JwtFactory.generate_token_openid(content.get('openid'))}
