# 더미 센서 구현 보고서

- **작성자:** 한송희 박사
- **작성일:** 2026-03-31
- **파일명:** mars_mission_computer.py

---

## 1. 개요

미션 컴퓨터 복구 이후 화성 기지의 환경 데이터를 수집하고 출력하는 기능이 필요하였다. 실제 센서를 연결하기 전 테스트 목적으로 랜덤 값을 생성하는 더미 센서(`DummySensor`) 클래스를 Python으로 구현하였다. 더미 센서는 기지 내외부의 온도, 습도, 광량, 이산화탄소 농도, 산소 농도 6가지 환경 값을 생성하며, 호출 시 로그 파일(`sensor_log.csv`)에 기록을 남긴다.

---

## 2. 사용 모듈 및 선택 이유

| 모듈 | 종류 | 사용 이유 |
|------|------|-----------|
| `random` | Python 표준 라이브러리 | 각 환경 값의 지정 범위 내에서 랜덤 값을 생성하기 위해 사용하였다. 과제 제약 조건에서 허용한 모듈이다. |
| `datetime` | Python 표준 라이브러리 | 로그 파일에 기록할 현재 날짜와 시간을 가져오기 위해 사용하였다. |

---

## 3. 주요 코드 설명

### 3.1 클래스 및 멤버 변수 정의

```python
class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            ...
        }
```

`DummySensor` 클래스를 정의하고 `__init__()` 메서드에서 `env_values` 딕셔너리를 멤버 변수로 선언하였다. `__init__()`은 클래스가 인스턴스화될 때 자동으로 실행되는 생성자 메서드이다. 초기값은 `None`으로 설정하여 `set_env()` 호출 전까지 값이 없음을 명시하였다.

### 3.2 `set_env()` 메서드

```python
def set_env(self):
    self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
    self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4)
    ...
```

`random.uniform(a, b)`로 지정된 범위 내의 실수 랜덤 값을 생성하여 `env_values` 각 항목에 저장한다. `round()`로 소수점 자릿수를 제한하였다. 온도·습도·광량·산소는 소수점 2자리, 이산화탄소는 범위가 작아 소수점 4자리로 설정하였다.

### 3.3 `get_env()` 메서드

```python
def get_env(self):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"{timestamp}, {self.env_values[...], ...}"
    with open('sensor_log.csv', 'a', encoding='utf-8') as log_file:
        log_file.write(log_line + '\n')
    return self.env_values
```

`datetime.now()`로 현재 시각을 가져오고, `strftime()`으로 `YYYY-MM-DD HH:MM:SS` 형식의 문자열로 변환한다. 날짜/시간과 6개 환경 값을 CSV 형식으로 구성하여 `sensor_log.csv` 파일에 추가(`'a'` 모드) 기록한다. `'a'` 모드는 기존 내용을 지우지 않고 이어서 쓰는 추가 모드이다. 마지막으로 `env_values`를 반환한다.

### 3.4 인스턴스 생성 및 메서드 호출

```python
ds = DummySensor()
ds.set_env()
print(ds.get_env())
```

`DummySensor()`로 `ds`라는 인스턴스를 생성한다. `set_env()`로 랜덤 값을 채운 뒤 `get_env()`를 호출하여 값을 반환받아 출력한다.

---

## 4. 각 환경 값의 랜덤 생성 범위

| 항목 | 범위 |
|------|------|
| 화성 기지 내부 온도 | 18 ~ 30 °C |
| 화성 기지 외부 온도 | 0 ~ 21 °C |
| 화성 기지 내부 습도 | 50 ~ 60 % |
| 화성 기지 외부 광량 | 500 ~ 715 W/m² |
| 화성 기지 내부 이산화탄소 농도 | 0.02 ~ 0.1 % |
| 화성 기지 내부 산소 농도 | 4 ~ 7 % |

---

## 5. 수행 결과

`ds.set_env()` 호출 시 각 항목에 랜덤 값이 생성되고, `ds.get_env()` 호출 시 아래와 같이 출력된다.

```
{
  'mars_base_internal_temperature': 18.84,
  'mars_base_external_temperature': 19.88,
  'mars_base_internal_humidity': 53.33,
  'mars_base_external_illuminance': 604.95,
  'mars_base_internal_co2': 0.0815,
  'mars_base_internal_oxygen': 5.08
}
```

동시에 `sensor_log.csv` 파일에 아래 형식으로 로그가 기록된다.

```
2026-03-30 02:19:05,18.84,19.88,53.33,604.95,0.0815,5.08
```

---

*본 보고서는 화성 기지 미션 컴퓨터 복구 과정에서 더미 센서 구현을 위해 작성되었습니다.*