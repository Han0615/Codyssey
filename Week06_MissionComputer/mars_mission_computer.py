import json
import random
import time


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


RunComputer = MissionComputer()
RunComputer.get_sensor_data()