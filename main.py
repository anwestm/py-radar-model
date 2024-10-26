from mpmath import linspace

#import signal_generation.nco
import signal_generation.pulse_generator
import matplotlib.pyplot as plt
import numpy as np


def main():

    #nco.plot_sin_lookup_table()

    Fs = 1e5
    ptg = signal_generation.pulse_generator.PulseGenerator(Fs)

    x = []
    amplitude = 2
    freq = 8000

    ptg.start_pulse_train(8000, amplitude, 0.01, 20)
    for i in range(50):
        x.append(ptg.sample())
        ptg.tick()


    fig = plt.figure(figsize=(10, 14))
    axs = fig.subplot_mosaic([["Signal", "Signal"], ["Re{Signal}", "Im{Signal}"], ["Phase", "Magnitude Log"]])
    axs["Signal"].set_title("Signal")
    axs["Signal"].set_xlabel("Time (s)")
    axs["Signal"].set_ylabel("Amplitude")
    axs["Signal"].plot(np.arange(0, len(x) / Fs, 1 / Fs), x, color="C0")

    axs["Re{Signal}"].set_title("Re{Signal}")
    axs["Re{Signal}"].set_xlabel("Time (s)")
    axs["Re{Signal}"].set_ylabel("Amplitude")
    axs["Re{Signal}"].plot(np.arange(0, len(x) / Fs, 1 / Fs), np.real(x), color="C1")

    axs["Im{Signal}"].set_title("Im{Signal}")
    axs["Im{Signal}"].set_xlabel("Time (s)")
    axs["Im{Signal}"].set_ylabel("Amplitude")
    axs["Im{Signal}"].plot(np.arange(0, len(x) / Fs, 1 / Fs), np.imag(x), color="C2")

    axs["Phase"].set_title("Phase Spectrum")
    axs["Phase"].phase_spectrum(x, Fs=Fs, color="C3")

    axs["Magnitude Log"].set_title("Magnitude Spectrum")
    axs["Magnitude Log"].magnitude_spectrum(x, Fs=Fs, scale='dB', color="C4")

   # dt = 1 / Fs
    #f = np.arange(0, len(x), dt)
   # plt.plot(f, X)
    plt.show()

    print("Done")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
