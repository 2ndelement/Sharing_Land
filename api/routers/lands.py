from typing import Optional, List, Tuple

from fastapi import APIRouter, Depends
from pydantic import HttpUrl, BaseModel

from api.depends import token_is_valid
from api.utils import Dao

land_router = APIRouter(
    prefix='/api/land'
)


class LandBody(BaseModel):
    """
    土地信息模型
    """
    description: str
    image_urls: Optional[List[HttpUrl]] = None
    position: Tuple[float, float]


class ModifyLandBody(BaseModel):
    description: Optional[str] = None
    image_urls: Optional[List[HttpUrl]] = None
    position: Optional[Tuple[float, float]] = None


@land_router.post('/create')
async def create_land(land_body: LandBody, common: dict = Depends(token_is_valid)):
    description = land_body.description
    lng, lat = land_body.position
    position = f'{lng};{lat}'
    image_urls = ''
    if land_body.image_urls:
        for url in land_body.image_urls:
            image_urls += url + ';'
        image_urls = image_urls[:-1]
    try:
        Dao.user_post_land(common.get('uid'), description, position, image_urls)
        return {'errcode': 0}
    except Exception:
        return {'errcode': 500, 'errmsg': '服务器内部故障'}


@land_router.get('/query')
async def query_land(uid: Optional[int] = None, common: dict = Depends(token_is_valid)):
    if uid:
        result = Dao.get_user_land_info(uid)
    else:
        result = Dao.get_user_land_info(common.get('uid'))
    return result
