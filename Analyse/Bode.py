import numpy as np 
import matplotlib.pyplot as plt 
import sys
import os 





liste_fichier  = os.listdir("../Mesures/Bode à vide/")
#print(np.genfromtxt("../Mesures/Bode à vide/0.3Hz.csv",delimiter=";"))
def clean() : 
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
        #np.savetxt("Cleaned/Bode a Vide/"+name.replace(".csv","")+"_Cleaned.csv",mat,delimiter=";") 

        
        plt.plot((mat[:,0])/1e6,mat[:,1],label="Base X")
        plt.plot((mat[:,0])/1e6,mat[:,5],label="Haut Y")

        plt.legend()
        plt.title("bode à vide " + name.replace(".csv",""))
        plt.xlabel("t (s)")
        plt.ylabel("a (mg)")
    #plt.savefig("Image/Bode a vide/"+name.replace("csv","png"))
def naiveString(l:list) :
    out = "" 
    for i in l : 
        out += i 
    return out
def bode()  : 
    gain = []
    freq = []
    plt.figure()
    for i,name in enumerate(liste_fichier) :
        plt.subplot(4,4,i+1)
        frame = np.genfromtxt("Cleaned/Bode a Vide/"+name.replace(".csv","_Cleaned.csv"),delimiter=";")
        freq.append(float(naiveString([i for i in name[:-4] if i in "0123456789."])))
        gain.append(20*np.log10((np.max(frame[:,6])-np.min(frame[:,6]))/(np.max(frame[:,1])-np.min(frame[:,1])))) 
        plt.plot(frame[:,0],frame[:,1])
        plt.plot(frame[:,0],frame[:,6])

    return (freq,gain)
f,g = bode()
plt.figure()
print(f)
plt.semilogx(f,g,"rx") 
plt.show()
        

