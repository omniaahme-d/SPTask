from datetime import datetime

def generate_report(ideas):
    report = f"""# Research Innovation Report\n*Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"""
    
    for idx, idea in enumerate(ideas, 1):
        report += f"""## Idea #{idx}\n
- **Focus Area**: {idea['direction']}
- **Keywords**: {', '.join(idea['keywords'])}
- **Potential Impact**: {idea['potential_impact']}/10
- **Confidence**: {idea['confidence']*100:.1f}%\n\n"""
    
    with open('innovation_report.md', 'w') as f:
        f.write(report)