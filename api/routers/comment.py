from typing import Optional

from fastapi import APIRouter, Depends, Path

from api.depends import token_is_valid
from api.models import CommentModel
from api.utils import Dao, ResponseDict, ErrorCode

comment_router = APIRouter(
    prefix='/api/comment'
)


@comment_router.post('/post')
def post_comment(comment: CommentModel, common: dict = Depends(token_is_valid)):
    content = comment.content
    lno = comment.lno
    uid = common['uid']
    try:
        Dao.user_post_comment(lno, uid, content)
        return ResponseDict(ErrorCode.success)
    except PermissionError:
        return ResponseDict(ErrorCode.permisson_forbidden, msg='土地不存在')
    except Exception:
        return ResponseDict(ErrorCode.internal_errors)


@comment_router.delete('/delete/{cno}')
def delete_comment(cno: int = Path(...), common: dict = Depends(token_is_valid)):
    uid = common['uid']
    try:
        Dao.delete_comment(cno, uid)
        return ResponseDict(ErrorCode.success)
    except PermissionError:
        return ResponseDict(ErrorCode.permisson_forbidden)
    except Exception:
        return ResponseDict(ErrorCode.internal_errors)


@comment_router.get('/query/land/{lno}')
def query_land_comment(lno: int = Path(...), common: dict = Depends(token_is_valid)):
    return Dao.query_land_comment(lno)
