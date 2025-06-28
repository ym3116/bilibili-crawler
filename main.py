import re
import time
import csv
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from concurrent.futures import ThreadPoolExecutor
from config import CONFIG, CHROME_BINARY_PATH, CHROMEDRIVER_PATH
from crawler import get_video_info
from html_checker import is_charged_video

# Load config values
keyword = CONFIG["keyword"]
max_pages = CONFIG["max_pages"]
scroll_times = CONFIG["max_scroll_times"]
output_csv = CONFIG["output_csv"]
max_threads = CONFIG["max_threads"]

# Set up Selenium with custom Chrome
options = Options()
options.binary_location = CHROME_BINARY_PATH
options.add_argument("--headless")
options.add_argument("--disable-gpu")
service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

bv_set = set()

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

driver.quit()
print(f"📦 Total BV IDs collected: {len(bv_set)}")

# Get basic video info
video_info_list = []
for bv in bv_set:
    info = get_video_info(bv)
    if info:
        video_info_list.append(info)

# Add is_charged_video using threads
def enrich_with_charge_status(video):
    bv = video["bv"]
    charged = is_charged_video(bv)
    video["is_charged"] = int(charged)
    print(f"🔎 {bv} charged = {charged}")
    return video

print("🚀 Checking charge status using threads...")
with ThreadPoolExecutor(max_workers=max_threads) as executor:
    video_info_list = list(executor.map(enrich_with_charge_status, video_info_list))

# Save results to CSV
csv_file = Path(output_csv)
with open(csv_file, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=video_info_list[0].keys())
    writer.writeheader()
    writer.writerows(video_info_list)

print(f"✅ Exported {len(video_info_list)} records to {csv_file.resolve()}")
