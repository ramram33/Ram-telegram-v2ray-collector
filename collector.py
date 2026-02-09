import urllib.request
import re
import base64
from datetime import datetime
import time

CHANNELS = ['@arisping', '@PrivateVPNs', '@AzadLinkIran', '@Vpn_m2s']
CONFIG_PATTERN = re.compile(r'(?:vmess|vless|ss|shadowsocks|trojan)://[^\s<>\"\'\?]+')

def get_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"      Skipping {url} due to error: {e}")
        return ""

def main():
    all_configs = set()
    print(f"--- Start: {datetime.now()} ---")

    for channel in CHANNELS:
        print(f"Scanning @{channel}...")
        web_url = f"https://t.me/s/{channel}"
        html = get_content(web_url)
        
        if html:
            found = CONFIG_PATTERN.findall(html)
            all_configs.update(found)
            print(f"   Found {len(found)} direct configs.")

    final_list = sorted(list(all_configs))
    
    # نوشتن فایل‌ها (حتی اگر خالی باشند برای جلوگیری از ارور گیت)
    with open("telegram_configs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_list))
    
    encoded = base64.b64encode("\n".join(final_list).encode("utf-8")).decode("utf-8")
    with open("telegram_configs_base64.txt", "w", encoding="utf-8") as f:
        f.write(encoded)

    print(f"--- Done: {len(final_list)} total configs ---")

if __name__ == "__main__":
    main()
