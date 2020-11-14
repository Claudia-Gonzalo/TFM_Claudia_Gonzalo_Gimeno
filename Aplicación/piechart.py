
# Script que ejecuta el diagrama de sectores en el modo archivo

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import sys

lista_str=[]
lista_i=[]

#Lectura de los parámetros
for arg in range(1,len(sys.argv)):
    lista_str.append(sys.argv[arg])


#Lectura de los datos
aux = ""
canales_leidos=[]
for fich in range(len(lista_str)):
    fichero = open(str(lista_str[fich]),'r')
    a_aux = str(lista_str[fich]).split("/")[1]
    canales_leidos.append(str(a_aux).split("_")[0])
    all_str = fichero.read()
    lista_i.append(all_str.split(","))


etiquetas = ["Delta","Theta", "Alpha", "Beta", "Gamma"]
colores = ['#EC937B', '#C4F880', '#B6F3EC', '#CAB6F3', '#F6C0DF']

lista=[]

#Preparación de los datos
if len(lista_i)>1:
    for elem in lista_i:
        lista_aux2=[]
        lista_aux=[]
        cont=0
        for i in range(len(elem)-1):
            if cont==5:
                cont=0
                lista_aux2.append(lista_aux)
                lista_aux = []
            else:
                lista_aux.append(round(float(elem[i]),2))
                cont= cont + 1
        lista.append(lista_aux2)
else:
    lista_aux=[]
    cont=0
    for i in range(len(lista_i[0])-1):
        if cont==5:
            cont=0
            lista.append(lista_aux)
            lista_aux = []
        else:
            lista_aux.append(round(float(lista_i[0][i]),2))
            cont= cont + 1


#Representar el gráfico con uno o dos canales
if len(lista)==2:
    fig, axarr = plt.subplots(3,figsize=(7,7))

    # Dibujo del primer gráfico
    print(canales_leidos)
    axarr[0].pie(lista[0][0],labels = etiquetas,autopct='%1.1f%%',colors= colores)
    axarr[0].set_position([0.065,0.3,.42,.5])
    axarr[0].set_title("Canal " + str(canales_leidos[0]),fontsize=16)

    #Slider
    axarr[1].set_position([0.1, 0.25, 0.8, 0.03])
    if len(lista[0])>len(lista[1]):
        lon = len(lista[0])
    else:
        lon = len(lista[1])
    risk = Slider(axarr[1], 'Tiempo', 0, lon-1, valinit=0, valstep=1)

    # Dibujo del segundo gráfico
    axarr[2].pie(lista[1][0],labels = etiquetas,autopct='%1.1f%%',colors= colores)
    axarr[2].set_position([0.53,0.3,0.42,0.5])
    axarr[2].set_title("Canal " + str(canales_leidos[1]),fontsize=16)

    #Actualización del gráfico acorde al slider
    def update(val):
        global lista, etiquetas
        axarr[0].clear()
        axarr[2].clear()
        if val < len(lista[0]):
            axarr[0].pie(lista[0][int(val)], labels = etiquetas,autopct='%1.1f%%',colors= colores)
            axarr[0].set_title( "Canal " + str(canales_leidos[0]),fontsize=16)
        else:
            axarr[0].pie(lista[0][len(lista[0])-1], labels = etiquetas,autopct='%1.1f%%',colors= colores)
            axarr[0].set_title("Canal " + str(canales_leidos[0]),fontsize=16)

        if val < len(lista[1]):
            axarr[2].pie(lista[1][int(val)], labels = etiquetas,autopct='%1.1f%%',colors= colores)
            axarr[2].set_title("Canal " + str(canales_leidos[1]),fontsize=16)
        else:
            axarr[2].pie(lista[1][len(lista[1])-1], labels = etiquetas,autopct='%1.1f%%',colors= colores)
            axarr[2].set_title("Canal " + str(canales_leidos[1]),fontsize=16)

        fig.canvas.draw_idle()


    risk.on_changed(update)
    plt.show()

# Análogo pero para un canal
else:

    fig, axarr = plt.subplots(2,figsize=(7,7))

    axarr[0].pie(lista[0],labels = etiquetas,autopct='%1.1f%%',colors= colores)
    axarr[0].set_position([0.25,0.4,.5,.5])
    axarr[0].set_title( "Canal " + str(canales_leidos[0]),fontsize=16)

    # Slider
    axarr[1].set_position([0.1, 0.35, 0.8, 0.03])
    risk = Slider(axarr[1], 'Tiempo', 0, len(lista)-1, valinit=0, valstep=1)

    def update(val):
        global lista, etiquetas
        axarr[0].clear()
        axarr[0].pie(lista[int(val)], labels = etiquetas,autopct='%1.1f%%',colors= colores)
        axarr[0].set_title("Canal " + str(canales_leidos[0]),fontsize=16)
        fig.canvas.draw_idle()


    risk.on_changed(update)
    plt.show()