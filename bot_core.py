import os
import requests
import feedparser
from bs4 import BeautifulSoup as bs

# --- 1. 基礎類別 (Base Class) ---
class NewsSource:
    """處理共通的存檔與狀態管理，避免重複寫讀寫檔邏輯"""
    def __init__(self, state_file):
        self.state_file = state_file

    def get_last_id(self):
        """讀取上一次發送的 ID"""
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                return f.read().strip()
        return None

    def save_last_id(self, last_id):
        """儲存這一次發送的 ID"""
        with open(self.state_file, "w") as f:
            f.write(str(last_id))

# --- 2. 通知模組 (Notifiers) ---
class DiscordNotifier:
    """專門負責將訊息發送到 Discord"""
    def __init__(self, webhook_url, username="梅菲斯特情報號"):
        self.webhook_url = webhook_url
        self.username = username

    def notify(self, content):
        if not self.webhook_url:
            print("錯誤：找不到 Webhook URL")
            return False
        
        payload = {"username": self.username, "content": content}
        headers = {"Content-Type": "application/json"}
        res = requests.post(self.webhook_url, json=payload, headers=headers)
        return res.status_code in [200, 204]

# --- 3. 抓取模組 (Scrapers) ---
class SteamScraper(NewsSource):
    """Steam API 抓取邏輯"""
    def __init__(self, app_id, state_file):
        super().__init__(state_file)
        self.app_id = app_id
        self.api_url = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/"
        self.cdn_prefix = "https://clan.cloudflare.steamstatic.com/images/"

    def fetch_new_posts(self):
        params = {
            "appid": self.app_id, 
            "count": 5, 
            "maxlength": 1000,
            "format": "json"
        }
        try:
            res = requests.get(self.api_url, params=params)
            if res.status_code != 200: return []
            
            data = res.json()
            items = data["appnews"]["newsitems"]
        except Exception as e:
            print(f"Steam 抓取錯誤: {e}")
            return []

        last_id = self.get_last_id()
        new_posts = []
        
        for item in items:
            if item["gid"] == last_id:
                break
            
            # 處理內文與圖片
            raw_content = item["contents"]
            if "{STEAM_CLAN_IMAGE}" in raw_content:
                raw_content = raw_content.replace("{STEAM_CLAN_IMAGE}/", self.cdn_prefix)
            
            clean_content = bs(raw_content, "html.parser").get_text().strip()
            
            new_posts.append({
                "gid": item["gid"],
                "title": item["title"],
                "url": item["url"],
                "content": clean_content
            })
        
        return reversed(new_posts)

class XRSSScraper(NewsSource):
    """X (Twitter) RSS 抓取邏輯"""
    def __init__(self, rss_url, state_file):
        super().__init__(state_file)
        self.rss_url = rss_url

    def fetch_new_posts(self):
        try:
            feed = feedparser.parse(self.rss_url)
            if not feed.entries: return []
            
            latest = feed.entries[0]
            last_link = self.get_last_id()

            if last_link is None:
                self.save_last_id(latest.link)
                print(f"X 抓取器初始化成功: {latest.link}")
                return []

            if latest.link != last_link:
                return [latest]
        except Exception as e:
            print(f"X RSS 抓取錯誤: {e}")
        
        return []
