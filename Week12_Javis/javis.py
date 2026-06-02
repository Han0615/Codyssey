import os
import wave
from datetime import datetime

import pyaudio 
# pip install pyaudio
class JavisRecorder:
    def __init__(self):
        self.record_dir = 'records'
        self._initialize_directory()

    def _initialize_directory(self):
        if not os.path.exists(self.record_dir):
            os.makedirs(self.record_dir)

    def record_voice(self, record_seconds=20): 
        chunk = 1024
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 44100

        audio = pyaudio.PyAudio()    # 오디오 제어 엔진 활성화

        print(f'\n[녹음 시작] {record_seconds}초 동안 음성을 기록합니다...')
        
        try:
            stream = audio.open(    # 마이크 스트림 개통
                format=audio_format,
                channels=channels,
                rate=rate,
                input=True,
                frames_per_buffer=chunk
            )

            frames = []
            
            for _ in range(0, int(rate / chunk * record_seconds)):
                data = stream.read(chunk)
                frames.append(data)

            print('[녹음 종료] 음성 데이터 수집을 완료했습니다.')

            stream.stop_stream()
            stream.close()

        except Exception as e:
            print(f'[시스템 오류] 마이크 인식 또는 녹음 중 문제가 발생했습니다: {e}')
            audio.terminate()
            return

        audio.terminate()

        now = datetime.now()
        file_name = now.strftime('%Y%m%d-%H%M%S') + '.wav'
        file_path = os.path.join(self.record_dir, file_name)
        
        try:
            with wave.open(file_path, 'wb') as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(audio.get_sample_size(audio_format))
                wf.setframerate(rate)
                wf.writeframes(b''.join(frames))
            print(f'[저장 성공] 기록이 안전하게 보관되었습니다: {file_path}')
        except OSError as e:
            print(f'[시스템 오류] 파일을 디스크에 저장할 수 없습니다: {e}')

if __name__ == '__main__':
    
    javis = JavisRecorder()
    
    javis.record_voice(record_seconds=20)
