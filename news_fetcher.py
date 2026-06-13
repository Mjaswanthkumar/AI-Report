import feedparser

RSS_FEEDS = [
    "https://openai.com/news/rss.xml",
    "https://huggingface.co/blog/feed.xml",
    "https://blog.google/technology/ai/rss/",
    "https://news.microsoft.com/source/topics/ai/feed/",
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/ai/feed/"
    "https://www.artificialintelligence-news.com/"
]

def get_news():
    articles = []

    for feed in RSS_FEEDS:
        parsed = feedparser.parse(feed)

        for entry in parsed.entries[:5]:
            articles.append({
                "title": entry.title,
                "summary": entry.get("summary", ""),
                "link": entry.link
            })
            # print("articles are here")
            # print(articles for art in articles)
    
    return articles