import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def read_inventory(filename):
    filepath = os.path.join(BASE_DIR, filename)
    inventory = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                inventory.append(row)
    except FileNotFoundError:
        print(f'[오류] 파일을 찾을 수 없습니다: {filepath}')
    except PermissionError:
        print(f'[오류] 파일 읽기 권한이 없습니다: {filepath}')
    except UnicodeDecodeError:
        print(f'[오류] 파일 인코딩 오류가 발생했습니다: {filepath}')
    except OSError as e:
        print(f'[오류] OS 오류가 발생했습니다: {e}')
    else:
        return inventory
    finally:
        print('파일 읽기 프로세스가 완료되었습니다.\n')
    return []


def print_inventory(inventory):
    print('=== 전체 화물 목록 ===')
    for item in inventory:
        print(
            f"물질: {item['Substance']:<25} "
            f"무게: {item['Weight (g/cm³)']:<10} "
            f"비중: {item['Specific Gravity']:<10} "
            f"강도: {item['Strength']:<12} "
            f"인화성: {item['Flammability']}"
        )
    print()


def sort_by_flammability(inventory):
    return sorted(
        inventory,
        key=lambda x: float(x['Flammability']),
        reverse=True
    )


def filter_dangerous(inventory):
    return [
        item for item in inventory
        if float(item['Flammability']) >= 0.7
    ]


def print_dangerous(dangerous_items):
    print('=== 위험 물질 목록 (인화성 지수 0.7 이상) ===')
    for item in dangerous_items:
        print(
            f"물질: {item['Substance']:<25} "
            f"인화성: {item['Flammability']}"
        )
    print()


def save_dangerous(dangerous_items, filename):
    filepath = os.path.join(BASE_DIR, filename)
    try:
        with open(filepath, 'w', encoding='utf-8', newline='') as file:
            fieldnames = [
                'Substance', 'Weight (g/cm³)',
                'Specific Gravity', 'Strength', 'Flammability'
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(dangerous_items)
    except PermissionError:
        print(f'[오류] 파일 쓰기 권한이 없습니다: {filepath}')
    except OSError as e:
        print(f'[오류] OS 오류가 발생했습니다: {e}')
    else:
        print(f'위험 물질 목록이 저장되었습니다: {filepath}\n')
    finally:
        print('파일 저장 프로세스가 완료되었습니다.\n')


def main():
    input_filename = 'Mars_Base_Inventory_List.csv'
    output_filename = 'Mars_Base_Inventory_danger.csv'

    inventory = read_inventory(input_filename)
    if not inventory:
        return
    
    print_inventory(inventory)

    sorted_inventory = sort_by_flammability(inventory)
    print('=== 인화성 높은 순으로 정렬된 목록 ===')
    for item in sorted_inventory:
        print(
            f"물질: {item['Substance']:<25} "
            f"인화성: {item['Flammability']}"
        )
    print()

    dangerous_items = filter_dangerous(sorted_inventory)
    print_dangerous(dangerous_items)

    save_dangerous(dangerous_items, output_filename)


if __name__ == '__main__':
    main()