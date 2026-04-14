# 미션 컴퓨터 시스템 정보 분석 보고서

- **작성자:** 한송희 박사
- **작성일:** 2026-04-14
- **파일명:** mars_mission_computer.py

---

## 1. 개요

미션 컴퓨터가 간헐적으로 다운되는 현상이 발생하여 컴퓨터의 상태를 파악할 필요가 생겼다. 이를 위해 기존 `MissionComputer` 클래스에 시스템 정보를 조회하는 `get_mission_computer_info()`와 실시간 부하를 조회하는 `get_mission_computer_load()` 메서드를 추가하였다. 또한 보너스 과제로 `setting.txt` 파일을 통해 출력 항목을 설정할 수 있도록 구현하였다.

---

## 2. 사용 모듈 및 선택 이유

| 모듈 | 종류 | 사용 이유 |
|------|------|-----------|
| `json` | 표준 라이브러리 | 시스템 정보와 부하 정보를 JSON 형식으로 출력하기 위해 사용하였다. |
| `os` | 표준 라이브러리 | `os.cpu_count()`로 CPU 코어 수를 가져오기 위해 사용하였다. |
| `platform` | 표준 라이브러리 | 운영체제 이름, 버전, CPU 타입을 가져오기 위해 사용하였다. |
| `random` | 표준 라이브러리 | 더미 센서의 환경 값을 랜덤으로 생성하기 위해 사용하였다. |
| `time` | 표준 라이브러리 | 5초 간격 반복과 5분 경과 측정을 위해 사용하였다. |
| `psutil` | 외부 라이브러리 (허용) | 메모리 크기, CPU·메모리 실시간 사용량을 가져오기 위해 사용하였다. 표준 라이브러리만으로는 실시간 사용량과 전체 메모리 크기를 크로스 플랫폼으로 가져올 수 없어 제약 조건상 허용된 시스템 정보 라이브러리로 사용하였다. |

---

## 3. 주요 코드 설명

### 3.1 `load_settings()` 함수

```python
def load_settings():
    try:
        with open('setting.txt', 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return None
    except OSError as e:
        print(f'[오류] 설정 파일 읽기 실패: {e}')
        return None
```

보너스 과제를 위한 함수이다. `setting.txt`에서 출력할 항목 목록을 읽어 리스트로 반환한다. 파일이 없으면 `None`을 반환하여 호출한 쪽에서 전체 항목을 출력하도록 한다. `get_mission_computer_info()`와 `get_mission_computer_load()` 두 메서드에서 공통으로 사용하기 때문에 클래스 외부에 독립 함수로 선언하였다.

### 3.2 `get_mission_computer_info()` 메서드

운영체제, 버전, CPU 타입, CPU 코어 수, 메모리 크기를 딕셔너리로 구성하여 JSON으로 출력한다.

- `platform.system()` — 운영체제 이름 반환 (예: `Windows`, `Linux`)
- `platform.version()` — 운영체제 버전 반환
- `platform.processor()` — CPU 타입 반환 (예: `x86_64`)
- `os.cpu_count()` — CPU 코어 수 반환
- `psutil.virtual_memory().total` — 전체 메모리를 바이트 단위로 반환. `1024 ** 3`으로 나누어 GB 단위로 변환

시스템 정보를 가져오는 부분 전체를 `try / except`로 감싸 예외 처리를 적용하였다. 이후 `load_settings()`로 `setting.txt`를 읽어 항목이 있으면 딕셔너리 컴프리헨션으로 해당 항목만 필터링하여 출력한다.

### 3.3 `get_mission_computer_load()` 메서드

CPU와 메모리의 실시간 사용량을 딕셔너리로 구성하여 JSON으로 출력한다.

- `psutil.cpu_percent(interval=1)` — 1초 동안 측정한 CPU 사용률을 퍼센트로 반환. `interval`을 지정하지 않으면 정확하지 않은 값이 나올 수 있어 1로 설정하였다.
- `psutil.virtual_memory().percent` — 현재 메모리 사용률을 퍼센트로 반환

`get_mission_computer_info()`와 동일하게 예외 처리와 `setting.txt` 필터링을 적용하였다.

---

## 4. 보너스 과제 — setting.txt

`setting.txt` 파일에 출력하고 싶은 항목명을 한 줄씩 작성하면 해당 항목만 출력된다. 파일이 없으면 전체 항목을 출력한다.

**설정 가능한 항목**

| 항목 키 | 설명 |
|---------|------|
| `os` | 운영체제 이름 |
| `os_version` | 운영체제 버전 |
| `cpu_type` | CPU 타입 |
| `cpu_cores` | CPU 코어 수 |
| `memory_size` | 전체 메모리 크기 |
| `cpu_usage` | CPU 실시간 사용량 |
| `memory_usage` | 메모리 실시간 사용량 |

---

## 5. 수행 결과

`runComputer.get_mission_computer_info()` 호출 시 아래와 같이 출력된다.

```json
{
    "os": "Windows",
    "os_version": "10.0.19045",
    "cpu_type": "Intel64 Family 6",
    "cpu_cores": 8,
    "memory_size": "16.0 GB"
}
```

`runComputer.get_mission_computer_load()` 호출 시 아래와 같이 출력된다.

```json
{
    "cpu_usage": "12.5 %",
    "memory_usage": "61.3 %"
}
```

---

*본 보고서는 화성 기지 미션 컴퓨터 상태 진단을 위해 작성되었습니다.*