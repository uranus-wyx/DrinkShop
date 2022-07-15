#!/usr/bin/python
#-*- coding: utf-8 -*-
#%%
##Import library
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
# from ..db.mongo import get_cached_mongo_db
from pymongo import MongoClient
mongo_db_url = '172.21.80.251:27017'
client = MongoClient(mongo_db_url, username='cathy', password='cathy')
db = client['Shop']
#%%
config = {
    'url': "https://www.chingshin.tw/product.php",
    'img':"//div[@class='detail_main']/img",
    'name':"//div[@class='detail_main']/h1",
    'info':"//*[@id='page-top']/section[2]/div/div[2]/div[2]/div[2]/p[2]",
}

def ChingShin():
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(config['url'])

    drink_url = driver.find_elements(By.XPATH, ".//*[@class='heart']/a[@href]")
    product_link_list = list(item.get_attribute('href') for item in drink_url)
    items_list = list()
    
    for product_link in product_link_list:

        driver.get(product_link)
        item = dict()
        item['url'] = product_link
        item['img'] = driver.find_element(By.XPATH, config['img']).get_attribute('currentSrc')
        item['name'] = driver.find_element(By.XPATH, config['name']).text
        item['info'] = driver.find_element_by_xpath(config['info']).text

        itemid = int(str(hash(item["name"]))[4:])
        item["itemid"] = itemid
        item["channel"] = '清心'
        item['price'] = None
        items_list.append(item)
    
    driver.quit()
    
    # db = get_cached_mongo_db()
    db.Drink.insert_many(items_list)
    
    return items_list

#%%
if __name__ == '__main__':
    data = ChingShin()
    


# %%

# %%
