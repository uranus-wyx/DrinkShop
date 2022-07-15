# -*- coding: utf-8 -*-

"""
mongodb 設定檔
~~~~~~~~~~~~~~~~

"""

from pymongo import MongoClient
from ..config import config

def get_cached_mongo_client():
    """
    Cache mongodb client so that we don't create it whenever needed.
    """
    return __MONGO_CLIENT

def get_cached_mongo_db():
    """
    get mongodb db based on cache mongodb client
    """  
    return __MONGO_CLIENT.get_database('Shop')

def __get_mongo_client():
    """
    Return a mongodb client
    """
    client = MongoClient(
        host=config['DB']['Url'], 
        username=config['DB']['User'], 
        password=config['DB']['Pwd']
    )
    return client

__MONGO_CLIENT = __get_mongo_client()
