import requests
import time
from collections import Counter
from datetime import datetime

class RedditCollector:
    def __init__(self, username):
        self.username = username
        self.headers = {
            "User-Agent": "cipherself/1.0 by cipherself-tool"
        }

    def fetch_all(self):
        print(f"[*] Fetching Reddit intelligence for u/{self.username}...")
        profile = self._fetch_profile()
        if not profile:
            return None
        
        time.sleep(1)
        comments = self._fetch_comments()
        
        time.sleep(1)
        posts = self._fetch_posts()
        
        # Process results
        about = profile.get('data', {})
        total_karma = about.get('comment_karma', 0) + about.get('link_karma', 0)
        created_utc = about.get('created_utc')
        
        # Subreddit activity
        subreddits = Counter([c.get('data', {}).get('subreddit') for c in comments])
        
        # Hours activity
        hours = Counter()
        for item in (comments + posts):
            ts = item.get('data', {}).get('created_utc')
            if ts:
                dt = datetime.fromtimestamp(ts)
                hours[dt.hour] += 1
        
        # Comment lengths
        comment_bodies = [c.get('data', {}).get('body', '') for c in comments]
        avg_len = sum(len(b) for b in comment_bodies) / len(comment_bodies) if comment_bodies else 0
        
        data = {
            "username": self.username,
            "created_utc": created_utc,
            "total_karma": total_karma,
            "top_subreddits": dict(subreddits.most_common(5)),
            "last_posts": [p.get('data', {}).get('title') for p in posts[:20]],
            "last_comments": [c.get('data', {}).get('body') for c in comments[:20]],
            "most_active_hour": hours.most_common(1)[0][0] if hours else None,
            "avg_comment_length": avg_len
        }
        return data

    def _fetch_profile(self):
        url = f"https://www.reddit.com/user/{self.username}/about.json"
        try:
            res = requests.get(url, headers=self.headers, timeout=10)
            if res.status_code == 200:
                return res.json()
            elif res.status_code == 404:
                print(f"[!] Reddit user u/{self.username} not found.")
            elif res.status_code == 403:
                print(f"[!] Reddit user u/{self.username} profile is private.")
        except Exception as e:
            print(f"[!] Reddit profile fetch failed: {e}")
        return None

    def _fetch_comments(self):
        url = f"https://www.reddit.com/user/{self.username}/comments.json?limit=100"
        try:
            res = requests.get(url, headers=self.headers, timeout=10)
            if res.status_code == 200:
                return res.json().get('data', {}).get('children', [])
        except Exception:
            pass
        return []

    def _fetch_posts(self):
        url = f"https://www.reddit.com/user/{self.username}/submitted.json?limit=100"
        try:
            res = requests.get(url, headers=self.headers, timeout=10)
            if res.status_code == 200:
                return res.json().get('data', {}).get('children', [])
        except Exception:
            pass
        return []
