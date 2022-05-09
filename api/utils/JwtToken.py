import jwt
from .Const import Const
from datetime import datetime


class JwtFactory:
    """
    此类操作JWT
    """
    _expire_message = dict(code=4000, msg="token 已经失效")
    _unknown_error_message = dict(code=4100, msg="token 解析失败")

    @classmethod
    def generate_token(cls, payload: dict) -> str:
        """
        通过payload生成一个token
        :param payload:payload dict
        :return: jwt_token
        """
        headers = dict(typ='jwt', alg='HS256')
        result = jwt.encode(payload=payload, key=Const.jwt_salt, algorithm='HS256', headers=headers)
        return result

    @classmethod
    def parse_token(cls, token: str) -> tuple[bool, dict]:
        """
        将token转换为payload,payload中取关键数据
        :param token:
        :return:
        """
        verify_status = False
        try:
            payload_data = jwt.decode(token, Const.jwt_salt, algorithms=['HS256'])
            verify_status = True
        except jwt.ExpiredSignatureError:
            payload_data = cls._expire_message
        except Exception as _err:
            payload_data = cls._unknown_error_message
        return verify_status, payload_data

    @classmethod
    def generate_token_openid(cls, openid: str) -> str:
        """
        通过openid生成token
        :param openid:用户的openid,待取出识别请求操作的用户
        :return:
        """
        payload = dict(openid=openid, exp=datetime.now() + Const.jwt_exp)
        return cls.generate_token(payload)
