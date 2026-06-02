import csv
import os
import speech_recognition as sr
class JavisRecorder:
    def __init__(self):
        self.record_dir = 'records'
        if not os.path.exists(self.record_dir):
            os.makedirs(self.record_dir)

    def transcribe_to_csv(self):
        recognizer = sr.Recognizer()
        chunk_length = 4.5

        wav_files = [f for f in os.listdir(self.record_dir) if f.endswith('.wav')]

        for wav_file in wav_files:
            wav_path = f"{self.record_dir}/{wav_file}"
            csv_path = f"{self.record_dir}/{wav_file.replace('.wav', '.csv')}"

            with open(csv_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['start_time', 'end_time', 'text'])

                with sr.AudioFile(wav_path) as source:
                    
                    current_time = 0.0
                    while True:
                        audio = recognizer.record(source, duration=chunk_length)
                        
                        if len(audio.frame_data) == 0:
                            break  
                            
                        end_time = current_time + chunk_length
                        
                        try:
                            text = recognizer.recognize_google(audio, language='ko-KR')
                            writer.writerow([round(current_time, 1), round(end_time, 1), text])
                            print(f"  - [{current_time:.1f}s ~ {end_time:.1f}s] {text}")
                        except:
                            pass
                        
                        current_time += chunk_length
                    
            print(f"[완료] {csv_path} 저장 성공")

    def search_keyword(self, keyword):
        print(f'\n--- [검색] "{keyword}" ---')
        csv_files = [f for f in os.listdir(self.record_dir) if f.endswith('.csv')]
        found = False

        for csv_file in csv_files:
            csv_path = f"{self.record_dir}/{csv_file}"
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                data_rows = [row for row in reader if len(row) >= 3]

                full_text = " ".join([row[2] for row in data_rows])

                if keyword in full_text:
                    print(f'\n[발견] {csv_file} 파일에 포함되어 있습니다!')
                    found = True
                    
                    for i in range(len(data_rows)):
                        curr = data_rows[i][2]
                        nxt = data_rows[i+1][2] if i + 1 < len(data_rows) else ""
                        if keyword in curr or keyword in (curr + " " + nxt):
                            print(f'  -> ⏱️ 시간: {data_rows[i][0]}s 부근')
                            break
                        
        if not found:
            print("검색 결과가 없습니다.")

if __name__ == '__main__':
    javis = JavisRecorder()
    javis.transcribe_to_csv()

    while True:
        word = input('\n🔍 검색어 (종료: q): ').strip()
        if word.lower() == 'q': 
            print("프로그램을 종료합니다.")
            break
        if word: 
            javis.search_keyword(word)