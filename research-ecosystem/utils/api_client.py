import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()

class NewsAPIClient:
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')
        self.base_url = "https://newsapi.org/v2/everything"
        self.logger = logging.getLogger(__name__)
    
    def get_news(self):
        try:
            response = requests.get(
                self.base_url,
                params={
                    'q': 'technology',
                    'apiKey': self.api_key,
                    'pageSize': 20,
                    'sortBy': 'publishedAt'
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json().get('articles', [])
        except requests.exceptions.RequestException as e:
            self.logger.error(f"News API Error: {e}")
            return []