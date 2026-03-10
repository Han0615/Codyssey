print('Hello Mars')

def read_log(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            contents = file.read()
    except FileNotFoundError:
        print(f'[오류] 파일을 찾을 수 없습니다: {filename}')
    except PermissionError:
        print(f'[오류] 파일 읽기 권한이 없습니다: {filename}')
    except UnicodeDecodeError:
        print(f'[오류] 파일 인코딩 오류가 발생했습니다: {filename}')
    except OSError as e:
        print(f'[오류] OS 오류가 발생했습니다: {e}')
    else:
        print(contents)
    finally:
        print('로그 읽기 프로세스가 완료되었습니다.')

def main():
    log_filename = 'mission_computer_main.log'
    read_log(log_filename)

if __name__ == '__main__':
    main()
