# 화성 기지 화물 인화성 분석 보고서

- **작성자:** 한송희 박사
- **작성일:** 2023-08-28
- **대상 파일:** Mars_Base_Inventory_List.csv
- **출력 파일:** Mars_Base_Inventory_danger.csv, Mars_Base_Inventory_List.bin

---

## 1. 개요

산소 탱크 폭발로 인한 화성 기지 사고 이후, 기지 내 보관 중인 화학물질 중 인화성이 높은 위험 물질을 식별하고 외부로 격리하기 위해 화물 목록(`Mars_Base_Inventory_List.csv`)을 분석하였다. Python을 활용하여 CSV 파일을 읽고 인화성 지수를 기준으로 정렬 및 필터링하여 위험 물질 목록을 별도의 CSV 파일과 바이너리 파일로 저장하였다.

---

## 2. 코드 설계 및 구현 설명

### 2.1 모듈 import

```python
import csv
import os
import pickle
```

- `csv` — CSV 파일을 읽고 쓰기 위한 Python 표준 라이브러리이다. 별도 설치 없이 사용 가능하다.
- `os` — 운영체제 기능을 다루는 표준 라이브러리이다. 파일 경로를 절대 경로로 변환하는 데 사용한다.
- `pickle` — Python 객체를 바이너리 파일로 저장하고 복원하기 위한 표준 라이브러리이다.

### 2.2 파일 경로 설정

```python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
```

- `__file__` — 현재 실행 중인 `main.py` 파일 자신의 경로를 나타내는 Python 내장 변수이다.
- `os.path.abspath(__file__)` — `main.py`의 상대 경로를 절대 경로로 변환한다.
- `os.path.dirname(...)` — 절대 경로에서 파일명을 제거하고 디렉토리 경로만 추출한다.
- 결과적으로 `BASE_DIR`은 `main.py`가 위치한 폴더의 절대 경로를 담게 된다. VS Code에서 실행 시 작업 디렉토리가 프로젝트 루트로 설정되어 파일을 찾지 못하는 문제가 발생할 수 있는데, 이를 방지하기 위해 `main.py` 기준의 절대 경로를 사용하였다.

### 2.3 요구사항 1, 2 — CSV 파일 읽기 및 리스트 변환

```python
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

print('=== 전체 화물 목록 ===')
for item in inventory:
    print(item)
```

- `inventory = []` — CSV에서 읽은 데이터를 담을 빈 리스트를 `try` 블록 바깥에 선언하였다. `try` 블록 안에서 선언할 경우 예외 발생 시 변수 자체가 존재하지 않아 이후 코드에서 오류가 발생할 수 있기 때문이다.
- `os.path.join(BASE_DIR, 'Mars_Base_Inventory_List.csv')` — `BASE_DIR`과 파일명을 결합하여 절대 경로를 생성한다. 운영체제마다 경로 구분자가 다를 수 있는데 `os.path.join()`이 이를 자동으로 처리해준다.
- `with open(...) as file` — `with` 구문은 블록이 종료될 때 예외 발생 여부와 관계없이 파일을 자동으로 닫아준다. `close()`를 직접 호출하지 않아도 되므로 리소스 누수를 방지할 수 있다.
- `'r'` — 읽기 모드이다.
- `encoding='utf-8'` — 파일의 인코딩을 UTF-8로 지정한다. 지정하지 않으면 운영체제 기본 인코딩으로 읽어 문자가 깨질 수 있다.
- `csv.DictReader(file)` — CSV 첫 번째 줄을 자동으로 헤더로 인식하여 각 행을 `{'Substance': ..., 'Flammability': ...}` 형태의 딕셔너리로 변환한다.
- `inventory.append(dict(row))` — `DictReader`가 반환하는 객체는 `OrderedDict` 타입이므로 `dict()`로 일반 딕셔너리로 변환하여 리스트에 추가한다. 이로써 CSV 전체 내용이 Python 리스트 객체로 변환된다.
- `FileNotFoundError` — 파일이 존재하지 않을 때 발생하는 예외이다.
- `OSError` — 디스크 오류, 권한 문제 등 파일 시스템 수준의 오류를 포괄적으로 처리한다.

### 2.4 요구사항 3 — 인화성 높은 순 정렬

```python
sorted_inventory = sorted(inventory, key=lambda x: float(x['Flammability']), reverse=True)
```

- `sorted()` — 원본 리스트를 변경하지 않고 새로운 정렬된 리스트를 반환하는 Python 내장 함수이다.
- `key=lambda x: float(x['Flammability'])` — 정렬 기준을 `Flammability` 값으로 지정한다. CSV에서 읽은 값은 모두 문자열이므로 `float()`으로 변환하여 수치 비교가 가능하도록 하였다. `lambda`는 이름 없는 익명 함수로 정렬 기준을 간결하게 표현할 때 사용한다.
- `reverse=True` — 내림차순(높은 값부터) 정렬이다.

### 2.5 요구사항 4 — 인화성 0.7 이상 필터링 및 출력, CSV 저장

```python
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
    print(f'[오류] 파일을 저장할 수 없습니다: {e}')
```

- `[item for item in sorted_inventory if float(item['Flammability']) >= 0.7]` — 리스트 컴프리헨션으로 인화성 지수 0.7 이상인 항목만 추출한다. 이미 정렬된 `sorted_inventory`에서 필터링하므로 결과도 인화성이 높은 순서를 유지한다.
- `'w'` — 쓰기 모드이다. 파일이 없으면 새로 생성하고, 있으면 덮어쓴다.
- `newline=''` — Windows 환경에서 CSV 저장 시 줄 사이에 빈 줄이 삽입되는 문제를 방지한다.
- `csv.DictWriter(file, fieldnames=dangerous[0].keys())` — 딕셔너리 리스트를 CSV로 저장하는 Writer이다. `dangerous[0].keys()`로 첫 번째 항목의 키를 헤더로 사용한다.
- `writer.writeheader()` — 헤더 줄을 파일에 먼저 작성한다.
- `writer.writerows(dangerous)` — 위험 물질 목록 전체를 한 번에 파일에 작성한다.

### 2.6 요구사항 5 — 정렬된 목록 바이너리 파일 저장

```python
try:
    with open(os.path.join(BASE_DIR, 'Mars_Base_Inventory_List.bin'), 'wb') as file:
        pickle.dump(sorted_inventory, file)
except OSError as e:
    print(f'[오류] 바이너리 파일을 저장할 수 없습니다: {e}')
```

- `'wb'` — 바이너리 쓰기 모드이다. 텍스트 모드(`'w'`)와 달리 데이터를 바이트 그대로 저장한다.
- `pickle.dump(sorted_inventory, file)` — 인화성 순으로 정렬된 `sorted_inventory` 리스트를 바이너리 형태로 직렬화하여 파일에 저장한다. 텍스트 파일과 달리 Python 객체의 구조를 그대로 유지하기 때문에 별도 파싱 없이 원본 데이터를 복원할 수 있다.

### 2.7 요구사항 6 — 바이너리 파일 읽기 및 출력

```python
try:
    with open(os.path.join(BASE_DIR, 'Mars_Base_Inventory_List.bin'), 'rb') as file:
        bin_data = pickle.load(file)
except OSError as e:
    print(f'[오류] 바이너리 파일을 읽을 수 없습니다: {e}')
    bin_data = []

print('\n=== 바이너리 파일에서 읽은 목록 ===')
for item in bin_data:
    print(item)
```

- `'rb'` — 바이너리 읽기 모드이다.
- `pickle.load(file)` — 바이너리 파일을 읽어 저장 전과 동일한 Python 객체로 복원한다. 복원된 `bin_data`는 저장 당시의 딕셔너리 리스트 그대로이다.
- `bin_data = []` — 예외 발생 시 빈 리스트로 초기화하여 이후 출력 코드가 오류 없이 실행되도록 한다.

---

## 3. 요구사항 7 — 텍스트 파일과 바이너리 파일의 차이점 및 장단점

텍스트 파일(`Mars_Base_Inventory_danger.csv`)과 바이너리 파일(`Mars_Base_Inventory_List.bin`)은 데이터를 저장하는 방식이 근본적으로 다르다.

**텍스트 파일**은 데이터를 사람이 읽을 수 있는 문자열 형태로 저장한다. 메모장이나 엑셀 같은 일반 편집기로 열 수 있고, 다른 프로그램이나 언어에서도 쉽게 읽을 수 있어 범용성이 높다. 다만 Python 리스트나 딕셔너리 같은 복잡한 객체를 저장하려면 문자열로 변환하는 별도의 로직이 필요하고, 읽을 때도 다시 적절한 타입으로 변환해야 한다.

**바이너리 파일**은 Python 객체를 바이트 형태 그대로 직렬화하여 저장한다. `pickle.dump()`로 저장하고 `pickle.load()`로 읽으면 저장 전과 완전히 동일한 Python 객체가 복원되므로 별도의 파싱이나 타입 변환이 필요 없다. 속도도 더 빠르고 복잡한 객체 구조도 그대로 보존된다. 다만 Python 전용 형식이기 때문에 메모장으로 열면 알아볼 수 없는 바이트 데이터가 표시되고, 다른 언어에서는 읽기 어렵다.

| 항목 | 텍스트 파일 (.csv) | 바이너리 파일 (.bin) |
|------|-------------------|---------------------|
| 저장 방식 | 문자열로 저장 | 바이트로 직렬화하여 저장 |
| 사람이 읽을 수 있는가 | 가능 | 불가능 |
| 다른 프로그램 호환 | 높음 | 낮음 (Python 전용) |
| 타입 변환 필요 여부 | 읽을 때 변환 필요 | 원본 그대로 복원 |
| 처리 속도 | 상대적으로 느림 | 상대적으로 빠름 |
| 장점 | 범용성, 가독성 | 편의성, 속도, 객체 구조 보존 |
| 단점 | 복잡한 객체 변환 로직 필요 | Python 전용, 가독성 없음 |

---

## 4. 분석 결과

### 4.1 전체 화물 현황

| 항목 | 내용 |
|------|------|
| 전체 물질 수 | 79종 |
| 인화성 지수 0.7 이상 (위험) | 33종 |
| 인화성 지수 0.7 미만 (안전) | 46종 |

### 4.2 인화성 0.7 이상 위험 물질 목록 (인화성 높은 순)

| 물질 | 인화성 지수 |
|------|-------------|
| Gunpowder | 0.98 |
| Hydrogen Peroxide | 0.98 |
| Sodium | 0.97 |
| Acetylene | 0.95 |
| Fossil Fuels | 0.95 |
| Asphalt | 0.95 |
| Natural Gas | 0.95 |
| Petroleum Products | 0.92 |
| Ammonium Nitrate | 0.92 |
| Carbon Disulfide | 0.92 |
| Chloroform | 0.92 |
| Uranium | 0.92 |
| Gasoline | 0.91 |
| Alkyl Benzene | 0.90 |
| Mineral Oil | 0.90 |
| Phosphates | 0.90 |
| Chemical Waste | 0.90 |
| Arsenic Compounds | 0.90 |
| Diesel Fuel | 0.90 |
| Ammonia | 0.88 |
| Acetic Acid | 0.88 |
| Copper Sulfate | 0.88 |
| Alcohol | 0.85 |
| Isopropyl Alcohol | 0.85 |
| Nitrates | 0.85 |
| Sulfuric Acid | 0.85 |
| Sunflower Oil | 0.85 |
| Natural Leather | 0.82 |
| Wood | 0.80 |
| Propane | 0.78 |
| Sulfuric Acid | 0.78 |
| Paper | 0.75 |
| Methane | 0.73 |

### 4.3 결론

총 79종의 화물 중 33종이 인화성 지수 0.7 이상의 위험 물질로 분류되었다. 특히 Gunpowder(화약), Hydrogen Peroxide(과산화수소), Sodium(나트륨)이 인화성 지수 0.95 이상으로 가장 위험도가 높아 즉각적인 격리가 필요하다. 위험 물질 목록은 `Mars_Base_Inventory_danger.csv`로 저장되었으며, 인화성 순 전체 목록은 `Mars_Base_Inventory_List.bin`으로 저장되었다.

---
