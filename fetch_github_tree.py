import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def get_github_tree(repo, path=""):
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for item in data:
                print(f"[{item['type']}] {item['path']} ({item.get('size', 0)} bytes)")
                if item['type'] == 'dir':
                    get_github_tree(repo, item['path'])
    except Exception as e:
        print(f"Error fetching {url}: {e}")

get_github_tree("Maniac2017/repository.estupalant")
