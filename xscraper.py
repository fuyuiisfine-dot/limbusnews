import requests
import os
import feedparser

class Browserbot:

    def __init__(self):

        self.lastfile = "LASTFILE.txt"
        # 乾淨、直覺、在本地絕對不會出錯的寫法
        self.RSS_URL = os.getenv("X_RSS_URL")

        if not self.RSS_URL:
        # 如果本地作業系統沒設定變數，就直接用這個真實網址
            self.RSS_URL = "https://rss.app/feeds/WQnu37hFsCx3HJ9y.xml"

    def get_lastlink(self):
        with open(self.lastfile,"r") as f:
            return f.read().strip()
        return None
    
    def save_lastlink(self,link):
        with open(self.lastfile,"w") as f:
            f.write(str(link))

    def x_fetch(self):

        
        print("正在檢查 Limbus Company X 狀態...")
        # 解析 RSS 內容
        feed = feedparser.parse(self.RSS_URL)
    
        # 確保有抓到資料
        if not feed.entries:
            print("暫時無法讀取 RSS 資料或該帳號尚未發文。")
            return

        # RSS 預設第一筆 (entries[0]) 就是最新的一條推文
        latest_entry = feed.entries[0]
        latest_link = latest_entry.link  # 取得推文的實際網址
        
        last_sent_link = self.get_lastlink()

        # 第一次執行：只紀錄不發送，避免把歷史推文洗版
        if last_sent_link is None:
            self.save_lastlink(latest_link)
            print(f"初始化成功，當前最新推文網址: {latest_link}")
            return
        # 檢查是否有新推文
        if latest_link != last_sent_link:

            print(f"偵測到新更新！準備發送: {latest_link}")
            
            payload = {
            "username": "梅菲斯特情報號",
            "content": f"📢 **Ciallo～(∠・ω< )⌒☆**\n{latest_link}"
            }
            headers = {
                "Content-Type": "application/json"
            }
            
            DISCORD_WEB_URL = os.getenv("DISCORD_WEBHOOK_URL")
            # 推送到 Discord Webhook
            response = requests.post(DISCORD_WEB_URL, json=payload, headers=headers)
            
            if response.status_code == 204:
                print("Discord 訊息發送成功。")
                self.save_lastlink(latest_link)  # 發送成功後更新紀錄
            else:
                print(f"發送 Discord 失敗，狀態碼: {response.status_code}")
        else:
            print("沒有偵測到新推文。")

    def main(self):

        print("Limbus Company RSS 監控機器人已啟動...")
        self.x_fetch()
        
        


        
        
if __name__ == "__main__":

    xbot = Browserbot()
    xbot.main()


        






