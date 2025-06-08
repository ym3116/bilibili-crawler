# test_on_single_video.py：用于测试，返回一个raw_test_output.json
import requests
from fake_useragent import UserAgent
import json
from html_checker import is_charged_by_html

bv = "BV1Ls7PzeEE1"  # 替换为你想测试的 BV号
ua = UserAgent()
url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv}"
headers = {"User-Agent": ua.random}

# 发请求获取 JSON 数据
res = requests.get(url, headers=headers)
print(f"✅ HTTP status: {res.status_code}")

try:
    raw = res.json()
    with open("raw_test_output.json", "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False, indent=2)
    print("✅ Raw JSON saved to raw_test_output.json")

    data = raw["data"]
    
    # ========== API判断方式 ==========
    is_charged_api = (
        data.get("rights", {}).get("ugc_pay", 0) == 1 or
        data.get("rights", {}).get("ugc_pay_preview", 0) == 1 or
        data.get("ugc_season", {}).get("is_pay_season", False)
    )

    print(f"🧪 API 判断结果 → is_charged: {is_charged_api}")

    # ========== HTML前端判断方式 ==========
    is_charged_html = is_charged_by_html(bv)

    print(f"🧪 HTML 判断结果 → is_charged: {is_charged_html}")

    # ========== 最终结果建议 ==========
    final_result = is_charged_api or is_charged_html
    print(f"\n📦 综合判断结果 → is_charged = {final_result}")

except Exception as e:
    print("❌ JSON解析失败：", e)
    print("⚠️ 响应内容前500字符如下：\n", res.text[:500])
