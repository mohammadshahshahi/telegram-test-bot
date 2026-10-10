import json
import os
import time
import urllib.parse
import urllib.request

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise SystemExit("BOT_TOKEN is not set")

API = f"https://api.telegram.org/bot{TOKEN}/"


def telegram(method, data=None):
    payload = urllib.parse.urlencode(data or {}).encode()
    req = urllib.request.Request(API + method, data=payload)
    with urllib.request.urlopen(req, timeout=40) as res:
        result = json.loads(res.read().decode("utf-8"))
    if not result.get("ok"):
        raise RuntimeError(result)
    return result["result"]


KEYBOARD = {
    "keyboard": [
        [{"text": "راهنما"}, {"text": "منو"}],
        [{"text": "درباره ربات"}]
    ],
    "resize_keyboard": True
}


def send(chat_id, text):
    telegram("sendMessage", {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": json.dumps(KEYBOARD, ensure_ascii=False)
    })


def handle(message):
    chat_id = message.get("chat", {}).get("id")
    text = (message.get("text") or "").strip()

    if not chat_id or not text:
        return

    if text.startswith("/start"):
        send(chat_id, "سلام! 👋 به ربات آزمایشی خوش اومدی.")
    elif text.startswith("/help") or text == "راهنما":
        send(chat_id, "راهنما:\n/start برای شروع\nهر پیامی بفرستی، جواب می‌دم.")
    elif text == "منو":
        send(chat_id, "منوی اصلی ربات فعاله.")
    elif text == "درباره ربات":
        send(chat_id, "این اولین ربات آزمایشی ماست.")
    else:
        send(chat_id, f"پیامت دریافت شد: {text}")


def main():
    offset = None
    print("Bot is running")
    while True:
        try:
            data = {"timeout": 30}
            if offset is not None:
                data["offset"] = offset

            for update in telegram("getUpdates", data):
                offset = update["update_id"] + 1
                message = update.get("message")
                if message:
                    handle(message)
        except KeyboardInterrupt:
            break
        except Exception as error:
            print("Error:", error)
            time.sleep(3)


if __name__ == "__main__":
    main()
