import numpy as np
from scipy.signal import chirp, correlate, welch, csd, hann
import sounddevice as sd
from scipy.fftpack import fft, ifftshift



class data:
    def __init__(self,figure, Fs, f_min, f_max, delta_F, ch_mesure, ch_ref, signal_type = "chirp",N_average = 1, name="mesure"):
        self.figure = figure[0]
        self.axes = figure[1]
        self.Fs = Fs
        self.f_min = f_min
        self.f_max = f_max
        self.temps = 1/delta_F
        self.name = name
        self.N_average = N_average
        self.ch_ref = ch_ref
        self.ch_mesure = ch_mesure
        
        self.N = self.temps*self.Fs
        
        if signal_type == "chirp":
            time = np.arange(self.N)/self.Fs #axe temporel pour la création du chirp
            
            signal=np.zeros(int((2+self.temps)*Fs))
            signal[Fs:int((1+self.temps)*Fs)] = chirp(time, self.f_min, self.temps, self.f_max, method='logarithmic', phi=90)
            
            self.record(signal)
            self.traitement()
            
        if signal_type == "white_noise":
            signal=np.zeros(int((2+self.temps)*Fs))
            print(int(self.temps*Fs))
            print(self.temps*Fs)
            signal[Fs:int((1+self.temps)*Fs)] = np.random.randn(int(self.temps*Fs))
            
            self.record(signal)
            self.traitement_welch()
        
        
        
    def record(self,signal):
        """
        

        Parameters
        ----------
        signal : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        n_min = int(1*self.Fs-0.2)
        n_max = int((1+self.temps+0.2)*self.Fs)
        
        self.x_mtr = np.zeros((n_max-n_min, self.N_average))
        self.y_mtr = np.zeros((n_max-n_min, self.N_average))
        
        
        for i in range(self.N_average):
            #On lit le sigal et on enregistre les signaux d'entrée
            data = sd.playrec(signal, self.Fs, channels=2, blocking=True)
            
            x = data[:,int(self.ch_ref)]
            y = data[:,int(self.ch_mesure)]
            
            
            #normalisation
            y = data[:,0]/2**23
            x = data[:,1]/2**23
            
            
            #corrélation pour enlever latence
            Rxy = correlate(signal, x)
            l = np.arange(-len(signal)+1, len(signal))
            N_max = np.argmax(Rxy)
            #t = l[N_max]/Fs #décalage en secondes
    
            #Décalage des signaux pour que leur début soit le même pour tous
            y = np.roll(y, -abs(l[N_max]))
            x = np.roll(x, -abs(l[N_max]))
            
            #on stock la mesure pour la traiter plus tard
            self.x_mtr[:,i] = x[n_min:n_max]
            self.y_mtr[:,i] = y[n_min:n_max]
        
        #Moyenne temporelle de tous les signaux
        self.x = np.mean(self.x_mtr, 1)
        self.y = np.mean(self.y_mtr, 1)
        

        
    def traitement(self):
        
        self.Nw = len(self.x)
        self.Ntfd = int(self.temps*self.Fs)
        Ntfd_c = 2*len(self.x)-1 #pour les correlations
        self.Y = fft(self.y, self.Ntfd)/self.Fs
        self.X = fft(self.x, self.Ntfd)/self.Fs
        self.freq = np.arange(self.Ntfd)*(self.Fs/self.Ntfd)

        self.H = self.Y/self.X
        
        
        Sxx_mtr = np.zeros((Ntfd_c,self.N_average), dtype=complex)
        Syy_mtr = np.zeros((Ntfd_c,self.N_average), dtype=complex)
        Sxy_mtr = np.zeros((Ntfd_c,self.N_average), dtype=complex)
        
        
        for i in range(self.N_average):
            x = self.x_mtr[:,i]
            y = self.y_mtr[:,i]
            
            Sxx = fft(ifftshift(correlate(x,x)),Ntfd_c)
            Syy = fft(ifftshift(correlate(y,y)),Ntfd_c)
            Sxy = fft(ifftshift(correlate(x,y)),Ntfd_c)
            
            Sxx_mtr[:,i]= Sxx
            Syy_mtr[:,i]= Syy
            Sxy_mtr[:,i]= Sxy
        
        
        Sxx = np.mean(Sxx_mtr, 1)
        Syy = np.mean(Syy_mtr, 1)
        Sxy = np.mean(Sxy_mtr, 1)
        
        self.coherence = np.round((np.abs(Sxy)**2/(Sxx*Syy)),3)
        self.freq2 = np.arange(Ntfd_c)*(self.Fs/Ntfd_c)        

        
        
    def data_plot(self):
        """
        Plot le module / phase et cohérence
        Set les limites des plots

        Returns
        -------
        None.

        """
        

        self.axes[0].plot(self.freq[1:self.Ntfd//2], 10*np.log(np.abs(self.H[1:self.Ntfd//2])), label=self.name)
        
        self.axes[0].set_xlim(self.f_min, self.f_max)

        self.axes[1].plot(self.freq[1:self.Ntfd//2], np.rad2deg(np.angle(self.H[1:self.Ntfd//2])), label=self.name)
        self.axes[1].set_xlim(self.f_min, self.f_max)
        
        self.axes[2].plot(self.freq2, self.coherence, label=self.name)
        self.axes[2].set_xlim(self.f_min, self.f_max)
        self.axes[2].set_ylim(None,1.1)
        
        

    def get_data(self):
        return self.freq, self.freq2, np.abs(self.H), np.angle(self.H), self.coherence
    
    def get_temporal_data(self):
        return self.x, self.y, self.Fs
        
        
    def traitement_welch(self):
        Nw = 512
        w = hann(Nw)
        
        Sxx_mtr = np.zeros((Nw//2+1,self.N_average), dtype=complex)
        Syy_mtr = np.zeros((Nw//2+1,self.N_average), dtype=complex)
        Sxy_mtr = np.zeros((Nw//2+1,self.N_average), dtype=complex)
        
        for i in range(self.N_average):
            x = self.x_mtr[:,i]
            y = self.y_mtr[:,i]
            

            freq, Sxx_mtr[i] = welch(x, fs = self.Fs, window = w, Nfft = 512) #à changer c'est du bricolage ça
            Syy_mtr[i] = welch(y, fs = self.Fs, window = w, Nfft = 512)[1]
            Sxy_mtr[i] = csd(x, y, fs = self.Fs, window = w, Nfft = 512)[1]
        
        
        Sxx = np.mean(Sxx_mtr, 1)
        Syy = np.mean(Syy_mtr, 1)
        Sxy = np.mean(Sxy_mtr, 1)
        
        
        self.H = Sxy/Sxx
        
        self.coherence = np.abs(Sxy)**2/(Sxx*Syy)
        
        
        
        
        
        
        