from typing import Optional, List, Tuple

from fastapi import APIRouter, Depends
from pydantic import HttpUrl, BaseModel

from api.depends import token_is_valid
from api.utils import Dao

land_router = APIRouter(
    prefix='/api/land'
)


class StrLandModel(BaseModel):
    description: Optional[str] = None
    image_urls: Optional[str] = None
    position: Optional[str] = None


class BaseLandBody(BaseModel):
    """
    土地信息模型
    """
    description: str
    image_urls: List[HttpUrl]
    position: Tuple[float, float]

    def parse_str(self) -> StrLandModel:
        kargs = dict()
        if self.description:
            kargs['description'] = self.description
        if self.image_urls:
            image_urls = ''
            for url in self.image_urls:
                image_urls += url + ','
            kargs['image_urls'] = image_urls.strip(',')

        if self.position:
            lng, lat = self.position
            position = f'{lng};{lat}'
            kargs['position'] = position
        return StrLandModel(**kargs)


class CreateLandBody(BaseLandBody):
    image_urls: Optional[List[HttpUrl]] = None


class ModifyLand(BaseLandBody):
    description: Optional[str] = None
    image_urls: Optional[List[HttpUrl]] = None
    position: Optional[Tuple[float, float]] = None


class ModifyLandBody(BaseModel):
    lno: int
    land_info: ModifyLand


@land_router.post('/create')
async def create_land(land_body: CreateLandBody, common: dict = Depends(token_is_valid)):
    str_land_body = land_body.parse_str()
    try:
        Dao.user_post_land(common.get('uid'), **str_land_body.dict())
        return {'errcode': 0, 'errmsg': ''}
    except Exception:
        return {'errcode': 500, 'errmsg': '服务器内部故障'}


@land_router.get('/query/user/{uid}')
async def query_land(uid: Optional[int] = None, common: dict = Depends(token_is_valid)):
    try:
        if uid:
            result = Dao.get_user_land_info(uid)
        else:
            result = Dao.get_user_land_info(common.get('uid'))
        return dict(errcode=0, land_info=result, errmsg='')
    except Exception:
        return dict(errcode=500, errmsg='服务器内部故障')


# TODO:待完成
@land_router.post('/modify')
async def modify_land(land_body: ModifyLandBody, common: dict = Depends(token_is_valid)):
    lno = land_body.lno
    land_info = land_body.land_info.parse_str()
    try:
        Dao.modify_land_info(lno, common.get('uid'), **land_info.dict())
        return {'errcode': 0, 'errmsg': ''}
    except PermissionError:
        return {'errcode': 400, 'errmsg': '不能修改别人的土地信息'}
    except Exception:
        return {'errcode': 500, 'errmsg': '服务器内部故障'}


# TODO:待完成
@land_router.delete('/delete/{lno}')
async def delete_land(lno: int, common: dict = Depends(token_is_valid)):
    pass


# TODO:待完成
@land_router.get('/close/{lno}')
async def close_land(lno: int, common: dict = Depends(token_is_valid)):
    pass
