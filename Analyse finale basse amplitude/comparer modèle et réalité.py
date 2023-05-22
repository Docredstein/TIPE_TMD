import matplotlib.pyplot as plt 
import numpy as np 
k = 2.7
c = 0.002
Hzero=1
M = 0.2
j=1j
frame = np.genfromtxt("sans pendule.csv",delimiter=";")


def fonction_de_transfert(w:float) : 
    return Hzero/(1+(c/k)*j*w - (M/k)*w**2)
plt.figure() 
ax =plt.subplot(2,1,1)
ax.set_xscale("log")
xerr =[0.03370238569077588, 0.036533944327018286, 0.027708461213654334, 0.07013105671091813, 0.06375349329297286, 0.0949018084203912, 0.08806333233058528, 0.06804986639769695, 0.112866511422542]
plt.errorbar(frame[:,0],frame[:,1],5,xerr,fmt="rx",label="mesure")
plt.ylabel("$G_{dB}$")
w = np.linspace(min(frame[:,0]),max(frame[:,0]+1),1000)
g = [20*np.log10(np.absolute(fonction_de_transfert(w[i]))) for i in range(len(w))] 
phi = [np.angle(fonction_de_transfert(i)) for i in w]
#print(g)
plt.semilogx(w,g,label="modèle") 
plt.legend()
ax = plt.subplot(2,1,2)
ax.set_xscale("log")
plt.semilogx(frame[:,0],frame[:,2],"rx")
plt.xlabel("$\omega$")
plt.ylabel("$\phi$")
plt.semilogx(w,phi)
plt.show()