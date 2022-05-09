"""
图片类接口路由
"""
import os
import re
from datetime import datetime

from fastapi import APIRouter, UploadFile, File, Depends, Path, HTTPException
from fastapi.responses import StreamingResponse

from api.depends import token_is_valid
from api.utils import Const

upload_route = APIRouter(
    prefix='/api/image'
)


@upload_route.post('/upload')
async def image_upload(file: UploadFile = File(...), openid: str = Depends(token_is_valid)):
    """
    上传图片
    :param file: 上传的图片文件
    :param openid: 此处无用仅来验证token
    :return:
    """
    filename = file.filename
    temp = filename.split('.')
    if temp[-1] not in ['png', 'jpg']:
        return {'errcode': 400, 'errmsg': '图片格式不支持'}
    else:
        try:
            filename = re.sub(r'\D', '', str(datetime.now())) + '.' + temp[-1]
            save_path = os.path.join(Const.image_save_dir, filename)
            res = await file.read()
            with open(save_path, 'wb') as f:
                f.write(res)
                f.close()
            return {'errcode:': 0,
                    'url': f'http://{Const.HOST}:{Const.PORT}/api/image/download/{filename}'}
        except Exception:
            return {'errcode': 400, 'errmsg': '未知错误'}


@upload_route.get('/download/{image_name}')
async def image_download(image_name: str = Path(...)):
    """
    下载图片
    :param image_name:待下载的图片名称
    :return: StreamingResponse 文件流
    """
    try:
        image_path = os.path.join(Const.image_save_dir, image_name)
        image = open(image_path, mode='rb')
        response = StreamingResponse(image, media_type='image/' + image_name.split('.')[-1])
        return response
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="找不到文件"
        )
