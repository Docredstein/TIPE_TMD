import qrcode 
img = qrcode.make("url:https://github.com/Docredstein/TIPE_TMD")
img.save("github.svg")
