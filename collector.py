import urllib.request
import re
import base64
from datetime import datetime

# لیست کانال‌ها
CHANNELS = ['arisping', 'sinavm', 'VmessProtocol', 'V2rayNGn', 'free4allVPN', 'PrivateVPNs']

# الگوی شناسایی کانفیگ‌ها
CONFIG_PATTERN = re.compile(r'(?:vmess|vless|ss|shadowsocks|trojan)://[^\s<>\"\'\?]+')

def get_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"      Error fetching {url}: {e}")
        return ""

def main():
    all_configs = set()
    print(f"--- Start Collection: {datetime.now()} ---")

    for channel in CHANNELS:
        print(f"Scanning @{channel}...")
        
        # استفاده از یک Mirror عمومی برای خواندن محتوای کانال (دور زدن بلاک آی‌پی گیت‌هاب)
        # این آدرس محتوای کانال را به فرمت ساده تبدیل می‌کند
        rss_url = f"https://rsshub.app/telegram/channel/{channel}"
        
        html = get_content(rss_url)
        
        if html:
            found = CONFIG_PATTERN.findall(html)
            # گاهی کاراکترهای HTML مثل &amp; یا کدگذاری‌های دیگر در لینک‌ها می‌مانند
            clean_found = [f.replace('&amp;', '&') for f in found]
            all_configs.update(clean_found)
            print(f"   Found {len(clean_found)} configs.")
        else:
            # اگر RSSHub اولی جواب نداد، یک آدرس کمکی دیگر (نمای وب مستقیم)
            web_url = f"https://t.me/s/{channel}"
            html = get_content(web_url)
            found = CONFIG_PATTERN.findall(html or "")
            all_configs.update(found)
            print(f"   Alternative fetch found {len(found)} configs.")

    final_list = sorted(list(all_configs))
    
    # حذف کانفیگ‌های خیلی کوتاه یا ناقص
    final_list = [c for c in final_list if len(c) > 20]

    with open("telegram_configs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_list))
    
    encoded = base64.b64encode("\n".join(final_list).encode("utf-8")).decode("utf-8")
    with open("telegram_configs_base64.txt", "w", encoding="utf-8") as f:
        f.write(encoded)

    print(f"--- Finished: {len(final_list)} total unique configs ---")

if __name__ == "__main__":
    main()

CHANNELS = ['@arisping', '@PrivateVPNs', '@AzadLinkIran', '@Vpn_m2s']

# الگوی شناسایی کانفیگ‌ها
CONFIG_PATTERN = re.compile(r'(?:vmess|vless|ss|shadowsocks|trojan)://[^\s<>\"\'\?]+')

def get_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"      Error fetching {url}: {e}")
        return ""

def main():
    all_configs = set()
    print(f"--- Start Collection: {datetime.now()} ---")

    for channel in CHANNELS:
        print(f"Scanning @{channel}...")
        
        # استفاده از یک Mirror عمومی برای خواندن محتوای کانال (دور زدن بلاک آی‌پی گیت‌هاب)
        # این آدرس محتوای کانال را به فرمت ساده تبدیل می‌کند
        rss_url = f"https://rsshub.app/telegram/channel/{channel}"
        
        html = get_content(rss_url)
        
        if html:
            found = CONFIG_PATTERN.findall(html)
            # گاهی کاراکترهای HTML مثل &amp; یا کدگذاری‌های دیگر در لینک‌ها می‌مانند
            clean_found = [f.replace('&amp;', '&') for f in found]
            all_configs.update(clean_found)
            print(f"   Found {len(clean_found)} configs.")
        else:
            # اگر RSSHub اولی جواب نداد، یک آدرس کمکی دیگر (نمای وب مستقیم)
            web_url = f"https://t.me/s/{channel}"
            html = get_content(web_url)
            found = CONFIG_PATTERN.findall(html or "")
            all_configs.update(found)
            print(f"   Alternative fetch found {len(found)} configs.")

    final_list = sorted(list(all_configs))
    
    # حذف کانفیگ‌های خیلی کوتاه یا ناقص
    final_list = [c for c in final_list if len(c) > 20]

    with open("telegram_configs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_list))
    
    encoded = base64.b64encode("\n".join(final_list).encode("utf-8")).decode("utf-8")
    with open("telegram_configs_base64.txt", "w", encoding="utf-8") as f:
        f.write(encoded)

    print(f"--- Finished: {len(final_list)} total unique configs ---")

if __name__ == "__main__":
    main()

