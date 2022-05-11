"""
图片类接口路由
"""
import os
import re
from datetime import datetime

from fastapi import APIRouter, UploadFile, File, Depends, Path, HTTPException
from fastapi.responses import FileResponse

from api.depends import token_is_valid
from api.utils import Const, ResponseDict, ErrorCode

upload_router = APIRouter(
    prefix='/api/image'
)


@upload_router.post('/upload')
async def image_upload(file: UploadFile = File(...), common: dict = Depends(token_is_valid)):
    """
    上传图片
    :param file: 上传的图片文件
    :param common: 此处无用仅来验证token,包含openid,uid
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
            return ResponseDict(ErrorCode.success,
                                url=f'http://{Const.HOST}:{Const.PORT}/api/image/download/{filename}')
        except Exception:
            return ResponseDict(ErrorCode.internal_errors)


@upload_router.get('/download/{image_name}')
async def image_download(image_name: str = Path(...)):
    """
    下载图片
    :param image_name:待下载的图片名称
    :return: StreamingResponse 文件流
    """
    try:
        image_path = os.path.join(Const.image_save_dir, image_name)
        return FileResponse(image_path)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="找不到文件"
        )
