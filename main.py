import os
import requests
from news_fetcher import get_news
from summarizer import summarize

def split_message(text, max_len=2000):
    return [text[i:i+max_len] for i in range(0, len(text), max_len)]



def send_telegram_message(text):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    print("Token exists:", bool(token))
    print("Token length:", len(token) if token else 0)
    print("Chat ID exists:", bool(chat_id))
    print("Chat ID:", chat_id)

    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")

    if not chat_id:
        raise ValueError("TELEGRAM_CHAT_ID is not set")

    url = f"https://api.telegram.org/bot{token}/getMe"

    print("Testing Telegram bot token...")

    response = requests.get(url)

    print("Telegram status:", response.status_code)
    print("Telegram response:", response.text)

    if response.status_code != 200:
        raise RuntimeError(
            f"Telegram token test failed: {response.status_code} {response.text}"
        )

    messages = split_message(text)

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    for msg in messages:
        payload = {
            "chat_id": chat_id,
            "text": msg
        }

        response = requests.post(url, json=payload)

        print("Send status:", response.status_code)
        print("Send response:", response.text)

        response.raise_for_status()





def main():
    articles = get_news()
    report = summarize(articles)

    print(report)  # still useful for GitHub logs
    send_telegram_message(report)


if __name__ == "__main__":
    main()