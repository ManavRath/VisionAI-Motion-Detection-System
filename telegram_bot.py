import requests
import os

# CONFIGURATION
# You need to get these from @BotFather and @userinfobot
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"

def send_telegram_alert(message, image_path=None):
    """
    Sends an alert message and optional photo to Telegram.
    """
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or CHAT_ID == "YOUR_CHAT_ID_HERE":
        print("Telegram alert skipped: Token or Chat ID not configured.")
        return

    base_url = f"https://api.telegram.org/bot{BOT_TOKEN}"
    
    try:
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as photo:
                requests.post(f"{base_url}/sendPhoto", data={"chat_id": CHAT_ID, "caption": message}, files={"photo": photo})
        else:
            requests.post(f"{base_url}/sendMessage", data={"chat_id": CHAT_ID, "text": message})
        print("Telegram alert sent successfully.")
    except Exception as e:
        print(f"Failed to send Telegram alert: {e}")

if __name__ == "__main__":
    # Test alert
    send_telegram_alert("⚠️ Test alert from Motion Sensor system.")
