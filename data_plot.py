import matplotlib.pyplot as plt
import numpy as np


def data_plot_FRF(figure, lst_mesure, f_min, f_max):
    fig, axe = figure
    
    for data_object in lst_mesure:
        freq, freq2, H_module, H_phase, coherence = data_object.get_data_FRF()
        
        Ntfd = data_object.Ntfd
        name = data_object.name
        
        axe[0].plot(freq[1:Ntfd//2], H_module[1:Ntfd//2], label=name)
        
        axe[0].set_xlim(f_min, f_max)

        axe[1].plot(freq[1:Ntfd//2], np.rad2deg(H_phase[1:Ntfd//2]), label=name)
        axe[1].set_xlim(f_min, f_max)
        
        axe[2].plot(freq2, coherence, label=name)
        axe[2].set_xlim(f_min, f_max)
        axe[2].set_ylim(0,1.1)
        
        
    plt.show()
    
def data_plot_Power_Spectrum(figure, lst_mesure, f_min, f_max):
    fig, axe = figure
    
    for data_object in lst_mesure:
        
        freq, X, Y = data_object.get_frequency_data()
        axe.plot(freq, X, label="Référence")
        axe.plot(freq, Y, label="Signal")
        
    plt.show()