import socket
import network
import machine
import utime

ssid = "PicoW"
password = "123456789"

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password) 
ap.active(True)

while ap.active == False:
    pass

print("Access point active")
print(ap.ifconfig())
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return(connection)
def webpage(value):
    html = f"""
            <!DOCTYPE html>
            <html>
            <body>
            ${value}?
            </body>
            </html>
            """
    return html
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
def temperature():
    temperature_value = sensor_temp.read_u16() * conversion_factor 
    temperature_Celcius = 27 - (temperature_value - 0.706)/0.00172169/ 8 
    #print(temperature_Celcius)
    #utime.sleep(2)
    return temperature_Celcius
def serve(connection):
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        
        print(request)
 
        value='%.2f'%temperature()    
        html=webpage(value)
        client.send(html)
        client.close()

try:
    
    connection=open_socket("192.168.4.1")
    serve(connection)
except KeyboardInterrupt:
    machine.reset()