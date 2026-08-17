import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://raw.githubusercontent.com/Maniac2017/repository.estupalant/main/Repo/repo_prep.py"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
        with open("repo_prep.py", "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Downloaded repo_prep.py ({len(content)} chars)")
except Exception as e:
    print("Error:", e)
