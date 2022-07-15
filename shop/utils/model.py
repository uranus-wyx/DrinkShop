# -*- coding: utf-8 -*-
"""
資料格式設定檔
"""
from typing import Optional, List
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    userid: str = Field(title='用戶ID')
    password: str = Field(title='密碼')

class ResigterBase(UserBase):
    username: str = Field(title='姓名')
    email: str = Field(title='信箱')
    phone: str = Field(title='電話')

class ItemBase(BaseModel):
    itemid: int = Field(title='商品ID')

class ItemCart(ItemBase):
    amount: int

class CartDelete(ItemBase):
    orderid: str = Field(title='訂單ID')

class CartBase(BaseModel):
    items: Optional[List[ItemCart]]

class CartUpd(CartBase):
    orderid: str = Field(title='訂單ID', description='order+數字')


