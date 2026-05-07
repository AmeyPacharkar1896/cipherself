from datetime import datetime
from cipherself.config.valuation_rules import (
    BASE_RATES, GITHUB_MULTIPLIERS, REDDIT_MULTIPLIERS, 
    SEARCH_MULTIPLIERS, LIFETIME_ACTIVE_YEARS
)
from cipherself.config import DEMO_DATA

class ValuationAnalyzer:
    def __init__(self, github_data=None, reddit_data=None, demo_mode=False):
        self.github_data = github_data
        self.reddit_data = reddit_data
        self.demo_mode = demo_mode

    def calculate(self):
        if self.demo_mode:
            return DEMO_DATA["valuation"]

        total_multiplier = 1.0
        sources_analyzed = []

        # 1. GitHub Multipliers
        if self.github_data and 'profile' in self.github_data:
            gh_mult = GITHUB_MULTIPLIERS["has_github"]
            stars = self.github_data.get('stars', 0)
            if stars > 10000: gh_mult *= GITHUB_MULTIPLIERS["stars_over_10000"]
            elif stars > 1000: gh_mult *= GITHUB_MULTIPLIERS["stars_over_1000"]
            elif stars > 100: gh_mult *= GITHUB_MULTIPLIERS["stars_over_100"]
            
            location = (self.github_data.get('profile', {}).get('location') or '').lower()
            if any(term in location for term in ['united states', 'usa', 'us']):
                gh_mult *= GITHUB_MULTIPLIERS["us_location"]
            
            last_active = self.github_data.get('last_active')
            if last_active:
                dt = datetime.strptime(last_active, "%Y-%m-%dT%H:%M:%SZ")
                if (datetime.now() - dt).days < 30:
                    gh_mult *= GITHUB_MULTIPLIERS["active_last_30_days"]
            
            if self.github_data.get('repos_count', 0) > 10:
                gh_mult *= GITHUB_MULTIPLIERS["over_10_repos"]
            
            total_multiplier *= gh_mult
            sources_analyzed.append("GitHub")

        # 2. Reddit Multipliers
        if self.reddit_data:
            rd_mult = REDDIT_MULTIPLIERS["has_reddit"]
            karma = self.reddit_data.get('total_karma', 0)
            if karma > 10000: rd_mult *= REDDIT_MULTIPLIERS["karma_over_10000"]
            elif karma > 1000: rd_mult *= REDDIT_MULTIPLIERS["karma_over_1000"]
            elif karma > 100: rd_mult *= REDDIT_MULTIPLIERS["karma_over_100"]
            
            created_utc = self.reddit_data.get('created_utc')
            if created_utc:
                years = (datetime.now() - datetime.fromtimestamp(created_utc)).days / 365
                if years > 5: rd_mult *= REDDIT_MULTIPLIERS["account_over_5_years"]
                elif years > 2: rd_mult *= REDDIT_MULTIPLIERS["account_over_2_years"]
            
            # Check tech subreddits
            tech_subs = {'programming', 'python', 'rust', 'golang', 'netsec', 'cybersecurity', 'linux', 'devops', 'compsci'}
            if any(sub.lower() in tech_subs for sub in self.reddit_data.get('top_subreddits', {})):
                rd_mult *= REDDIT_MULTIPLIERS["active_in_tech_subreddits"]
                
            if len(self.reddit_data.get('top_subreddits', {})) >= 5:
                rd_mult *= REDDIT_MULTIPLIERS["over_5_active_subreddits"]
                
            total_multiplier *= rd_mult
            sources_analyzed.append("Reddit")

        # 3. Search Multipliers
        search_results = self.github_data.get('search_results', []) if self.github_data else []
        if search_results:
            s_mult = SEARCH_MULTIPLIERS["has_public_mentions"]
            if len(search_results) >= 5:
                s_mult *= SEARCH_MULTIPLIERS["over_5_mentions"]
            total_multiplier *= s_mult
            sources_analyzed.append("Public Records")

        # Final Calculations
        google = BASE_RATES["google_ads"] * total_multiplier
        meta = BASE_RATES["meta_ads"] * total_multiplier
        brokers = BASE_RATES["data_brokers"] * total_multiplier
        
        monthly_total = google + meta + brokers
        lifetime = monthly_total * 12 * LIFETIME_ACTIVE_YEARS
        
        # Richness Score
        source_count = len(sources_analyzed)
        if source_count >= 3:
            richness = "High"
        elif source_count == 2:
            richness = "Medium"
        else:
            richness = "Low"

        return {
            "google": google,
            "meta": meta,
            "brokers": brokers,
            "total": monthly_total,
            "lifetime": lifetime,
            "richness": richness,
            "sources": ", ".join(sources_analyzed) if sources_analyzed else "None"
        }
