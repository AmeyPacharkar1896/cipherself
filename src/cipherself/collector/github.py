import requests
from datetime import datetime
from collections import Counter
from cipherself.config import GITHUB_BASE_URL

class GitHubCollector:
    def __init__(self, username):
        self.username = username
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "cipherself-cli"
        }

    def fetch_all(self):
        profile = self._fetch_profile()
        if not profile:
            return None
        
        repos = self._fetch_repos()
        events = self._fetch_events()
        
        data = {
            "profile": profile,
            "repos_count": len(repos),
            "languages": self._calculate_languages(repos),
            "stars": sum(r.get("stargazers_count", 0) for r in repos),
            "activity_stats": self._process_events(events),
            "pinned_readmes": self._fetch_pinned_readmes(repos[:5]),
            "last_active": self._get_last_active(events)
        }
        return data

    def _fetch_profile(self):
        response = requests.get(f"{GITHUB_BASE_URL}/users/{self.username}", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None

    def _fetch_repos(self):
        response = requests.get(f"{GITHUB_BASE_URL}/users/{self.username}/repos?per_page=100", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return []

    def _fetch_events(self):
        response = requests.get(f"{GITHUB_BASE_URL}/users/{self.username}/events?per_page=100", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return []

    def _calculate_languages(self, repos):
        languages = Counter()
        for repo in repos:
            lang = repo.get("language")
            if lang:
                languages[lang] += 1
        return dict(languages.most_common(5))

    def _process_events(self, events):
        hours = Counter()
        days = Counter()
        for event in events:
            if event.get("type") == "PushEvent":
                created_at = event.get("created_at")
                dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                hours[dt.hour] += 1
                days[dt.strftime("%A")] += 1
        
        return {
            "hours": dict(hours),
            "days": dict(days)
        }

    def _fetch_pinned_readmes(self, repos):
        readmes = []
        for repo in repos:
            name = repo.get("name")
            readme_url = f"{GITHUB_BASE_URL}/repos/{self.username}/{name}/readme"
            response = requests.get(readme_url, headers=self.headers)
            if response.status_code == 200:
                content_data = response.json()
                readmes.append({"repo": name, "url": content_data.get("html_url")})
        return readmes

    def _get_last_active(self, events):
        if events:
            return events[0].get("created_at")
        return None
