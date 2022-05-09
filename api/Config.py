import configparser
import os
import logging


def getConfig(section, key):
    """
    获取配置文件的指定值
    :param section:部分名
    :param key:键名
    :return:对应值
    """
    config = configparser.ConfigParser()
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../api.conf"))
    config.read(path)
    res = ''
    try:
        res = config.get(section, key)
    except Exception:
        logging.error(f'配置文件 {section}:{key} 未填写')
    return res
