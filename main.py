#from mpmath import linspace

#import signal_generation.nco
import signal_generation.pulse_generator
import matplotlib.pyplot as plt
import numpy as np
import signal_generation.pulse_memory
import receiver.matched_filter

Fs = 1e5
ptg = signal_generation.pulse_generator.PulseGenerator(Fs)
pm = signal_generation.pulse_memory.PulseMemory()
mf = receiver.matched_filter.MatchFilter()

def main():

    #nco.plot_sin_lookup_table()



    x = []
    amplitude = 20
    freq = 1000

    ptg.start_chirped_pulse_train(freq, amplitude, 0.01, 50, 2000)
    for i in range(10000):
        sample = ptg.sample()
        #sample += (np.random.rand()-0.5 + 1j * (np.random.rand()-0.5)) * 10
        x.append(sample)
        pm.handle_sample(sample, ptg.inside_pulse_window())
        ptg.tick()

    rx = mf.handle_samples(x, pm.get_latest_pulse())

    plot_tx(x)
    plot_rx(rx)

    plt.show()

    print("Done")

def plot_rx(x):

    fig = plt.figure(figsize=(10, 12))
    axs = fig.subplot_mosaic([["Matched Filter"]])
    axs["Matched Filter"].set_title("Signal")
    axs["Matched Filter"].set_xlabel("Time (s)")
    axs["Matched Filter"].set_ylabel("Amplitude")
    axs["Matched Filter"].plot(np.arange(0, len(x) / Fs, 1 / Fs), x, color="C0")

def plot_tx(x):

    fig = plt.figure(figsize=(10, 12))
    axs = fig.subplot_mosaic([["Signal", "Latest Pulse"], ["Re{Signal}", "Im{Signal}"], ["Phase", "Magnitude Log"]])
    axs["Signal"].set_title("Signal")
    axs["Signal"].set_xlabel("Time (s)")
    axs["Signal"].set_ylabel("Amplitude")
    axs["Signal"].plot(np.arange(0, len(x) / Fs, 1 / Fs), x, color="C0")

    axs["Latest Pulse"].set_title("Latest Pulse")
    axs["Latest Pulse"].set_xlabel("Time (s)")
    axs["Latest Pulse"].set_ylabel("Amplitude")
    axs["Latest Pulse"].plot(np.arange(0, len(pm.get_latest_pulse()) / Fs, 1 / Fs), pm.get_latest_pulse(), color="C0")

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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
