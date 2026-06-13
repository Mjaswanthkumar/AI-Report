from news_fetcher import get_news
from summarizer import summarize

articles = get_news()

brief = summarize(articles)

print(brief)