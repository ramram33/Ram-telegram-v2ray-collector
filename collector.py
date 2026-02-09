import urllib.request
import re
import base64
from datetime import datetime
from typing import List

# لیست کانال‌ها (بدون نیاز به @)
CHANNELS = [
    '@arisping',
    '@PrivateVPNs',
    '@AzadLinkIran',
    '@Vpn_m2s',
]

CONFIG_PATTERN = re.compile(r'(?:vmess|vless|ss|shadowsocks|trojan)://[^\s<>\"\'\?]+')
SUB_LINK_PATTERN = re.compile(r'https?://(?:[a-zA-Z0-9-]+\.)+[a-z]{2,}(?::\d+)?/[^\s<>\"\'\?]+')

def get_content(url: str) -> str:
    try:
        # شبیه‌سازی کامل یک مرورگر واقعی
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"   ⚠️ خطا در بارگذاری لینک: {e}")
        return ""

def main():
    all_configs = set()
    print(f"🚀 شروع جمع‌آوری: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    for channel in CHANNELS:
        print(f"🔎 بررسی کانال: @{channel}")
        
        # تلاش برای گرفتن پیام‌های آخر با اضافه کردن پارامتر اتفاقی
        web_url = f"https://t.me/s/{channel}?before={int(time.time())}"
        html_content = get_content(web_url)
        
        if not html_content:
            continue

        # استخراج مستقیم
        found = CONFIG_PATTERN.findall(html_content)
        if found:
            print(f"   ✅ {len(found)} کانفیگ مستقیم پیدا شد.")
            all_configs.update(found)

        # استخراج و بررسی لینک‌های ساب (فقط لینک‌هایی که شبیه ساب هستند)
        links = SUB_LINK_PATTERN.findall(html_content)
        for link in set(links):
            if any(x in link for x in ['/t.me/', 'google.com', 'youtube.com', 'twitter.com', 'github.com/login']):
                continue
            
            # اگر لینک حاوی کلماتی مثل sub یا v2ray بود یا پسوند خاصی داشت، بررسی کن
            if any(word in link.lower() for word in ['sub', 'v2ray', 'config', 'get', 'api', 'raw']):
                sub_content = get_content(link)
                if sub_content:
                    # بررسی محتوای معمولی یا Base64
                    try:
                        decoded = base64.b64decode(sub_content.strip() + "===", validate=False).decode('utf-8', errors='ignore')
                        if "://" in decoded: sub_content = decoded
                    except: pass
                    
                    sub_found = CONFIG_PATTERN.findall(sub_content)
                    if sub_found:
                        print(f"   🔗 {len(sub_found)} کانفیگ از لینک ساب استخراج شد.")
                        all_configs.update(sub_found)

    # پاکسازی نهایی: حذف موارد تکراری و کاراکترهای مزاحم
    final_list = sorted([c.strip() for c in all_configs if len(c) > 15])
    
    with open("telegram_configs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_list))
    
    encoded_content = base64.b64encode("\n".join(final_list).encode("utf-8")).decode("utf-8")
    with open("telegram_configs_base64.txt", "w", encoding="utf-8") as f:
        f.write(encoded_content)

    print(f"✨ مجموع کل: {len(final_list)} کانفیگ ذخیره شد.")

if __name__ == "__main__":
    main()

