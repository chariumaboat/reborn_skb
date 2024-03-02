from util import *

local_data = read_local_data('./combined_data.json')
print(f'local data length: {len(local_data)}')
new_data = get_new_data()
saved_ids = [i['id'] for i in local_data]

for i in new_data:
    if i['id'] not in saved_ids:
        local_data.append(i)

print(f'save data length: {len(local_data)}')
save_data(local_data)
