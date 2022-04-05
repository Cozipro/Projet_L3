import numpy as np
from scipy import signal
from scipy.fftpack import fft
from scipy.io import wavfile


Fs = 44100

def sinus(freq, amplitude, RSB, i, duration = 1):
    """
        freq = frequency of the signal (Hz)
        amplitude = amplitude of the signal
        RSB = signal-to-noise ratio (dB)
        i = animation variable
    """

    time = np.arange(0, duration, 1/(Fs))

    function = amplitude * np.sin(2 * np.pi * freq * time + i)

    noise = np.mean(function ** 2) / (10 ** (RSB / 10))
    function += np.sqrt(noise) * np.random.randn(len(time))
    function+= noise

    return time, function

def multiple_sinus(freq, amplitude,  RSB, i, duration = 1):
    """
        freq = frequency of the signal (Hz)
        amplitude = amplitude of the signal
        RSB = signal-to-noise ratio (dB)
        i = animation variable
    """

    time = np.arange(0, duration, 1/(Fs))

    function_1 = amplitude * np.sin(2 * np.pi * freq * time + i)
    function_2 = amplitude * np.sin(2 * np.pi * (freq*6/5) * time + i)
    function_3 = amplitude * np.sin(2 * np.pi * (freq * 3 / 2) * time + i)
    function_4 = amplitude * np.sin(2 * np.pi * (freq * 2) * time + i)

    function_final = function_1 + function_2 + function_3 + function_4

    noise = np.mean(function_final ** 2) / (10 ** (RSB / 10))
    function_final += np.sqrt(noise) * np.random.randn(len(time))
    function_final += noise

    return time, function_final


def sawtooth(freq, amplitude, RSB, i, duration = 1):
    """
       freq = frequency of the signal (Hz)
       amplitude = amplitude of the signal
       RSB = signal-to-noise ratio (dB)
       i = animation variable
    """

    time = np.arange(0, duration, 1/Fs)
    function = amplitude * signal.sawtooth(2 * np.pi * freq * time + i)
    noise = np.mean(function ** 2) / (10 ** (RSB / 10))
    function += np.sqrt(noise) * np.random.randn(len(time))
    function += noise
    return time, function


def multiple_sawtooth(freq, amplitude, RSB, i, duration = 1):
    """
       freq = frequency of the signal (Hz)
       amplitude = amplitude of the signal
       RSB = signal-to-noise ratio (dB)
       i = animation variable
    """

    time = np.arange(0, duration, 1 / Fs)
    function_1 = amplitude*signal.sawtooth(2 * np.pi * freq * time + i)
    function_2 = amplitude*signal.sawtooth(2 * np.pi * (freq*6/5)* time + i)
    function_3 = amplitude*signal.sawtooth(2 * np.pi * (freq*3/2) * time+ i)
    function_4 = amplitude*signal.sawtooth(2 * np.pi * freq *2* time + i)

    function_final = function_1 + function_2 + function_3 + function_4

    noise = np.mean(function_final ** 2) / (10 ** (RSB / 10))
    function_final += np.sqrt(noise) * np.random.randn(len(time))
    function_final += noise

    return time, function_final

def triangle(freq, amplitude, RSB, i, duration = 1):
    """
       freq = frequency of the signal (Hz)
       amplitude = amplitude of the signal
       RSB = signal-to-noise ratio (dB)
       i = animation variable
    """
    time = np.arange(0, duration, 1 / Fs)
    function = amplitude*signal.triangle(2 * np.pi * freq * time + i)

    noise = np.mean(function ** 2) / (10 ** (RSB / 10))
    function += np.sqrt(noise) * np.random.randn(len(time))
    function += noise

    return time, function


def multiple_triangle(freq, amplitude, RSB, i, duration = 1):
    """
       freq = frequency of the signal (Hz)
       amplitude = amplitude of the signal
       RSB = signal-to-noise ratio (dB)
       i = animation variable
    """

    time = np.arange(0, duration, 1 / Fs)

    function_1 = amplitude*signal.sawtooth(2 * np.pi * freq * time + i , 0.5)
    function_2 = amplitude*signal.sawtooth(2 * np.pi * (freq*6/5) * time + i, 0.5)
    function_3 = amplitude*signal.sawtooth(2 * np.pi * (freq*3/2) * time + i, 0.5)
    function_4 = amplitude*signal.sawtooth(2 * np.pi * (freq *2) * time + i, 0.5)

    function_final = function_1 + function_2 + function_3 + function_4

    noise = np.mean(function_final ** 2) / (10 ** (RSB / 10))
    function_final += np.sqrt(noise) * np.random.randn(len(time))
    function_final += noise

    return time, function_final



def square(freq, amplitude, RSB, i, duration = 1):
    """
       freq = frequency of the signal (Hz)
       amplitude = amplitude of the signal
       RSB = signal-to-noise ratio (dB)
       i = animation variable
    """

    time = np.arange(0, duration, 1/Fs)

    function = amplitude*signal.square(2 * np.pi * freq * time  + i)

    noise = np.mean(function ** 2) / (10 ** (RSB / 10))
    function += np.sqrt(noise) * np.random.randn(len(time))
    function += noise

    return time, function

def Gibbs(freq, RSB, number_of_sin, i, duration = 1):
    """
       freq = frequency of the signal (Hz)
       RSB = signal-to-noise ratio (dB)
       number_of_sin = nombre de sinus à sommer
       i = animation variable
    """
    time = np.arange(0, duration, 1/Fs)

    function = 0

    for k in range(1, number_of_sin):

        function = function + ((np.sin(2*np.pi*((2*k)-1)*freq*time+i))/((2*k)-1))
        function = (4/np.pi) * function

    noise = np.mean(function ** 2) / (10 ** (RSB / 10))
    function += np.sqrt(noise) * np.random.randn(len(time))
    function += noise

    return time, function


def multiple_square(freq, amplitude, RSB, i, duration = 1):
    """
       freq = frequency of the signal (Hz)
       amplitude = amplitude of the signal
       RSB = signal-to-noise ratio (dB)
       i = animation variable
    """
    time = np.arange(0, duration, 1/Fs)

    function_1 = amplitude* signal.square(2 * np.pi * freq * time  + i)
    function_2 = amplitude * signal.square(2 * np.pi * (freq*6/5) * time + i )
    function_3 = amplitude * signal.square(2 * np.pi * (freq*3/2) * time + i)
    function_4 = amplitude * signal.square(2 * np.pi * freq * 2* time + i)

    function_final = function_1 + function_2 + function_3 + function_4

    noise = np.mean(function_final ** 2) / (10 ** (RSB / 10))
    function_final += np.sqrt(noise) * np.random.randn(len(time))
    function_final += noise

    return time, function_final


def white_noise(N=50000):
    """
      N = Number of point of the white_noise. Default, 50000.
    """
    function = np.random.randn(N)
    time = np.arange(N)/Fs
    return time, function


def FFT(function, Fs, duration = 1):
    """
       Function who calculate the FFT of the signal 'function'
       with a sampling rate FS.
    """
    Ntfd = len(function)
    fft_data = abs(fft(function, Ntfd))
    frequency = np.arange(Ntfd) * Fs / Ntfd
    return frequency, fft_data


# The following functions could not be completed, but you can still try them



def chirp(Fmin, Fmax, i, duration = 1):
    """
        Fmin = minimal frequency of the signal (Hz)
        Fmin = maximal frequency of the signal (Hz)
        i = animation variable
    """

    time = np.arange(0, duration, 1 / Fs)
    function = signal.chirp(time + i , f0=Fmin, f1=Fmax, t1=duration,  method='logarithmic', phi=90)

    return time, function


def tone_bursts(freq, amplitude, i, duration = 1):
    """
       freq = frequency of the signal
       amplitude = amplitude of the signal
       i = animation variable
    """

    time = np.arange(0, duration, 1/Fs)
    phi0 = 2*np.pi*np.random.rand(1)
    sigma_t = 0.05/6
    tc = 3*sigma_t
    x = amplitude*np.cos(2*np.pi*freq*time+phi0+i)
    w = np.exp(-(time-tc)**2/(2*sigma_t**2))
    function = x*w

    return time, function


wavfile.write('sinus.wav', 44100, sinus(500, 1.2, 100, 0, duration = 50)[1])
