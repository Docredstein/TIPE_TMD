import matplotlib.pyplot as plt 
import math as m 
import numpy as np
Arraylen = 50


l = [m.floor(255*m.sin(i*m.pi/Arraylen)) for i in range(Arraylen+1)]
x = np.linspace(0,Arraylen,Arraylen+1)
print(list(l))
plt.plot(x,l)
plt.show()