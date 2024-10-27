import numpy as np

class MatchFilter:

    def __init__(self) -> None:
        pass

    
    def handle_samples(self, samples, reference_pulse):

        conj_pulse = np.conjugate(reference_pulse)
        reversed_pulse  = np.flip(conj_pulse)

        # TODO: handle 

        return np.convolve(samples, reversed_pulse)

    