import numpy as np 
import matplotlib.pyplot as plt 
import sys
import os 





liste_fichier  = os.listdir("../Mesures/Bode à vide/")
#print(np.genfromtxt("../Mesures/Bode à vide/0.3Hz.csv",delimiter=";"))
for name in liste_fichier :
    plt.figure()
    try :
        frame = np.genfromtxt("../Mesures/Bode à vide/"+name,delimiter=";")
    except Exception: 
        print(name, Exception)
    mat = [frame[:,0]]

    for i in range(1,len(frame[0])) : 
        out = []
        std = np.std(frame[:,i]) 
        mean = np.mean(frame[:,i])
        for j in frame[:,i] :
            if abs(j-mean)>2*std :
                out.append(mean)
            else :
                out.append(j)
        mat.append(out)
    mat = np.transpose(mat) 
    #np.savetxt("Cleaned/Bode a Vide/"+name.replace(".csv","")+"_Cleaned.csv",mat) 

    
    plt.plot((mat[:,0]-mat[0,0])/1e6,mat[:,1],label="Base X")
    plt.plot((mat[:,0]-mat[0,0])/1e6,mat[:,5],label="Haut Y")

    plt.legend()
    plt.title("bode à vide " + name.replace(".csv",""))
    plt.xlabel("t (s)")
    plt.ylabel("a (mg)")
    #plt.savefig("Image/Bode a vide/"+name.replace("csv","png"))

plt.show()

