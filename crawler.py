# crawler.py: gets video info from Bilibili API
import requests
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
from html_checker import is_charged_video


ua = UserAgent()

def is_charge(bvid):
    """
    判断视频是否为充电视频，调用 html_checker 的 is_charged_by_html 方法。
    """
    return is_charged_video(bvid)

def get_video_info(bv):
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv}"
    headers = {"User-Agent": ua.random}

    try:
        res = requests.get(url, headers=headers, timeout=5)
        data = res.json()["data"]
        # 判断是否充电
        is_charged = is_charge(bv)

        print(f"🔍 {bv} → charged = {int(is_charged)}")
        
        return {
            "bv": bv,
            "title": data["title"],
            "desc": data["desc"],
            "view": data["stat"]["view"],
            "like": data["stat"]["like"],
            "coin": data["stat"]["coin"],
            "favorite": data["stat"]["favorite"],
            "share": data["stat"]["share"],
            "duration": data["duration"],
            "pubdate": data["pubdate"],
            "cover": data["pic"],
            "is_charged": int(is_charged)
        }
    except Exception as e:
        print(f"❌ Failed to get info for {bv}: {e}")
        return None

def get_all_info(bv_list):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(get_video_info, bv_list))
    return [r for r in results if r]
