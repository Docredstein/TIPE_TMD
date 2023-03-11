#testSerial.py
import serial 
import time
import numpy as np 
import numpy.random as rd 
import matplotlib.pyplot as plt 
"""
Marlin = serial.Serial("COM5",250000) 
Marlin.close()
Marlin.baudrate = 250000
Marlin.open()
time.sleep(1)
print(Marlin.read_all())
print(Marlin.write(b"G0 X10\n"))
print(Marlin.baudrate)

time.sleep(1)
print(Marlin.read_all())
Marlin.close()"""
x = np.linspace(0,10,100) 
y = [rd.random()*x**2 for i in range(10)]
y = np.array(y)
#y.transpose()
plt.plot(x,y.transpose())
plt.show()
