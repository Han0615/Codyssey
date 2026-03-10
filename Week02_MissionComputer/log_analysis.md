# 미션 컴퓨터 로그 분석 보고서

- **작성자:** 한송희 박사
- **작성일:** 2023-08-27
- **대상 파일:** mission_computer_main.log

---

## 1. 개요

화성 기지에서 발생한 폭발 사고의 원인을 파악하기 위해 미션 컴퓨터에 남아있던 로그 파일(`mission_computer_main.log`)을 분석하였다. 사고로 인해 모든 응용 프로그램이 삭제된 상황에서, Python을 활용하여 직접 로그 분석 프로그램(`main.py`)을 개발하고 사고 원인을 규명하였다.

---

## 2. 개발 환경 선정

### 2.1 Python을 선택한 이유

- 문법이 간결하여 긴급 상황에서도 빠르게 개발할 수 있다.
- 파일 입출력과 예외 처리가 기본 내장되어 있어 외부 라이브러리 없이 로그 처리가 가능하다.

### 2.2 개발 도구 선정 — VS Code

마이크로소프트의 무료 코드 편집기인 VS Code를 선택하였다. 가볍고 빠르며 Python 확장 플러그인을 통해 코드 자동완성, 디버깅, 실행 환경을 모두 지원한다.

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

| 예외 | 발생 상황 | 출력 메시지 | 처리 이유 |
|------|-----------|-------------|-----------|
| `FileNotFoundError` | 파일이 존재하지 않을 때 | `[오류] 파일을 찾을 수 없습니다` | 로그 파일이 삭제되었거나 경로가 잘못된 경우 대비 |
| `PermissionError` | 파일 읽기 권한이 없을 때 | `[오류] 파일 읽기 권한이 없습니다` | 시스템 보안 설정으로 접근이 차단된 경우 대비 |
| `UnicodeDecodeError` | 파일 인코딩이 맞지 않을 때 | `[오류] 파일 인코딩 오류가 발생했습니다` | 로그 파일이 다른 인코딩으로 저장된 경우 대비 |
| `OSError` | 디스크 오류 등 OS 수준 오류 | `[오류] OS 오류가 발생했습니다` | 하드웨어 손상 등 예측 불가한 오류 포괄 처리 |

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
| 2023-08-27 10:32:00 | INFO | Initial telemetry received. Rocket is on its trajectory. |
| 2023-08-27 10:35:00 | INFO | Approaching max-Q. Aerodynamic pressure increasing. |
| 2023-08-27 10:37:00 | INFO | Max-Q passed. Vehicle is stable. |
| 2023-08-27 10:40:00 | INFO | First stage engines throttled down as planned. |
| 2023-08-27 10:42:00 | INFO | Main engine cutoff confirmed. Stage separation initiated. |
| 2023-08-27 10:45:00 | INFO | Second stage ignition. Rocket continues its ascent. |
| 2023-08-27 10:48:00 | INFO | Payload fairing jettisoned. Satellite now exposed. |
| 2023-08-27 10:50:00 | INFO | Orbital insertion calculations initiated. |
| 2023-08-27 10:52:00 | INFO | Navigation systems show nominal performance. |
| 2023-08-27 10:55:00 | INFO | Second stage burn nominal. Rocket velocity increasing. |
| 2023-08-27 10:57:00 | INFO | Entering planned orbit around Earth. |
| 2023-08-27 11:00:00 | INFO | Orbital operations initiated. Satellite deployment upcoming. |
| 2023-08-27 11:05:00 | INFO | Satellite deployment successful. Mission objectives achieved. |
| 2023-08-27 11:10:00 | INFO | Initiating deorbit maneuvers for rocket's reentry. |
| 2023-08-27 11:15:00 | INFO | Reentry sequence started. Atmospheric drag noticeable. |
| 2023-08-27 11:20:00 | INFO | Heat shield performing as expected during reentry. |
| 2023-08-27 11:25:00 | INFO | Main parachutes deployed. Rocket descent rate reducing. |
| 2023-08-27 11:28:00 | INFO | Touchdown confirmed. Rocket safely landed. |
| 2023-08-27 11:30:00 | INFO | Mission completed successfully. Recovery team dispatched. |
| 2023-08-27 11:35:00 | INFO | Oxygen tank unstable. |
| 2023-08-27 11:40:00 | INFO | Oxygen tank explosion. |
| 2023-08-27 12:00:00 | INFO | Center and mission control systems powered down. |

### 4.3 단계별 미션 진행 현황

로그를 시간 순서에 따라 분석하면 다음과 같이 미션이 진행되었음을 알 수 있다.

1. **시스템 초기화 및 발사 준비 (10:00 ~ 10:27):** 전력, 통신, 추진, 생명 유지 장치 등 모든 시스템이 정상적으로 초기화되고 최종 점검 완료.
2. **발사 및 상승 (10:30 ~ 10:45):** 정상 이륙 후 Max-Q 통과, 1단 분리 및 2단 점화까지 모든 과정 정상 수행.
3. **궤도 진입 및 임무 수행 (10:48 ~ 11:05):** 지구 궤도 진입 후 위성 분리 성공, 임무 목표 달성.
4. **귀환 및 착륙 (11:10 ~ 11:30):** 역추진 기동 후 대기권 재진입, 낙하산 전개 및 안전 착륙 완료. 임무 성공적으로 종료.
5. **사고 발생 (11:35 ~ 12:00):** 임무 완료 후 산소 탱크 불안정 감지, 5분 뒤 폭발 발생. 이후 모든 시스템 종료.

---

## 5. 사고 원인 분석

### 5.1 로그 기반 분석

로그 파일의 모든 이벤트는 `INFO` 레벨로 기록되어 있다. 임무 완료(11:30) 직후인 11:35에 산소 탱크 불안정(`Oxygen tank unstable`) 이 감지되었고, 불과 5분 후인 11:40에 산소 탱크 폭발(`Oxygen tank explosion`)이 발생하였다. 이후 12:00에 모든 시스템이 종료되었다.

주목할 점은 폭발 발생 전 사전 경고가 단 한 건(11:35)에 불과하고, 불안정 감지부터 폭발까지의 시간이 5분으로 매우 짧아 대응이 불가능했다는 것이다.

### 5.2 결론

로그 분석 결과 **사고의 직접적인 원인은 산소 탱크 폭발**로 확인된다. 발사부터 착륙까지 모든 미션 과정은 정상적으로 수행되었으나, 임무 완료 직후 산소 탱크에서 불안정 징후가 감지되었고 이것이 폭발로 이어져 화성 기지 전체 시스템이 종료되었다.

추가 조사가 필요한 항목은 다음과 같다.

- 산소 탱크 불안정의 근본 원인 파악 (제조 결함, 충격 손상, 압력 이상 등)
- 발사 전 산소 탱크 점검 기록 재검토
- 하드웨어 물리적 손상 부위 육안 점검

---
