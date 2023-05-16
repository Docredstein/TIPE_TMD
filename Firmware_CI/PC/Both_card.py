# importation des modules

#22 mm de large pendule et 55mm barre 7.5mm de dia 15 ext
import serial.tools.list_ports  # pour la communication avec le port série
import serial
import matplotlib.pyplot as plt  # pour le tracé de graphe
import matplotlib.animation
from matplotlib import animation  # pour la figure animée
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# import time # gestion du temps
import numpy as np  # numpy pour l'importation des donnees en format txt
import time
import tkinter
import tkinter.simpledialog
import tkinter.filedialog
import threading
plt.rcParams["figure.autolayout"] = True
"""
bg = "#230A63"
active_bg = "#448747"
bd = 1
fg = "#BAB038"
accent_fg = "#A44ABA"
accent_bg = "#BA024E" """

COLORS = {
    "bg": "#1B1B1B",   # background color
    "fg": "#F2F2F2",   # foreground color
    "accent": "#5DA5DA",  # accent color
    "highlight": "#2A2A2A",  # highlight color
    "text": "#CCCCCC",  # text color
}
X = 0


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
    time.sleep(1)
    print(mData.read_all().decode())
    mData.write(b"G91\n")
    #mData.write(b"G0 X10000 F5000")
    mData.write(b"M121\n")
    mData.write(b"M92 X640\n") #640
    #mData.write(b"G0 X1000 F2000")
    # time.sleep(1)
    # print(mData.read_all().decode())
    time.sleep(1)
    print(mData.read_all().decode())
    return mData


Marlin = recup_port_Printer()
Board = recup_port_Arduino()

freq = 0
filename = "default.csv"
Recording = False
mesure = []
fig = plt.figure()

ax = [fig.add_subplot() for i in range(14)]


def osciller():
    global X, freq
    freq = freq_slider.get()
    print(f'moving at {freq} Hz')
    Marlin.write(b"G91\n")
    #time.sleep(1)
    Marlin.write((f"G0 X{10*freq*30} F{int(600*freq)}\n").encode())
    X += 1000
    print(f"X={X}")
    print("ok")
    time.sleep(0.5)
    print(Marlin.read_all())


def save():
    filename = tkinter.filedialog.asksaveasfilename(title="enregistrer les mesures", filetypes=[
                                                    ("csv", "*.csv")], defaultextension=[("csv", "*.csv")])
    global mesure
    if filename is None:
        return
    #print(mesure)
    with open(filename, "w+") as file:
        for ligne in mesure:
            for valeur in ligne:
                file.write(f"{valeur};")
            file.write("\n")
#Board = serial.Serial()


def read_Value():
    global Recording
    while Recording == True:
        # print("a")

        # time.sleep(0.1)
        if Board.in_waiting > 80:
            raw = Board.readline()
            raw = raw.decode()
            if raw[0] == "?":
                raw = raw.rstrip().replace("\n", "").split(";")
                # print(raw)
                newmes = [0]*len(raw)
                newmes[0] = int(raw[0][1:])
                for i in range(1, len(raw)-1):
                    try :   
                        newmes[i] = float(raw[i])
                    except : 
                        print(raw[i],i)
                mesure.append(newmes)


#rec_btn_str = "Appuyez pour commencer l'enregistrement"
rec_btn_str=tkinter.StringVar()
Record_thread = None


def record():
    global Recording, rec_btn_str, Record_thread
    if not Recording:
        # Board.flush()
        Recording = True
        #Board.write(b"S")
        Record_thread = threading.Thread(target=read_Value, daemon=True)
        rec_btn_str.set("Appuyez pour arreter l'enregistrement")
        # Record_thread.run()
        Record_thread.start()

    else:
        # print(mesure)
        Recording = False
        #Board.write(b"T")
        Record_thread.join()
        Record_thread = None
        Marlin.write(b"M18\n")
        
        rec_btn_str.set("Appuyez pour commencer l'enregistrement")

    print("Button finished")


def close():
    global Recording
    Recording = False
    if Record_thread is not None:
        Record_thread.join()
    base.destroy()
    exit(0)


def animate(i, mesure):
    mes = np.array(mesure)
    x = mes[:, 0]
    y = [mes[:, i] for i in range(1, len(mesure[0]))]
    for i in range(len(mesure[0]-1)):
        ax[i].clear()
        ax[i].plot(x, y[i])


def set_freq(val):
    freq = val

def reset_cap() :
    Board.write(b"R") 
    Board.close()
    time.sleep(1) 
    Board.open()
def reset_mar():
    Marlin.write("M502")
    Marlin.close()
    time.sleep(0.5)
    Marlin = recup_port_Printer()

#anim = animation.FuncAnimation(fig,animate,fargs=mesure,frames=100)

while True :
    base = tkinter.Tk()
    """
    canvas = FigureCanvasTkAgg(fig, master=base)
    canvas.draw()
    toolbar = NavigationToolbar2Tk(fig,master=base)
    toolbar.update()"""
    base.title("Mesures TIPE 2023")

    base.protocol("WM_DELETE_WINDOW", close)
    base.geometry("1280x720")
    base.configure(bg=COLORS["bg"])

    top_frame = tkinter.Frame(base, bg=COLORS["bg"])
    top_frame.pack(side="top", fill="x")

    label = tkinter.Label(top_frame, text="Fréquence (Hz)",
                        fg=COLORS["fg"], bg=COLORS["bg"], font=("Helvetica", 18))
    label.pack(side="top")


    freq_slider = tkinter.Scale(top_frame, orient="horizontal", command=set_freq, tickinterval=0.5, width=15, resolution=0.1, length=4000,
                                from_=0, to=10, fg=COLORS["fg"], bg=COLORS["accent"], font=("Helvetica", 18))
    freq_slider.pack()
    freq_slider.pack(side="left", padx=20, pady=10)
    status_label = tkinter.Label(top_frame, text="Status :",
                                fg=COLORS["fg"], bg=COLORS["bg"], font=("Helvetica", 18))
    status_label.pack()


    bottom_frame = tkinter.Frame(base, bg=COLORS["bg"])
    bottom_frame.pack(side="bottom", fill="x")

    button_freq = tkinter.Button(bottom_frame, text="Lancer le Mouvement",
                                command=osciller, fg=COLORS["fg"], bg=COLORS["accent"], font=("Helvetica", 18))
    button_freq.pack(side="left", padx=20, pady=20)


    button_rec = tkinter.Button(bottom_frame, text=rec_btn_str, command=record,
                                fg=COLORS["fg"], bg=COLORS["accent"], font=("Helvetica", 18))
    button_rec.pack(side="left", padx=20, pady=20)

    button_file = tkinter.Button(bottom_frame, text="Enregistrer le fichier",
                                command=save, fg=COLORS["fg"], bg=COLORS["accent"], font=("Helvetica", 18))
    button_file.pack(side="left", padx=20, pady=20)
    button_reset = tkinter.Button(bottom_frame, text="Reset Capteur", command=reset_cap,
                                fg=COLORS["fg"], bg=COLORS["accent"], font=("Helvetica", 18))
    button_reset.pack(side="left", padx=20, pady=20)
    button_reset_marlin = tkinter.Button(bottom_frame, text="Reset Printer",
                                        command=reset_mar, fg=COLORS["fg"], bg=COLORS["accent"], font=("Helvetica", 18))
    button_reset_marlin.pack(side="left", padx=20, pady=20)
    base.state("zoomed")
    tkinter.mainloop()
# record()
# plt.show()
# print(filename)
"""Marlin
Board.close()
Marlin.close()"""
