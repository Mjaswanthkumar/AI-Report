import os
import requests
from news_fetcher import get_news
from summarizer import summarize

def split_message(text, max_len=2000):
    return [text[i:i+max_len] for i in range(0, len(text), max_len)]


def send_telegram_message(text):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    # print("token:", token)
    # print("chat_id:", chat_id)

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    messages = split_message(text)

    for msg in messages:
        payload = {
            "chat_id": chat_id,
            "text": msg
        }
        response = requests.post(url, json=payload)

    print("status:", response.status_code)
    print("response:", response.text)


def main():
    articles = get_news()
    report = summarize(articles)

    print(report)  # still useful for GitHub logs
    send_telegram_message(report)


if __name__ == "__main__":
    main()