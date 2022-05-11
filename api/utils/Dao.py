import logging
from datetime import datetime
from typing import Optional

import pymysql

from .Annotation import output_response, common_response
from .Parse import str_to_list
from .Const import Const


def ctime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


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
            raise e

    @classmethod
    @common_response()
    def user_post_land(cls, uid: int, description: str, position: str, image_urls: Optional[str] = None):
        try:
            cur = cls._cursor
            if image_urls:
                image_urls = f"'{image_urls}'"
            else:
                image_urls = 'null'
            cur.execute(
                f"insert into Land(description, image_urls, uid, position, create_time) "
                f"values ('{description}',{image_urls},'{uid}','{position}','{ctime()}')")
            cls._db.commit()
        except Exception as e:
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
            raise e

    @classmethod
    @output_response('land_info')
    def get_user_land_info(cls, uid: int, close_enabled: bool = False) -> list:
        try:
            fields = ['lno', 'description', 'image_urls', 'position', 'create_time', 'modify_time']
            cur = cls._cursor
            sql = f"select lno, description, image_urls, position, create_time, modify_time " \
                  f"from Land " \
                  f"where uid = {uid} "
            if not close_enabled:
                sql += 'and close = 0'
            rowcount = cur.execute(sql)
            if not rowcount:
                raise PermissionError
            land_infos = list()
            for row in cur.fetchall():
                land_info = dict()
                for i in range(len(row)):
                    land_info[fields[i]] = row[i]
                if land_info['image_urls']:
                    land_info['image_urls'] = str_to_list(land_info['image_urls'], str)
                land_info['position'] = str_to_list(land_info['position'], float)
                land_infos.append(land_info)
            return land_infos
        except Exception as e:
            raise e

    @classmethod
    @common_response()
    def modify_land_info(cls, lno: int, uid: int, **kargs):
        sql = f"update Land set modify_time = '{ctime()}',"
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
            raise e

    @classmethod
    @common_response()
    def delete_land(cls, lno: int, uid: int):
        cur = cls._cursor
        verify_sql = f"select 1 from Land where lno = {lno} and uid = {uid} limit 1"
        try:
            cur.execute(verify_sql)
            if not cur.rowcount:
                raise PermissionError
            delete_comment_sql = f"delete from comment where lno = {lno}"
            cur.execute(delete_comment_sql)
            delete_land_sql = f"delete from land where lno = {lno}"
            cur.execute(delete_land_sql)
            cls._db.commit()
        except Exception as e:
            raise e

    @classmethod
    @common_response()
    def change_close_land(cls, lno: int, uid: int):
        cur = cls._cursor
        verify_sql = f"select 1 from Land where lno = {lno} and uid = {uid} limit 1"
        try:
            cur.execute(verify_sql)
            if not cur.rowcount:
                raise PermissionError
            close_land_sql = f"update land set close = !close where lno = {lno}"
            cur.execute(close_land_sql)
            cls._db.commit()
        except Exception as e:
            raise e

    @classmethod
    def user_post_comment(cls, lno: int, uid: int, content: str):
        cur = cls._cursor
        verify_sql = f"select 1 from land where lno = {lno}"
        comment_sql = f"insert into Comment(lno,uid,content,post_time) " \
                      f"values ({lno},{uid},'{content}','{ctime()}') "
        try:
            cur.execute(verify_sql)
            if not cur.rowcount:
                raise PermissionError
            cur.execute(comment_sql)
            cls._db.commit()
        except Exception as e:
            raise e

    @classmethod
    def delete_comment(cls, cno: int, uid: int):
        cur = cls._cursor
        try:
            sum_rowcount = 0
            verify_sql = f"select 1 from comment where cno = {cno} and uid = {uid} limit 1"
            sum_rowcount += cur.execute(verify_sql)
            verify_sql = f"select 1 from land where lno in (select lno from comment where cno = {cno}) limit 1"
            sum_rowcount += cur.execute(verify_sql)
            if not sum_rowcount:
                raise PermissionError
            delete_comment_sql = f"delete from comment where cno = {cno}"
            cur.execute(delete_comment_sql)
            cls._db.commit()
        except Exception as e:
            raise e

    @classmethod
    @output_response('comment_info')
    def query_land_comment(cls, lno):
        try:
            cur = cls._cursor
            verify_sql = f"select 1 from land where lno = {lno} limit 1"
            cur.execute(verify_sql)
            if not cur.rowcount:
                raise PermissionError
            query_sql = f"select cno,content,user.uid,avatar_url,nickname " \
                        f"from comment,user " \
                        f"where comment.lno = {lno} " \
                        f"and comment.uid = user.uid"
            cur.execute(query_sql)
            comment_infos = list()
            for cno, content, uid, avatar_url, nickname in cur.fetchall():
                comment_info = dict(cno=cno, content=content, uid=uid, avatar_url=avatar_url, nickname=nickname)
                comment_infos.append(comment_info)
            return comment_infos
        except Exception as e:
            raise e
