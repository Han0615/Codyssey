# 미션 컴퓨터 구현 보고서

- **작성자:** 한송희 박사
- **작성일:** 2026-04-05
- **파일명:** mars_mission_computer.py

---

## 1. 개요

화성 기지 미션 컴퓨터 복구 이후 환경 데이터를 지속적으로 수집하고 모니터링하는 기능이 필요하였다. 더미 센서(`DummySensor`)로부터 랜덤 환경 데이터를 읽어 5초마다 JSON 형식으로 출력하는 `MissionComputer` 클래스를 구현하였다. 또한 5분마다 각 환경값의 평균을 출력하며, `Ctrl+C` 입력 시 시스템을 안전하게 종료한다.

---

## 2. 사용 모듈 및 선택 이유

| 모듈 | 종류 | 사용 이유 |
|------|------|-----------|
| `json` | Python 표준 라이브러리 | 환경 데이터를 JSON 형식으로 출력하기 위해 사용하였다. |
| `random` | Python 표준 라이브러리 | 더미 센서의 랜덤 환경 값 생성을 위해 사용하였다. 제약 조건에서 허용한 모듈이다. |
| `time` | Python 표준 라이브러리 | 5초 간격 반복(`time.sleep`)과 5분 경과 측정(`time.time`)을 위해 사용하였다. 제약 조건에서 허용한 시간 관련 모듈이다. |

---

## 3. 주요 코드 설명

### 3.1 DummySensor 클래스

실제 센서 연결 전 테스트를 위한 더미 센서 클래스이다.

- `__init__()` — `env_values` 딕셔너리를 멤버 변수로 선언하고 초기값을 `None`으로 설정한다.
- `set_env()` — `random.uniform(a, b)`로 각 항목의 지정 범위 내 실수 랜덤 값을 생성하여 `env_values`에 저장한다. 이산화탄소는 범위가 작아 소수점 4자리, 나머지는 2자리로 반올림한다.
- `get_env()` — `env_values`를 반환한다.

### 3.2 MissionComputer 클래스

환경 데이터를 주기적으로 수집하고 출력하는 클래스이다.

- `__init__()` — `env_values`를 빈 딕셔너리로, `history`를 빈 리스트로 초기화한다. `env_values`의 실제 항목은 `get_sensor_data()` 실행 시 `DummySensor`로부터 채워진다. `history`는 5분 평균 계산을 위해 매 5초 측정값을 누적 저장하는 용도이다.
- `get_sensor_data()` — 5초마다 센서 데이터를 읽어 JSON 형식으로 출력하고, 5분마다 평균값을 출력한다. `KeyboardInterrupt`로 루프를 종료한다.

### 3.3 5초 반복 및 종료 처리

```python
try:
    while True:
        ...
        time.sleep(5)
except KeyboardInterrupt:
    print('System stopped....')
```

`while True`로 무한 반복하며 `time.sleep(5)`로 5초 간격을 유지한다. `Ctrl+C` 입력 시 `KeyboardInterrupt` 예외가 발생하여 루프를 종료하고 종료 메시지를 출력한다.

### 3.4 5분 평균 계산

```python
if time.time() - start_time >= 300:
    avg = {
        key: round(sum(h[key] for h in self.history) / len(self.history), 4)
        for key in self.env_values
    }
```

`time.time()`으로 경과 시간을 측정하여 300초(5분)가 지나면 `history`에 누적된 값의 평균을 딕셔너리 컴프리헨션으로 계산하여 출력한다.

---

## 4. 각 환경값 랜덤 생성 범위

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

`RunComputer.get_sensor_data()` 호출 시 5초마다 아래와 같이 JSON 형식으로 출력된다.

```json
{
    "mars_base_internal_temperature": 28.37,
    "mars_base_external_temperature": 13.95,
    "mars_base_internal_humidity": 58.84,
    "mars_base_external_illuminance": 659.41,
    "mars_base_internal_co2": 0.0619,
    "mars_base_internal_oxygen": 4.55
}
```

5분 경과 시 평균값이 추가로 출력되며, `Ctrl+C` 입력 시 `System stopped....`를 출력하고 종료된다.

---

*본 보고서는 화성 기지 미션 컴퓨터 환경 모니터링 기능 구현을 위해 작성되었습니다.*