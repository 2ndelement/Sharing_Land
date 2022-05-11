from typing import Optional

from pydantic import BaseModel, HttpUrl

from api.utils import Const, list_to_str


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


class StrLandModel(BaseModel):
    description: Optional[str] = None
    image_urls: Optional[str] = None
    position: Optional[str] = None


class BaseLandBody(BaseModel):
    """
    土地信息模型
    """
    description: str
    image_urls: list[HttpUrl]
    position: tuple[float, float]

    def parse_str(self) -> StrLandModel:
        kargs = dict()
        if self.description:
            kargs['description'] = self.description
        if self.image_urls:
            kargs['image_urls'] = list_to_str(self.image_urls)
        if self.position:
            kargs['position'] = list_to_str(list(self.position))
        return StrLandModel(**kargs)


class CreateLandBody(BaseLandBody):
    image_urls: Optional[list[HttpUrl]] = None

    class Config:
        schema_extra = {
            "example": {
                'description': '测试用描述信息',
                'image_urls': ['http://127.0.0.1/image/1', 'http://127.0.0.1/image/2'],
                'position': [128.010101, 32.101010]
            }
        }


class ModifyLand(BaseLandBody):
    description: Optional[str] = None
    image_urls: Optional[list[HttpUrl]] = None
    position: Optional[tuple[float, float]] = None


class ModifyLandBody(BaseModel):
    lno: int
    land_info: ModifyLand


class CommentModel(BaseModel):
    content: str
    lno: int
