import numpy as np
import matplotlib.pyplot as plt 
import os 
import scipy.signal as sig


for i in os.listdir("Cleaned/coup de vent") : 
    if "py"  in i :
        pass
    
    else :
        frame = np.genfromtxt("Cleaned/coup de vent/"+i,delimiter=";",invalid_raise=False)
        
        print(i)
        print(frame.shape)
        for j in range(len(frame)) : 
            if abs(frame[j,5]) > np.mean(frame[:,5])+200 : 
                break
        if j<len(frame)-1 :
            plt.errorbar((frame[j:,0]-frame[j,0])*1e-6,sig.savgol_filter(frame[j:,5],50,3),15,0,label=i) 
plt.grid("both")
plt.xlabel("t(s)") 
plt.xlim(left=0)
plt.ylabel("$a$ (mg)")
plt.legend()
plt.show() 