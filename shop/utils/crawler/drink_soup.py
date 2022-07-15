# coding: utf-8
#%%
import time
import requests
from bs4 import BeautifulSoup
from ..db.mongo import get_cached_mongo_db
db = get_cached_mongo_db()
#%%
#%%
def fetchUrl(url):
    resp = requests.get(url=url)
    resp.encoding = 'UTF-8'
    data = BeautifulSoup(resp.text, 'html.parser')
    return data
#%%
def kebuke():
    url = 'https://www.kebuke.com/menu/'
    data = fetchUrl(url=url)
    product_eles = data.find_all("div", {"class": "menu-item"})
    items_list = list()

    for element in product_eles:
        # 商品內頁
        item_href = element.find('a')['href']
        # 商品名稱
        item_name = element.find("p", {"class": "menu-item__name"}).text.strip()
        # 商品價格
        item_price = element.find("p", {"class": "menu-item__price"}).text.strip()
        # 商品簡介
        item_desc = element.find("p", {"class": "menu-item__desc"}).text.strip()
        # 爬取商品內頁
        item_page = fetchUrl(url=item_href)
        # 商品內頁圖片
        item_image = item_page.find('meta', {'name':'twitter:image'})['content']
        # # 商品內頁詳細說明
        # item_page_desc = (item_image.find("p", {"class": "single-product__info-desc"}).text)
        itemid = int(str(hash(item_name))[4:])

        item = dict()
        item['channel'] = '可不可熟成紅茶'
        item['itemid'] = itemid
        item['name'] = item_name
        item['price'] = item_price
        item['info'] = item_desc
        item['url'] = item_href
        item['img'] = item_image
        
        items_list.append(item)
    db.Drink.insert_many(items_list)
    return items_list
#%%
def milkshop():
    url = "https://www.milkshoptea.com/products.php"
    data = fetchUrl(url=url)
    product_eles = data.select("li.col-6 a")

    item_href_list = list()
    for product_ele in product_eles:
        link = "https://www.milkshoptea.com/" + product_ele.get("href")
        if link not in item_href_list:
            item_href_list.append(link)

    items_list = list()
    for item_href in item_href_list:
        item_data = fetchUrl(url=item_href)
        product_eles = item_data.select(".row.products_box2")
        for element in product_eles:
            item = dict()
            item['channel'] = '迷客夏'
            item["url"] = item_href
            item["img"] = "https://www.milkshoptea.com/" + element.select_one(".img-fluid").get("src")
            item_name = element.select_one("h3").text.replace(' ','').replace('L','').replace('\u3000','').replace('M','')
            item['name'] = item_name
            item['itemid'] = int(str(hash(item_name))[4:])
            item["info"] = "".join([x.text for x in element.select("p")])
            item["price"] = None
            items_list.append(item)
    db.Drink.insert_many(items_list)
    return items_list
# %%
def tenren():

    items_list = []
    website = "https://www.tenren.com.tw/Content/Goods/"
    url = f"{website}List.aspx?SiteID=10&MmmID=654036521237004377&CatId=2015062316440646010"
    data = fetchUrl(url=url)
    
    category_link_list = list(website + x.get("href") for x in data.select(".ProductCatList.eqHeight .item .photo a"))

    for category_link in category_link_list:
        data = fetchUrl(url=category_link)

        product_link_list = [website + x.get("href") for x in data.select(".ProductList.eqHeight .item .photo a")]
        for product_link in product_link_list:
            data = fetchUrl(url=product_link)

            item = dict()
            item["url"] = product_link
            #部分圖片遺失
            try:
                item["img"] = data.select_one(".p_img img").get("src").replace("../../","https://www.tenren.com.tw/")
            except:
                item["img"] = None

            item["name"] = data.select_one('.p_title').text.replace("\r", "").replace("\n", "").replace(" ","")
            item["info"] = data.select_one('.desc').text.replace("\r", "").replace("\n", "").replace(" ","")
            item["price"] = None
            item["itemid"] = int(str(hash(item["name"]))[4:])
            item["channel"] = '天仁茗茶'

            items_list.append(item)
            time.sleep(.1)
    db.Drink.insert_many(items_list)
    return items_list

#%%
def startbacks():

    catid_list = ['1','8','4','10','40','26']
    items_list = list()
    for catid in catid_list:
        url = "https://www.starbucks.com.tw/products/drinks/view.jspx?catId=" + catid
        data = fetchUrl(url=url)
        
        data.select('article ul li')[0]
        product_link_list = list("https://www.starbucks.com.tw/" + x.get("href") for x in data.select('article ul li a'))

        for product_link in product_link_list:
            data = fetchUrl(url=product_link)
            item = dict()
            item["url"] = product_link
            item["img"] = "https://www.starbucks.com.tw" + data.select_one(".about .image_block img").get("src")
            item["name"] = data.select_one(".about .title_cn").text
            item["info"] = data.select_one(".text_block .info").text.replace(' ','').replace('\n','').replace('\xa0','').replace('\t','').replace('\r','')
            item["price"] = data.select_one(".nutrition_block tr td").text.replace('$','')
            item["itemid"] = int(str(hash(item["name"]))[4:])
            item["channel"] = '星巴克'

            items_list.append(item)
            time.sleep(.1)
    db.Drink.insert_many(items_list)
    return items_list
#%%

#%%
if __name__ == '__main__':
    data_kebuke = kebuke()
    data_milkshop = milkshop()
    data_tenren = tenren()
    data_star = startbacks()
# %%
