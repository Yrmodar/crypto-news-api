from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI(title="Crypto News API", version="1.0")

@app.get("/")
def home():
    return {"message": "Welcome to the Crypto News API"}

@app.get("/news")
def get_crypto_news():
    news_data = []

    # --- CoinDesk ---
    try:
        coindesk_url = "https://www.coindesk.com/"
        res = requests.get(coindesk_url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        articles = soup.find_all("a", class_="card-title", limit=5)

        for a in articles:
            title = a.get_text(strip=True)
            link = "https://www.coindesk.com" + a["href"]
            news_data.append({
                "source": "CoinDesk",
                "title": title,
                "url": link
            })
    except Exception as e:
        print("CoinDesk error:", e)

    # --- CoinTelegraph ---
    try:
        cointelegraph_url = "https://cointelegraph.com/"
        res = requests.get(cointelegraph_url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        articles = soup.find_all("a", class_="post-card-inline__title-link", limit=5)

        for a in articles:
            title = a.get_text(strip=True)
            link = "https://cointelegraph.com" + a["href"]
            news_data.append({
                "source": "CoinTelegraph",
                "title": title,
                "url": link
            })
    except Exception as e:
        print("CoinTelegraph error:", e)

    if not news_data:
        return {"error": "Unable to fetch crypto news at the moment."}

    return {"count": len(news_data), "news": news_data}
