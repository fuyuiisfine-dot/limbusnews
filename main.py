import requests
import os
from bs4 import BeautifulSoup
import sys

#webhook url but need to improve its security in the future
WEBHOOK_URL = os.getenv("WEB_URL")
cdn_prefix = "https://clan.cloudflare.steamstatic.com/images/"
Last_GID = "last_new_id.txt"

#get last steam gid
def getlastgid():
    if os.path.exists(Last_GID):
        with open(Last_GID,"r") as f:
            return f.read().strip()
    else:
        return None
    
#save steam gid
def savegid(newsid):
    with open(Last_GID,"w") as f:
        f.write(str(newsid))

#get steam news
def fetch_limbus_news():

    if not WEBHOOK_URL:
        print("錯誤：找不到 DISCORD_WEBHOOK_URL 環境變數！")
        sys.exit(1)  # 讓程式主動停止，並噴出好懂的錯誤訊息
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
        content = news_item["contents"]

        #處理圖片顯示問題，讓圖片能正常顯示在discord上
        if "{STEAM_CLAN_IMAGE}" in content:
            content = content.replace("{STEAM_CLAN_IMAGE}/", cdn_prefix)
        else:
            return content
        
        payload = {
        "username": "梅菲斯特情報號",
        "content": f"📢 **最新消息通知**\n{title}\n連結: {link}\n大綱 : {content}"
        }
        #4. 透過 Webhook 發送
        requests.post(WEBHOOK_URL, json=payload)
        savegid(current_gid)
        print("訊息已送出！")
        
    else:
        print("目前沒有新消息")


if __name__ == "__main__":
    fetch_limbus_news()
    