# 화성 기지 화물 인화성 분석 보고서

- **작성자:** 한송희 박사
- **작성일:** 2023-08-28
- **대상 파일:** Mars_Base_Inventory_List.csv
- **출력 파일:** Mars_Base_Inventory_danger.csv, Mars_Base_Inventory_List.bin

---

## 1. 개요

산소 탱크 폭발로 인한 화성 기지 사고 이후, 기지 내 보관 중인 화학물질 중 인화성이 높은 위험 물질을 식별하고 외부로 격리하기 위해 화물 목록(`Mars_Base_Inventory_List.csv`)을 분석하였다. Python을 활용하여 CSV 파일을 읽고 인화성 지수를 기준으로 정렬 및 필터링하여 위험 물질 목록을 별도의 CSV 파일과 바이너리 파일로 저장하였다.

---

## 2. 사용 모듈 및 선택 이유

| 모듈 | 종류 | 사용 이유 |
|------|------|-----------|
| `csv` | Python 표준 라이브러리 | CSV 파일을 읽고 쓰기 위해 사용하였다. `csv.DictReader`로 헤더 기반 딕셔너리 변환, `csv.DictWriter`로 CSV 저장을 처리한다. |
| `os` | Python 표준 라이브러리 | 파일 경로를 절대 경로로 변환하기 위해 사용하였다. VS Code 실행 시 작업 디렉토리가 프로젝트 루트로 설정되어 파일을 찾지 못하는 문제를 방지한다. |
| `pickle` | Python 표준 라이브러리 | Python 객체를 바이너리 형태로 직렬화하여 `.bin` 파일로 저장하기 위해 사용하였다. |

세 모듈 모두 Python 표준 라이브러리로 별도 설치 없이 사용 가능하며, 과제 제약 조건(외부 라이브러리 사용 금지)을 충족한다.

---

## 3. 주요 코드 설명

### 3.1 파일 경로 설정

```python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
```

`__file__`은 현재 실행 중인 파일 자신의 경로를 나타내는 Python 내장 변수이다. `os.path.abspath()`로 절대 경로로 변환하고, `os.path.dirname()`으로 파일명을 제거해 폴더 경로만 추출한다. 이후 모든 파일을 열 때 `os.path.join(BASE_DIR, '파일명')` 형태로 사용하여 항상 `main.py`와 같은 폴더에서 파일을 찾고 저장하도록 하였다.

### 3.2 CSV 파일 읽기 — `csv.DictReader`

```python
with open(os.path.join(BASE_DIR, 'Mars_Base_Inventory_List.csv'), 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        inventory.append(dict(row))
```

`with open()` 구문은 블록이 종료될 때 파일을 자동으로 닫아 리소스 누수를 방지한다. `csv.DictReader`는 CSV 첫 줄을 헤더로 인식하여 각 행을 `{'Substance': ..., 'Flammability': ...}` 형태의 딕셔너리로 변환한다. `dict(row)`로 변환하는 이유는 `DictReader`가 반환하는 타입이 `OrderedDict`이기 때문에 일반 딕셔너리로 변환하기 위함이다.

### 3.3 인화성 높은 순 정렬 — `sorted()`

```python
sorted_inventory = sorted(inventory, key=lambda x: float(x['Flammability']), reverse=True)
```

`sorted()`는 원본 리스트를 변경하지 않고 새로운 정렬된 리스트를 반환한다. `key=lambda x: float(x['Flammability'])`로 정렬 기준을 인화성 지수로 지정하였다. CSV에서 읽은 값은 모두 문자열이므로 `float()`으로 변환하여 수치 비교가 가능하도록 하였다. `reverse=True`는 내림차순 정렬이다.

### 3.4 인화성 0.7 이상 필터링 — 리스트 컴프리헨션

```python
dangerous = [item for item in sorted_inventory if float(item['Flammability']) >= 0.7]
```

리스트 컴프리헨션으로 조건을 만족하는 항목만 추출하였다. 이미 정렬된 `sorted_inventory`에서 필터링하므로 결과도 인화성이 높은 순서를 유지한다.

### 3.5 CSV 저장 — `csv.DictWriter`

```python
writer = csv.DictWriter(file, fieldnames=dangerous[0].keys())
writer.writeheader()
writer.writerows(dangerous)
```

`csv.DictWriter`는 딕셔너리 리스트를 CSV로 저장한다. `dangerous[0].keys()`로 첫 항목의 키를 헤더로 사용하고, `writeheader()`로 헤더를 먼저 작성한 뒤 `writerows()`로 전체 데이터를 한 번에 저장한다. `newline=''`은 Windows 환경에서 빈 줄이 삽입되는 문제를 방지한다.

### 3.6 바이너리 파일 저장 — `pickle.dump()`

```python
with open(os.path.join(BASE_DIR, 'Mars_Base_Inventory_List.bin'), 'wb') as file:
    pickle.dump(sorted_inventory, file)
```

`'wb'`는 바이너리 쓰기 모드이다. `pickle.dump()`는 Python 객체를 바이트로 직렬화하여 파일에 저장한다. 객체의 타입과 구조를 그대로 보존하기 때문에 복원 시 별도 파싱이 필요 없다.

### 3.7 바이너리 파일 읽기 — `file.read()`

```python
with open(os.path.join(BASE_DIR, 'Mars_Base_Inventory_List.bin'), 'rb') as file:
    bin_data = file.read()
```

`'rb'`는 바이너리 읽기 모드이다. `pickle.load()` 대신 `file.read()`를 사용한 이유는 Python 객체로 복원하지 않고 바이트 데이터 그대로 출력하기 위해서이다. 출력 시 `\x80\x04\x95...` 형태의 바이너리 데이터가 표시되어 텍스트 파일과의 차이를 직접 확인할 수 있다.

### 3.8 예외 처리

파일을 다루는 모든 구간에 `try / except` 구조를 적용하였다. 파일이 없을 경우는 `FileNotFoundError`, 권한 오류나 디스크 오류 등 나머지 파일 시스템 오류는 `OSError`로 포괄 처리하였다.

---

## 4. 수행 결과

| 항목 | 내용 |
|------|------|
| 전체 물질 수 | 79종 |
| 인화성 지수 0.7 이상 (위험) | 33종 |
| 인화성 지수 0.7 미만 (안전) | 46종 |
| 위험 물질 CSV 저장 | Mars_Base_Inventory_danger.csv |
| 정렬 목록 바이너리 저장 | Mars_Base_Inventory_List.bin |

인화성 지수가 가장 높은 물질은 Gunpowder(화약)와 Hydrogen Peroxide(과산화수소)로 0.98이었으며, Sodium(나트륨) 0.97, Acetylene(아세틸렌)·Fossil Fuels·Asphalt·Natural Gas 0.95 순으로 위험도가 높았다. 총 33종의 위험 물질이 `Mars_Base_Inventory_danger.csv`로 저장되었다.

---

## 5. 텍스트 파일과 바이너리 파일의 차이점 및 장단점

텍스트 파일은 데이터를 사람이 읽을 수 있는 문자열 형태로 저장한다. 메모장, 엑셀 등 일반 편집기로 열 수 있고 다른 언어·프로그램과의 호환성이 높다. 다만 Python 리스트나 딕셔너리 같은 복잡한 객체를 저장하려면 별도의 변환 로직이 필요하고, 읽을 때도 타입 변환이 필요하다.

바이너리 파일은 Python 객체를 바이트 형태 그대로 직렬화하여 저장한다. 파일을 그대로 읽으면 `\x80\x04\x95...`와 같이 사람이 읽을 수 없는 데이터가 출력된다. Python 객체의 구조를 그대로 보존하기 때문에 읽을 때 별도 파싱 없이 원본 데이터를 복원할 수 있으며 처리 속도도 빠르다. 다만 Python 전용 형식이라 다른 언어에서는 읽기 어렵고 가독성이 없다.

| 항목 | 텍스트 파일 (.csv) | 바이너리 파일 (.bin) |
|------|-------------------|---------------------|
| 저장 방식 | 문자열로 저장 | 바이트로 직렬화하여 저장 |
| 가독성 | 사람이 읽을 수 있음 | 읽을 수 없음 (`\x80\x04\x95...`) |
| 다른 프로그램 호환 | 높음 (엑셀, 메모장 등) | 낮음 (Python 전용) |
| 타입 변환 | 읽을 때 변환 필요 | 원본 객체 그대로 복원 |
| 처리 속도 | 상대적으로 느림 | 상대적으로 빠름 |
| 장점 | 범용성, 가독성 | 편의성, 속도, 구조 보존 |
| 단점 | 변환 로직 필요 | 범용성 낮음, 가독성 없음 |

---

*본 보고서는 화성 기지 돔 수리 전 인화성 물질 격리를 위해 작성된 화물 분석 보고서입니다.*
