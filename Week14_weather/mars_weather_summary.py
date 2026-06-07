import csv
import pymysql # pip install pymysql

class MySQLHelper:
    def __init__(self, host, user, password, db, charset='utf8'):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        self.connection = None

    def connect(self):
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db,
            charset=self.charset
        )

    def execute_update(self, query, args=None):
        if not self.connection:
            self.connect()
        
        with self.connection.cursor() as cursor:
            cursor.execute(query, args)
        
        self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()


def create_mars_weather_table(db_helper):
    # 명세서 요구사항에 맞춘 mars_weather 테이블 생성
    query = (
        'CREATE TABLE IF NOT EXISTS mars_weather ('
        'weather_id INT AUTO_INCREMENT PRIMARY KEY, '
        'mars_date DATETIME NOT NULL, '
        'temp INT, '
        'storm INT'
        ')'
    )
    db_helper.execute_update(query)
    print('mars_weather 테이블 생성이 완료되었습니다.')


def read_and_insert_weather_data(db_helper, file_path):
    # CSV 파일을 읽어서 내용을 확인하는 코드
    print('--- CSV 파일 데이터 읽기 및 확인 ---')
    
    insert_query = 'INSERT INTO mars_weather (mars_date, temp, storm) VALUES (%s, %s, %s)'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        print(f'헤더 정보: {headers}')
        
        count = 0
        for row in reader:
            mars_date = row[1]
            # 파일에는 21.4 같은 실수가 있으나 테이블 조건이 INT이므로 정수 변환
            temp = int(float(row[2]))
            storm = int(row[3])
            
            # 읽어온 내용을 화면에 출력하여 확인 (요구사항 반영)
            print(f'데이터 확인 -> 날짜: {mars_date}, 온도: {temp}, 폭풍: {storm}')
            
            # 데이터를 INSERT 쿼리로 변환하여 반복적으로 실행
            db_helper.execute_update(insert_query, (mars_date, temp, storm))
            count += 1
            
    print(f'--- 총 {count}건의 데이터가 mars_weather 테이블에 성공적으로 입력되었습니다. ---')


def main():
    # 본인의 MySQL 설치 환경에 맞게 정보를 입력해 주세요.
    db_host = 'localhost'
    db_user = 'root'
    db_password = 'root'
    db_name = 'mars_db'
    
    db_helper = MySQLHelper(db_host, db_user, db_password, db_name)
    
    try:  # <--- 여기서 시작했다면
        create_mars_weather_table(db_helper)
        csv_file_name = 'mars_weathers_data.CSV'
        read_and_insert_weather_data(db_helper, csv_file_name)
        
    except Exception as e:  # <--- 이 부분이 꼭 있어야 하고, try와 세로줄이 맞아야 합니다!
        print(f'시스템 오류 발생: {e}')
        
    finally:  # <--- 이 부분도 마찬가지입니다!
        db_helper.close()
        
if __name__ == '__main__':
    main()