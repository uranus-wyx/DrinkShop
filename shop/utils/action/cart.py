#%%
# -*- coding: utf-8 -*-
"""
購物車服務
"""
from ..db.mongo import get_cached_mongo_db
from datetime import datetime
import pandas as pd
#%%

def get_orderid():
    """
    訂單編號
    Return: order1
    """
    db = get_cached_mongo_db()
    code = 'order'
    try:
        data = list(db.Cart.find().sort("created_at",-1).limit(1))
        _id = int(data[0][f'orderid'].split(f'{code}')[1])+1
    except:
        _id = 1
    orderid  = code + str(_id)
    return orderid
    
def add_items(item:dict, userid:int):
    """
    新增商品進購物車
    itemid: 商品ID
    amount: 商品數量
    userid: 用戶ID
    """
    db = get_cached_mongo_db()
    orderid = get_orderid()
    db.Cart.insert_one({
        'userid':userid,
        'orderid':orderid,
        'item':item,
        'created_at':datetime.now(),
        'modified_at':datetime.now(),
        'status':1
    })

def delete_items(userid:int, orderid:str, itemid:int):
    """
    在購物車刪除商品
    itemid: 商品ID
    userid: 用戶ID
    """
    db = get_cached_mongo_db()

    data = db.Cart.find_one(
        {'userid':userid, 'orderid':orderid}, 
        {'_id':0, 'item':1}
    )
    data = list(filter(lambda i: i['itemid'] != itemid, data['item']))
    
    db.Cart.update_one(
        {
            'userid':userid,
            'orderid':orderid,
        },
        {'$set': {
            'item':data,
            'modified_at':datetime.now(),
        }}
    )

def show_items(userid:int):
    """
    顯示該用戶的購物車內容物
    userid: 用戶ID
    
    """
    db = get_cached_mongo_db()
    df = pd.DataFrame(db.Cart.find({'userid':userid}, {'_id':0}))
    if len(df)>0:
        df['created_at'] = df['created_at'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        df['modified_at'] = df['modified_at'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        data = df.to_dict('records')
    else:
        data = list()
    return data

def update_items(item:dict, orderid:str, userid:int):
    """
    更新商品進購物車
    itemid: 商品ID
    amount: 商品數量
    userid: 用戶ID
    price: 價格
    """
    db = get_cached_mongo_db()

    data = db.Cart.find_one(
        {'userid':userid, 'orderid':orderid}, 
        {'_id':0, 'item':1}
    )
    data['item'].extend(item)

    db.Cart.update_one(
        {
            'userid':userid,
            'orderid':orderid
        },
        {'$set':{
            'item':data['item'],
            'modified_at':datetime.now()
        }}
    )
    return