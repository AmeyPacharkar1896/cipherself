from cipherself.config import (
    DEMO_DATA, CPM_LOW, CPM_HIGH, BROKER_LOW, BROKER_HIGH, ACTIVE_YEARS
)

class ValuationAnalyzer:
    def __init__(self, data, demo_mode=False):
        self.data = data
        self.demo_mode = demo_mode

    def calculate(self):
        if self.demo_mode:
            return DEMO_DATA["valuation"]

        profile = self.data.get('profile', {})
        repos = self.data.get('repos_count', 0)
        stars = self.data.get('stars', 0)
        search_count = len(self.data.get('search_results', []))
        location = (profile.get('location') or '').lower()
        
        # Multipliers
        loc_mult = 1.5 if ('united states' in location or 'usa' in location or 'us' == location) else 1.0
        
        if repos > 50 or stars > 100:
            activity_level = "High"
        elif repos > 10:
            activity_level = "Medium"
        else:
            activity_level = "Low"
            
        mention_mult = 1.0 + (min(search_count, 10) * 0.05)
        
        # Calculations
        google = (CPM_HIGH if activity_level == "High" else CPM_LOW) * loc_mult * mention_mult / 10.0
        meta = (CPM_HIGH * 0.6 if activity_level == "High" else CPM_LOW * 0.6) * loc_mult * mention_mult / 10.0
        brokers = (BROKER_HIGH if activity_level == "High" else BROKER_LOW) * loc_mult * mention_mult
        
        total = google + meta + brokers
        total = max(2.0, min(total, 50.0))
        lifetime = total * 12 * ACTIVE_YEARS
        
        # Richness Score
        if stars > 50000 or search_count > 7:
            richness = "High"
        elif stars >= 1000 or (3 <= search_count <= 7):
            richness = "Medium"
        else:
            richness = "Low"
        
        return {
            "google": google,
            "meta": meta,
            "brokers": brokers,
            "total": total,
            "lifetime": lifetime,
            "richness": richness
        }
