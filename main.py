import os
from bot_core import SteamScraper, XRSSScraper, DiscordNotifier
from dotenv import load_dotenv

# 載入 .env 檔案（如果在本地執行）
load_dotenv()

def main():
    # 1. 準備工具
    # 優先從環境變數讀取 Webhook URL
    webhook = os.getenv("DISCORD_WEBHOOK_URL")
    discord = DiscordNotifier(webhook)

    # 2. 設定檢查源
    # Steam: Limbus Company AppID = 1973530
    steam_bot = SteamScraper(app_id=1973530, state_file="last_new_id.txt")
    
    # X (Twitter): 使用 RSS 服務
    rss_url = os.getenv("X_RSS_URL", "https://rss.app/feeds/WQnu37hFsCx3HJ9y.xml")
    x_bot = XRSSScraper(rss_url=rss_url, state_file="LASTFILE.txt")

    # 3. 執行 Steam 檢查
    print("正在檢查 Steam 更新...")
    for post in steam_bot.fetch_new_posts():
        msg = (f"📌 **Ciallo～(∠・ω< )⌒☆:{post['title']}**\n"
               f"[點我查看連結]({post['url']})\n"
               f"大綱:\n{post['content'][:500]}...") # 限制大綱長度避免訊息過長
               
        if discord.notify(msg):
            steam_bot.save_last_id(post['gid'])
            print(f"成功發送 Steam 新聞: {post['title']}")

    # 4. 執行 X 檢查
    print("正在檢查 X 更新...")
    for post in x_bot.fetch_new_posts():
        msg = f"📢 **Ciallo～(∠・ω< )⌒☆**\n{post.link}"
        if discord.notify(msg):
            x_bot.save_last_id(post.link)
            print(f"成功發送 X 推文: {post.link}")

if __name__ == "__main__":
    main()
