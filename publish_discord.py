from util import *
import random
import json
from pprint import pprint
import hashlib
import sys
import os
from discordwebhook import Discord
from PIL import Image

NO_IMG_HASH = '5d6737777450ade1eae0106458ddaea4'
DISCORD_WEBHOOK_URL = os.environ['DISCORD_WEBHOOK_URL']


def is_png_corrupted(file_path):
    try:
        img = Image.open(file_path)
        img.verify()
        return True  # PNGデータは正常です
    except (IOError, SyntaxError):
        return False  # PNGデータが壊れています


def create_post_text(json):
    user_id = json['userId']
    id = json['id']
    return f'https://twitter.com/i/user/{user_id}\nhttps://twitter.com/{user_id}/status/{id}'


def get_random_media():
    with open('./data.json/data.json', 'r') as f:
        data = json.load(f)
    raw_json = random.choice(data)
    id = raw_json['id']
    length = len(raw_json['media'])
    for flag, i in enumerate(raw_json['media']):
        print(i['item']['mediaUrl'])
        response = requests.get(i['item']['mediaUrl'])
        image_data = response.content
        with open(f'./img/{id}_{flag}.png', "wb") as f:
            f.write(image_data)
    text = create_post_text(raw_json)
    return [f'./img/{id}_{i}.png' for i in range(length)], text


def get_md5(path):
    with open(path, 'rb') as f:
        data = f.read()
    return hashlib.md5(data).hexdigest()


def port_discord_with_img(path, text):
    discord = Discord(url=DISCORD_WEBHOOK_URL)
    with open(path, 'rb') as f:
        discord.post(content=text, file={"attachment": f})


def port_discord(text):
    discord = Discord(url=DISCORD_WEBHOOK_URL)
    discord.post(content=text)


# TODO リファクタリングする、jsonから投稿文も作成する
while True:
    media_key, text = get_random_media()
    if media_key:
        for i in media_key:
            h = get_md5(i)
            if h != NO_IMG_HASH and is_png_corrupted(i):
                print(media_key)
                port_discord(text)
                for i in media_key:
                    port_discord_with_img(i, '')
                print('done')
                sys.exit()
