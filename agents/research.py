import requests
from datetime import datetime, timedelta
from ..utils.api_client import NewsAPIClient
import logging

class ResearchAgent:
    def __init__(self):
        self.api_client = NewsAPIClient()
        self.logger = logging.getLogger(__name__)
    
    def fetch_data(self):
        """Fetch data with fallback to simulated data"""
        try:
            data = self.api_client.get_news()
            if not data:
                raise ValueError("Empty API response")
            return self.preprocess(data)
        except Exception as e:
            self.logger.error(f"API Error: {e}")
            return self.simulate_data()
    
    def preprocess(self, data):
        """Basic preprocessing pipeline"""
        processed = []
        for item in data:
            processed.append({
                'title': item['title'].strip(),
                'content': item['content'][:500],  # Truncate
                'published_at': datetime.strptime(item['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'),
                'source': item['source']['name']
            })
        return processed
    
    def simulate_data(self):
        """Fallback simulated data"""
        return [{
            'title': 'Simulated Tech Breakthrough in AI',
            'content': 'Researchers announce simulated progress in neural networks...',
            'published_at': datetime.now() - timedelta(hours=1),
            'source': 'Simulated News'
        }]