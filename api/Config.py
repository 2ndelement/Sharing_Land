import configparser
import os
import logging


def getConfig(section, key):
    config = configparser.ConfigParser()
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../api.conf"))
    config.read(path)
    res = ''
    try:
        res = config.get(section, key)
    except Exception:
        logging.error(f'配置文件 {section}:{key} 未填写')
        exit(-1)
    return res
