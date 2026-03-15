import csv
from datetime import datetime

print('Hello Mars')

def parse_log(filename):
    log_entries = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                log_entries.append(row)
    except FileNotFoundError:
        print(f'[오류] 파일을 찾을 수 없습니다: {filename}')
    except PermissionError:
        print(f'[오류] 파일 읽기 권한이 없습니다: {filename}')
    except UnicodeDecodeError:
        print(f'[오류] 파일 인코딩 오류가 발생했습니다: {filename}')
    except OSError as e:
        print(f'[오류] OS 오류가 발생했습니다: {e}')
    else:
        return log_entries
    finally:
        print('로그 읽기 프로세스가 완료되었습니다.\n')
    return []


def print_log(log_entries):
    print('=== 전체 로그 내용 ===')
    for entry in log_entries:
        print(f"{entry['timestamp']}, {entry['event']}, {entry['message']}")
    print()


def analyze_event_level(log_entries):
    abnormal_levels = ['WARNING', 'ERROR', 'CRITICAL']
    results = [
        entry for entry in log_entries
        if entry['event'].strip().upper() in abnormal_levels
    ]
    return results


def analyze_keywords(log_entries):
    keywords = [
        'unstable', 'explosion', 'failure', 'anomaly',
        'malfunction', 'abort', 'powered down', 'critical', 'error'
    ]
    results = []
    for entry in log_entries:
        message_lower = entry['message'].lower()
        for keyword in keywords:
            if keyword in message_lower:
                results.append(entry)
                break
    return results


def analyze_time_interval(log_entries):
    time_format = '%Y-%m-%d %H:%M:%S'
    intervals = []

    for i in range(1, len(log_entries)):
        t1 = datetime.strptime(log_entries[i - 1]['timestamp'].strip(), time_format)
        t2 = datetime.strptime(log_entries[i]['timestamp'].strip(), time_format)
        intervals.append((t2 - t1).seconds)

    if not intervals:
        return []

    avg_interval = sum(intervals) / len(intervals)
    results = []
    for i, interval in enumerate(intervals):
        if interval > avg_interval * 2:
            results.append((log_entries[i + 1], interval, avg_interval))
    return results


def print_analysis(log_entries):
    print('=== 사고 원인 분석 ===')
    anomalies = set()

    # 방법 1: 이벤트 레벨 기반
    level_results = analyze_event_level(log_entries)
    if level_results:
        print('\n[분석 1] 비정상 이벤트 레벨 감지:')
        for entry in level_results:
            print(f"  {entry['timestamp']} | {entry['event']} | {entry['message']}")
            anomalies.add(entry['timestamp'])
    else:
        print('\n[분석 1] 비정상 이벤트 레벨 감지: 해당 없음')

    # 방법 2: 키워드 기반
    keyword_results = analyze_keywords(log_entries)
    if keyword_results:
        print('\n[분석 2] 이상 징후 키워드 감지:')
        for entry in keyword_results:
            print(f"  {entry['timestamp']} | {entry['event']} | {entry['message']}")
            anomalies.add(entry['timestamp'])
    else:
        print('\n[분석 2] 이상 징후 키워드 감지: 해당 없음')

    # 방법 3: 시간 간격 기반
    time_results = analyze_time_interval(log_entries)
    if time_results:
        print('\n[분석 3] 비정상 시간 간격 감지:')
        for entry, interval, avg in time_results:
            print(
                f"  {entry['timestamp']} | 간격: {interval}초 "
                f"(평균: {avg:.1f}초)"
            )
            anomalies.add(entry['timestamp'])
    else:
        print('\n[분석 3] 비정상 시간 간격 감지: 해당 없음')

    print('\n=== 종합 분석 결과 ===')
    if anomalies:
        print(f'총 {len(anomalies)}건의 이상 징후가 감지되었습니다.')
        print('사고 원인 분석을 위해 추가 조사가 필요합니다.')
    else:
        print('이상 징후가 감지되지 않았습니다.')


def main():
    log_filename = 'mission_computer_main.log'
    log_entries = parse_log(log_filename)
    if log_entries:
        print_log(log_entries)
        print_analysis(log_entries)


if __name__ == '__main__':
    main()
