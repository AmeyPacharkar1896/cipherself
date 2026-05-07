import requests
import time
from bs4 import BeautifulSoup
from cipherself.config import USER_AGENT, GOOGLE_SEARCH_URL, DUCKDUCKGO_SEARCH_URL

class SearchCollector:
    def __init__(self, name):
        self.name = name

    def fetch_top_results(self, limit=10):
        results = []
        query = f'"{self.name}"'
        headers = {"User-Agent": USER_AGENT}
        
        try:
            print(f"[*] Attempting Google search for {query}...")
            url = f"{GOOGLE_SEARCH_URL}{requests.utils.quote(query)}"
            res = requests.get(url, headers=headers, timeout=10)
            
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                for g in soup.select("div.g")[:limit]:
                    title_elem = g.select_one("h3")
                    link_elem = g.select_one("a")
                    snippet_elem = g.select_one("div[style*='-webkit-line-clamp']") or g.select_one(".VwiC3b")
                    
                    if title_elem and link_elem:
                        snippet_text = snippet_elem.get_text() if snippet_elem else "No snippet available."
                        results.append({
                            "title": title_elem.get_text(),
                            "url": link_elem.get("href"),
                            "snippet": (snippet_text[:147] + "...") if len(snippet_text) > 150 else snippet_text
                        })
            
            if len(results) < 5:
                print("[!] Google results insufficient or blocked. Falling back to DuckDuckGo...")
                time.sleep(3)
                results += self._fetch_duckduckgo(query, limit - len(results))
                
        except Exception as e:
            print(f"[!] Google search failed: {e}. Falling back to DuckDuckGo...")
            results = self._fetch_duckduckgo(query, limit)
            
        return results[:limit]

    def _fetch_duckduckgo(self, query, limit):
        results = []
        headers = {"User-Agent": USER_AGENT}
        try:
            url = f"{DUCKDUCKGO_SEARCH_URL}{requests.utils.quote(query)}"
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
