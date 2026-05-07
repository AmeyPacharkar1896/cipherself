from datetime import datetime
from cipherself.config import DEMO_DATA

class PersonalityAnalyzer:
    def __init__(self, data, demo_mode=False):
        self.data = data
        self.demo_mode = demo_mode

    def infer(self):
        if self.demo_mode:
            return " ".join(DEMO_DATA["personality_inferences"])
        
        profile = self.data.get('profile', {})
        languages = self.data.get('languages', {})
        activity = self.data.get('activity_stats', {})
        repos = self.data.get('repos_count', 0)
        stars = self.data.get('stars', 0)
        
        inferences = []
        
        # 1. Nocturnal Check
        hours = activity.get('hours', {})
        total_commits = sum(hours.values())
        if total_commits > 0:
            night_commits = sum(count for hour, count in hours.items() if 0 <= hour <= 6)
            if (night_commits / total_commits) > 0.3:
                inferences.append("Subject shows nocturnal work patterns suggesting self-directed work environment.")
        
        # 2. Systems Focus
        systems_langs = {'C', 'Rust', 'Assembly', 'C++', 'Go'}
        if any(lang in systems_langs for lang in languages):
            inferences.append("Low-level systems focus indicates preference for precision over abstraction.")
        
        # 3. Disciplined Check (Account Age)
        created_at = profile.get('created_at')
        if created_at:
            dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
            years = (datetime.now() - dt).days / 365
            if years >= 10:
                inferences.append("Long-term consistent presence suggests disciplined, non-trend-driven approach to technology.")
        
        # 4. Quality Over Quantity (Stars/Repo ratio)
        if repos > 0:
            ratio = stars / repos
            if stars > 500 and ratio > 10:
                inferences.append("High community impact relative to repository count suggests quality over quantity output.")
        
        # 5. Breadth of Influence (Languages)
        if len(languages) >= 5:
            inferences.append("Broad technological stack suggests high adaptability and cross-domain competency.")
        
        # 6. Active Contributor
        last_active = self.data.get('last_active')
        if last_active:
            dt = datetime.strptime(last_active, "%Y-%m-%dT%H:%M:%SZ")
            days_since = (datetime.now() - dt).days
            if days_since < 30 and total_commits > 50:
                inferences.append("Recent high-intensity activity indicates subject is currently engaged in high-value output cycles.")

        if not inferences:
            return "Subject maintains a focused digital presence with specific technological interests."
            
        return " ".join(inferences[:5])
