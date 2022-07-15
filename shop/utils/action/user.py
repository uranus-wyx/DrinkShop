# -*- coding: utf-8 -*-
"""
使用者功能相關
"""
import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from werkzeug.security import (
    generate_password_hash, 
    check_password_hash
)
from ..db.mongo import get_cached_mongo_db
from ..config import config

class Auth():
    hasher= CryptContext(schemes=['bcrypt'])
    secret = config['API']['secret']
    
    def encode_token(self, userid:str):
        
        payload = {
            'exp' : datetime.now() + timedelta(days=1),
            'iat' : datetime.now(),
            'scope': 'access_token',
            'sub' : {
                'userid':userid
            }
        }
        token = jwt.encode(
            payload, 
            self.secret,
            algorithm='HS256'
        )
        # return token

        ## 本機端測試要加 放上docker不用
        token_encode = str(token.decode("utf-8")) 
        return token_encode

    def decode_token(self, token:str):
        try:
            now = datetime.now()
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            exp = datetime.utcfromtimestamp(payload['exp'])
            if exp > now:
                db = get_cached_mongo_db()
                userid = payload['sub']['userid']
                if db.User.find_one({'userid':userid, 'status':1}):
                    return userid
                else:
                    raise HTTPException(status_code=401, detail='Scope for the token is invalid')
              
            else:
                raise HTTPException(status_code=401, detail='Scope for the token is invalid')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')


# 註冊
def user_register(
    username: str, userid:str, password:str, email:str, phone: str):
    """
    用戶註冊
    username:
    userid:
    password:
    email:
    phone:
    """

    db = get_cached_mongo_db()
    now = datetime.now()
    hash_pwd = generate_password_hash(password)
    try:
        if db.User.find_one({'userid':userid, 'status':1}):
            ret = '該用戶已註冊過'
            return ret

        db.User.insert_one({
            'username':username,
            'userid':userid,
            'password':hash_pwd,
            'email':email,
            'phone':phone,
            'status':1,
            'created_at':now,
            'modified_at':now
        })
        ret = '註冊成功'
    except:
        ret = '資料庫存取失敗'
    return ret

# 登入
def user_login(userid:str, password:str):
    
    db = get_cached_mongo_db()
    token = None
    try:
        userinfo = db.User.find_one({'userid':userid, 'status':1})
        if userinfo:
            check_password = check_password_hash(
                pwhash=userinfo['password'], 
                password=password
            )
            if check_password:
                token = Auth().encode_token(userid=userid)
                ret = '登入成功'
            else:
                ret = '請再次檢查密碼是否輸入正確'   
        else:
            ret = '請再次檢查帳號是否輸入正確'   
        
    except:
        ret = '登入失敗'
    
    msg = {
        'token': token,
        'ret':ret
    }
    return msg