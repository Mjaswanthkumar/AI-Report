import os
import requests

from news_fetcher import get_news
from summarizer import summarize


def split_message(text, max_len=1500):
    return [
        text[i:i + max_len]
        for i in range(0, len(text), max_len)
    ]


# --------------------------------------------------
# WhatsApp
# --------------------------------------------------

def send_whatsapp_message(text):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM_NUMBER")
    to_number = os.getenv("TO_PHONE_NUMBER")

    if not all([account_sid, auth_token, from_number, to_number]):
        print("Error: Missing WhatsApp/Twilio environment variables.")
        return False

    url = (
        f"https://api.twilio.com/2010-04-01/"
        f"Accounts/{account_sid}/Messages.json"
    )

    messages = split_message(text, max_len=1500)

    success = True

    for msg in messages:
        payload = {
            "From": from_number,
            "To": to_number,
            "Body": msg
        }

        response = requests.post(
            url,
            data=payload,
            auth=(account_sid, auth_token)
        )

        print("WhatsApp status:", response.status_code)
        print("WhatsApp response:", response.text)

        if response.status_code not in (200, 201):
            success = False

    return success


# --------------------------------------------------
# Telegram
# --------------------------------------------------

def send_telegram_message(text):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token:
        print("Error: TELEGRAM_BOT_TOKEN is not set.")
        return False

    if not chat_id:
        print("Error: TELEGRAM_CHAT_ID is not set.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    messages = split_message(text, max_len=4000)

    success = True

    for msg in messages:
        payload = {
            "chat_id": chat_id,
            "text": msg
        }

        response = requests.post(
            url,
            json=payload
        )

        print("Telegram status:", response.status_code)
        print("Telegram response:", response.text)

        if response.status_code != 200:
            success = False

    return success


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    # print("Fetching news...")

    # articles = get_news()

    # print(f"Fetched {len(articles)} articles.")

    # print("Generating AI summary...")

    # report = summarize(articles)

    # print("AI report generated.")
    # print(report)

    # print("\nSending report to WhatsApp...")

    whatsapp_success = send_whatsapp_message("Hi")

    print("\nSending report to Telegram...")

    telegram_success = send_telegram_message("Hi")

    print("\n--------------------------------")
    print("Delivery summary")
    print("--------------------------------")
    print("WhatsApp:", "SUCCESS" if whatsapp_success else "FAILED")
    print("Telegram:", "SUCCESS" if telegram_success else "FAILED")


if __name__ == "__main__":
    main()

