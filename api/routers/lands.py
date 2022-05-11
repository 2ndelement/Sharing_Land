from typing import Optional

from fastapi import APIRouter, Depends

from api.depends import token_is_valid
from api.models import CreateLandBody, ModifyLandBody
from api.utils import Dao, ResponseDict, ErrorCode

land_router = APIRouter(
    prefix='/api/land'
)


@land_router.post('/create')
async def create_land(land_body: CreateLandBody, common: dict = Depends(token_is_valid)):
    str_land_body = land_body.parse_str()
    return Dao.user_post_land(common.get('uid'), **str_land_body.dict())


@land_router.get('/query/user/{uid}')
async def query_land(uid: Optional[int] = None, common: dict = Depends(token_is_valid)):
    close_enabled = False
    if not uid:
        close_enabled = True
        uid = common.get('uid')
    return Dao.get_user_land_info(uid, close_enabled=close_enabled)


# TODO:待完成
@land_router.post('/modify')
async def modify_land(land_body: ModifyLandBody, common: dict = Depends(token_is_valid)):
    lno = land_body.lno
    land_info = land_body.land_info.parse_str()
    return Dao.modify_land_info(lno, common.get('uid'), **land_info.dict())


# TODO:待完成
@land_router.delete('/delete/{lno}')
async def delete_land(lno: int, common: dict = Depends(token_is_valid)):
    uid = common['uid']
    return Dao.delete_land(lno, uid)


# TODO:待完成
@land_router.get('/change_close/{lno}')
async def change_close_land(lno: int, common: dict = Depends(token_is_valid)):
    uid = common['uid']
    return Dao.change_close_land(lno, uid)
