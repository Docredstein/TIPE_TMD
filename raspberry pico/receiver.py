import requests
import time
h = {"Host":"192.168.4.1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","Upgrade-Insecure-Requests":"1"}
r = requests.get("http://youtube.com")

r = requests.get("http://192.168.4.1",headers=h,verify=False)

print(r)
time.sleep(0.1)