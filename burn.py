import os
from time import sleep

class CPUFingerBurn:
    def __init__(self, samples_per_second=2):
        assert samples_per_second > 0, 'Sample you must!'
        sample_size_in_seconds = 8
        self.min_num_samples = 8
        self.temps = []
        self.num_samples = max(round(samples_per_second * sample_size_in_seconds), self.min_num_samples)
        self.delay_between_samples = 1 / samples_per_second
        self.state = 'NOT PRESSED'

    def run(self):
        while True:
            self.record_temperature()
            self.update_state()
            self.print_state()
            sleep(self.delay_between_samples)

    def record_temperature(self):
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            self.temps.append(int(f.read()))
        self.temps = self.temps[-self.num_samples:]

    def update_state(self):
        if self.temp_increased:
            self.to_state('NOT PRESSED')
        if self.temp_decreased:
            self.to_state('PRESSED')

    def print_state(self):
        bar = "*"*int(self.current_temp//500) # a crude "graph"
        colour = '\033[91m' if self.state == 'PRESSED' else ''
        print(f'{colour}{self.current_temp} button is {self.state:>12} {bar}\033[00m')

    def to_state(self, state):
        self.state = state

    @property
    def state(self):
        return self.state

    @property 
    def temp_increased(self):
        if len(self.temps) < self.min_num_samples:
            return False
        precent_change = round(self.current_temp/self.avg_temp * 10000)/100
        return precent_change > 101

    @property 
    def temp_decreased(self):
        if len(self.temps) < self.min_num_samples:
            return False
        precent_change = round(self.current_temp/self.avg_temp * 10000)/100
        return precent_change < 97

    @property
    def avg_temp(self):
        if len(self.temps) < self.min_num_samples:
            return 999999999
        return sum(self.temps) / len(self.temps)

    @property
    def current_temp(self):
        return self.temps[-1]


sm = CPUFingerBurn()
sm.run()
