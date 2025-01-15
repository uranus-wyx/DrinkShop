# DrinkShop

- 需求: 想喝飲料但又不曉得該喝哪家飲料店，乾脆就把所有找得到關鍵字的品項都顯示出來
- 功能:
    - 搜尋
    - 顯示商品
    - 加入購物車
    - 更新購物車
    - 刪除購物車
    - 顯示購物車
- 技術
    - 後端：
        - 語言:Python
        - 框架:FastAPI
        - 爬蟲:bs4, selenium
            -網站：可不可熟成紅茶，迷客夏，天仁茗茶，清心，星巴克
        - 資料庫:mongo
        
    - 前端：
        - 框架:React
        - 套件:daisyui
    - 環境：
        - GCP
        - Nginx
        - Docker

- API 文件：https://lunch.ftfintech.com.tw:8890/api/shop/docs
- 前端網站(僅搜尋功能)：https://lunch.ftfintech.com.tw:8890/shop/
- 操作影片：https://user-images.githubusercontent.com/55674807/179158772-d9e2952c-839d-48bc-a429-e23e5262dfcd.mp4



- 總共花費時間？耗時2.5天
- 專案中最困難是？
    以專案角度來說，構想要做什麼主題是最難的，以技術層面來說，定義API傳遞的資料結構上是最難的，例如/shop/utils/model.py，在設計規格時會需要時常反覆思考要如何保有彈性，以便未來擴展能更順利。
- 哪一部分最感興趣？ 
    對專案的架構設計是最感興趣的，架構設計做得好，會讓團隊更容易理解此專案結構，日後維護也會更方便。
