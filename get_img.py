import requests
import json
from pprint import pprint


def read_local_data(path):
    with open(path, 'r') as file:
        local_data = json.load(file)
        return local_data


def get_new_data():
    base_url = 'https://search.yahoo.co.jp/realtime/api/v1/pagination?p='
    keyword = "すぐ消す"
    r = requests.get(f'{base_url}{keyword}')
    j = json.loads(r.text)
    data = j['timeline']['entry']
    return data


def merge_data(data, local_data):
    combined_data = list(set(data + local_data))
    return combined_data


def save_data(data):
    file_path = "./combined_data.json"
    with open(file_path, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


local_data = read_local_data('./combined_data.json')
print(f'local data length: {len(local_data)}')
new_data = get_new_data()
saved_ids = [i['id'] for i in local_data]

for i in new_data:
    if i['id'] not in saved_ids:
        local_data.append(i)

print(f'save data length: {len(local_data)}')
save_data(local_data)
