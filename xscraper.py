import requests
import os
from bs4 import BeautifulSoup as bs
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager # the import one is important
import time
import json

class Browserbot():

    def __init__(self):
        self.driver = None
        self.brave_path = r"C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    def setdriver(self):

        options = Options()
        options.binary_location = self.brave_path
        # 被瀏覽器提示被自動化腳本使用，從而登入不了，詢問後得到這代碼
        # 待理解
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # 2. 隱藏自動化特徵 (這對 X/Twitter 等網站非常重要)
        options.add_argument("--disable-blink-features=AutomationControlled")

        service = Service(ChromeDriverManager().install()) #get the webdriver_manager.chrome
        self.driver = webdriver.Chrome(service=service, options=options)
        # 被瀏覽器提示被自動化腳本使用，從而登入不了，詢問後得到這代碼
        # 待理解
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
        """
        })
        return self.driver

    def x_get_cookies(self,url):
        driver = self.setdriver()
        driver.get(url)
        input("請在瀏覽器完成登入後，回到這裡按 Enter 鍵...")
        cookies = driver.get_cookies()
        with open("cookies.json","w") as f:
            json.dump(cookies,f)
        driver.quit()


    def x_fetch(self,url):
        # 1. 啟動並載入 Cookie (假設你已經執行過 x_fetch 邏輯) 
        # # 系統化理由：等待動態腳本渲染推文
        driver = self.setdriver()
        driver.get(url)
        try:
            with open("cookies.json","r") as f:
                cookies = json.load(f)
            for xcookies in cookies:
                driver.add_cookie(xcookies)
            driver.refresh()
            time.sleep(5)
        except FileNotFoundError:
            print("找不到 Cookie 檔案，請先執行儲存流程")
        print(driver.title)
        # 2. 抓取推文
        # X 的推文內容通常存放在 data-testid="tweetText" 的標籤中
        try:
            # 使用 find_elements (複數) 抓取頁面上目前可見的所有推文
            from selenium.webdriver.common.by import By
            tweets = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweetText"]')
            
            print(f"--- 成功抓取到 {len(tweets)} 則內容 ---")
            
            news_list = []
            #這邊不會 enuerate 做甚麼的
            for i, tweet in enumerate(tweets):
                try:
                    content = tweet.text
                    title = content.replace("\n", " ")[:15] + "..."
                    # 3. 連結 (Link) 
                    # 邏輯：在推文內找尋包含 "/status/" 字眼的 <a> 標籤，這就是推文唯一連結
                    link_element = tweet.find_element(By.XPATH, './/a[contains(@href, "/status/")]')
                    link = link_element.get_attribute("href")
                    # 4. 封裝資料
                    news_list.append({
                    "title": title,
                    "content": content,
                    "link": link
                    })
                    print(f"成功抓取第 {i+1} 則：{title}")
                    print(f"{i+1}. {content[:50]}...") # 預覽前50字
                except Exception as e:
                    print(f"第 {i+1} 則部分資訊抓取失敗: {e}")
                    continue
            payload = {
            "username": "梅菲斯特情報號",
            "content": f"📢 **最新消息通知**\n{news_list['title']}\n連結: {news_list['link']}\n大綱 : {news_list['content']}"
            }

            #透過 Webhook 發送
            WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
            requests.post(WEBHOOK_URL, json=payload)

        except Exception as e:
            print(f"抓取失敗: {e}")
            return []
        finally:
            # 視需求決定是否關閉
            # self.driver.quit()
            driver.quit()
        
if __name__ == "__main__":

    xbot = Browserbot()
    xbot.x_get_cookies("https://x.com/i/flow/login")
    xbot.x_fetch("https://x.com/LimbusCompany_B")

#抓取內容失敗，待修繕
        






