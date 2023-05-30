import matplotlib.pyplot as plt 
import numpy as np
from pylab import *
from scipy.optimize import curve_fit

###Invariants###
k=2
k1=0.5

h1=0.001
h=0.05

M=0.2
m=0.073

j=complex(0,1)


def H1(w):
    return (k1+j*h1*w-m*w**2)
def H2(w):
    return ((H1(w))*k)/(H1(w)*(k+j*h*w-(m+M)*w**2) - (w**(2)*m)**2)

puissance_w=np.arange(-2,3,0.01)
W=10**puissance_w
w=np.arange(0.1,20,0.001)
module=20*np.log10(np.absolute(H2(w)))




# ###Sans pendule###
# 
# ks=2.5
# 
# 
# c=0.005
# 
# 
# Ms=0.19
# 
# 
# def H(w):
#     return 1/(1+j*c/ks*w-Ms/ks*w**2)
# 
# frame = np.genfromtxt("sans pendule.csv",delimiter=";",invalid_raise=False)
# print(frame)
# frame[7][1]=10
# 
# sansp=20*np.log10(np.absolute(H(w)))
# 
# plt.figure(figsize=(13,4))
# plt.semilogx(w,sansp)
# plt.semilogx(frame[:,0],frame[:,1],"b.", linestyle='None')
# #xerr =[0.03370238569077588, 0.036533944327018286, 0.027708461213654334, 0.07013105671091813, 0.06375349329297286, 0.0949018084203912, 0.08806333233058528, 0.06804986639769695, 0.112866511422542]
# plt.errorbar(frame[:,0],frame[:,1],2,0.1,'r', linestyle='None')
# plt.xlabel("Fréquence d'excitation en Hz")
# plt.ylabel("Gain en dB")
# plt.title("Sans pendule",fontsize=20)
# plt.xlim((0.4,8))
# plt.grid(True,'both')
# plt.show()



###################################################################################################
# 
# 
# frame = np.genfromtxt("masse en bas (9.4gcm) de  100g.csv",delimiter=";",invalid_raise=False)
# print(frame)
# frame[7][1]=6
# frameb=np.concatenate((frame,np.array([[0.5,1.344,0.7]])))
# print(frameb)
# 
# # k=1.5
# # k1=0.2
# # 
# # h1=0.005
# # h=0.005
# # 
# # M=0.19
# # m=0.1
# 
# plt.figure(figsize=(13,4))
# plt.semilogx(w,module)
# plt.semilogx(frameb[:,0],frameb[:,1],"b.", linestyle='None')
# xerr =[0.03370238569077588, 0.036533944327018286, 0.027708461213654334, 0.07013105671091813, 0.06375349329297286, 0.0949018084203912, 0.08806333233058528, 0.06804986639769695, 0.112866511422542]
# plt.errorbar(frameb[:,0],frameb[:,1],2,0.1,'r', linestyle='None')
# plt.xlabel("Fréquence d'excitation en Hz")
# plt.ylabel("Gain en dB")
# plt.title("Pendule de 100g à 9.4 cm",fontsize=20)
# plt.xlim((0.4,8))
# plt.grid(True,'both')
# plt.show()


#######################################################################333
# frame = np.genfromtxt("pendule à 5 cm de l'axe , 100g.csv",delimiter=";",invalid_raise=False)
# print(frame)
# frame[3][1]=7.745657
# frame[4][1]=-26.032079
# #frameb=np.concatenate((frame,np.array([[0.5,1.344,0.7]])))
# print(frame)
# 
# # k=1.5
# # k1=0.7
# # 
# # h1=0.02
# # h=0.008
# # 
# # M=0.2
# # m=0.1
# 
# plt.figure(figsize=(13,4))
# plt.semilogx(w,module)
# plt.semilogx(frame[:,0],frame[:,1],"b.", linestyle='None')
# xerr =[0.03370238569077588, 0.036533944327018286, 0.027708461213654334, 0.07013105671091813, 0.06375349329297286, 0.0949018084203912, 0.08806333233058528, 0.06804986639769695, 0.112866511422542]
# plt.errorbar(frame[:,0],frame[:,1],2,0.1,'r', linestyle='None')
# plt.xlabel("Fréquence d'excitation en Hz")
# plt.ylabel("Gain en dB")
# plt.title("Pendule de 100g à 5 cm",fontsize=20)
# plt.xlim((0.4,8))
# plt.grid(True,'both')
# plt.show()

#########################################
# frame = np.genfromtxt("masse à 3 cm de l'axe de 100g.csv",delimiter=";",invalid_raise=False)
# print(frame)
# frame[0][1]=1.745657
# frame[4][1]=-19.589898
# frame[5][1]=-14.7853437
# # frame[4][1]=-26.032079
# #frameb=np.concatenate((frame,np.array([[0.5,1.344,0.7]]))) print(frame)
# 
# k=2.5
# k1=1
# 
# h1=0.04
# h=0.005
# 
# M=0.3
# m=0.1

# plt.figure(figsize=(13,4))
# plt.semilogx(w,module)
# plt.semilogx(frame[:,0],frame[:,1],"b.", linestyle='None')
# xerr =[0.03370238569077588, 0.036533944327018286, 0.027708461213654334, 0.07013105671091813, 0.06375349329297286, 0.0949018084203912, 0.08806333233058528, 0.06804986639769695, 0.112866511422542]
# plt.errorbar(frame[:,0],frame[:,1],2,0.1,'r', linestyle='None')
# plt.xlabel("Fréquence d'excitation en Hz")
# plt.ylabel("Gain en dB")
# plt.title("Pendule de 100g à 3 cm",fontsize=20)
# plt.xlim((0.4,8))
# plt.grid(True,'both')
# plt.show()

############################################

frame = np.genfromtxt("masse à 9.4 cm de 73,3g de l'axe.csv",delimiter=";",invalid_raise=False)
print(frame)
frame[0][1]=0.765268
frame[3][0]=1.367889
frame[4][1]=3.567689
frame[2][1]=-34.65471

#frameb=np.concatenate((frame,np.array([[0.5,1.344,0.7]]))) print(frame)

# k=2
# k1=0.5
# 
# h1=0.001
# h=0.05
# 
# M=0.2
# m=0.073

plt.figure(figsize=(13,4))
plt.semilogx(w,module)
plt.semilogx(frame[:,0],frame[:,1],"b.", linestyle='None')
xerr =[0.03370238569077588, 0.036533944327018286, 0.027708461213654334, 0.07013105671091813, 0.06375349329297286, 0.0949018084203912, 0.08806333233058528, 0.06804986639769695, 0.112866511422542]
plt.errorbar(frame[:,0],frame[:,1],2,0.1,'r', linestyle='None')
plt.xlabel("Fréquence d'excitation en Hz")
plt.ylabel("Gain en dB")
plt.title("Pendule de 73.3g à 9.4 cm",fontsize=20)
plt.xlim((0.4,8))
plt.grid(True,'both')
plt.show()
