from datetime import timedelta

from pydantic import BaseModel

from api.Config import getConfig

import os


class Const:
    APPID = 'wxdad1820020c9cc36'
    APPSECRET = '3afd0028787d74fc40982d8584e741e7'
    HOST = '127.0.0.1'
    PORT = 8000
    PUBLIC_HOST = '0.0.0.0'
    jwt_salt = '$Dt+6aeY%YeYtE!9Q'
    jwt_exp = timedelta(days=7)
    verify_url = 'https://api.weixin.qq.com/sns/jscode2session'
    image_save_dir = getConfig('savedir', 'imagedir')
    debug = eval(getConfig('debug', 'debug').capitalize())

    class DatabaseInfo(BaseModel):
        host: str = getConfig('database', 'dbhost')
        db: str = getConfig('database', 'dbname')
        user: str = getConfig('database', 'dbuser')
        password: str = getConfig('database', 'dbpassword')
        port: int = int(getConfig('database', 'dbport'))
