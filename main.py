import requests
import os
from bs4 import BeautifulSoup

# 這是你剛才複製的 Webhook URL
WEBHOOK_URL = "https://discordapp.com/api/webhooks/1483905208181457117/Bz5sUjYX7auxz_TgazkjW7VcQzXMfr1mib7YqBrSuLc1TJbnqfEO90p_jMWgBLFD2Hvz"
Last_GID = "last_new_id.txt"
def getlastgid():
    if os.path.exists(Last_GID):
        with open(Last_GID,"r") as f:
            return f.read().strip()
    else:
        return None
def savegid(newsid):
    with open(Last_GID,"w") as f:
        f.write(str(newsid))

def fetch_limbus_news():

    api_url = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/"
    params = {
        "appid": 1973530,
        "count": 1,          # 只拿最新一則
        "maxlength": 500,    # 直接限制字數
        "format": "json"
    }

    response = requests.get(api_url, params=params)
    data = response.json() # 將 JSON 轉為 Python 字典
    
    # 依照結構抓出需要的資料
    news_item = data["appnews"]["newsitems"][0]
    current_gid = news_item["gid"]
    last_id = getlastgid()
    if current_gid != last_id:
        # 3. 準備發送給 Discord 的資料
        title = news_item["title"]
        link = news_item["url"]

        payload = {
        "username": "梅菲斯特情報號",
        "content": f"📢 **最新消息通知**\n{title}\n連結: {link}\n"
        }
        #4. 透過 Webhook 發送
        requests.post(WEBHOOK_URL, json=payload)
        print("訊息已送出！")
        
    else:
        print("目前沒有新消息")


if __name__ == "__main__":
    fetch_limbus_news()
    