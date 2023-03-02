import matplotlib.pyplot as plt
import numpy as np
from math import pi
import numpy.random as rd

def degtorad(t):
    return (t*pi/180)

l_baguette = 0.28
u_l_baguette = 0.01

# Bouchon n°1
 
angledeg=np.array([5,10,15,20,25,30,35,40])
anglerad=degtorad(angledeg)
force1=np.array([0.1,0.4,0.45,0.625,0.8,1,1.25,1.5])
u_F = 0.05
u_theta = 3
coef = []
for i in range(1000) :
    F_MC = force1 + u_F*rd.uniform(-1,1,len(force1)) 
    theta_MC = angledeg + u_theta*rd.uniform(-1,1,len(force1))
    theta_MC = degtorad(theta_MC)
    poly = np.polyfit(theta_MC,F_MC,1)
    coef.append(poly)
coef = np.array(coef)
print("Bouchon n°1 : %f"%np.mean(coef[:,1]),np.mean(coef[:,0]))
a_1 = np.mean(coef[:,0])
b_1 = np.mean(coef[:,1])
plt.errorbar(anglerad,force1,u_F,degtorad(u_theta))
x1 = np.linspace(min(anglerad),max(anglerad),1000)
y1 = np.polyval([a_1,b_1],x1)
plt.plot(x1,y1)
plt.xlabel("angle en rad")
plt.ylabel("force en N")
plt.title('Bouchon 1')
#plt.scatter(anglerad,force)
#plt.show()


#Bouchon n°2

angledeg=np.array([5,10,15,20,25,30,35,40])
anglerad=degtorad(angledeg)
force2=np.array([0.08,0.2,0.3,0.5,0.67,0.8,0.82,0.85])
u_F = 0.05
u_theta = 3
coef = []
for i in range(1000) :
    F_MC = force2 + u_F*rd.uniform(-1,1,len(force2)) 
    theta_MC = angledeg + u_theta*rd.uniform(-1,1,len(force2))
    theta_MC = degtorad(theta_MC)
    poly = np.polyfit(theta_MC,F_MC,1)
    coef.append(poly)
coef = np.array(coef)
print("Bouchon n°2 : %f"%np.mean(coef[:,1]),np.mean(coef[:,0]))
a_2 = np.mean(coef[:,0])
b_2 = np.mean(coef[:,1])
plt.errorbar(anglerad,force2,u_F,degtorad(u_theta))
x2 = np.linspace(min(anglerad),max(anglerad),1000)
y2 = np.polyval([a_2,b_2],x2)
plt.plot(x2,y2)
plt.xlabel("angle en rad")
plt.ylabel("force en N")
plt.title('Bouchon 2')
#plt.scatter(anglerad,force)
#plt.show()



#Bouchon n°3


angledeg=np.array([5,10,15,20,25,30,35,40])
anglerad=degtorad(angledeg)
force3=np.array([0.08,0.2,0.3,0.45,0.65,0.75,0.85,0.95])
u_F = 0.05
u_theta = 3
coef = []
for i in range(1000) :
    F_MC = force3 + u_F*rd.uniform(-1,1,len(force3)) 
    theta_MC = angledeg + u_theta*rd.uniform(-1,1,len(force3))
    theta_MC = degtorad(theta_MC)
    poly = np.polyfit(theta_MC,F_MC,1)
    coef.append(poly)
coef = np.array(coef)
print("Bouchon n°3 : %f"%np.mean(coef[:,1]),np.mean(coef[:,0]))
a_3 = np.mean(coef[:,0])
b_3 = np.mean(coef[:,1])
plt.errorbar(anglerad,force3,u_F,degtorad(u_theta))
x3 = np.linspace(min(anglerad),max(anglerad),1000)
y3 = np.polyval([a_3,b_3],x3)
plt.plot(x3,y3)
plt.xlabel("angle en rad")
plt.ylabel("force en N")
plt.title('Bouchon 3')
#plt.scatter(anglerad,force)
#plt.show()


#Bouchon n°4

angledeg=np.array([5,10,15,20,25,30,35,40])
anglerad=degtorad(angledeg)
force4=np.array([0.12,0.22,0.3,0.55,0.6,0.8,0.9,1.2])
u_F = 0.05
u_theta = 3
coef = []
for i in range(1000) :
    F_MC = force4 + u_F*rd.uniform(-1,1,len(force4)) 
    theta_MC = angledeg + u_theta*rd.uniform(-1,1,len(force4))
    theta_MC = degtorad(theta_MC)
    poly = np.polyfit(theta_MC,F_MC,1)
    coef.append(poly)
coef = np.array(coef)
print("Bouchon n°4 : %f"%np.mean(coef[:,1]),np.mean(coef[:,0]))
a_4 = np.mean(coef[:,0])
b_4 = np.mean(coef[:,1])
plt.errorbar(anglerad,force4,u_F,degtorad(u_theta))
x4 = np.linspace(min(anglerad),max(anglerad),1000)
y4= np.polyval([a_4,b_4],x4)
plt.plot(x4,y4)
plt.xlabel("angle en rad")
plt.ylabel("force en N")
plt.title('Bouchon 4')
#plt.scatter(anglerad,force)
plt.savefig("force de rappel.png")
a_mean = np.mean([a_1,a_2,a_3,a_4])
print(f"a_mean = {a_mean} N/rad")
k_mean = a_mean*l_baguette
print(f"k_mean = {k_mean:.3f} N.m.rad^-1")

