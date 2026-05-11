import requests
import os
from bs4 import BeautifulSoup as bs
import sys
import re

#webhook url but need to improve its security in the future
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
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
import re

def process_visual_content(text):
    # 1. 尋找圖片網址 (以 .png, .jpg 結尾的)
    # 我們讓它變成 [點擊看圖](網址)，且不加 <> 以便觸發預覽
    img_pattern = r'(https?://[^\s]+\.(?:png|jpg|jpeg|gif))'
    text = re.sub(img_pattern, r'[🖼️ 點擊看圖](\1)', text)
    
    # 2. 尋找一般網址 (非圖片)
    # 一般網址建議加上 < >，因為我們通常不希望大綱裡的雜七雜八連結生出一堆預覽框
    other_url_pattern = r'(?<!\()https?://(?!.*(?:png|jpg|jpeg|gif))[^\s]+'
    text = re.sub(other_url_pattern, r'[🔗 連結](<\0>)', text)
    
    return text
def separate_content(raw_html):
    soup = bs(raw_html, "html.parser")
    
    # --- 1. 提取所有圖片網址 ---
    # 尋找所有的 <img> 標籤
    img_tags = soup.find_all("img")
    # 從標籤中取出 src 屬性
    image_urls = [img['src'] for img in img_tags if img.has_attr('src')]
    
    # --- 2. 提取純文字 ---
    # get_text() 會自動忽略所有標籤，只留下文字
    clean_text = soup.get_text(separator="\n", strip=True) 
    
    return clean_text, image_urls

#get steam news
def steam_fetch_limbus_news():

    if not WEBHOOK_URL:
        print("錯誤：找不到 DISCORD_WEBHOOK_URL 環境變數！")
        sys.exit(1)  # 讓程式主動停止，並噴出好懂的錯誤訊息
    api_url = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/"
    params = {
        "appid": 1973530,    
        "count": 3,          # 只拿最新一則
        "maxlength": 1000,    # 直接限制字數
        "format": "json"
    }

    response = requests.get(api_url, params=params)
    print(f"debug : status code = {response.status_code}")
    if(response.status_code != 200):
        print("error")
        return
    if response.status_code == 200:
        try:
            data = response.json() # 將 JSON 轉為 Python 字典
        except requests.exceptions.JSONDecodeError:
            print("get something but not a json")
    else:
        print("get nothing")
    
    # 依照結構抓出需要的資料
    news_item = data["appnews"]["newsitems"]
    last_gid = getlastgid()
    new_posts = []
    for item in news_item:
        if item["gid"] == last_gid:
            break
        new_posts.append(item)
    for post in reversed(new_posts):
        #準備發送給 Discord 的資料
        title = post["title"]
        link = post["url"]
        raw_content = post["contents"]
        print(raw_content)
            
        #處理圖片顯示問題，讓圖片能正常顯示在discord上
        if "{STEAM_CLAN_IMAGE}" in raw_content:
            raw_content = raw_content.replace("{STEAM_CLAN_IMAGE}/", cdn_prefix)
            ## else: return content 切記return 後的自動結束此函式
        
        soup = bs(raw_content,"html.parser")
        clean_content = soup.get_text().strip()
        print("-----")
        print(clean_content)
        text, images = separate_content(raw_content)
        image_links_str = ""
        for i, img_url in enumerate(images[:3]):
            # 注意：這裡不加 < > 以便觸發 Discord 的圖片預覽
            image_links_str += f"[🖼️ 圖 {i+1}]({img_url}) "
        #如果沒有圖片，則顯示「無內文圖片」
        display_images = image_links_str if image_links_str else "無內文圖片"


        payload = {
            "username": "梅菲斯特情報號",
            "content": (f"📌\n**標題:{title}**\n"
                        f"[點我查看]({link})\n"
                        f"大綱:\n{text}\n"
                        f"[圖連結]({display_images})")
        }
            
        #透過 Webhook 發送
        requests.post(WEBHOOK_URL, json=payload)
        
    print(f"成功發送超連結組（共 {len(new_posts)} 則）")
    if new_posts:
        savegid(new_posts[0]["gid"])
        print(f"已更新最新 GID 為: {new_posts[0]['gid']}")
    else:
        print(f"目前沒有最新的新聞，目前最新的 GID 是:{getlastgid()}")

if __name__ == "__main__":
    steam_fetch_limbus_news()
    
