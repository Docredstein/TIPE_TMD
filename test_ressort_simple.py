from tkinter import ttk 
import tkinter as tk 
fenetre = tk.Tk("Simulation")
dessin = tk.Canvas(fenetre,width=500,height=500)
dessin.create_line(50,50,200,200)
dessin.create_rectangle(100,100,400,300)
dessin.pack()
fenetre.mainloop()