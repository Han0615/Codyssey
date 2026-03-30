import random
from datetime import datetime


class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None,
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_env(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = (
            f"{timestamp},"
            f"{self.env_values['mars_base_internal_temperature']},"
            f"{self.env_values['mars_base_external_temperature']},"
            f"{self.env_values['mars_base_internal_humidity']},"
            f"{self.env_values['mars_base_external_illuminance']},"
            f"{self.env_values['mars_base_internal_co2']},"
            f"{self.env_values['mars_base_internal_oxygen']}"
        )
        try:
            with open('sensor_log.csv', 'a', encoding='utf-8') as log_file:
                log_file.write(log_line + '\n')
        except OSError as e:
            print(f'[오류] 로그 파일 저장 실패: {e}')

        return self.env_values


ds = DummySensor()
ds.set_env()
print(ds.get_env())