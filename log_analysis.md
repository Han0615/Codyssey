# 미션 컴퓨터 로그 분석 보고서

- **작성자:** 한송희 박사
- **작성일:** 2023-09-11
- **대상 파일:** mission_computer_main.log

---

## 1. 개요

화성 기지에서 발생한 폭발 사고의 원인을 파악하기 위해 미션 컴퓨터에 남아있던 로그 파일(`mission_computer_main.log`)을 분석하였다. 사고로 인해 모든 응용 프로그램이 삭제된 상황에서, Python을 활용하여 직접 로그 분석 프로그램(`main.py`)을 개발하고 사고 원인을 규명하였다.

---

## 2. 개발 환경 선정

### 2.1 Python을 선택한 이유

- 문법이 간결하여 긴급 상황에서도 빠르게 개발할 수 있다.
- 파일 입출력과 예외 처리가 기본 내장되어 있어 외부 라이브러리 없이 로그 처리가 가능하다.
- 과제 제약 조건(기본 라이브러리만 사용)을 충족한다.

### 2.2 개발 도구 선정 — VS Code

마이크로소프트의 무료 코드 편집기인 **VS Code**를 선택하였다. 가볍고 빠르며 Python 확장 플러그인을 통해 코드 자동완성, 디버깅, 실행 환경을 모두 지원한다. PyCharm 대비 설치가 간편하고 빠르게 사용할 수 있어 긴급한 상황에 적합하며, Jupyter Notebook보다 스크립트 파일 관리에 적합하다.

---

## 3. 코드 설계 및 구현 설명

### 3.1 파일 처리 방법 — `with` 구문 (Context Management)

Python에서 파일을 처리할 때 `with` 구문을 사용하면 블록이 종료될 때 예외 발생 여부와 관계없이 파일이 **자동으로 닫힌다.** 이는 리소스 누수를 방지하고 코드를 안전하게 만든다.

```python
with open('mission_computer_main.log', 'r', encoding='utf-8') as file:
    contents = file.read()
```

### 3.2 예외 처리 — `try / except / else / finally`

파일 처리 시 발생할 수 있는 예외를 안전하게 처리하기 위해 다음 구조를 사용하였다.

```
try:      정상적으로 실행할 코드
except:   예외 발생 시 실행할 코드
else:     예외가 발생하지 않았을 때만 실행할 코드
finally:  예외 여부와 관계없이 항상 실행할 코드
```

각 예외 항목과 선택 이유는 다음과 같다.

| 예외 | 발생 상황 | 처리 이유 |
|------|-----------|-----------|
| `FileNotFoundError` | 파일이 존재하지 않을 때 | 로그 파일이 삭제되었거나 경로가 잘못된 경우 대비 |
| `PermissionError` | 파일 읽기 권한이 없을 때 | 시스템 보안 설정으로 접근이 차단된 경우 대비 |
| `UnicodeDecodeError` | 파일 인코딩이 맞지 않을 때 | 로그 파일이 다른 인코딩으로 저장된 경우 대비 |
| `OSError` | 디스크 오류 등 OS 수준 오류 | 하드웨어 손상 등 예측 불가한 오류 포괄 처리 |

`else` 블록에 출력 코드를 배치한 이유는 파일을 성공적으로 읽었을 때만 내용을 출력하기 위함이다. `finally` 블록은 성공·실패 여부와 무관하게 항상 실행되어 프로세스 종료 메시지를 출력한다.

---

## 4. 로그 파일 분석

### 4.1 로그 파일 구조

`mission_computer_main.log` 파일은 CSV 형식으로, 다음 3개 필드로 구성되어 있다.

```
timestamp, event, message
```

- **timestamp:** 이벤트 발생 시각 (YYYY-MM-DD HH:MM:SS)
- **event:** 이벤트 레벨 (INFO, WARNING, ERROR, CRITICAL 등)
- **message:** 이벤트 상세 내용

### 4.2 전체 로그 내용

| timestamp | event | message |
|-----------|-------|---------|
| 2023-08-27 10:00:00 | INFO | Rocket initialization process started. |
| 2023-08-27 10:02:00 | INFO | Power systems online. Batteries at optimal charge. |
| 2023-08-27 10:05:00 | INFO | Communication established with mission control. |
| 2023-08-27 10:08:00 | INFO | Pre-launch checklist initiated. |
| 2023-08-27 10:10:00 | INFO | Avionics check: All systems functional. |
| 2023-08-27 10:12:00 | INFO | Propulsion check: Thrusters responding as expected. |
| 2023-08-27 10:15:00 | INFO | Life support systems nominal. |
| 2023-08-27 10:18:00 | INFO | Cargo bay secured and sealed properly. |
| 2023-08-27 10:20:00 | INFO | Final system checks complete. Rocket is ready for launch. |
| 2023-08-27 10:23:00 | INFO | Countdown sequence initiated. |
| 2023-08-27 10:25:00 | INFO | Engine ignition sequence started. |
| 2023-08-27 10:27:00 | INFO | Engines at maximum thrust. Liftoff imminent. |
| 2023-08-27 10:30:00 | INFO | Liftoff! Rocket has left the launchpad. |

### 4.3 단계별 미션 진행 현황

로그를 시간 순서에 따라 분석하면 다음과 같이 미션이 진행되었음을 알 수 있다.

1. **시스템 초기화 (10:00 ~ 10:20):** 전력, 통신, 추진, 생명 유지 장치 등 모든 시스템이 정상적으로 초기화됨.
2. **발사 준비 (10:20 ~ 10:27):** 최종 점검 완료 후 카운트다운 및 엔진 점화 시퀀스 시작.
3. **발사 (10:30):** 로켓이 발사대를 이탈하며 정상 이륙.
4. **로그 종료:** 발사 이후의 기록이 존재하지 않음.

---

## 5. 사고 원인 분석

### 5.1 로그 기반 분석

로그 파일에 기록된 모든 이벤트는 `INFO` 레벨이며, 발사 시점(10:30)을 끝으로 기록이 중단된다. 발사 이후의 비행, 화성 접근, 착륙 과정에 대한 로그가 전혀 존재하지 않는다.

이는 다음 두 가지 가능성을 시사한다.

1. **로그 저장 시스템의 손상:** 사고 발생 시 충격으로 인해 로그 저장 드라이브가 손상되어 발사 이후 데이터가 소실되었을 가능성.
2. **시스템 두절:** 발사 이후 미션 컴퓨터와의 연결이 끊어져 로그가 기록되지 않았을 가능성.

### 5.2 결론

로그 파일만으로는 **사고의 직접적인 원인을 특정하기 어렵다.** 로그는 발사까지 모든 시스템이 정상이었음을 보여주며, 발사 이후 기록이 존재하지 않기 때문에 화성 착륙 과정에서 발생한 폭발의 원인을 이 로그만으로 규명하는 것은 불가능하다.

추가 조사가 필요한 항목은 다음과 같다.

- 별도 드라이브에 저장된 다른 데이터 파일 분석
- 발사 이후 구간의 로그 데이터 복구 시도
- 하드웨어 물리적 손상 부위 육안 점검

---

*본 보고서는 화성 기지 사고 원인 규명을 위해 작성된 1차 분석 보고서입니다.*