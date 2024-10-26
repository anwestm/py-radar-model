from mpmath import linspace

import signal_generation.nco
import matplotlib.pyplot as plt
import numpy as np


def main():
    Fs = 1e5
    nco = signal_generation.nco.NCO(f_s=Fs, waveform_amplitude_bits=14, accumulator_bits=12, waveform_length_bits=12, phase_offset=0)
    #nco.plot_sin_lookup_table()

    nco.configure_nco(amplitude=30, freq=8000)

    x = []
    amplitude = 0
    for i in range(3000):
        amplitude = 200+100*np.sin((i/1000)*2*np.pi)
        nco.configure_nco(amplitude=amplitude, freq=8000)
        x.append(nco.get_sample())
        #x.append(nco.get_sample())
        nco.tick()


    fig = plt.figure(figsize=(10, 7))
    axs = fig.subplot_mosaic([["Signal", "Signal"], ["Phase", "Magnitude Log"]])
    axs["Signal"].set_title("Signal")
    axs["Signal"].set_xlabel("Time (s)")
    axs["Signal"].set_ylabel("Amplitude")
    axs["Signal"].plot(np.arange(0, len(x) / Fs, 1 / Fs), x, color="C0")

    axs["Phase"].set_title("Phase Spectrum")
    axs["Phase"].phase_spectrum(x, Fs=Fs, color="C1")

    axs["Magnitude Log"].set_title("Magnitude Spectrum")
    axs["Magnitude Log"].magnitude_spectrum(x, Fs=Fs, scale='dB', color="C2")

   # dt = 1 / Fs
    #f = np.arange(0, len(x), dt)
   # plt.plot(f, X)
    plt.show()

    print("Done")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
