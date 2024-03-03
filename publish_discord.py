from util import *
import random
import json
from pprint import pprint
import hashlib
import sys
import os
from discordwebhook import Discord

NO_IMG_HASH = '5d6737777450ade1eae0106458ddaea4'
DISCORD_WEBHOOK_URL = os.environ['DISCORD_WEBHOOK_URL']


def get_random_media_key():
    # combined_data.jsonを読み込んでランダムにmediaキーを取得する
    # んでファイルパスだけ返す
    with open('combined_data.json', 'r') as f:
        data = json.load(f)
    raw_json = random.choice(data)
    id = raw_json['id']
    length = len(raw_json['media'])
    return [f'./img/{id}_{i}.png' for i in range(length)]


def get_md5(path):
    with open(path, 'rb') as f:
        data = f.read()
    return hashlib.md5(data).hexdigest()


def port_discord(path, text):
    discord = Discord(url=DISCORD_WEBHOOK_URL)
    with open(path, 'rb') as f:
        discord.post(content=text, file={"attachment": f})


# 取得したリストが空ではない
# 画像のmd5が5d6737777450ade1eae0106458ddaea4ではない場合ループを抜ける

# TODO
# リファクタリングする、jsonから投稿文も作成する
while True:
    media_key = get_random_media_key()
    if media_key:
        for i in media_key:
            h = get_md5(i)
            if h != NO_IMG_HASH:
                print(media_key)
                for i in media_key:
                    port_discord(i, 'test')
                sys.exit()
