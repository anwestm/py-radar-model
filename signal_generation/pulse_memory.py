import numpy as np


class PulseMemory:

    def __init__(self):
        self.latest_pulse = np.zeros(0)
        self.buffer = np.zeros(0)
        pass

    def handle_sample(self, sample, pulse_active):
        if pulse_active:
            self.buffer = np.append(self.buffer, sample)
        else:
            if len(self.buffer) > 0:
                self.latest_pulse = self.buffer
                self.buffer = np.zeros(0)


    def save_recorded_pulse(self, data):
        self.latest_pulse = data

    def get_latest_pulse(self):
        return self.latest_pulse