import json
import os
import platform
import random
import time

import psutil


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
        return self.env_values


ds = DummySensor()


def load_settings():
    "setting.txt에서 출력할 항목을 읽어온다. 파일이 없으면 None을 반환"
    try:
        with open('setting.txt', 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return None
    except OSError as e:
        print(f'[오류] 설정 파일 읽기 실패: {e}')
        return None


class MissionComputer:
    def __init__(self):
        self.env_values = {}
        self.history = []

    def get_sensor_data(self):
        start_time = time.time()
        try:
            while True:
                ds.set_env()
                self.env_values = ds.get_env().copy()
                self.history.append(self.env_values.copy())
                print(json.dumps(self.env_values, indent=4))

                if time.time() - start_time >= 300:
                    avg = {
                        key: round(sum(h[key] for h in self.history) / len(self.history), 4)
                        for key in self.env_values
                    }
                    print('\n=== 5분 평균 값 ===')
                    print(json.dumps(avg, indent=4))
                    self.history = []
                    start_time = time.time()

                time.sleep(5)
        except KeyboardInterrupt:
            print('System stopped....')

    def get_mission_computer_info(self):
        try:
            info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'cpu_type': platform.processor(),
                'cpu_cores': os.cpu_count(),
                'memory_size': f'{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB',
            }
        except Exception as e:
            print(f'[오류] 시스템 정보 조회 실패: {e}')
            return

        settings = load_settings()
        if settings:
            info = {k: v for k, v in info.items() if k in settings}

        print(json.dumps(info, indent=4))

    def get_mission_computer_load(self):
        try:
            load = {
                'cpu_usage': f'{psutil.cpu_percent(interval=1)} %',
                'memory_usage': f'{psutil.virtual_memory().percent} %',
            }
        except Exception as e:
            print(f'[오류] 부하 정보 조회 실패: {e}')
            return

        settings = load_settings()
        if settings:
            load = {k: v for k, v in load.items() if k in settings}

        print(json.dumps(load, indent=4))


runComputer = MissionComputer()
runComputer.get_mission_computer_info()
runComputer.get_mission_computer_load()