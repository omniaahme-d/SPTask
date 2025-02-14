import random
import logging
import heapq
import numpy as np
from utils.report_generator import generate_report

class InnovationAgent:
    def __init__(self):
        self.ideas = []
        self.logger = logging.getLogger(__name__)

    def generate_ideas(self, insights):
        """Generate research ideas from analyzed insights"""
        if not insights:
            self.logger.warning("No insights provided for idea generation.")
            return []

        try:
            global_keywords = set()  # Track used keywords to avoid repetition

            ideas = [
                self._create_idea(insight, variation, global_keywords)
                for insight in insights
                for variation in range(2)  # Two variations per insight
            ]

            # Select the top 5 ideas based on priority score
            self.ideas = heapq.nlargest(5, ideas, key=lambda x: x['confidence'] * x['potential_impact'])
            generate_report(self.ideas)
            return self.ideas
        except Exception as e:
            self.logger.error(f"Innovation Error: {e}", exc_info=True)
            return []

    def _create_idea(self, insight, variation, global_keywords):
        """Generate unique research ideas with diverse focuses"""
        keywords = insight.get('keywords', [])
        primary_kw = next((kw for kw in keywords if kw not in global_keywords), "emerging tech")
        secondary_kw = next((kw for kw in keywords if kw not in [primary_kw] + list(global_keywords)), "AI applications")

        directions = [
            f"Advanced applications of {primary_kw} and {secondary_kw}",
            f"Ethical considerations in {primary_kw} development"
        ]

        global_keywords.update([primary_kw, secondary_kw])  # Prevent keyword repetition

        return {
            'trend_id': insight.get('trend_id', 'unknown'),
            'keywords': keywords,
            'potential_impact': random.randint(1, 10),
            'confidence': np.random.uniform(0.5, 1.0),  # More realistic confidence values
            'direction': directions[variation]
        }
