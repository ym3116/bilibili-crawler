import requests
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
from config import CRAWL_PARAMS

ua = UserAgent()

import requests
import time
from fake_useragent import UserAgent

ua = UserAgent()



def get_video_info(bv):
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv}"
    headers = {"User-Agent": ua.random}

    try:
        res = requests.get(url, headers=headers, timeout=5)
        res = requests.get(url, headers=headers, timeout=5)

        if res.status_code != 200:
            print(f"⚠️ BV {bv}: status code = {res.status_code}")
            return None

        if not res.text.startswith('{'):
            print(f"⚠️ BV {bv}: response not JSON. Content = {res.text[:100]}")
            return None

        data = res.json()["data"]
        return {
            "bv": bv,
            "title": data.get("title", ""),
            "author": data.get("owner", {}).get("name", ""), # 作者名称
            "author_mid": data.get("owner", {}).get("mid", ""), # 作者的 MID
            "desc": data.get("desc", ""),
            "view": data["stat"].get("view", 0),
            "like": data["stat"].get("like", 0),
            "coin": data["stat"].get("coin", 0),
            "favorite": data["stat"].get("favorite", 0),
            "share": data["stat"].get("share", 0),
            "comment": data["stat"].get("reply", 0),
            "danmaku": data["stat"].get("danmaku", 0), # 弹幕数量
            "duration": data.get("duration", 0), # 视频时长，单位秒
            "pubdate": data.get("pubdate", 0), # 发布时间，格式为 Unix 时间戳
            "cover": data.get("pic", ""),
            "charged": data.get("is_upower_exclusive", False), # 是否为充电视频
        }
    except Exception as e:
        print(f"❌ Failed to get info for {bv}: {e}")
        return None

def get_all_video_info(bv_list):
    with ThreadPoolExecutor(max_workers=CONFIG["max_threads"]) as executor:
        results = list(executor.map(get_video_info, bv_list))
    return [r for r in results if r]

