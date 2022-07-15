# -*- coding: utf-8 -*-
"""
服務主入口
"""
from typing import Optional
from fastapi import (
    APIRouter, HTTPException, Security
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from utils.config import config

from utils.action.search import (
    search_items, get_items
)
from utils.action.user import (
    user_register, user_login, Auth
)
from utils.action.cart import (
    add_items, delete_items, update_items, show_items
)
from utils.model import (
    ItemBase, ResigterBase, UserBase, CartBase, CartDelete, CartUpd
)

router = APIRouter()
security = HTTPBearer()
auth = Auth()
API = config['API']['url']

## 回覆訊息格式
def reply_response(code: int, desc: str, result: Optional[dict] = None):
    msg = {
        'Result':result,
        'Status': {
            'Code': code,
            'Desc':desc
        }
    } 
    return msg

@router.get(f'/{API}/SearchItems', tags=['商品'])
async def SearchItems(keyword: str):
    try:
        data = search_items(keyword=keyword)
        msg = reply_response(
            result = data,
            code = 200,
            desc = '搜尋商品成功'
        )
        return JSONResponse(status_code=200, content=msg)
    except:
        msg = reply_response(
            result = None,
            code = 400,
            desc='搜尋商品失敗'
        )
        return JSONResponse(status_code=400, content=msg)

@router.post(f'/{API}/ContentItems', tags=['商品'])
async def ContentItems(item: ItemBase):
    try:
        data = get_items(
            itemid=item.itemid
        )
        msg = reply_response(
            result = data,
            code = 200,
            desc = '商品內頁成功'
        )
        return JSONResponse(status_code=200, content=msg)
    except:
        msg = reply_response(
            result = None,
            code = 400,
            desc='商品內頁失敗'
        )
        return JSONResponse(status_code=400, content=msg)

@router.post(f'/{API}/RegisterUser', tags=['用戶'])
async def RegisterUser(User: ResigterBase):

    userid = User.userid
    password = User.password
    username = User.username
    email = User.email
    phone = User.phone

    try:
        ret = user_register(
            username=username, 
            userid=userid, 
            password=password, 
            email=email, 
            phone=phone
        )

        msg = reply_response(
            result={'userid':userid},
            code=200,
            desc=ret
        )
        return JSONResponse(status_code=200, content=msg)

    except:
        msg = reply_response(
            result=None,
            code=400,
            desc='註冊失敗'
        )
        return JSONResponse(status_code=400, content=msg)

@router.post(f'/{API}/LoginUser', tags=['用戶'])
async def LoginUser(User: UserBase):
    
    userid = User.userid
    password = User.password
    
    try:
        data = user_login(
            userid=userid,
            password=password
        )
        
        msg = reply_response(
            result={'token':data['token']},
            code=200,
            desc=data['ret']
        )
        return JSONResponse(status_code=200, content=msg)

    except:
        msg = reply_response(
            result=None,
            code=400,
            desc='登入失敗'
        )
        return JSONResponse(status_code=400, content=msg)


@router.post(f'/{API}/AddCart', tags=['購物車'])
async def AddCart(Item:CartBase, credentials: HTTPAuthorizationCredentials = Security(security)):
    item = {**Item.dict()}
    userid = auth.decode_token(credentials.credentials)
    if userid:
        try:
            add_items(
                userid=userid, 
                item=item['items']
            )
            msg = reply_response(
                result=None,
                code=200,
                desc='成功'
            )
            return JSONResponse(status_code=200, content=msg)

        except:
            msg = reply_response(
                result=None,
                code=400,
                desc='失敗'
            )
            return JSONResponse(status_code=400, content=msg)
    else:
        raise HTTPException(status_code=401, detail='Invalid token')

@router.post(f'/{API}/DeleteCart', tags=['購物車'])
async def DeleteCart(Item:CartDelete, credentials: HTTPAuthorizationCredentials = Security(security)):
    item = {**Item.dict()}
    userid = auth.decode_token(credentials.credentials)
    if userid:
        print(item['itemid'],item['orderid'])
        try:
            delete_items(
                itemid=item['itemid'],
                orderid=item['orderid'],
                userid=userid
            )
            msg = reply_response(
                result=None,
                code=200,
                desc='成功'
            )
            return JSONResponse(status_code=200, content=msg)

        except:
            msg = reply_response(
                result=None,
                code=400,
                desc='失敗'
            )
            return JSONResponse(status_code=400, content=msg)
    else:
        raise HTTPException(status_code=401, detail='Invalid token')

@router.get(f'/{API}/ShowCart', tags=['購物車'])
async def ShowCart(credentials: HTTPAuthorizationCredentials = Security(security)):
    userid = auth.decode_token(credentials.credentials)
    print('userid',userid)
    if userid:
        try:
            data = show_items(userid=userid)
            msg = reply_response(
                result=data,
                code=200,
                desc='成功'
            )
            return JSONResponse(status_code=200, content=msg)

        except:
            msg = reply_response(
                result=None,
                code=400,
                desc='失敗'
            )
            return JSONResponse(status_code=400, content=msg)
    else:
        raise HTTPException(status_code=401, detail='Invalid token')


@router.post(f'/{API}/UpdateCart', tags=['購物車'])
async def UpdateCart(Item:CartUpd, credentials: HTTPAuthorizationCredentials = Security(security)):
    item = {**Item.dict()}
    userid = auth.decode_token(credentials.credentials)
    if userid:
        try:
            update_items(
                userid=userid, 
                item=item['items'],
                orderid=item['orderid']
            )
            msg = reply_response(
                result=None,
                code=200,
                desc='成功'
            )
            return JSONResponse(status_code=200, content=msg)

        except:
            msg = reply_response(
                result=None,
                code=400,
                desc='失敗'
            )
            return JSONResponse(status_code=400, content=msg)
    else:
        raise HTTPException(status_code=401, detail='Invalid token')

