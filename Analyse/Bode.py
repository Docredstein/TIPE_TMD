import numpy as np 
import matplotlib.pyplot as plt 
import sys
import os 
from numpy.fft import fft 



folder = "masse en haut faible amplitude/"
liste_fichier  = os.listdir("ToClean/"+folder)
#print(np.genfromtxt("../Mesures/Bode à vide/0.3Hz.csv",delimiter=";"))
def clean() : 
    for name in liste_fichier :
        plt.figure()
        frame = None
        try :
            frame = np.genfromtxt("ToClean/"+folder+name,delimiter=";",usecols=np.arange(0,7),invalid_raise=False)
        except Exception as err: 
            print(name, err.__repr__())
            print(f"\033[91mERROR : The folder could not be read\033[0m : ToClean/{folder+name}")
        #print(frame)
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
        #print(mat)
        #np.savetxt("Cleaned/Bode a Vide/"+name.replace(".csv","")+"_Cleaned.csv",mat,delimiter=";") 

        
        plt.plot((mat[:,0])*1e-6,mat[:,1],label="Base X")
        plt.plot((mat[:,0])*1e-6,mat[:,5],label="Haut Y")

        plt.legend()
        plt.title( name.replace(".csv",""))
        plt.xlabel("t (s)")
        plt.ylabel("a (mg)")
        try :
            plt.savefig("Image/"+folder+name.replace("csv","png"))
        except FileNotFoundError:
            os.mkdir("Image/"+folder)
            plt.savefig("Image/"+folder+name.replace("csv","png"))
        try :
            np.savetxt("Cleaned/"+folder+name,mat,delimiter=";")
        except FileNotFoundError:
            os.mkdir("Cleaned/"+folder)
            np.savetxt("Cleaned/"+folder+name,mat,delimiter=";")

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
        frame = np.genfromtxt("Cleaned/"+folder+name,delimiter=";")
        #print(len(frame))
        bas = frame[:,1] 
        haut = frame[:,5]
        bas = bas - np.mean(bas) 
        haut = haut - np.mean(haut) 
        fft_bas = fft(bas)
        fft_haut = fft(haut)
        n = np.arange(len(fft_bas))
        
        frequence = (n/(frame[-1,0]-frame[0,0]))*1e6 #f = n/deltaT
        #print(n)
        #print(frequence)
        f_ind = np.argmax(np.abs(fft_bas)[:end_freq(frequence,10)]) 
        
        print(f_ind)
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
    #plt.show()
    return (freq, gain, phase)
for folder in os.listdir("ToClean/") :
    print(f"\033[92mTreating folder :\033[0m {folder}")
    #folder = "masse en haut faible amplitude/"
    try : 
        folder = folder + "/"
        liste_fichier  = os.listdir("ToClean/"+folder+"/")
        clean()
        print(f"\033[92mfolder Cleaned, creating bode diagramm\033[0m")
    except :
        print("\033[91mERROR\033[0m")
        raise
    print(bode())
    print(f"\033[92m\033[47mfolder all done")
    


