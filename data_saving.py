import numpy as np
import os
import shutil
from scipy.io import wavfile

def data_saving(lst):
    """
    Parameters
    ----------
    lst : List
        List contenant les data_object.

    Returns
    -------
    None.

    """

    for data_object in lst:
        data_name = data_object.name
        
        parent_dir = "D:/Desktop/Université/projets_personnels/smaartV12/"
        path = os.path.join(parent_dir, data_name)
        
        try:
            os.mkdir(path)
        except FileExistsError:
            shutil.rmtree(path)
            os.mkdir(path)
        
        freq, freq2, H_abs, H_angle, coherence = data_object.get_data_FRF()
        
    
        temp = np.concatenate((freq, H_abs, H_angle)).reshape(3, len(freq)).T
        np.savetxt("{}/MOD_PHASE.txt".format(path), temp, header="Freq / Module de H / Phase de H")
        
        
        temp = np.concatenate((freq2, np.abs(coherence))).reshape(2, len(freq2)).T
        np.savetxt("{}/COHERENCE.txt".format(path), temp, header="Freq / COHERENCE")
        
        x, y, Fs = data_object.get_temporal_data()
        
        maxi = max(max(x), max(y))
        temp = np.concatenate((x/maxi, y/maxi)).reshape(2, len(x)).T
        
        wavfile.write("{}/{}.wav".format(path,data_name), Fs, temp)

    
if __name__ == '__main__':    
    data_saving(None)