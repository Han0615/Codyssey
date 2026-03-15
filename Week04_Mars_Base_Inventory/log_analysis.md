# 화성 기지 화물 인화성 분석 보고서

- **작성자:** 한송희 박사
- **작성일:** 2023-08-28
- **대상 파일:** Mars_Base_Inventory_List.csv
- **출력 파일:** Mars_Base_Inventory_danger.csv

---

## 1. 개요

산소 탱크 폭발로 인한 화성 기지 사고 이후, 기지 내에 보관 중인 화학물질 중 인화성이 높은 위험 물질을 식별하고 외부로 격리하기 위해 화물 목록(`Mars_Base_Inventory_List.csv`)을 분석하였다. Python을 활용하여 CSV 파일을 읽고, 인화성 지수를 기준으로 정렬 및 필터링하여 위험 물질 목록(`Mars_Base_Inventory_danger.csv`)을 별도로 저장하였다.

---

## 2. 개발 환경

- **언어:** Python 3.x
- **개발 도구:** VS Code
- **사용 모듈:** `csv` (Python 표준 라이브러리, 별도 설치 불필요)
- **코딩 스타일:** PEP 8 준수 (홑따옴표 기본 사용, 대입문 공백, 들여쓰기 4칸 공백)

---

## 3. 코드 설계 및 구현 설명

### 3.1 CSV 파일 읽기 및 리스트 변환

`csv.DictReader`를 사용하여 CSV 파일의 헤더(`Substance`, `Weight`, `Specific Gravity`, `Strength`, `Flammability`)를 기준으로 각 행을 딕셔너리로 읽어들여 리스트에 추가하였다.

```python
with open(filename, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        inventory.append(row)
```

단순 텍스트로 읽는 방식과 달리 필드별로 분리된 데이터를 `item['Flammability']`와 같이 명확하게 접근할 수 있어 정렬 및 필터링에 용이하다.

### 3.2 인화성 높은 순 정렬

Python 내장 함수 `sorted()`와 `lambda`를 사용하여 `Flammability` 필드를 기준으로 내림차순 정렬하였다.

```python
sorted_inventory = sorted(
    inventory,
    key=lambda x: float(x['Flammability']),
    reverse=True
)
```

CSV에서 읽은 값은 문자열이므로 `float()`으로 변환하여 수치 비교가 가능하도록 하였다.

### 3.3 인화성 0.7 이상 필터링

리스트 컴프리헨션을 사용하여 인화성 지수가 0.7 이상인 항목만 추출하였다.

```python
dangerous_items = [
    item for item in inventory
    if float(item['Flammability']) >= 0.7
]
```

### 3.4 위험 물질 목록 CSV 저장

`csv.DictWriter`를 사용하여 필터링된 위험 물질 목록을 `Mars_Base_Inventory_danger.csv` 파일로 저장하였다. `newline=''` 옵션을 지정하여 Windows 환경에서 발생할 수 있는 빈 줄 삽입 문제를 방지하였다.

```python
with open(filename, 'w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(dangerous_items)
```

### 3.5 예외 처리

파일 읽기와 저장 모두 `try / except / finally` 구조로 예외를 처리하였다.

| 예외 | 발생 상황 | 처리 이유 |
|------|-----------|-----------|
| `FileNotFoundError` | 파일이 존재하지 않을 때 | CSV 파일이 삭제되었거나 경로가 잘못된 경우 대비 |
| `PermissionError` | 파일 읽기/쓰기 권한이 없을 때 | 시스템 보안 설정으로 접근이 차단된 경우 대비 |
| `UnicodeDecodeError` | 파일 인코딩이 맞지 않을 때 | CSV 파일이 다른 인코딩으로 저장된 경우 대비 |
| `OSError` | 디스크 오류 등 OS 수준 오류 | 하드웨어 손상 등 예측 불가한 오류 포괄 처리 |

`finally` 블록은 성공·실패 여부와 무관하게 항상 실행되어 프로세스 종료 메시지를 출력한다.

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

총 79종의 화물 중 33종이 인화성 지수 0.7 이상의 위험 물질로 분류되었다. 특히 **Gunpowder(화약)**, **Hydrogen Peroxide(과산화수소)**, **Sodium(나트륨)** 이 인화성 지수 0.95 이상으로 가장 위험도가 높아 즉각적인 격리가 필요하다. 해당 위험 물질 목록은 `Mars_Base_Inventory_danger.csv`로 저장되었으며, 이를 기반으로 화성 기지 외부 격리 작업을 진행할 수 있다.

---
