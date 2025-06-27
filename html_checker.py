# html_checker.py: 用于识别是否为充电视频，直接抓取前端是否包含专属视频等关键词
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from config import CHROME_BINARY_PATH, CHROMEDRIVER_PATH


def is_charged_by_html(bvid):
    url = f"https://www.bilibili.com/video/{bvid}"

    options = Options()
    options.binary_location = CHROME_BINARY_PATH
    options.add_argument("--headless")  # 可选关闭图形界面
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
    driver.get(url)

    time.sleep(10)  # 等页面加载弹窗

    html = driver.page_source
    driver.quit()

    # 关键词列表：任选其一即判断为专属视频
    charge_keywords = [
        "试看中", "去开通", "专属视频", "仅会员可观看", "包月充电", "开通权益"
    ]

    is_charged = any(keyword in html for keyword in charge_keywords)

    if is_charged:
        print(f"⚡ BV号 {bvid} 被判断为充电视频（前端识别）")
    else:
        print(f"✅ BV号 {bvid} 是免费视频")

    return is_charged

