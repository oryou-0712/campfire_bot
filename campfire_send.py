import os
import csv
import random
import time
from datetime import datetime
from utils import get_target_urls, get_user_id_from_url, has_hearted, send_discord_notification

SEND_LIMIT = 300
CSV_LOG_FILE = 'send_log.csv'
PROGRESS_FILE = 'send_progress.txt'
SKIP_USER_FILE = 'skip_user_ids.txt'
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1362319619934785577/FDVzt64ahdjxdDTgiTNEbb-mtdDLZ1ddiT4_MG8aOXDVwxM3UR7CXVGTnZ-MiDI9geSs'
TEMPLATE_MESSAGE = 'ホマレです！このプロジェクト素敵ですね！応援しています！'

def load_skip_user_ids():
    if not os.path.exists(SKIP_USER_FILE):
        return set()
    with open(SKIP_USER_FILE, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

def log_result(url, user_id, status, reason=''):
    file_exists = os.path.isfile(CSV_LOG_FILE)
    with open(CSV_LOG_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['timestamp', 'url', 'user_id', 'status', 'reason'])
        writer.writerow([datetime.now().isoformat(), url, user_id, status, reason])

def append_progress(count):
    with open(PROGRESS_FILE, 'a', encoding='utf-8') as f:
        f.write(f'{datetime.now().isoformat()} - Sent {count} projects\n')

def main():
    urls = get_target_urls()
    skip_user_ids = load_skip_user_ids()
    sent_count = 0

    for url in urls:
        if sent_count >= SEND_LIMIT:
            break
        try:
            user_id = get_user_id_from_url(url)
            if user_id in skip_user_ids:
                log_result(url, user_id, 'skipped', 'already_sent')
                continue
            if has_hearted(url):
                log_result(url, user_id, 'skipped', 'hearted')
                continue
            # メッセージ送信処理（仮実装）
            print(f'[送信] {url} -> {user_id}')
            log_result(url, user_id, 'success')
            sent_count += 1
            with open(SKIP_USER_FILE, 'a', encoding='utf-8') as skipfile:
                skipfile.write(f'{user_id}\n')
            time.sleep(0.5)
        except Exception as e:
            log_result(url, '', 'error', str(e))
            continue

    append_progress(sent_count)
    send_discord_notification(DISCORD_WEBHOOK_URL, f'【送信完了】本日の送信数: {sent_count}件')

if __name__ == '__main__':
    print("クラファン自動質問BOT 起動中 ...")
    main()