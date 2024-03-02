from util import *

local_data = read_local_data('./combined_data.json')
print(f'local data length: {len(local_data)}')
new_data = get_new_data()
saved_ids = [i['id'] for i in local_data]

for i in new_data:
    if i['id'] not in saved_ids:
        local_data.append(i)
    # 保存するため、mediaキーがあるか確認
    if 'media' in i:
        # mediaキーにあるリストを出力
        for flag, m in enumerate(i['media']):
            url = m['item']['mediaUrl']
            id = i['id'] + '_' + str(flag)
            save_image(url, id)

print(f'save data length: {len(local_data)}')
save_data(local_data)
