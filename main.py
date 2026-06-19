import os
import requests
from news_fetcher import get_news
from summarizer import summarize

def split_message(text, max_len=2000):
    return [text[i:i+max_len] for i in range(0, len(text), max_len)]


def send_whatsapp_message(text):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM_NUMBER")
    to_number = os.getenv("TO_PHONE_NUMBER")

    if not all([account_sid, auth_token, from_number, to_number]):
        print("Error: Missing WhatsApp/Twilio environment variables.")
        return

    # Check for placeholder values
    if "your_twilio_account_sid_here" in account_sid or "your_twilio_auth_token_here" in auth_token:
        print("Warning: Twilio credentials are still set to placeholders in .env.")
        return

    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"

    messages = split_message(text, max_len=1500)  # Twilio recommends sending within reasonable sizes

    for msg in messages:
        payload = {
            "From": from_number,
            "To": to_number,
            "Body": msg
        }
        response = requests.post(url, data=payload, auth=(account_sid, auth_token))
        print("status:", response.status_code)
        print("response:", response.text)


def main():
    articles = get_news()
    report = summarize(articles)

    print(report)  # still useful for GitHub logs
    send_whatsapp_message(report)


if __name__ == "__main__":
    main()