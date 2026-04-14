# 미션 컴퓨터 구현 보고서

- **작성자:** 한승민
- **작성일:** 2026-04-14
- **파일명:** mars_mission_computer.py

---

## 1. 개요

화성 기지 미션 컴퓨터 복구 이후 환경 데이터를 지속적으로 수집하고 모니터링하는 기능과 함께, 컴퓨터의 상태를 파악하기 위한 시스템 정보 및 부하 조회 기능이 필요하였다. 더미 센서(`DummySensor`)로부터 랜덤 환경 데이터를 읽어 5초마다 출력하는 기능 외에, 운영체제, CPU, 메모리 등의 시스템 정보와 실시간 부하 상태를 JSON 형식으로 출력하는 기능을 `MissionComputer` 클래스에 추가로 구현하였다. 또한 `setting.txt` 파일을 통해 출력할 정보 항목을 설정할 수 있도록 확장하였다.

---

## 2. 사용 모듈 및 선택 이유

| 모듈 | 종류 | 사용 이유 |
|------|------|-----------|
| `json` | Python 표준 라이브러리 | 환경 데이터 및 시스템 정보를 JSON 형식으로 출력하기 위해 사용하였다. |
| `os` | Python 표준 라이브러리 | CPU 코어 수 등 시스템의 기본적인 하드웨어 정보를 가져오기 위해 사용하였다. |
| `platform` | Python 표준 라이브러리 | 운영체제 이름, 버전, CPU 타입 등의 시스템 식별 정보를 가져오기 위해 사용하였다. |
| `random` | Python 표준 라이브러리 | 더미 센서의 랜덤 환경 값 생성을 위해 사용하였다. 제약 조건에서 허용한 모듈이다. |
| `time` | Python 표준 라이브러리 | 5초 간격 반복(`time.sleep`)과 5분 경과 측정(`time.time`)을 위해 사용하였다. 제약 조건에서 허용한 시간 관련 모듈이다. |
| `psutil` | 외부 라이브러리 | 운영체제에 관계없이 실시간 CPU 사용량, 메모리 크기 및 사용량을 안정적으로 조회하기 위해 제약사항 예외를 적용하여 사용하였다. |

---

## 3. 주요 코드 설명

### 3.1 DummySensor 클래스

실제 센서 연결 전 테스트를 위한 더미 센서 클래스이다.

- `__init__()` — `env_values` 딕셔너리를 멤버 변수로 선언하고 초기값을 `None`으로 설정한다.
- `set_env()` — `random.uniform(a, b)`로 각 항목의 지정 범위 내 실수 랜덤 값을 생성하여 `env_values`에 저장한다. 이산화탄소는 범위가 작아 소수점 4자리, 나머지는 2자리로 반올림한다.
- `get_env()` — `env_values`를 반환한다.

### 3.2 load_settings 함수

보너스 과제 구현을 위한 설정 파일 읽기 함수이다.

- `setting.txt` 파일을 읽어 출력하고자 하는 키(항목)들을 리스트 형태로 반환한다.
- 파일이 존재하지 않거나(`FileNotFoundError`) 읽기 오류(`OSError`)가 발생할 경우 예외 처리를 통해 `None`을 반환하여 시스템 정보 전체 항목이 출력되도록 처리한다.

### 3.3 MissionComputer 클래스

환경 데이터 및 시스템 상태를 수집하고 제어하는 메인 클래스이다.

- `__init__()` — `env_values`를 빈 딕셔너리로, `history`를 빈 리스트로 초기화한다. `env_values`의 실제 항목은 `get_sensor_data()` 실행 시 `DummySensor`로부터 채워진다. 
- `get_sensor_data()` — 5초마다 센서 데이터를 읽어 JSON 형식으로 출력하고, 5분마다 평균값을 출력한다. `KeyboardInterrupt`로 루프를 종료한다.
- `get_mission_computer_info()` — `platform`, `os`, `psutil` 모듈을 활용하여 OS 종류, 버전, CPU 타입, 코어 수, 총 메모리 크기(GB)를 수집한다. `load_settings()`의 결과에 따라 지정된 항목만 필터링하여 JSON 포맷으로 출력한다.
- `get_mission_computer_load()` — `psutil` 모듈을 활용하여 실시간 CPU 사용량과 메모리 사용량을 수집한다. 마찬가지로 설정 파일에 따라 필터링 후 출력한다.

### 3.4 5초 반복 및 종료 처리

```python
try:
    while True:
        ...
        time.sleep(5)
except KeyboardInterrupt:
    print('System stopped....')