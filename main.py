# get bv_list.py, call crawler.py to get video info and store it in a csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from config import CHROME_BINARY_PATH, CHROMEDRIVER_PATH
import time, re

def get_bv_list(keyword="食贫道", scroll_times=5):
    options = Options()
    options.binary_location = CHROME_BINARY_PATH
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
    url = f"https://search.bilibili.com/all?keyword={keyword}"
    driver.get(url)
    time.sleep(3)

    bv_set = set()
    for i in range(scroll_times):
        print(f"📜 Scrolling page {i+1}/{scroll_times} ...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        html = driver.page_source
        found = re.findall(r'BV[0-9A-Za-z]{10}', html)
        bv_set.update(found)
        print(f"🔍 Found {len(found)} BVs in this round.")

    driver.quit()
    print(f"✅ Total unique BV IDs collected: {len(bv_set)}")
    return list(bv_set)

if __name__ == "__main__":
    bv_list = get_bv_list(keyword="食贫道", scroll_times=6)
    # (Optional) Save BV list to local file
    with open("bv_list.txt", "w") as f:
        for bv in bv_list:
            f.write(bv + "\n")
    print("📁 BV list saved to bv_list.txt")
    
    
    # ======== call crawler.py to get video info ========
    
    from crawler import get_all_info
    import pandas as pd

    # 读取 BV 列表
    with open("bv_list.txt", "r") as f:
        bv_list = [line.strip() for line in f if line.strip()]

    print(f"🚀 Total BV IDs to process: {len(bv_list)}")

    # 多线程抓取视频信息
    data = get_all_info(bv_list)

    # 保存为 CSV
    df = pd.DataFrame(data)
    df.to_csv("bilibili_video_info.csv", index=False, encoding='utf-8-sig')
    print("✅ Saved video info to bilibili_video_info.csv")

