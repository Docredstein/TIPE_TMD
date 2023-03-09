#testSerial.py
import serial 
import time

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
Marlin.close()