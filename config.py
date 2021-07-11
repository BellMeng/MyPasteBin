'''
@File    ：config.py
@Author  ：Bell_Meng
@Date    ：2021/7/10 9:38 
'''

import os


class MySQLConfig(object):
    user = 'root'
    password = 'whm980617'
    ip = 'localhost'
    port = '3306'
    database = 'pastebin'

    @property
    def URI(self):
        return 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(self.user, self.password, self.ip, self.port,
                                                                    self.database)


class BaseConfig(object):
    """
    基本配置文件
    """
    SQLALCHEMY_DATABASE_URI = MySQLConfig().URI
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    SECRET_KEY = '--*.&This is a test by XiaChuFang.?./*--'
