# importation des modules
import serial.tools.list_ports  # pour la communication avec le port série
import serial
import matplotlib.pyplot as plt  # pour le tracé de graphe
import matplotlib.animation
from matplotlib import animation  # pour la figure animée
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk 
# import time # gestion du temps
import numpy as np  # numpy pour l'importation des donnees en format txt
import time
import tkinter
import tkinter.simpledialog
import tkinter.filedialog
import threading
plt.rcParams["figure.autolayout"] = True

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
    #mData = serial.Serial
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

"""
Marlin = recup_port_Printer()
Board = recup_port_Arduino()
"""
freq = 0
filename = "default.csv"
Recording = False
mesure = [[0]*15,[1]*15]
fig = plt.figure()

ax = [fig.add_subplot() for i in range(14)]
def osciller():
    Board.write(f"G0 X15000 F{60*freq}")
def save() :
    filename = tkinter.filedialog.asksaveasfilename(title="enregistrer les mesures",filetypes=[("csv","*.csv")],defaultextension=[("csv","*.csv")])
    if filename is None : 
        return 
    with open(filename,"w+") as file:
        for ligne in mesure :
            for valeur in ligne :
                file.write(f"{valeur};")
            file.write("\n")
#Board = serial.Serial()

def read_Value() :
    global Recording
    while Recording == True : 
        #print("a")
        
        time.sleep(1)
        """if Board.in_waiting()>15 : 
            newmes = Board.readline() 
            newmes = newmes.split(";") 
            newmes[0] = int(newmes)
            for i in range(1,len(newmes)) :
                newmes[i] = float(newmes[i])
            mesure.append(newmes)"""
rec_btn_str = "Appuyez pour commencer l'enregistrement"
Record_thread = None

def record() :
    global Recording,rec_btn_str,Record_thread
    if not Recording :
        #Board.flush()
        Recording = True
        Record_thread = threading.Thread(target=read_Value,daemon=True)
        rec_btn_str = "Appuyez pour arreter l'enregistrement"
        #Record_thread.run()
        Record_thread.start()
        
        
    else :
        Recording = False 
        Record_thread.join()
        Record_thread = None
        rec_btn_str = "Appuyez pour commencer l'enregistrement"
        
    print("Button finished")
def close() :
    global Recording
    Recording = False 
    if Record_thread is not None :
        Record_thread.join()
    base.destroy()
    exit(0)
    
def animate(i,mesure) :
    mes = np.array(mesure)
    x = mes[:,0]
    y = [mes[:,i] for i in range(1,len(mesure[0]))] 
    for i in range(len(mesure[0]-1)) :
        ax[i].clear()
        ax[i].plot(x,y[i])

    
anim = animation.FuncAnimation(fig,animate,fargs=mesure,frames=100)

base = tkinter.Tk()
canvas = FigureCanvasTkAgg(fig, master=base)
canvas.draw()
toolbar = NavigationToolbar2Tk(fig,master=base)
toolbar.update()
base.title("Mesures TIPE 2023")

base.protocol("WM_DELETE_WINDOW",close)
base.geometry("1280x720")
base.configure(bg="#05022E", highlightbackground=accent_bg,
                highlightcolor=accent_fg, bd=bd, relief=relief)

button_freq = tkinter.Button(base, text="Lancer le Mouvement", command=osciller, bg=bg,
                                fg=fg, highlightbackground=accent_bg, highlightcolor=accent_fg, bd=bd, relief=relief)
button_freq.pack()

freq_slider = tkinter.Scale(base, orient="horizontal", variable=freq, tickinterval=0.5, width=15, resolution=0.1, length=500,
                            from_=0, to=10, label="Fréquence", bg=bg, fg=fg, highlightbackground=accent_bg, highlightcolor=accent_fg, bd=bd, relief=relief)
freq_slider.pack()

button_file = tkinter.Button(base,text="Enregistrer",command=save,bg=bg, fg=fg, highlightbackground=accent_bg, highlightcolor=accent_fg, bd=bd, relief=relief)
button_file.pack()

button_rec = tkinter.Button(base,text=rec_btn_str,command=record,bg=bg, fg=fg, highlightbackground=accent_bg, highlightcolor=accent_fg, bd=bd, relief=relief)
button_rec.pack()

base.state("zoomed")
tkinter.mainloop()
#record()
#plt.show()
# print(filename)
"""Marlin
Board.close()
Marlin.close()"""



