import logging
from datetime import datetime
from typing import Optional

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
    def user_post_land(cls, uid: int, description: str, position: str, image_urls: Optional[str] = None, ):
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
        """
        通过openid查询uid,不存在则返回0
        :param openid:
        :return:
        """
        try:
            cur = cls._cursor
            cur.execute(f"select uid "
                        f"from User "
                        f"where openid= '{openid}'")
            if cur.rowcount:
                return cur.fetchone()[0]
            else:
                return 0
        except Exception as e:
            logging.error(e)
            raise e

    @classmethod
    def get_user_land_info(cls, uid: int) -> list:
        try:
            cur = cls._cursor
            # todo: 查询指定用户的发布土地信息,
            #  构建为[{key1:value,key2:[value1,value2]},{}]类似的形式返回
            #  例:[{
            #  'lno':1,
            #  'description':'喜欢我的地吗',
            #  'image_urls':[url1,url2],
            #  'position':[lng,lat]
            #  'create_time': '2022-05-10 10:10:01'
            #  },{
            #  'lno':2,
            #  'description':'喜欢我的地吗',
            #  'image_urls':[url1],
            #  'position':[lng,lat]
            #  'create_time': '2022-05-10 10:10:02'
            #  'modify_time': '2022-05-10 10:10:03'
            #  },
            #  ]
        except Exception as e:
            logging.error(e)
            raise e

    @classmethod
    def modify_land_info(cls, lno: int, uid: int, **kargs):
        sql = "update Land set "
        for k, v in kargs.items():
            if v is not None:
                sql += f"{k} = '{v}',"
        sql = sql.strip(',')
        sql += f"where lno = {lno} and uid = {uid}"
        cur = cls._cursor
        try:
            rows = cur.execute(sql)
            if rows == 0:
                raise PermissionError
            cls._db.commit()
        except Exception as e:
            logging.error(e)
            raise e
