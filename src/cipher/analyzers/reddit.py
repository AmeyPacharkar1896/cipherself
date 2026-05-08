from datetime import datetime

class RedditAnalyzer:
    def __init__(self, reddit_data, github_data=None):
        self.reddit_data = reddit_data
        self.github_data = github_data

    def infer(self):
        if not self.reddit_data:
            return []
        
        inferences = []
        subreddits = self.reddit_data.get('top_subreddits', {})
        karma = self.reddit_data.get('total_karma', 0)
        created_utc = self.reddit_data.get('created_utc')
        avg_len = self.reddit_data.get('avg_comment_length', 0)
        most_active_hour = self.reddit_data.get('most_active_hour')

        # 1. Technical Presence
        tech_subs = {'programming', 'python', 'rust', 'golang', 'netsec', 'cybersecurity', 'linux', 'devops', 'compsci'}
        if any(sub.lower() in tech_subs for sub in subreddits):
            inferences.append("Subject maintains active technical community presence beyond professional platforms.")
        
        # 2. Identity Separation
        if self.github_data and most_active_hour is not None:
            gh_hours = self.github_data.get('activity_stats', {}).get('hours', {})
            if gh_hours:
                gh_peak = sorted(gh_hours.items(), key=lambda x: x[1], reverse=True)[0][0]
                if abs(gh_peak - most_active_hour) > 3:
                    inferences.append("Divergence between professional and social activity windows suggests distinct work/personal identity separation.")
        
        # 3. Communication Style
        if avg_len > 200:
            inferences.append("Subject prefers long-form discussion over quick reactions — indicates analytical communication style.")
        
        # 4. Community Norms
        if created_utc:
            years = (datetime.now() - datetime.fromtimestamp(created_utc)).days / 365
            if years > 5:
                inferences.append("Long-term Reddit presence suggests comfort with pseudonymous identity and online community norms.")
        
        # 5. Engagement Level
        if karma < 100:
            inferences.append("Minimal Reddit engagement suggests lurker behavior — subject consumes more than they contribute publicly.")
        elif karma > 10000:
            inferences.append("High karma accumulation indicates subject actively shapes community discussions.")

        return inferences[:3] if len(inferences) >= 3 else inferences
