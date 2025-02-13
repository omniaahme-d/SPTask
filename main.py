import requests
import time
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_articles(api_key, country='us', retries=3, timeout=10):
    """
    Fetch articles from NewsAPI with error handling.
    """
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": country,
        "apiKey": api_key
    }
    
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()  # Raise error for bad responses
            data = response.json()
            if data.get("status") != "ok":
                raise ValueError("API did not return OK status")
            return data.get("articles", [])
        except requests.exceptions.RequestException as e:
            print(f"[Attempt {attempt+1}] Request error: {e}. Retrying in 5 seconds...")
            attempt += 1
            time.sleep(5)
    print("Failed to fetch articles after multiple attempts.")
    return []

def remove_duplicate_articles(articles):
    """
    Remove duplicate articles based on their title.
    """
    seen_titles = set()
    unique_articles = []
    for article in articles:
        title = article.get("title")
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_articles.append(article)
    return unique_articles

def extract_keywords(text):
    """
    Extract keywords from text by removing punctuation, lowering case,
    splitting into words, and filtering out common stopwords.
    """
    if not text:
        return []
    
    # Define simple stopwords and remove punctuation
    stopwords = {"the", "and", "of", "to", "in", "a", "for", "on", "is", "at", "with", "as", "by", "from"}
    text = re.sub(r"[^\w\s]", "", text).lower()
    words = text.split()
    # Filter out stopwords and short words
    keywords = [word for word in words if word not in stopwords and len(word) > 2]
    return keywords

def process_articles(articles):
    """
    Process articles by removing duplicates and extracting keywords.
    Adds a new field 'keywords' to each article.
    """
    unique_articles = remove_duplicate_articles(articles)
    for article in unique_articles:
        # Combine title and description to form a text block for keyword extraction
        combined_text = f"{article.get('title', '')} {article.get('description', '')}"
        article["keywords"] = extract_keywords(combined_text)
    return unique_articles

def main():
    if not NEWS_API_KEY:
        print("ERROR: Please set the NEWS_API_KEY in your .env file.")
        return

    # Step 1: Fetch articles from the API
    articles = fetch_articles(NEWS_API_KEY)
    if not articles:
        return

    # Step 2: Filter and preprocess data (remove duplicates and extract keywords)
    processed_articles = process_articles(articles)

    # Display the processed articles
    for idx, article in enumerate(processed_articles, start=1):
        print(f"\nArticle {idx}:")
        print(f"Title: {article.get('title')}")
        print(f"Keywords: {article.get('keywords')}")
    
if __name__ == "__main__":
    main()
