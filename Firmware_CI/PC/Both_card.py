# importation des modules
import serial.tools.list_ports  # pour la communication avec le port série
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation  # pour la figure animée
# import time # gestion du temps
import numpy as np  # numpy pour l'importation des donnees en format txt
import time
import tkinter


bg = "#230A63"
active_bg = "#448747"
bd = 1
fg = "#BAB038"
accent_fg = "#A44ABA"
accent_bg = "#BA024E"
relief = "raised"


def recup_port_Arduino():
    ports = list(serial.tools.list_ports.comports())
    mData = serial.Serial
    for p in ports:
        # print(p.pid)
        if "CH340" in p.description:
            mData = serial.Serial(p.device, 115200)
    # return None
    print(mData.is_open)  # Affiche et vérifie que le port est ouvert
    print(mData.name)  # Affiche le nom du port
    return mData


def recup_port_Printer():
    ports = list(serial.tools.list_ports.comports())
    mData = serial.Serial
    for p in ports:
        if p.pid == 0x6001:
            mData = serial.Serial(p.device, 250000)
    # return None
    # print(mData.is_open)
    # print(mData.name)
    time.sleep(0.5)
    print(mData.read_all().decode())
    mData.write(b"G91\n")
    #mData.write(b"G0 X10000 F5000")
    mData.write(b"M121\n")
    mData.write(b"M502 X32000\n")
    #mData.write(b"G0 X1000 F2000")
    # time.sleep(1)
    # print(mData.read_all().decode())

    return mData


Marlin = recup_port_Printer()
Board = recup_port_Arduino()
freq = 0
filename = "default.csv"


def osciller():
    Board.write(f"G0 X15000 F{60*freq}")


def main():

    base = tkinter.Tk()
    base.geometry("1280x720")
    base.configure(bg="#05022E", highlightbackground=accent_bg,
                   highlightcolor=accent_fg, bd=bd, relief=relief)
    button_freq = tkinter.Button(base, text="Lancer le Mouvement", command=osciller, bg=bg,
                                 fg=fg, highlightbackground=accent_bg, highlightcolor=accent_fg, bd=bd, relief=relief)
    button_freq.pack()

    freq_slider = tkinter.Scale(base, orient="horizontal", variable=freq, tickinterval=0.5, width=15, resolution=0.1, length=500,
                                from_=0, to=10, label="Fréquence", bg=bg, fg=fg, highlightbackground=accent_bg, highlightcolor=accent_fg, bd=bd, relief=relief)
    freq_slider.pack()

    entry_filename = tkinter.Entry(base, textvariable=filename, bg=bg, fg=fg,
                                   highlightbackground=accent_bg, highlightcolor=accent_fg, bd=bd, relief=relief)

    entry_filename.pack()

    # tkinter.mainloop()
    # print(filename)
    Marlin
    Board.close()
    Marlin.close()


main()
