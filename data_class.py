import numpy as np
from scipy.signal import chirp, correlate, windows, lfilter, savgol_filter
import sounddevice as sd
from scipy.fftpack import fft, ifft, fftshift, ifftshift
import matplotlib.pyplot as plt


class data:
    def __init__(self,figure, Fs, f_min, f_max, temps, ch_mesure, ch_ref, signal_type = "chirp",N_average = 1, name="mesure"):
        self.figure = figure[0]
        self.axes = figure[1]
        self.Fs = Fs
        self.f_min = f_min
        self.f_max = f_max
        self.temps = 1/temps
        self.name = name
        self.N_average = N_average
        
        self.N = self.temps*self.Fs
        
        if signal_type == "chirp":
            time = np.arange(self.N)/self.Fs #axe temporel pour la création du chirp
            
            signal=np.zeros(int((2+self.temps)*Fs))
            signal[Fs:int((1+self.temps)*Fs)] = chirp(time, self.f_min, self.temps, self.f_max, method='logarithmic', phi=90)
            
        elif signal_type == "white_noise":
            signal=np.zeros(int((self.temps+2)*self.Fs))
            
            signal[Fs:int((1+self.temps)*Fs)] = np.random.randn(int(self.N)) # white gaussian noise
            signal /= np.max(signal)
        
        self.x_mtr = np.zeros((len(signal),N_average))
        self.y_mtr = np.zeros((len(signal),N_average))
        
        
        #plt.figure()
        for i in range(N_average):
            data = sd.playrec(signal, self.Fs, channels=2, blocking=True)
            
            x = data[:,int(ch_ref)]
            y = data[:,int(ch_mesure)]
            
            
            #normalisation
            y = data[:,0]/2**15
            x = data[:,1]/2**15
            
            
            #corrélation pour enlever latence
            Rxy = correlate(signal, x)
            l = np.arange(-len(signal)+1, len(signal))
            N_max = np.argmax(Rxy)
            t = l[N_max]/Fs
    
            y = np.roll(y, -abs(l[N_max]))
            x = np.roll(x, -abs(l[N_max]))
            print(-abs(l[N_max]))
            
            self.x_mtr[:,i] = x
            self.y_mtr[:,i] = y
            
            #plt.plot(np.arange(len(x))/self.Fs, x)
        
        
        x = np.mean(self.x_mtr, 1)
        y = np.mean(self.y_mtr, 1)
        
        
        
        #plt.show()
        
        """
        t = np.arange(len(x))/Fs
        fig, ax = plt.subplots(2)
        for i in range(N_average):
            ax[0].plot(t, x_mtr[:,i], label="{}".format(i))
            
            ax[1].plot(t, y_mtr[:,i], label="{}".format(i))
            
        ax[0].plot(t, x, label = "moyenne")
        ax[1].plot(t, y, label = "moyenne")
        for axe in ax:
            axe.grid(True)
            axe.legend()
        plt.show()"""
        
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
        self.Ntfd = self.Nw #à faire:puissance de deux supérieure
        Ntfd_c = 2*len(self.x)-1 #pour les correlations
        self.Y = fft(self.y, self.Ntfd)
        self.X = fft(self.x, self.Ntfd)
        self.freq = np.arange(self.Ntfd)*(self.Fs/self.Ntfd)

        self.H = self.Y/self.X
        
        
    
        self.H2 = np.abs(self.H[1:self.Ntfd//2])
        # On va appliquer le filtre sur des fenêtres de la taille du signal/Ncut
        Ncut = 24
        Nwin = int(self.H2.size/Ncut)
        # Il nous faut un Nwin impair
        Nwin = Nwin if Nwin % 2 else Nwin + 1
        # On filtre data à l'ordre N=4 (on peut baisser l'ordre pour lisser plus)
        self.H2= savgol_filter(self.H2, Nwin, 3)
        
        """
        N_oct = 24
        
        f = self.freq[1:self.Ntfd//2]
        X = np.abs(self.H[1:self.Ntfd//2])
        X_oct = np.zeros(len(X))
        for i in range(len(f)):
            sigma = (f[i]/N_oct)/np.pi                      # standard deviation
            g = np.exp(-(((f-f[i])**2)/(2*(sigma**2))))
            g = g/np.sum(g)

            X_oct[i] = np.sum(g*X)
        self.H3 = X_oct
        """
        
        
        
        Sxx_mtr = np.zeros((Ntfd_c,self.N_average), dtype=complex)
        Syy_mtr = np.zeros((Ntfd_c,self.N_average), dtype=complex)
        Sxy_mtr = np.zeros((Ntfd_c,self.N_average), dtype=complex)
        
        
        
        #plt.figure()
        
        for i in range(self.N_average):
            x = self.x_mtr[:,i]
            y = self.y_mtr[:,i]
            
            Sxx = fft(ifftshift(correlate(x,x)))
            Syy = fft(ifftshift(correlate(y,y)))
            Sxy = fft(ifftshift(correlate(x,y)))
            
            Sxx_mtr[:,i]= Sxx
            Syy_mtr[:,i]= Syy
            Sxy_mtr[:,i]= Sxy
            

        
        self.freq2 = np.arange(Ntfd_c)*(self.Fs/Ntfd_c)
        

    
        
        Sxx = np.mean(Sxx_mtr, 1)
        Syy = np.mean(Syy_mtr, 1)
        Sxy = np.mean(Sxy_mtr, 1)
        
        
        
        self.coherence2 = np.abs(Sxy)**2/(Sxx*Syy)
        
        
        
        
        
    def data_plot(self):
        

        self.axes[0].plot(self.freq[1:self.Ntfd//2:10], 20*np.log(np.abs(self.H[1:self.Ntfd//2:10])), label=self.name)
        self.axes[0].plot(self.freq[1:self.Ntfd//2:10], 20*np.log(np.abs(self.H2[1:self.Ntfd//2:10])), label=self.name)
        #self.axes[1].semilogx(self.freq[1:self.Ntfd//2:10], 20*np.log(np.abs(self.H3[1:self.Ntfd//2:10])), label=self.name)
        
        self.axes[0].set_xlim(self.f_min, self.f_max)
        self.axes[0].legend()

        self.axes[1].plot(self.freq[1:self.Ntfd//2:10], np.rad2deg(np.angle(self.H[1:self.Ntfd//2:10])), label=self.name)
        self.axes[1].set_xlim(self.f_min, self.f_max)
        
        self.axes[2].plot(self.freq2, self.coherence2, color="r")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        