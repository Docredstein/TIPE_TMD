import matplotlib.pyplot as plt 
import numpy as np 
k = 3
c = 0.01
M = 0.15
j=1j
frame = np.genfromtxt("sans pendule.csv",delimiter=";")


def fonction_de_transfert(w:float) : 
    return 1/(1+(c/k)*j*w - (M/k)*w**2)
plt.figure() 
plt.subplot(2,1,1)

plt.semilogx(frame[:,0],frame[:,1],"rx",label="mesure")
plt.ylabel("$G_{dB}$")
w = np.linspace(min(frame[:,0]),max(frame[:,0]+1),1000)
g = [20*np.log10(np.absolute(fonction_de_transfert(w[i]))) for i in range(len(w))] 
phi = [fonction_de_transfert(i) for i in w]
print(g)
plt.semilogx(w,g,label="modèle") 
plt.legend()
plt.subplot(2,1,2)
plt.semilogx(frame[:,0],frame[:,2],"rx")
plt.xlabel("$\omega$")
plt.ylabel("$\phi$")
plt.semilogx(w,phi)
plt.show()