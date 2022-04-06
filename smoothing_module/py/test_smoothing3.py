

import smoothing as sm
import matplotlib.pyplot as plt
import numpy as np

import time

if __name__ == "__main__":
    data = np.loadtxt("H.txt", skiprows=1)
    freq, Y = data.T

    start = time.time()
    Y_smooth1 = sm.smoothingMT(Y, freq, 12, 4) #smoothingMT(X, f, N_oct, nb_threads)
    stop = time.time()

    print("Native : ", stop - start, "s")

    plt.figure()
    plt.plot(freq, 20*np.log10(Y), label='original')
    plt.plot(freq, 20*np.log10(Y_smooth1), label="sums")
    plt.legend()
    plt.xlim(50, 10000)
    plt.show()