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
            
        n_min = int(1*Fs-0.2)
        n_max = int((1+self.temps+0.2)*Fs)
        
        self.x_mtr = np.zeros((n_max-n_min,N_average))
        self.y_mtr = np.zeros((n_max-n_min,N_average))
        
        
        
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
            
            self.x_mtr[:,i] = x[n_min:n_max]
            self.y_mtr[:,i] = y[n_min:n_max]
        
        
        self.x = np.mean(self.x_mtr, 1)
        self.y = np.mean(self.y_mtr, 1)
           
        
        #self.x = x
        #self.y = y
        
        self.traitement()
        
    def traitement(self):
        """
        Calcule la fonction de transfert et la fonction de cohérence.

        Returns
        -------
        None.

        """
        
        self.Nw = len(self.x)
        self.Ntfd = self.Nw #à faire:puissance de deux supérieure
        Ntfd_c = 2*len(self.x)-1 #pour les correlations
        self.Y = fft(self.y, self.Ntfd)
        self.X = fft(self.x, self.Ntfd)
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
        

        self.axes[0].plot(self.freq[1:self.Ntfd//2:10], 20*np.log(np.abs(self.H[1:self.Ntfd//2:10])), label=self.name)
        
        self.axes[0].set_xlim(self.f_min, self.f_max)
        self.axes[0].legend()

        self.axes[1].plot(self.freq[1:self.Ntfd//2:10], np.rad2deg(np.angle(self.H[1:self.Ntfd//2:10])), label=self.name)
        self.axes[1].set_xlim(self.f_min, self.f_max)
        
        self.axes[2].plot(self.freq2, self.coherence, label=self.name)
        self.axes[2].set_ylim(None,1.1)
        
        
        
        
    def save_txt(self):
        """
        Enregistre un fichier .txt contennant les paramètres de l'acquisition, 
        ainsi qu'un fichier contenant la mesure
        

        Returns
        -------
        None.

        """
        temp = np.zeros((len(self.freq[1:self.Ntfd//2]),3))
        temp[:,0] = self.freq[1:self.Ntfd//2]
        temp[:,1]=np.abs(self.H[1:self.Ntfd//2])
        temp[:,2] = np.angle(self.H[1:self.Ntfd//2])
        np.savetxt("{}_MOD_PHASE.txt".format(self.name), temp, header="Freq / Module de H / Phase de H")
        
        
        temp = np.zeros((len(self.freq[1:self.Ntfd//2]),2))
        temp[:,0] = self.freq[1:self.Ntfd//2]
        temp[:,0] = self.coherence[1:self.Ntfd//2]
        np.savetxt("{}_COHERENCE.txt".format(self.name), temp, header="Freq / COHERENCE")

        
        
        
        
        
        
        
        
        
        
        