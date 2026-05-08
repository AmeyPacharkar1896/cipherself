import requests
headers = {"User-Agent": "cipher/1.0 by cipher-tool"}
print("Comments:")
r = requests.get("https://www.reddit.com/user/spez/comments.json?limit=10", headers=headers)
print(r.status_code, r.text[:200])
print("Posts:")
r = requests.get("https://www.reddit.com/user/spez/submitted.json?limit=10", headers=headers)
print(r.status_code, r.text[:200])
