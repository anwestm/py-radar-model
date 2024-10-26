import signal_generation.nco
import numpy as np

class PulseGenerator:

    def __init__(self, clock_freq):
        self.__f_s = clock_freq
        waveform_amplitude_bits = 14
        accumulator_bits = 16
        waveform_length_bits = 16
        self.__nco_i = signal_generation.nco.NCO(clock_freq, waveform_amplitude_bits, accumulator_bits, waveform_length_bits,
                                          phase_offset=0)
        self.__nco_q = signal_generation.nco.NCO(clock_freq, waveform_amplitude_bits, accumulator_bits, waveform_length_bits,
                                          phase_offset=-np.pi / 2)

        self.__pulse_time_acc = 0
        self.__pulse_pw = 0
        self.__pulse_prf = 0


    def start_pulse_train(self, freq, amplitude, pw, prf):
        self.__nco_i.configure_nco(amplitude=amplitude, freq=freq)
        self.__nco_q.configure_nco(amplitude=amplitude, freq=freq)

        self.__pulse_pw = pw
        self.__pulse_prf = prf
        pass

    def stop_pulse_train(self):
        self.__pulse_time_acc = 0

    def sample(self):
        clk_dt = 1 / self.__f_s
        pri = 1 / self.__pulse_prf

        sample = 0 + 1j * 0
        if self.__pulse_time_acc <= self.__pulse_pw:
            sample = self.__nco_i.get_sample() + 1j * self.__nco_q.get_sample()

        self.__pulse_time_acc += clk_dt
        if self.__pulse_time_acc >= pri:
            self.__pulse_time_acc = 0


        return sample

    def tick(self):
        self.__nco_i.tick()
        self.__nco_q.tick()