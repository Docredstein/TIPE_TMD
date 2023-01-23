import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import numpy as np
import lib

sim = lib.simulation()
ref = np.array([[-5,0],[5,0]] )
L = 10
g=9.81
bat = [[0,0],L,[0,1],np.pi/4] #origin, length, normal,theta

dt = 1e-3
J=0.15
m=1e-1
k=0.1
fig = plt.figure() # initialise la figure
plt.xlim((-7,7))
plt.ylim(-1,15)
base = lib.barre((-5,0),0,10,0,0,0,True)
bare = lib.barre((0,0),np.pi/4,5,0.15,np.pi/2,0,parent = base)

"""
def animate(i): 
    t = i * dt
    theta_p = (-k*(bat[3])+m*g*bat[1]*np.cos(bat[3])/2)/J
    bat[3] = bat[3] + theta_p
    print(bat[3])
    barre.set_data(bat[0], (bat[0][0]+np.cos(bat[3])*bat[1],bat[0][1]+np.sin(bat[3])*bat[1]))
    return barre,
 
ani = animation.FuncAnimation(fig, animate, frames=250,
                              interval=1000, blit=True, repeat=False)
plt.show()"""