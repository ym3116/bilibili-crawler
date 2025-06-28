import requests
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
from config import CONFIG

ua = UserAgent()

def get_video_info(bv):
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv}"
    headers = {"User-Agent": ua.random}

    try:
        res = requests.get(url, headers=headers, timeout=5)
        data = res.json()["data"]
        return {
            "bv": bv,
            "title": data.get("title", ""),
            "desc": data.get("desc", ""),
            "view": data["stat"].get("view", 0),
            "like": data["stat"].get("like", 0),
            "coin": data["stat"].get("coin", 0),
            "favorite": data["stat"].get("favorite", 0),
            "share": data["stat"].get("share", 0),
            "duration": data.get("duration", 0),
            "pubdate": data.get("pubdate", 0),
            "cover": data.get("pic", ""),
        }
    except Exception as e:
        print(f"❌ Failed to get info for {bv}: {e}")
        return None

def get_all_video_info(bv_list):
    with ThreadPoolExecutor(max_workers=CONFIG["max_threads"]) as executor:
        results = list(executor.map(get_video_info, bv_list))
    return [r for r in results if r]
