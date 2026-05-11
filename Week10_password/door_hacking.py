import itertools
import multiprocessing
import string
import time
import zipfile

ZIP_FILE = 'emergency_storage_key.zip'
CHARS = string.digits + string.ascii_lowercase
PASSWORD_LENGTH = 6


def unlock_zip():
    print(f'[시작] {time.strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'[정보] 문자 조합: 숫자 + 소문자 알파벳 / 자릿수: {PASSWORD_LENGTH}자리')
    start_time = time.time()
    count = 0

    try:
        with zipfile.ZipFile(ZIP_FILE) as zf:
            for combo in itertools.product(CHARS, repeat=PASSWORD_LENGTH):
                password = ''.join(combo)
                count += 1

                if count % 500000 == 0:
                    elapsed = time.time() - start_time
                    print(f'[시도] {count:,}회 | 경과 시간: {elapsed:.1f}초 | 현재: {password}')

                try:
                    zf.extractall(pwd=password.encode())
                    elapsed = time.time() - start_time
                    print(f'\n[성공] 암호 발견: {password}')
                    print(f'[완료] 총 시도: {count:,}회 | 소요 시간: {elapsed:.1f}초')

                    with open('password.txt', 'w', encoding='utf-8') as f:
                        f.write(password)
                    print('[저장] password.txt 저장 완료')
                    return password

                except Exception:
                    continue

    except FileNotFoundError:
        print(f'[오류] 파일을 찾을 수 없습니다: {ZIP_FILE}')
    except OSError as e:
        print(f'[오류] 파일 처리 중 오류 발생: {e}')

    print('[실패] 암호를 찾지 못했습니다.')
    return None


def _worker(args):
    """멀티프로세싱용 워커 함수 — 지정된 첫 글자 범위 내에서 암호를 탐색한다."""
    start_char, zip_file = args
    try:
        with zipfile.ZipFile(zip_file) as zf:
            for combo in itertools.product(CHARS, repeat=PASSWORD_LENGTH - 1):
                password = start_char + ''.join(combo)
                try:
                    zf.extractall(pwd=password.encode())
                    return password
                except Exception:
                    continue
    except Exception:
        pass
    return None


def unlock_zip_fast():
    """보너스 과제: 멀티프로세싱으로 병렬 탐색하여 더 빠르게 암호를 해독한다."""
    print(f'[시작 - 빠른 탐색] {time.strftime("%Y-%m-%d %H:%M:%S")}')
    start_time = time.time()

    args = [(char, ZIP_FILE) for char in CHARS]

    try:
        with multiprocessing.Pool() as pool:
            for result in pool.imap_unordered(_worker, args):
                if result:
                    pool.terminate()
                    elapsed = time.time() - start_time
                    print(f'\n[성공] 암호 발견: {result}')
                    print(f'[완료] 소요 시간: {elapsed:.1f}초')

                    try:
                        with open('password.txt', 'w', encoding='utf-8') as f:
                            f.write(result)
                        print('[저장] password.txt 저장 완료')
                    except OSError as e:
                        print(f'[오류] 파일 저장 실패: {e}')

                    return result

    except FileNotFoundError:
        print(f'[오류] 파일을 찾을 수 없습니다: {ZIP_FILE}')
    except OSError as e:
        print(f'[오류] 파일 처리 중 오류 발생: {e}')

    print('[실패] 암호를 찾지 못했습니다.')
    return None


if __name__ == '__main__':
    unlock_zip_fast()