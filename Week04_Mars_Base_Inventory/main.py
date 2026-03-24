import csv
import os
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. CSV 파일 읽기
inventory = []

try:
    with open(os.path.join(BASE_DIR, 'Mars_Base_Inventory_List.csv'), 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            inventory.append(dict(row))
except FileNotFoundError:
    print('[오류] 파일을 찾을 수 없습니다.')
except OSError as e:
    print(f'[오류] 파일을 읽을 수 없습니다: {e}')

# 2. 전체 목록 출력
print('=== 전체 화물 목록 ===')
for item in inventory:
    print(item)

# 3. 인화성 높은 순 정렬
sorted_inventory = sorted(inventory, key=lambda x: float(x['Flammability']), reverse=True)

print('\n=== 인화성 높은 순으로 정렬된 목록 ===')
for item in sorted_inventory:
    print(item)

# 4. 인화성 0.7 이상 필터링 및 출력, CSV 저장
dangerous = [item for item in sorted_inventory if float(item['Flammability']) >= 0.7]

print('\n=== 인화성 지수 0.7 이상 위험 물질 ===')
for item in dangerous:
    print(item)

try:
    with open(os.path.join(BASE_DIR, 'Mars_Base_Inventory_danger.csv'), 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=dangerous[0].keys())
        writer.writeheader()
        writer.writerows(dangerous)
except OSError as e:
    print(f'[오류] CSV 파일을 저장할 수 없습니다: {e}')

# 5. 정렬된 목록 바이너리 파일 저장
try:
    with open(os.path.join(BASE_DIR, 'Mars_Base_Inventory_List.bin'), 'wb') as file:
        pickle.dump(sorted_inventory, file)
except OSError as e:
    print(f'[오류] 바이너리 파일을 저장할 수 없습니다: {e}')

# 6. 바이너리 파일 그대로 읽어서 출력
bin_data = b''

try:
    with open(os.path.join(BASE_DIR, 'Mars_Base_Inventory_List.bin'), 'rb') as file:
        bin_data = file.read()
except OSError as e:
    print(f'[오류] 바이너리 파일을 읽을 수 없습니다: {e}')

print('\n=== 바이너리 파일에서 읽은 목록 ===')
print(bin_data)
