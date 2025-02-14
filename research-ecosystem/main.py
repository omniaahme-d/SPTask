import logging
from agents.research import ResearchAgent
from agents.analysis import AnalysisAgent
from agents.innovation import InnovationAgent
from utils.messaging import MessageBus
import time
import sys
import os
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent))
def main():
    logging.basicConfig(level=logging.INFO)
    
    # Initialize components
    message_bus = MessageBus()
    research_agent = ResearchAgent()
    analysis_agent = AnalysisAgent()
    innovation_agent = InnovationAgent()
    
    
    while True:
        try:
            # Research Phase
            news_data = research_agent.fetch_data()
            message_bus.post('analysis', news_data)
            print(news_data)
            
            # Analysis Phase
            raw_data = message_bus.get('analysis')
            insights = analysis_agent.detect_trends(raw_data)
            message_bus.post('innovation', insights)
            
            # Innovation Phase
            insights = message_bus.get('innovation')
            innovation_agent.generate_ideas(insights)
            
            time.sleep(3600)  # Run hourly
            
        except KeyboardInterrupt:
            logging.info("Shutting down ecosystem...")
            break

if __name__ == "__main__":
    main()