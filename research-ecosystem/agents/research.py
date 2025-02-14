import logging
from datetime import datetime, timedelta
from utils.api_client import NewsAPIClient
import requests
class ResearchAgent:
    def __init__(self):
        self.api_client = NewsAPIClient()
        self.logger = logging.getLogger(__name__)

    def fetch_data(self):
        """Fetch data with fallback to simulated data"""
        try:
            data = self.api_client.get_news()
            if not data:
                self.logger.warning("Empty API response, using simulated data.")
                return self.simulate_data()
            return self.preprocess(data)
        except (requests.RequestException, ValueError) as e:
            self.logger.error(f"API Error: {e}, falling back to simulated data.")
            return self.simulate_data()

    def preprocess(self, data):
        """Optimized preprocessing pipeline"""
        return [
            {
                'title': item.get('title', 'No Title').strip(),
                'content': item.get('content', '')[:500],  # Truncate
                'published_at': self.parse_date(item.get('publishedAt')),
                'source': item.get('source', {}).get('name', 'Unknown')
            }
            for item in data
        ]

    def parse_date(self, date_str):
        """Safely parse date string with fallback"""
        try:
            return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ') if date_str else datetime.utcnow()
        except ValueError:
            self.logger.warning(f"Invalid date format: {date_str}, using current time.")
            return datetime.utcnow()

    def simulate_data(self):
        """Fallback simulated data"""
        return [{
            'title': 'Simulated Tech Breakthrough in AI',
            'content': 'Researchers announce simulated progress in neural networks...',
            'published_at': datetime.utcnow() - timedelta(hours=1),
            'source': 'Simulated News'
        }]
