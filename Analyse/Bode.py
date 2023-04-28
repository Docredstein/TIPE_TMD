import numpy as np 
import matplotlib.pyplot as plt 
import sys
import os 
from numpy.fft import fft 



folder = "Cleaned/Bode a vide/"
liste_fichier  = os.listdir(folder)
#print(np.genfromtxt("../Mesures/Bode à vide/0.3Hz.csv",delimiter=";"))
def clean() : 
    for name in liste_fichier :
        plt.figure()
        try :
            frame = np.genfromtxt(folder+name,delimiter=";")
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
def end_freq(l:list,end_freq:float)->int :
    for i in range(len(l)) :
        if l[i]>=end_freq :
            return i
    raise Exception("fréquence non trouvée")
def bode()  : 
    gain = []
    phase = []
    freq = []
    plt.figure()
    for i,name in enumerate(liste_fichier) :
        frame = np.genfromtxt(folder+name,delimiter=";")
        bas = frame[:,1] 
        haut = frame[:,5]
        bas = bas - np.mean(bas) 
        haut = haut - np.mean(haut) 
        fft_bas = fft(bas)
        fft_haut = fft(haut)
        n = np.arange(len(fft_bas))
        
        frequence = (n/(frame[-1,0]-frame[0,0]))*1e6 #f = n/deltaT
        f_ind = np.argmax(np.abs(fft_bas)[:end_freq(frequence,10)]) 
        #print(frequence)
        #print(f_ind)
        freq.append(frequence[f_ind])
        gain.append(20*np.log(np.abs(fft_haut[f_ind])/np.abs(fft_bas[f_ind]))) 
        phase.append(np.angle(fft_haut[f_ind])-np.angle(fft_bas[f_ind]))
        #print(name,freq[-1],gain[-1],phase[-1])
    plt.subplot(2,1,1)
    plt.semilogx(freq,gain,"x")
    plt.grid(True,"both")
    plt.ylabel("$G_{dB}$ (dB)")
    plt.subplot(2,1,2) 
    plt.semilogx(freq,phase,"x")
    plt.ylabel("φ (rad)")
    plt.xlabel("Fréquence d'excitation (Hz)")
    plt.grid(True,"both")
    plt.suptitle(folder.split("/")[-2])
    plt.savefig("Image/"+folder.replace(" ","_").split("/")[-2]+".png")
    out = np.concatenate((freq,gain,phase)).reshape((len(freq),3))
    np.savetxt(folder.split("/")[-2]+".csv",out,delimiter=";")
    plt.show()
    return (freq, gain, phase)
print(bode())
    


