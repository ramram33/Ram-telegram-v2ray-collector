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

# الگوهای شناسایی پروتکل‌ها و لینک‌های ساب
CONFIG_PATTERN = re.compile(r'(?:vmess|vless|ss|shadowsocks|trojan)://[^\s<>\"]+')
SUB_LINK_PATTERN = re.compile(r'https?://[^\s<>\"]+')

def get_content(url: str) -> str:
    """دریافت محتوای یک آدرس اینترنتی"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8', errors='ignore')
    except:
        return ""

def process_sub_link(url: str) -> set:
    """استخراج کانفیگ از لینک‌های سابسکرایب"""
    configs = set()
    # فیلتر کردن لینک‌های غیرمفید
    if any(x in url for x in ['t.me', 'google', 'instagram', 'youtube', 'github.com']):
        return configs
    
    content = get_content(url)
    if content:
        # اگر محتوا Base64 بود، آن را دیکود کن
        try:
            decoded = base64.b64decode(content + "===").decode('utf-8', errors='ignore')
            content = decoded
        except:
            pass
        
        found = CONFIG_PATTERN.findall(content)
        configs.update(found)
    return configs

def main():
    all_configs = set()
    print(f"🚀 شروع جمع‌آوری در تاریخ: {datetime.now()}")

    for channel in CHANNELS:
        print(f"🔎 اسکن کانال: {channel}...")
        # استفاده از نمای وب تلگرام (t.me/s/...)
        web_url = f"https://t.me/s/{channel}"
        html_content = get_content(web_url)
        
        if not html_content:
            print(f"❌ نتوانستم محتوای {channel} را بخوانم.")
            continue

        # ۱. استخراج مستقیم کانفیگ‌ها از متن پیام‌ها
        direct_configs = CONFIG_PATTERN.findall(html_content)
        all_configs.update(direct_configs)

        # ۲. استخراج لینک‌های ساب و بررسی داخل آن‌ها
        sub_links = SUB_LINK_PATTERN.findall(html_content)
        for link in sub_links:
            configs_from_sub = process_sub_link(link)
            all_configs.update(configs_from_sub)

    # ذخیره نتایج
    config_list = sorted(list(all_configs))
    
    # فایل متنی ساده
    with open("telegram_configs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(config_list))
    
    # فایل Base64 (مناسب برای اضافه کردن به اپلیکیشن‌ها)
    encoded_content = base64.b64encode("\n".join(config_list).encode("utf-8")).decode("utf-8")
    with open("telegram_configs_base64.txt", "w", encoding="utf-8") as f:
        f.write(encoded_content)

    print(f"✅ پایان. {len(config_list)} کانفیگ جمع‌آوری شد.")

if __name__ == "__main__":
    main()