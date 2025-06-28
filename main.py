import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
from crawler import get_all_info
from html_checker import is_charged_video

# ✅ 从 config.json 中读取关键词和页数
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

keyword = config.get("keyword", "")
max_pages = config.get("max_pages", 5)

# ✅ 启动 Selenium（无头模式）
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)

bv_set = set()
for page in range(1, max_pages + 1):
    print(f"🔍 Crawling page {page}...")
    url = f"https://search.bilibili.com/all?keyword={keyword}&page={page}"
    driver.get(url)
    time.sleep(2)
    try:
        items = driver.find_elements(By.XPATH, '//a[@href]')
        for item in items:
            href = item.get_attribute("href")
            if href and "BV" in href:
                parts = href.split("BV")
                for p in parts[1:]:
                    if len(p) >= 10:
                        bv_id = "BV" + p[:10]
                        bv_set.add(bv_id)
    except Exception as e:
        print(f"❌ Failed on page {page}: {e}")

driver.quit()
bv_list = list(bv_set)
print(f"✅ Found {len(bv_list)} BV IDs")

# ✅ 用 API 获取主数据
video_info_list = get_all_info(bv_list)

# ✅ 用 html_checker 添加更准确的 is_charged 标签
for video in video_info_list:
    try:
        video["is_charged_html"] = is_charged_video(video["bv"])
        print(f"🔎 {video['bv']} charged_html = {video['is_charged_html']}")
    except Exception as e:
        print(f"⚠️ Failed to check charge status for {video['bv']}: {e}")
        video["is_charged_html"] = None

# ✅ 存储到 CSV
df = pd.DataFrame(video_info_list)
df.to_csv("bilibili_video_info.csv", index=False, encoding="utf-8-sig")
print("✅ Saved to bilibili_video_info.csv")
