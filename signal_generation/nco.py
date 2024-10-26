import math
import numpy as np
import matplotlib.pyplot as plt

class NCO:

    sin_lookup_table = None

    def __init__(self, f_s, waveform_amplitude_bits, accumulator_bits, waveform_length_bits, phase_offset=0):
        """
        :param f_s: Sample frequency
        :param waveform_amplitude_bits: LUT item bit size (wave amplitude bit count) (y-axis)
        :param accumulator_bits: Phase accumulator length in bits
        :param waveform_length_bits: LUT sample count (in bits)  (x-axis)
        """
        self.__f_s = f_s
        self.__M = waveform_amplitude_bits
        self.__N = accumulator_bits
        self.__P = waveform_length_bits

        self.__generate_sin_lookup_table()

        self.__phase_accumulator = phase_offset / (2 * np.pi) * 2**self.__N

        self.__fcw = 0

        self.__amplitude = self.__bit_to_max_signed_ampl(self.__M)

    def __bit_to_max_signed_ampl(self, bit):
        return 2 ** (bit - 1) - 1

    def __generate_sin_lookup_table(self):
        self.sin_lookup_table = np.zeros(int(2**self.__P))

        amplitude = self.__bit_to_max_signed_ampl(self.__M)
        lut_len = len(self.sin_lookup_table)
        for i in range(lut_len):
            self.sin_lookup_table[i] = int(amplitude * np.sin(2 * math.pi * i / lut_len))

    def configure_nco(self, freq, amplitude):
        self.__fcw = np.round(freq * (2 ** self.__N) / self.__f_s)
        self.__amplitude = amplitude

    def get_sample(self):

        lut_index = self.__phase_accumulator // (2 ** (self.__N - self.__P))
        lut_index = min(int(lut_index), len(self.sin_lookup_table) - 1)

        # Normalize and rescale amplitude
        return self.__amplitude * (self.sin_lookup_table[lut_index] / self.__bit_to_max_signed_ampl(self.__M))
        #return self.sin_lookup_table[lut_index]

    def tick(self):
        self.__phase_accumulator += self.__fcw

        #self.__phase_accumulator %= 2**self.__N

        if self.__phase_accumulator >= 2**self.__N:
            self.__phase_accumulator -= 2 ** self.__N
        if self.__phase_accumulator < 0:
            self.__phase_accumulator += 2 ** self.__N

    def plot_sin_lookup_table(self):
        x = np.linspace(1, len(self.sin_lookup_table), len(self.sin_lookup_table))
        plt.scatter(x, self.sin_lookup_table)
        plt.show()