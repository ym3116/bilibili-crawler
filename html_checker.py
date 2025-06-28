# html_checker.py: 用于识别是否为充电视频，直接抓取前端是否包含专属视频等关键词
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from config import CHROME_BINARY_PATH, CHROMEDRIVER_PATH
# charge_utils.py
import requests

def is_charged_video(bv, fast_mode=True):
    """
    判断 B 站视频是否为“专属/充电”内容
    - fast_mode=True: 用 requests 抓 html，关键词判断（推荐）
    - fast_mode=False: fallback 到 selenium 检测（更稳）
    """
    try:
        url = f"https://www.bilibili.com/video/{bv}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.bilibili.com"
        }
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            raise Exception("请求失败")

        html = res.text
        keywords = ["专属视频", "试看中", "充电专属"]

        for kw in keywords:
            if kw in html:
                return True

        if fast_mode:
            return False
        else:
            # fallback to selenium 判断
            return is_charged_by_html(bv)

    except Exception as e:
        print(f"⚠️ is_charged_video 错误: {bv} - {e}")
        return None  # 无法判断


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


