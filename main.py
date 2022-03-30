import tkinter
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from data_class import data
import sounddevice as sd

plt.rc_context(
        {'axes.edgecolor': 'white', 'xtick.color': 'white', 'ytick.color': 'white', 'figure.facecolor': 'white'})
figure = plt.subplots(3, sharex= True)
lst_mesure = []


lst_devices_in = []
lst_devices_out = []
lst_devices = []

lst_save = []

#Liste contenant toutes les cartes son
devices = sd.query_devices()

#Triage des cartes pour les input/output
for device in devices:
    
    if device.get("max_input_channels") == 0:
        lst_devices_out.append(device.get("name"))
    elif device.get("max_output_channels") == 0:
        lst_devices_in.append(device.get("name"))
    lst_devices.append(device.get("name"))
    

m = tkinter.Tk() #creation de la fenetre
m.title("Logiciel de mesure acoustique") #titre de la fenetre

#création des labels
tkinter.Label(m, text="Interface IN").grid(row=0)
tkinter.Label(m, text="Interface OUT").grid(row=1)
tkinter.Label(m, text="Ch mesure").grid(row=2)
tkinter.Label(m, text="Ch référence").grid(row=3)
tkinter.Label(m, text='Freq min').grid(row=4)
tkinter.Label(m, text='Freq max').grid(row=5)
tkinter.Label(m, text='Δf / N_avg').grid(row=6)
tkinter.Label(m, text="Nom").grid(row=0, column=2)


ch_mesure = tkinter.Entry(m)
ch_ref = tkinter.Entry(m)
f_min_wd = tkinter.Entry(m)
f_max_wd = tkinter.Entry(m)
temps = tkinter.Entry(m)
n_average_entry = tkinter.Entry(m)
name_wdg = tkinter.Entry(m)

ch_mesure.grid(row=2, column=1)
ch_ref.grid(row=3, column=1)
f_min_wd.grid(row=4, column=1)
f_max_wd.grid(row=5, column=1)
temps.grid(row=6, column=1)
n_average_entry.grid(row=6, column=2)
name_wdg.grid(row=0, column=3)

ch_mesure.insert(0,"0")
ch_ref.insert(0,"1")
f_min_wd.insert(0,"20")
f_max_wd.insert(0,"20000")
temps.insert(0,"1")
n_average_entry.insert(0,"1")

device_in_wd = ttk.Combobox(m, values=lst_devices_in)
device_in_wd.grid(row=0,column=1)

device_out_wd = ttk.Combobox(m, values=lst_devices_out)
device_out_wd.grid(row=1,column=1)


def trace():
    figure[0].set_facecolor('k')

    
    for axe in figure[1]:
        axe.clear()
        axe.grid(True, alpha = 0.25)

    figure[1][0].set_title("MODULE", color="white")
    figure[1][1].set_title("PHASE", color="white")
    figure[1][2].set_title("COHERENCE", color="white")
    plt.tight_layout()
            
    for data_object in lst_mesure:
        data_object.data_plot()
    
    for axe in figure[1]:
        axe.set_facecolor('k')
        axe.legend()
        axe.spines['right'].set_visible(False)
        axe.spines['top'].set_visible(False)
    
    fig = plt.gcf()
    fig.show()
        
    

def mesure():
    ch_mesure_val = float(ch_mesure.get())
    ch_ref_val = float(ch_ref.get())
    f_min_value = float(f_min_wd.get())
    f_max_value = float(f_max_wd.get())
    temps_value = float(temps.get())
    name_value = str(name_wdg.get())
    n_average = int(n_average_entry.get())
    Fs_value = 44100
    
    interface_in = device_in_wd.get()
    interface_out = device_out_wd.get()
    
    sd.default.device = [lst_devices.index(interface_in),lst_devices.index(interface_out)]   
    
    lst_mesure.append(data(figure=figure, Fs=Fs_value, f_min=f_min_value, f_max=f_max_value, temps=temps_value, 
                           ch_mesure=ch_mesure_val, ch_ref=ch_ref_val, 
                           signal_type="chirp", 
                           name=name_value, N_average= n_average))
    

    #lst_save.append(tkinter.Button(m,text="Sauvegarder"))
    for index, truc in enumerate(lst_save):
        truc.grid(row=index, column=6)
        
    
    
    trace()
    
def clear():
    for i in lst_mesure[::-1]:
        lst_mesure.remove(i)
    
    
    for i in lst_save[::-1]:
        i.destroy()
        lst_save.remove(i)
        
    trace()
    
def save():
    for data_object in lst_mesure:
        data_object.save_txt()

B = tkinter.Button(m, text ="Mesure", command = mesure)
B.grid(row=7, column=0)

B_clear = tkinter.Button(m, text="Effacer", command = clear)
B_clear.grid(row=7, column = 1)

B_quit = tkinter.Button(m, text="Quit", command =m.quit)
B_quit.grid(row=7, column=2)

B_save = tkinter.Button(m, text="Sauvegarder", command = save)
B_save.grid(row=7, column=3)







m.mainloop()
plt.show()

        
        