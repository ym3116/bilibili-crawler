import re
import time
import csv
import requests
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from concurrent.futures import ThreadPoolExecutor
from config import KEYWORDS, UPLOADER_LIST, CRAWL_PARAMS, CHROME_BINARY_PATH, CHROMEDRIVER_PATH, CRAWL_MODE
from crawler import get_video_info
#from html_checker import is_charged_video

# Load config values
max_pages = CRAWL_PARAMS["max_pages"]
scroll_times = CRAWL_PARAMS["max_scroll_times"]
output_csv = CRAWL_PARAMS["output_csv"]
max_threads = CRAWL_PARAMS["max_threads"]

# Set up Selenium with custom Chrome
options = Options()
options.binary_location = CHROME_BINARY_PATH
options.add_argument("--headless")
options.add_argument("--disable-gpu")
service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

bv_set = set()

if CRAWL_MODE == "keyword":
    print("🔍 Running in KEYWORD mode...")

    for keyword in KEYWORDS:
        print(f"🔍 Crawling keyword: {keyword}, pages: {max_pages}")
        for page in range(1, max_pages + 1):
            url = f"https://search.bilibili.com/all?keyword={keyword}&page={page}"
            driver.get(url)

            for i in range(scroll_times):
                print(f"📜 Scrolling page {page}, scroll {i+1}/{scroll_times} ...")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                html = driver.page_source
                found = re.findall(r'BV[0-9A-Za-z]{10}', html)
                bv_set.update(found)
                print(f"🔍 Found {len(found)} BVs in this round.")

            print(f"✅ Page {page}: Total unique BVs collected so far: {len(bv_set)}")


elif CRAWL_MODE == "mid":
    print("🔍 Running in MID mode...")

    for uploader in UPLOADER_LIST:
        name = uploader["name"]
        mid = uploader["mid"]
        print(f"👤 Fetching videos for {name} (mid={mid})")

        for page in range(1, max_pages + 1):
            url = f"https://api.bilibili.com/x/space/wbi/arc/search?mid={mid}&pn={page}&ps=30&order=pubdate"
            headers = {"User-Agent": "Mozilla/5.0"}
            try:
                res = requests.get(url, headers=headers, timeout=5)
                res.raise_for_status()
                data = res.json()
                vlist = data["data"]["list"]["vlist"]
                if not vlist:
                    break
                for video in vlist:
                    bv_set.add(video["bvid"])
                print(f"📥 Page {page}: Collected {len(vlist)} videos for {name}")
                time.sleep(0.5)
            except Exception as e:
                print(f"❌ Error on page {page} for {name} (mid={mid}): {e}")
                break


driver.quit()
print(f"📦 Total BV IDs collected: {len(bv_set)}")

# start exporting to CSV
video_info_list = []
for bv in bv_set:
    info = get_video_info(bv)
    if info:
        video_info_list.append(info)


csv_file = Path(output_csv)
with open(csv_file, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=video_info_list[0].keys())
    writer.writeheader()
    writer.writerows(video_info_list)

print(f"✅ Exported {len(video_info_list)} records to {csv_file.resolve()}")
