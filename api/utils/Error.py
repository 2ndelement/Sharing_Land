from enum import Enum
from typing import Optional


class ErrorCode(tuple[int, str], Enum):
    success = 0, '操作成功'
    permisson_forbidden = 300, '权限拒绝'
    login_failure = 400, '登录失败'
    internal_errors = 500, '服务器内部错误'


class ResponseDict(dict):

    def __init__(self, errcode: ErrorCode, msg: Optional[str] = None, **kargs):
        super().__init__(errcode=errcode.value[0], errmsg=errcode.value[1], **kargs)
        if msg:
            self['errmsg'] = msg

