# momentum_score.py

import requests
from textblob import TextBlob
import os
import random  # You forgot to import this for job/funding mock scores

# ✅ Use correct environment variable name
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY=378fab4bb3624e76992beefa2dad2f5f")  # Make sure your .env has: NEWSAPI_KEY=your_key_here

def get_news_sentiment(company_name):
    url = f"https://newsapi.org/v2/everything?q={company_name}&language=en&sortBy=publishedAt&pageSize=10&apiKey={NEWSAPI_KEY}"
    try:
        res = requests.get(url)
        articles = res.json().get("articles", [])
        if not articles:
            return 50  # Neutral score

        sentiment_scores = []
        for article in articles:
            title = article.get("title", "")
            if title:
                blob = TextBlob(title)
                sentiment_scores.append(blob.sentiment.polarity)

        avg_score = sum(sentiment_scores) / len(sentiment_scores)
        normalized_score = int((avg_score + 1) * 50)  # Convert [-1, 1] → [0, 100]
        return normalized_score
    except:
        return 50  # fallback

def get_momentum_score(company_name):
    # Simulated values (you can replace these with real data later)
    job_score = random.randint(30, 100)
    funding_score = random.randint(30, 100)
    traffic_score = random.randint(30, 100)
    linkedin_growth_score = random.randint(30, 100)

    news_sentiment_score = get_news_sentiment(company_name)

    # Weighted score
    final_score = int(
        0.25 * job_score +
        0.15 * funding_score +
        0.2  * traffic_score +
        0.3  * news_sentiment_score +
        0.1  * linkedin_growth_score
    )

    if final_score > 75:
        badge = "🟢 <strong>Surging</strong>"
    elif final_score > 50:
        badge = "🟡 <strong>Growing</strong>"
    else:
        badge = "🔴 <strong>Flat</strong>"

    return final_score, badge
