# -*- coding: utf-8 -*-
"""
搜尋服務
"""
from ..db.mongo import get_cached_mongo_db

def search_items(keyword:str):
    """
    搜尋商品
    keyword:關鍵字
    """
    db = get_cached_mongo_db()
    data = list(db.Drink.find({
        '$or':[
            {'name':{ '$regex': f'{keyword}' }},
            {'info':{ '$regex': f'{keyword}' }},
        ]
    },{
        '_id':0,
    }))

    return data

def get_items(itemid:int):
    """
    抓取商品詳細資訊
    itemid: 商品ID
    """
    db = get_cached_mongo_db()
    data = db.Drink.find_one({'itemid':itemid},{'_id':0})
    return data