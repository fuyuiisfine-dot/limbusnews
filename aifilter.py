import asyncio
import google.generativeai as genai
from playwright.async_api import async_playwright

genai.configure(api_key="AIzaSyAOBbTpdYnD0j-xZ0gZ1cjAvjrzkIm1soc")
model = genai.GenerativeModel('gemini-1.5-flash')

async def analyze_data(content):
    """此用於給AI分析資料"""
    prompt = f"""
    你是一位專業的資訊過濾助手。以下是從網站抓取的標題與內容：
    ---
    {content}
    ---
    請幫我執行以下任務：
    1. 篩選出與「Update Notice」、「Bug fixes」、「Identity Preview」最相關的資訊。
    2. 如果有相關資訊，請簡潔地列出標題並說明推薦理由。
    3. 如果沒有相關資訊，請回覆「今日無重大相關更新」。
    """
    response = model.generate_content(prompt)
    return response.text

async def main():
    async with async_playwright() as p:
        # 啟動瀏覽器
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # 前往你想監控的網站 (這裡以 TechNews 為例)
        print("🔍 正在掃描網頁內容...")
        await page.goto("https://store.steampowered.com/news/app/1973530?l=tchinese", wait_until="networkidle")
        
        # 抓取網頁中所有的 <h2> 標題
        # 這是一個『構築系』的動作：將雜亂的網頁轉為結構化資料
        elements = await page.locator("h2").all_inner_texts()
        
        # 整理成一段文字，只取前 15 條避免資訊過載
        formatted_content = "\n".join([f"- {text}" for text in elements[:15]])
        
        print("🧠 正在啟動 AI 進行重要性判斷...")
        result = await analyze_data(formatted_content)
        
        print("\n" + "="*30)
        print("📢 AI 過濾結果：")
        print(result)
        print("="*30)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

