import numpy as np
from scipy.signal import chirp, correlate, windows, lfilter
import sounddevice as sd
from scipy.fftpack import fft, ifft, fftshift


class data:
    def __init__(self,figure, Fs, f_min, f_max, temps, ch_mesure, ch_ref, signal_type = "chirp", name="mesure"):
        self.figure = figure[0]
        self.axes = figure[1]
        self.Fs = Fs
        self.f_min = f_min
        self.f_max = f_max
        self.temps = temps
        self.name = name
        
        self.N = self.temps*self.Fs
        self.delay = 0
        self.oppo = 1
        
        if signal_type == "chirp":
            time = np.arange(self.N)/self.Fs #axe temporel pour la création du chirp
            
            signal=np.zeros(int((2+self.temps)*Fs))
            signal[Fs:int((1+self.temps)*Fs)] = chirp(time, self.f_min, self.temps, self.f_max, method='logarithmic', phi=90)
            
        elif signal_type == "white_noise":
            signal=np.zeros(int((self.temps+2)*self.Fs))
            
            signal[Fs:int((1+self.temps)*Fs)] = np.random.randn(int(self.N)) # white gaussian noise
            signal /= np.max(signal)
        
        
        
        
        data = sd.playrec(signal, self.Fs, channels=2, blocking=True)
        
        x = data[:,int(ch_ref)]
        y = data[:,int(ch_mesure)]
        
        print(x.dtype)
        
        #normalisation
        y = data[:,0]/2**15
        x = data[:,1]/2**15
        
        
        #corrélation pour enlever le temps de vol
        Rxy = correlate(x, y)
        l = np.arange(-len(data)+1, len(data))
        N_max = np.argmax(Rxy)
        t = l[N_max]/Fs

        def delaysequence(x,n0):
            Nx = len(x)
            n0=int(n0)
            if n0<0:n0=1
            if n0>Nx-1:n0=Nx-1
            y = np.zeros(Nx,dtype=float)
            y[n0:] = x[:Nx-n0]
            return y;

        x = delaysequence(x, abs(l[N_max]))
        
        if signal_type == "chirp":
            Wr = np.zeros(len(x))
            
            n_min = int(1*Fs-0.2)
            n_max = int((1+self.temps+0.2)*Fs)
            Wr[n_min:n_max]=1
            W = Wr
            
        elif signal_type == "white_noise":
            n_min = int(1*Fs-0.2)
            n_max = int((1+self.temps+0.2)*Fs)
            
            win = np.zeros(len(signal))
            
            N_win = n_max-n_min
            win[n_min: n_max] = windows.hann(N_win,sym = True)
            
            W = win
    
        self.x = x*W
        self.y = y*W
        
        self.traitement()
        
    def traitement(self):
        self.Nw = len(self.x)
        self.Ntfd = self.Nw*3
        self.Y = fft(self.y, self.Ntfd)
        self.X = fft(self.x, self.Ntfd)
        self.freq = np.arange(self.Ntfd)*(self.Fs/self.Ntfd)

        self.H = self.Y/self.X
        self.h= np.real(ifft(self.H))
        self.h /= np.max(self.h[:int(self.Fs)])
        self.t_h = np.arange(self.Ntfd)/self.Fs
        
        Rxy = 1/self.Ntfd*fftshift(np.real(ifft(self.Y*np.conj(self.X))))
        Rxx = 1/self.Ntfd*fftshift(np.real(ifft(np.abs(self.X)**2)))
        Ryy = 1/self.Ntfd*fftshift(np.real(ifft(np.abs(self.Y)**2)))

        l = -self.Ntfd//2+np.arange(self.Ntfd)

        Sxy = fft(Rxy)
        Sxx = fft(Rxx)
        Syy = fft(Ryy)

        self.coherence = np.real(np.abs(Sxy)**2/(Sxx*Syy))
        
        #test (attention à la RI)
        self.H = self.oppo*self.H*np.exp(-1j*2*self.freq*self.delay*1e-3)
        
        print(self.Fs)
        print(self.Ntfd)
        print(self.Fs/self.Ntfd)
        
    def data_plot(self):
        N_avg = 365
        h_avg = np.ones(N_avg)/N_avg
        H_avg = lfilter(h_avg, [1.],np.abs(self.H))
        
        
        
        self.axes[0].plot(self.t_h[:int(0.2*self.Fs)], self.h[:int(0.2*self.Fs)], label=self.name)


        #ax11 = self.axes[1].twinx()
        #ax11.semilogx(self.freq, self.coherence, color="b")

        self.axes[1].semilogx(self.freq[1:self.Ntfd//2:10], 20*np.log(np.abs(self.H[1:self.Ntfd//2:10])), label=self.name)
        self.axes[1].semilogx(self.freq[1:self.Ntfd//2:10], 20*np.log(H_avg[1:self.Ntfd//2:10]), label=self.name)
        
        self.axes[1].set_xlim(self.f_min, self.f_max)
        self.axes[1].legend()

        self.axes[2].semilogx(self.freq[1:self.Ntfd//2:10], np.rad2deg(np.angle(self.H[1:self.Ntfd//2:10])), label=self.name)
        self.axes[2].set_xlim(self.f_min, self.f_max)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        