import logging
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
            sql_is_exist_openid = f'''select 1 from User
                      where openid = '{openid}'
                      limit 1
            '''
            sql_insert_new_user = f'''insert into User (openid, avatar_url, nickname)
                       values ('{openid}', '{avatar_url}','{nickname}')
            '''
            sql_update_user_info = f'''update User 
                       set avatar_url = '{avatar_url}',nickname = '{nickname}'
                       where openid = '{openid}'
            '''

            cur.execute(sql_is_exist_openid)

            if cur.rowcount:
                cur.execute(sql_update_user_info)
            else:
                cur.execute(sql_insert_new_user)

            cls._db.commit()

        except Exception as e:
            logging.error(e)
            raise e
