import numpy as np
import os
import shutil

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
        
        freq, freq2, H_abs, H_angle, coherence = data_object.get_data()
        
        temp = np.zeros((len(freq),3))
        temp[:,0] = freq
        temp[:,1]= H_abs
        temp[:,2] = H_angle
        np.savetxt("{}/MOD_PHASE.txt".format(path), temp, header="Freq / Module de H / Phase de H")
        
        print(freq2.dtype)
        temp = np.zeros((len(freq2),2))
        temp[:,0] = freq2
        temp[:,1] = np.abs(coherence)
        np.savetxt("{}/COHERENCE.txt".format(path), temp, header="Freq / COHERENCE")

        
if __name__ == '__main__':    
    data_saving(None)