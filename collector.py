import requests
import json
from datetime import datetime
from collections import Counter
from googlesearch import search
from bs4 import BeautifulSoup
import time
import random

class GitHubCollector:
    BASE_URL = "https://api.github.com"

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
            "pinned_readmes": self._fetch_pinned_readmes(repos[:5]), # Proxy for pinned: first 5
            "last_active": self._get_last_active(events)
        }
        return data

    def _fetch_profile(self):
        response = requests.get(f"{self.BASE_URL}/users/{self.username}", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None

    def _fetch_repos(self):
        response = requests.get(f"{self.BASE_URL}/users/{self.username}/repos?per_page=100", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return []

    def _fetch_events(self):
        # Events API provides recent activity (last 90 days or 300 events)
        response = requests.get(f"{self.BASE_URL}/users/{self.username}/events?per_page=100", headers=self.headers)
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
            # Try to get README content
            readme_url = f"{self.BASE_URL}/repos/{self.username}/{name}/readme"
            response = requests.get(readme_url, headers=self.headers)
            if response.status_code == 200:
                content_data = response.json()
                # Content is base64 encoded, but we just want a snippet or summary
                # For now, let's just store the URL or a small part if possible
                readmes.append({"repo": name, "url": content_data.get("html_url")})
        return readmes

    def _get_last_active(self, events):
        if events:
            return events[0].get("created_at")
        return None

class SearchCollector:
    def __init__(self, name):
        self.name = name

    def fetch_top_results(self, limit=10):
        results = []
        query = f'"{self.name}"'
        
        # 1. Try Google
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        
        try:
            print(f"[*] Attempting Google search for {query}...")
            url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
            res = requests.get(url, headers=headers, timeout=10)
            
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                # Look for div.g elements
                for g in soup.select("div.g")[:limit]:
                    title_elem = g.select_one("h3")
                    link_elem = g.select_one("a")
                    snippet_elem = g.select_one("div[style*='-webkit-line-clamp']") or g.select_one(".VwiC3b")
                    
                    if title_elem and link_elem:
                        results.append({
                            "title": title_elem.get_text(),
                            "url": link_elem.get("href"),
                            "snippet": (snippet_elem.get_text()[:147] + "...") if snippet_elem and len(snippet_elem.get_text()) > 150 else (snippet_elem.get_text() if snippet_elem else "No snippet available.")
                        })
            
            if len(results) < 5:
                print("[!] Google results insufficient or blocked. Falling back to DuckDuckGo...")
                time.sleep(3) # Delay before fallback
                results += self._fetch_duckduckgo(query, limit - len(results))
                
        except Exception as e:
            print(f"[!] Google search failed: {e}. Falling back to DuckDuckGo...")
            results = self._fetch_duckduckgo(query, limit)
            
        return results[:limit]

    def _fetch_duckduckgo(self, query, limit):
        results = []
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        try:
            url = f"https://duckduckgo.com/html/?q={requests.utils.quote(query)}"
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                for item in soup.select(".result")[:limit]:
                    title_elem = item.select_one(".result__a")
                    snippet_elem = item.select_one(".result__snippet")
                    if title_elem:
                        snippet = snippet_elem.get_text() if snippet_elem else "No snippet available."
                        results.append({
                            "title": title_elem.get_text(),
                            "url": title_elem.get("href"),
                            "snippet": (snippet[:147] + "...") if len(snippet) > 150 else snippet
                        })
        except Exception as e:
            print(f"[!] DuckDuckGo search failed: {e}")
        return results
