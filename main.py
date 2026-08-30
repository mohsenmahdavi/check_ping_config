import os
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/mix",
    "https://raw.githubusercontent.com/MahdiBland/V2RayAggregator/master/sub/sub_merge.txt"
]

def get_configs():
    configs = []
    for url in SOURCES:
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                lines = res.text.splitlines()
                for line in lines:
                    line = line.strip()
                    if line.startswith(("vless://", "vmess://", "ss://", "trojan://")):
                        configs.append(line)
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
    return configs

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "disable_web_page_preview": True
    }
    res = requests.post(url, json=payload)
    return res.status_code == 200

def main():
    print("Fetching configs...")
    configs = get_configs()
    print(f"Found {len(configs)} configs.")
    
    if not configs:
        print("No configs found.")
        return

    selected = configs[:5]
    message = "✅ **کانفیگ‌های جدید و فعال:**\n\n" + "\n\n".join(selected)
    
    if send_telegram(message):
        print("Successfully sent to Telegram channel!")
    else:
        print("Failed to send message to Telegram.")

if __name__ == "__main__":
    main()
