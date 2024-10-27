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
        self.__pulse_freq_acc = 0
        self.__pulse_pw = 0
        self.__pulse_prf = 0
        self.__pulse_freq = 0
        self.__pulse_ampl = 0
        self.__pulse_chirp_bw = 0


    def start_pulse_train(self, freq, amplitude, pw, prf):
        self.__nco_i.configure_nco(amplitude=amplitude, freq=freq)
        self.__nco_q.configure_nco(amplitude=amplitude, freq=freq)

        self.__pulse_pw = pw
        self.__pulse_prf = prf
        self.__pulse_freq = freq
        self.__pulse_ampl = amplitude

    def start_chirped_pulse_train(self, freq, amplitude, pw, prf, chirp_bw):
        self.__pulse_chirp_bw = chirp_bw
        self.__pulse_freq_acc = freq - (chirp_bw / 2)
        self.start_pulse_train(freq, amplitude, pw, prf)

    def stop_pulse_train(self):
        self.__pulse_time_acc = 0
        self.__pulse_chirp_bw = 0

    def sample(self):
        sample = 0 + 1j * 0
        if self.inside_pulse_window():
            self.__nco_i.configure_nco(amplitude=self.__pulse_ampl, freq=self.__pulse_freq_acc)
            self.__nco_q.configure_nco(amplitude=self.__pulse_ampl, freq=self.__pulse_freq_acc)
            #print(self.__pulse_freq_acc)
            sample = self.__nco_i.get_sample() + 1j * self.__nco_q.get_sample()

        return sample

    def inside_pulse_window(self):
        return self.__pulse_time_acc < self.__pulse_pw

    def tick(self):
        clk_dt = 1 / self.__f_s
        pri = 1 / self.__pulse_prf
    
        self.__pulse_time_acc += clk_dt
        if self.__pulse_time_acc >= pri:
            self.__pulse_time_acc = 0
            self.__pulse_freq_acc = self.__pulse_freq - self.__pulse_chirp_bw / 2

        if self.__pulse_chirp_bw != 0:
            # How many samples do we have to reach the max chrip freq before the pulse ends?
            freq_step_count = self.__pulse_pw / clk_dt
            self.__pulse_freq_acc += self.__pulse_chirp_bw / freq_step_count

        self.__nco_i.tick()
        self.__nco_q.tick()