import asyncio
import re
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon import errors
import base64
from typing import List

# تنظیمات تلگرام (این‌ها رو با مقادیر واقعی خودت جایگزین کن)
API_ID = 35891940  # api_id خودت
API_HASH = 'dd3090e2039b0b8db6f2ae3a7b3dc6f4'  # api_hash خودت
PHONE_NUMBER = '+989399492648'  # شماره تلفنت با +98

# کانال‌های معتبر و فعال (بر اساس وضعیت ۱۴۰۵/۲۰۲۶)
TELEGRAM_CHANNELS = [
    '@sinavm',           # ساب لینک مستقیم و آپدیت هر ۳ ساعت
    '@VmessProtocol',    # کانفیگ‌های تست‌شده و پایدار
    '@V2rayNGn',         # قدیمی و پرکانفیگ
    '@free4allVPN',      # کیفیت خوب با کم اسپم
    '@PrivateVPNs',      # خصوصی‌تر و با کیفیت بالا
]

async def fetch_from_telegram(channel_username: str, limit: int = 50) -> List[str]:
    configs = set()
    client = TelegramClient('telegram_v2ray_session', API_ID, API_HASH)

    try:
        await client.start(phone=PHONE_NUMBER)

        entity = await client.get_entity(channel_username)
        messages = await client(GetHistoryRequest(
            peer=entity,
            limit=limit,
            offset_id=0,
            offset_date=None,
            add_offset=0,
            max_id=0,
            min_id=0,
            hash=0
        ))

        # regex برای استخراج فقط vmess:// و vless://
        pattern = re.compile(r'(vmess://|vless://)[^\s<>\"]*')

        for message in messages.messages:
            if message.message:
                found = pattern.findall(message.message)
                configs.update(found)

        print(f"از کانال {channel_username} → {len(configs)} کانفیگ پیدا شد")

    except errors.FloodWaitError as e:
        print(f"خطای فلود از {channel_username}: صبر {e.seconds} ثانیه")
    except Exception as e:
        print(f"خطا در دریافت از {channel_username}: {e}")

    finally:
        await client.disconnect()

    return list(configs)

def collect_all_configs() -> List[str]:
    configs = []
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    for channel in TELEGRAM_CHANNELS:
        tg_configs = loop.run_until_complete(fetch_from_telegram(channel, limit=50))
        configs.extend(tg_configs)
    return list(set(configs))  # حذف تکراری‌ها

def save_to_files(configs: List[str]):
    if not configs:
        print("هیچ کانفیگی جمع نشد. چک کن اینترنت، کانال‌ها یا لاگین تلگرام رو.")
        return

    with open("telegram_configs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(configs))
    print(f"فایل telegram_configs.txt ساخته شد ({len(configs)} کانفیگ)")

    content = "\n".join(configs).encode("utf-8")
    encoded = base64.b64encode(content).decode("utf-8")
    with open("telegram_configs_base64.txt", "w", encoding="utf-8") as f:
        f.write(encoded)
    print("فایل telegram_configs_base64.txt ساخته شد")

if __name__ == "__main__":
    print("شروع جمع‌آوری کانفیگ‌ها از تلگرام...\n")
    configs = collect_all_configs()
    print(f"\nتعداد کانفیگ‌های منحصربه‌فرد: {len(configs)}")
    save_to_files(configs)
