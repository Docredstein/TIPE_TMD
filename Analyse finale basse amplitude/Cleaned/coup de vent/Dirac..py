import numpy as np
import matplotlib.pyplot as plt 
import os 
for i in os.listdir() : 
    if ".csv" not in i :
        pass
    try :
        frame = np.genfromtxt(i,delimiter=";",invalid_raise=False)
    except:
        print(i)
    for j in range(len(frame)) : 
        if abs(frame[j,5]) > 10 : 
            break
    plt.plot(frame[j:,0]-frame[j,0],frame[j:,5],label=i) 
plt.grid("both")
plt.xlabel("t(s)") 
plt.ylabel("$a$ (mg)")
plt.show() 