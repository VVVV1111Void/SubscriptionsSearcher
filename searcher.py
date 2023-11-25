import json
import subprocess
import sqlite3
import time
import pandas as pd
import datetime
import ast
import os
CSV_FILE = './input/subscriptions.csv'

# YT-DLP's Prints to the terminal is not separatable due to said separation characters appearing in video titles.
# So we have to use randomized separators to manually separate each entry as YT-DLP prints it out.
TITLE_URL_DESC_SEP = 'SEPTHING_5021020401'
VIDEO_SEPARATOR = '69tjl1lfj2uf1'
ENCOUNTERED_FILE = 'encountered.txt'
CACHE_FILE = 'cache.txt'
DB = 'subscriptions.db'
SLEEP_INT = 1.25
FORMAT = f"%(title)s{TITLE_URL_DESC_SEP}%(webpage_url)s{TITLE_URL_DESC_SEP}%(description)s{VIDEO_SEPARATOR}"

def load_cache():
    # Read the cache for channels that were scanned for videos before.
    last_run = '20000718'
    encountered = []

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, mode='r+') as f:
            last_run: str = f.read().strip()

    if os.path.exists(ENCOUNTERED_FILE):
        with open(ENCOUNTERED_FILE, mode='r+') as f:
            content = f.read()
            encountered: list[str] = ast.literal_eval(content)

    return last_run, encountered

def to_channel_url(channelID: str):
    if not channelID.startswith('http://www.youtube.com/channel/'):
        return f'http://www.youtube.com/channel/{channelID}/videos' # Limit the scope to youtube videos
    return channelID

def download_channel_info(subscriptions: list = []):
    videos: list[tuple[str, str, str]] = [] # title, url, desc
    failed = []
    last_run, encountered = load_cache()
    for sub in subscriptions:
        time.sleep(SLEEP_INT) # Youtube blocks too much downloads within a short period of time.
        # For new channels, download all videos
        command = ["yt-dlp", "-i", "--flat-playlist", '--print', f'{FORMAT}', to_channel_url(sub)]
        # For old channels, download new videos after the previous scan.
        if sub in encountered:
            command = ["yt-dlp", "-i", "--dateafter", f'{last_run}', "--flat-playlist", '--print', f'{FORMAT}', to_channel_url(sub)]
        try:
            out = subprocess.check_output(command, start_new_session=True).decode().strip()
            ch_vids = out.split(VIDEO_SEPARATOR) # Split into strings of title, url, and descriptions
            vids: list = [tuple(x.strip('\n').split(TITLE_URL_DESC_SEP)) for x in ch_vids if x != ''] # Separate urls, titles, and descriptions, remove empty strings
            videos.extend(vids)
        # Some channels will fail when they have no videos or are terminated. Save for later checking.
        except:
            failed.append(to_channel_url(sub))
            continue

    with open('failed.txt', mode='w+') as f:
        f.write(str(failed))
        f.close()
        f.write("\n-------------------------------\n")
    return videos


def main():
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()
    
    fl = pd.read_csv('./input/subscriptions.csv')
    col = 'Channel Id'
    subscriptions = fl[col].values.tolist()

    videos: list[tuple[str, str, str]] = download_channel_info(subscriptions)
    cursor.executemany("INSERT INTO videos VALUES (?, ?, ?)", videos)
    connection.commit()

    with open('encountered.txt', mode='wt+') as f:
        f.write(str(subscriptions))

    with open('cache.txt', mode='wt+',) as f:
        t = datetime.datetime.now()
        f_t = t.strftime("%Y%m%d")
        f.write(f_t)

main()