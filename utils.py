import requests
from bs4 import BeautifulSoup
import re

def get_target_urls():
    # 仮のURLリスト
    return [
        "https://camp-fire.jp/projects/view/123456",
        "https://camp-fire.jp/projects/view/789012"
    ]

def get_user_id_from_url(url):
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.text, 'html.parser')
        creator_elem = soup.find("a", class_="project-owner-name")
        if not creator_elem:
            return None
        href = creator_elem.get("href", "")
        match = re.search(r'/users/([^/]+)', href)
        if match:
            return match.group(1)
        return None
    except Exception:
        return None

def has_hearted(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        return 'unlike-button' in res.text or 'js-unlike-button' in res.text
    except Exception:
        return False

def send_discord_notification(webhook_url, message):
    try:
        data = {"content": message}
        headers = {"Content-Type": "application/json"}
        response = requests.post(webhook_url, json=data, headers=headers)
        return response.status_code == 204
    except Exception:
        return False
