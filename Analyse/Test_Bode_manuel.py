import numpy as np 
from numpy.fft import fft 
import matplotlib.pyplot as plt 
def max_ind(l) -> tuple	:
    (u,i) = (l[0],0)
    for j in range(1,len(l)) :
        if u<l[j] :
            u,i = l[j],j
    return (u,i)

x = np.genfromtxt("./Cleaned/Bode a Vide/0.5Hz_Cleaned.csv",delimiter=";")
print(x)
X = fft(x[:,1]-np.mean(x[:,1])) 
Y = fft(x[:,5]-np.mean(x[:,5]))
N = len(X) 
n = np.arange(N)

freq = (n/(x[-1,0]-x[0,0]))*1e6
plt.subplot(3,1,1)
plt.stem(freq[:200],np.abs(X)[:200],"b")
plt.stem(freq[:200],np.abs(Y)[:200],"r")
plt.subplot(3,1,2)
plt.plot(freq[:200],np.angle(X)[:200])
plt.plot(freq[:200],np.angle(Y)[:200])
plt.subplot(3,1,3)
plt.plot(x[:,0],x[:,1])
plt.plot(x[:,0],x[:,5])

plt.show()