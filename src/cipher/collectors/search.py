import requests
import time
from bs4 import BeautifulSoup
from cipher.config.constants import USER_AGENT, GOOGLE_SEARCH_URL, DUCKDUCKGO_SEARCH_URL

class SearchCollector:
    def __init__(self, name):
        self.name = name

    def fetch_top_results(self, limit=10):
        print(f"[*] Attempting public search for \"{self.name}\"...")
        return self._fetch_duckduckgo_lite(self.name, limit)

    def _fetch_duckduckgo_lite(self, query, limit):
        results = []
        url = "https://lite.duckduckgo.com/lite/"
        data = {"q": query}
        headers = {"User-Agent": USER_AGENT}
        
        try:
            res = requests.post(url, data=data, headers=headers, timeout=10)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                for tr in soup.select("tr"):
                    a = tr.select_one("a.result-url")
                    snippet_elem = tr.select_one(".result-snippet")
                    
                    if a and snippet_elem:
                        snippet = snippet_elem.get_text(strip=True)
                        results.append({
                            "title": a.get_text(strip=True) or a.get("href"),
                            "url": a.get("href"),
                            "snippet": (snippet[:147] + "...") if len(snippet) > 150 else snippet
                        })
                        if len(results) >= limit:
                            break
        except Exception as e:
            print(f"[!] Search failed: {e}")
            
        return results
