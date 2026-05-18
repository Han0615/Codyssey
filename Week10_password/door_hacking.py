import itertools
import multiprocessing
import os
import string
import time
import io

# C 언어 기반으로 최적화된 외부 라이브러리 적용
import pyzipper 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_FILE = os.path.join(BASE_DIR, 'emergency_storage_key.zip')
CHARS = string.digits + string.ascii_lowercase
PASSWORD_LENGTH = 6

def save_password(password):
    """해독된 암호를 파일로 저장하고 압축을 해제합니다."""
    try:
        with pyzipper.AESZipFile(ZIP_FILE) as zf:
            zf.extractall(pwd=password.encode('utf-8'))
        
        txt_path = os.path.join(BASE_DIR, 'password.txt')
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(password)
        print(f'[저장] {txt_path} 에 암호 기록 및 파일 압축 해제 완료')
    except OSError as e:
        print(f'[오류] 파일 저장 실패: {e}')

def _worker(args):
    """
    워커 노드: 할당된 시작 글자 범위 내에서 암호를 탐색합니다.
    """
    start_char, zip_bytes, stop_event, result_queue = args
    zip_buffer = io.BytesIO(zip_bytes)
    
    try:
        with pyzipper.AESZipFile(zip_buffer) as zf:
            first_file = zf.namelist()[0]
            count = 0  # 시도 횟수 카운터 추가
            
            for combo in itertools.product(CHARS, repeat=PASSWORD_LENGTH - 1):
                count += 1
                
                # [성능 최적화] 10만 번마다 한 번씩만 킬 스위치를 확인하여 통신 병목 제거
                if count % 100000 == 0 and stop_event.is_set():
                    return
                
                password = start_char + ''.join(combo)
                try:
                    zf.read(first_file, pwd=password.encode('utf-8'))
                    
                    stop_event.set()
                    result_queue.put(password)
                    return
                
                except RuntimeError:
                    continue
                except pyzipper.zipfile.BadZipFile:
                    continue
                except Exception:
                    continue
                    
    except Exception as e:
        pass

def unlock_zip():
    """매니저 노드: 멀티프로세싱 환경을 통제하고 자원을 분배합니다."""
    print(f'[시작 - 고성능 탐색] {time.strftime("%Y-%m-%d %H:%M:%S")}')
    start_time = time.time()

    if not os.path.exists(ZIP_FILE):
        print(f'[오류] 해당 경로에 파일이 없습니다: {ZIP_FILE}')
        return

    # [핵심] 1. 대상 파일을 하드디스크에서 한 번만 읽어 RAM(메모리)에 적재
    try:
        with open(ZIP_FILE, 'rb') as f:
            zip_bytes = f.read()
    except OSError as e:
        print(f'[오류] 파일을 메모리로 읽는 중 오류 발생: {e}')
        return

    # [핵심] 2. 프로세스 간 통신(IPC)을 위한 이벤트와 큐 생성
    manager = multiprocessing.Manager()
    stop_event = manager.Event()
    result_queue = manager.Queue()

    # 각 프로세스에 전달할 인자 세팅 (시작 글자 분할, 메모리 데이터, IPC 객체)
    args = [(char, zip_bytes, stop_event, result_queue) for char in CHARS]

    # CPU 바운드 작업에 유리한 멀티프로세싱 풀 가동
    pool = multiprocessing.Pool()
    
    try:
        # 비동기적으로 워커 노드 실행
        pool.map_async(_worker, args)
        
        # 큐에 결과가 들어올 때까지 대기하거나 모든 작업이 끝날 때까지 대기
        while not stop_event.is_set():
            time.sleep(0.1) # CPU 점유율 조절을 위한 짧은 대기
            
            # 워커들이 모두 종료되었는데도 이벤트가 셋팅되지 않았다면 실패한 것
            # (실제 상용 환경에서는 워커 종료 상태를 더 엄밀하게 체크해야 하지만, 
            # 여기서는 편의상 큐 확인 로직을 우선합니다)
            
        if not result_queue.empty():
            found_password = result_queue.get()
            elapsed = time.time() - start_time
            print(f'\n[성공] 암호 발견: {found_password}')
            print(f'[완료] 소요 시간: {elapsed:.1f}초')
            
            pool.terminate() # 나머지 좀비 프로세스 즉각 처단 (Kill Switch 보완)
            save_password(found_password)
            return found_password

    except KeyboardInterrupt:
        print("\n[중지] 사용자에 의해 강제 종료되었습니다.")
        pool.terminate()
    finally:
        pool.close()
        pool.join()

    print('\n[실패] 암호를 찾지 못했습니다.')
    return None

if __name__ == '__main__':
    multiprocessing.freeze_support()
    unlock_zip()