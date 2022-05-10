import logging
from datetime import datetime

import pymysql
from .Const import Const


class Dao:
    """
    此类实现数据库操作
    """
    _db = None
    try:
        _db = pymysql.connect(**Const.DatabaseInfo().dict())
    except Exception as e:
        logging.error(e)
        exit(-1)
    _cursor = _db.cursor()

    @classmethod
    def update_user(cls, openid: str, avatar_url: str, nickname: str):
        """
        向数据库内更新用户信息
        :param openid: 小程序开发ID
        :param avatar_url: 用户头像链接
        :param nickname: 用户昵称
        :return:
        """
        try:
            cur = cls._cursor
            sql_is_exist_openid = f"select 1 " \
                                  f"from User " \
                                  f"where openid = '{openid}'" \
                                  f"limit 1"

            sql_insert_new_user = f"insert into User (openid, avatar_url, nickname)" \
                                  f"values ('{openid}', '{avatar_url}','{nickname}')"

            sql_update_user_info = f"update User " \
                                   f"set avatar_url = '{avatar_url}',nickname = '{nickname}'" \
                                   f"where openid = '{openid}'"

            cur.execute(sql_is_exist_openid)

            if cur.rowcount:
                cur.execute(sql_update_user_info)
            else:
                cur.execute(sql_insert_new_user)

            cls._db.commit()

        except Exception as e:
            logging.error(e)
            raise e

    @classmethod
    def user_post_land(cls, uid: int, description: str, position: str, image_urls: str, ):
        try:
            cur = cls._cursor
            create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if image_urls:
                image_urls = f"'{image_urls}'"
            else:
                image_urls = 'null'
            cur.execute(
                f"insert into Land(description, image_urls, uid, position, create_time) "
                f"values ('{description}',{image_urls},'{uid}','{position}','{create_time}')")
            cls._db.commit()
        except Exception as e:
            logging.error(e)
            raise e

    @classmethod
    def get_uid_by_openid(cls, openid: str) -> int:
        try:
            cur = cls._cursor
            cur.execute(f"select uid "
                        f"from User "
                        f"where openid= '{openid}'")
            if cur.rowcount:
                return 0
            else:
                return cur.fetchone()[0]
        except Exception as e:
            logging.error(e)
            raise e

    @classmethod
    def get_user_land_info(cls, uid: int):
        try:
            cur = cls._cursor
        except Exception as e:
            logging.error(e)
            raise e
