import requests
from bs4 import BeautifulSoup
url = "https://lite.duckduckgo.com/lite/"
data = {"q": "Linus Torvalds"}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
res = requests.post(url, data=data, headers=headers)
print("Status:", res.status_code)
if res.status_code == 200:
    soup = BeautifulSoup(res.text, 'html.parser')
    for tr in soup.select('tr'):
        a = tr.select_one('a.result-url')
        if a:
            print("URL:", a.get('href'))
        snippet = tr.select_one('.result-snippet')
        if snippet:
            print("Snippet:", snippet.text.strip())
