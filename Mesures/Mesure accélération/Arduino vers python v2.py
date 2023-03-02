#importation des modules
import serial.tools.list_ports # pour la communication avec le port série
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation # pour la figure animée
# import time # gestion du temps
import numpy as np # numpy pour l'importation des donnees en format txt
from scipy.optimize import curve_fit



# Fonction pour la récupération des données série venant de la carte Arduino
def recup_port_Arduino() :
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'Arduino' in p.description :
            mData = serial.Serial(p.device,115200)
    print(mData.is_open) # Affiche et vérifie que le port est ouvert
    print(mData.name) # Affiche le nom du port
    return mData

Data =recup_port_Arduino()

liste_distance=[]

##test pour 20 lignes

# for i in range(20):
#     line1=Data.readline()
#     ldonnées=line1.strip()
#     #ldonnées=line1.split()
#     L=str(ldonnées.decode())
#     L=L.split(",")
#     if len(L)==6:
#         print(L[1],len(L))
#    # print(ldonnées,len(ldonnées))
#     
#     
#     if len(ldonnées) !=0 : # parfois des lignes de données vides peuvent être envoyées, il faut les "écarter"
#         distance = (L[1])  # après consultation des données, nous choisissons le 5ème élément de listeDonnees
#         liste_distance.append(distance)
#         print ("distance : ", distance, " mm")
# print(liste_distance)
# Data.close()   # pour arrêter la lecture des données série



#acquision temps
import time # gestion du temps


#initialisation des listes
liste_temps_mesure =[] # liste pour stocker le temps"brut"
liste_temps=[] # liste pour stocker les valeurs de temps en partant de t=0
laccéx=[]  #liste pour stocker les accélérations selon x



##### Acquition temporelle ######


t_acquisition= 2 #en secondes
tempsreel=0
while tempsreel <= t_acquisition:
    line1=Data.readline()
    L=line1.strip()  #on enlève les caractères en début et fin
    ldonnées=str(L.decode())   #conversion en chaine de caractères pour pouvoir utiliser split + decodage des bits
    ldonnées=ldonnées.split(",")         #on sépare les éléments pour en faire une liste
    #print(ldonnées,len(ldonnées))
    
    if len(ldonnées)== 6:    #pour éviter les beugs , 6 éléments (3 accé et 3 rotations)
        accé_x = float(ldonnées[0])  #  On veut l'accélération selon x donc la prmière valeur de la liste
        tempsmes = time.time()
        liste_temps_mesure.append(tempsmes) # temps mesuré "brut" stocké dans une liste
        tempsreel = tempsmes - liste_temps_mesure[0] # pour faire partir le temps de 0 (cette valeur de temps sera stockée dans une autre liste : liste_temps)

        laccéx.append(accé_x)
        #print("a = %f"%(accé_x), " m/s²") # affichage de la valeur de l'accélération selon x en m/s²
        liste_temps.append(tempsreel)
        #print("temps réel= %f"%(tempsreel), " s") # affichage de la valeur du temps en partant de 0

Data.close() # pour arrêter la lecture des données série





#####Tracé du graphique#####

plt.title('a=f(t)') # titre du graphique
plt.plot(liste_temps,laccéx, color ='m', marker = '.',lw=0.8) 
plt.xlim (min(liste_temps),max(liste_temps))  #limtes pour les axes avec les valeurs extrêmes de I et de U
plt.ylim(min(laccéx)-0.5,max(laccéx)+0.5)
plt.xlabel('temps en s')
plt.ylabel('accélération en m/s²')
plt.show()




#### Création d'un csv####



#Ecriture dans un fichier txt
lines=['t\td\n'] #première ligne du fichier txt
for i in range (len (laccéx)):
    line = str(liste_temps[i]) +'\t'+ str(laccéx[i])+'\n'
    lines.append(line)

fichier = open('mesureX.txt', 'w')
fichier.writelines(lines) #création d'un nouveau fichier texte
