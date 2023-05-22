import numpy as np 
import matplotlib.pyplot as plt 
import sys
import os 
from tqdm import tqdm
from numpy.fft import fft 



folder = "masse en haut faible amplitude/"
liste_fichier  = os.listdir("ToClean/")
#print(np.genfromtxt("../Mesures/Bode à vide/0.3Hz.csv",delimiter=";"))
def clean() : 
    for name in tqdm(liste_fichier) :
        plt.figure(figsize=(10,5))
        frame = None
        try :
            frame = np.genfromtxt("ToClean/"+folder+name,delimiter=";",usecols=np.arange(0,7),invalid_raise=False)
        except Exception as err: 
            #print(name, err.__repr__())
            print(f"\033[91mERROR : The folder could not be read\033[0m : ToClean/{folder+name}")
        #print(frame)
        mat = [frame[:,0]]

        for i in range(1,len(frame[0])) : 
            out = []
            std = np.std(frame[:,i]) 
            mean = np.mean(frame[:,i])
            for j in frame[:,i] :
                if abs(j-mean)>2*std :
                    out.append(0)
                else :
                    out.append(j-mean)
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
            plt.savefig("Image/"+folder+name.replace(".csv",".pdf"))
        except FileNotFoundError:
            os.mkdir("Image/"+folder)
            plt.savefig("Image/"+folder+name.replace(".csv",".pdf"))
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
    xerr = []
    yerr = []
    plt.figure(figsize=(10,5))
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
        
        #print(f_ind)
        freq.append(frequence[f_ind])
        gain.append(20*np.log(np.abs(fft_haut[f_ind])/np.abs(fft_bas[f_ind]))) 
        phase.append(np.angle(fft_haut[f_ind])-np.angle(fft_bas[f_ind]))
        xerr.append(abs((frequence[f_ind+1]-frequence[f_ind])))
        #print(yerr)
        yerr.append(5)
        print(name,xerr)
        #print(name,freq[-1],gain[-1],phase[-1])
    ax = plt.subplot(2,1,1)
    #ax = plt.axes()
    ax.set_xscale("log")
    plt.grid(True,"both")
    plt.errorbar(freq,gain,yerr,xerr,fmt="rx")
    
    #plt.semilogx(freq,gain,"rx")
    
    plt.ylabel("$G_{dB}$ (dB)")
    plt.subplot(2,1,2) 
    plt.semilogx(freq,phase,"x")
    plt.ylabel("φ (rad)")
    plt.xlabel("Fréquence d'excitation (Hz)")
    plt.grid(True,"both")
    plt.suptitle(folder.split("/")[-2])
    plt.savefig("Image/"+folder.replace(" ","_").split("/")[-2]+".pdf")
    #plt.show()
    out = [[freq[i],gain[i],phase[i]] for i in range(len(freq))]
    #print(out)
    np.savetxt(folder.split("/")[-2]+".csv",out,delimiter=";")
    #plt.show()
    return (freq, gain, phase)
def bode_norme()  : 
    gain = []
    phase = []
    freq = []
    xerr = []
    yerr= []
    phierr = []
    plt.figure(figsize=(10,5))
    for i,name in enumerate(liste_fichier) :
        frame = np.genfromtxt("Cleaned/"+folder+name,delimiter=";")
        #print(len(frame))
        bas = np.sqrt(np.square(frame[:,1])+np.square(frame[:,2]))
        haut = np.sqrt(np.square(frame[:,4])+np.square(frame[:,5]))
        bas = bas - np.mean(bas) 
        haut = haut - np.mean(haut) 
        fft_bas = fft(bas)
        fft_haut = fft(haut)
        n = np.arange(len(fft_bas))
        
        frequence = (n/(frame[-1,0]-frame[0,0]))*1e6 #f = n/deltaT
        #print(n)
        #print(frequence)
        f_ind = np.argmax(np.abs(fft_bas)[:end_freq(frequence,10)]) 
        
        #print(f_ind)
        freq.append(frequence[f_ind])
        gain.append(20*np.log(np.abs(fft_haut[f_ind])/np.abs(fft_bas[f_ind]))) 
        phase.append(np.angle(fft_haut[f_ind])-np.angle(fft_bas[f_ind]))
        xerr.append((frequence[f_ind+1]-frequence[f_ind]))
        yerr.append(abs(20*np.log10(np.max(20+np.absolute(fft_haut[f_ind]))/(np.absolute(fft_bas[f_ind])))))
        #print(name,freq[-1],gain[-1],phase[-1])
    plt.subplot(2,1,1)
    ax = plt.axes()
    ax.set_xscale("log")
    plt.errorbar(freq,gain,xerr,yerr,fmt="rx")
    plt.grid(True,"both")
    plt.ylabel("$G_{dB}$ (dB)")
    plt.subplot(2,1,2)
    
    plt.semilogx(freq,phase,"x")
    plt.ylabel("φ (rad)")
    plt.xlabel("Fréquence d'excitation (Hz)")
    plt.grid(True,"both")
    plt.suptitle(folder.split("/")[-2]+"en norme")
    plt.savefig("Image/"+folder.replace(" ","_").split("/")[-2]+"_norme"+".pdf")
    out = np.concatenate((freq,gain,phase)).transpose()
    np.savetxt(folder.split("/")[-2]+"_norme"+".csv",out,delimiter=";")
    #plt.show()
    return (freq, gain, phase)


if __name__ == "__main__" :
    for folder in tqdm(os.listdir("ToClean/")) :
        print(f"\033[92m Treating folder :\033[0m {folder}")
        #folder = "masse en haut faible amplitude/"
        try : 
            folder = folder + "/"
            liste_fichier  = os.listdir("ToClean/"+folder+"/")
            clean()
            print(f"\033[92mfolder Cleaned, creating bode diagramm\033[0m")
        except :
            print("\033[91mERROR\033[0m")
            raise
        bode()
        #bode_norme() #Ne fonctionne pas ==> ce n'est pas linéaire
        print(f"\033[92mfolder completely treated\033[0m")
    print(f"\033[92m\033[4mfolder all done")
    #plt.show()


