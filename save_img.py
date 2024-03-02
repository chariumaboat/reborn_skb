from util import *

local_data = read_local_data('./combined_data.json')
for i in local_data:
    # mediaキーがあるか確認
    if 'media' in i:
        # mediaキーにあるリストを出力
        for flag, m in enumerate(i['media']):
            url = m['item']['mediaUrl']
            id = i['id'] + '_' + str(flag)
            print(url, id)
            save_image(url, id)
