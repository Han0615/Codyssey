import os

# 보너스 과제: 해독 결과 검증을 위한 텍스트 사전
# 화성 기지, 생존, 시스템 관련 영단어들을 등록해 둡니다.
DICTIONARY = ['mars', 'base', 'door', 'open', 'oxygen', 'system', 'emergency', 'help', 'safe']

def _shift_character(char, shift):
    """문자 하나를 주어진 칸(shift)만큼 카이사르 암호로 해독하여 반환하는 헬퍼 함수입니다."""
    if not char.isalpha():
        return char
        
    # 대문자와 소문자의 아스키코드 시작점 설정
    start = ord('A') if char.isupper() else ord('a')
    
    # 카이사르 암호 해독 연산: (현재문자 - 시작점 - 이동칸수) % 알파벳개수 + 시작점
    # 파이썬의 % 연산자는 음수일 때도 양수 나머지를 반환하므로 뒤로 도는 처리가 자연스럽게 됩니다.
    return chr((ord(char) - start - shift) % 26 + start)

def caesar_cipher_decode(target_text):
    """
    자리수(1~26)에 따라 암호표를 바꿔가며 해독 결과를 출력하고,
    사용자 입력 또는 보너스 사전 감지를 통해 result.txt에 저장하는 함수입니다.
    """
    print('--- 카이사르 암호 해독 시작 ---\n')
    
    auto_detected_shift = -1
    auto_detected_text = ''

    # 알파벳 개수인 26번 반복하여 모든 가능성을 검사합니다.
    for shift in range(1, 27):
        # target_text의 모든 문자에 대해 해독 수행
        decrypted_chars = [_shift_character(char, shift) for char in target_text]
        decrypted = ''.join(decrypted_chars)
        
        print(f'[{shift:2d}번째 자리수 이동] {decrypted}')

        # 보너스 과제 로직: 해독된 문장에 사전(DICTIONARY)의 단어가 포함되어 있는지 검사
        decrypted_lower = decrypted.lower()
        if any(word in decrypted_lower for word in DICTIONARY):
            print(f'\n[자동 감지] 암호 속에서 사전 키워드가 발견되어 반복을 멈춥니다! (자리수: {shift})')
            auto_detected_shift = shift
            auto_detected_text = decrypted
            break

    # 최종 저장할 자리수와 텍스트 변수
    save_shift = -1
    save_text = ''

    # 사전 탐색으로 자동 감지되었을 경우 사용자에게 확인
    if auto_detected_shift != -1:
        choice = input('자동 감지된 결과를 저장하시겠습니까? (y/n): ').strip().lower()
        if choice == 'y':
            save_shift = auto_detected_shift
            save_text = auto_detected_text

    # 자동 감지가 되지 않았거나, 사용자가 수동 입력을 원할 경우
    if save_shift == -1:
        while True:
            try:
                user_input = input('\n눈으로 식별되는 올바른 문장의 자리수 번호를 입력하세요 (취소: 0): ')
                selected_shift = int(user_input)
                
                if selected_shift == 0:
                    print('[취소] 저장을 취소하고 종료합니다.')
                    return
                elif 1 <= selected_shift <= 26:
                    save_shift = selected_shift
                    # 선택된 번호로 다시 한번 텍스트를 해독하여 저장본 준비
                    save_text = ''.join([_shift_character(c, selected_shift) for c in target_text])
                    break
                else:
                    print('[안내] 1부터 26 사이의 올바른 자리수 번호를 입력해 주세요.')
            except ValueError:
                print('[안내] 숫자만 입력해 주세요.')

    # 파일 저장 및 예외 처리
    try:
        with open('result.txt', 'w', encoding='utf-8') as file:
            file.write(save_text)
        print(f'\n[성공] {save_shift}번째 자리수 해독 결과가 result.txt에 안전하게 저장되었습니다.')
        print(f'[저장 내용] {save_text}')
    except OSError as e:
        print(f'\n[오류] result.txt 파일 저장 중 시스템 오류가 발생했습니다: {e}')

if __name__ == '__main__':
    # 1. 파일 읽기 및 예외 처리
    try:
        with open('password.txt', 'r', encoding='utf-8') as file:
            encrypted_text = file.read().strip()
            
        if not encrypted_text:
            print('[오류] password.txt 파일이 비어있습니다. 이전 과정에서 정상적으로 암호가 해독되었는지 확인하세요.')
        else:
            print(f'[정보] 읽어온 암호 텍스트: {encrypted_text}\n')
            caesar_cipher_decode(encrypted_text)
            
    except FileNotFoundError:
        print('[오류] password.txt 파일을 찾을 수 없습니다. 파일이 동일한 폴더에 있는지 확인해 주세요.')
    except OSError as e:
        print(f'[오류] 파일을 읽는 중 시스템 오류가 발생했습니다: {e}')