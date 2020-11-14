
#Script que ejecuta el gráfico de barras en el modo serie

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import sys
import random, threading
import math
import pandas as pd

lista_str=[]
lista_i=[]

#Lectura de los argumentos
canales_lectura=[]
freq=sys.argv[1]
guardado=sys.argv[2]
for c in range(3,len(sys.argv)):
    canales_lectura.append(int(sys.argv[c]))
canales_lectura.sort()


list_ac = [[] for i in range(32)]
list_canal_ac= list()

### Lista de pueros disponibles:
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
aux_port = ""
for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
        aux_port=str(port)
   
#Configura y abre el puerto serie:     
import serial
ser=serial.Serial()
ser.port= str(aux_port)
ser.baudrate=1000000
ser.open()
if int(freq)==500:
    muestras=100
    actual_freq=2
    comnd_ComDirecta=[
    # Comando 0x11 => 17; LOS COMANDOS SE ENVIAN EN DECIMAL (0x11 en Hexa es 17 en deci)
        17, 
    # Número de bytes del comando (solo los indicados (n bytes))
    #Nº canales AC/4->32/4=8
    #2*nº canales-> DA DOS Nº-> 32*2=64 y 6*2=12 [1º con los canales AC y luego con los otros, los de 10Hzs]
    #Nº canales=32
    #+2 +2
    #   8+64+12+32+6+2+2=126  (cuando pone canales hay que sumar primero los normales y luego los de 10Hzs)
        126, 
    #Additional bytes:
    #Channel configuaracitons 
    # N bytes puestos a 0,  N=num canales AC / 4 = 8->32/4=8, son 8 bytes de 0s
    #  (8 bytes)
        0, 0, 0, 0, 0, 0, 0, 0, 
    #Sampling rate:[Son 2 bytes para AC y luego para el resto, con su frecuencia]
    # Frecuencia de muestreo (fs) 2 bytes por canal, canales AC
    #  (64 bytes)
        244, 1, 244, 1, 244, 1, 244, 1, 244, 1, 244, 1, 244, 1, 244, 1, 
        244, 1, 244, 1, 244, 1, 244, 1, 244, 1, 244, 1, 244, 1, 244, 1, 
        244, 1, 244, 1, 244, 1, 244, 1, 244, 1, 244, 1, 244, 1, 244, 1, 
        244, 1, 244, 1, 244, 1, 244, 1, 244, 1, 244, 1, 244, 1, 244, 1, 
    # Frecuencia de muestreo (fs) 2 bytes/canal, 
    #    canales DC, Pulso, Oxi, Luz, Evento (6 en total)
    #  (12 bytes)
        10, 0, 10, 0, 10, 0, 10, 0, 10, 0, 10, 0, 
    #Channel module 1 byte por canal
    # Channel modules 500/fs, canales AC
    #  (32 bytes)
        1, 1, 1, 1, 1, 1, 1, 1, 
        1, 1, 1, 1, 1, 1, 1, 1, 
        1, 1, 1, 1, 1, 1, 1, 1, 
        1, 1, 1, 1, 1, 1, 1, 1, 
    # Channel modules, resto canales
    #  (6 bytes)
        50, 50, 50, 50, 50, 50, 
    # Ratio de fs => fsmax/fsmin => 500/10
    #  (2 bytes), máxima y luego minima
        50, 0, 
    # Tamaño del paquete:
    #A=2* sumatorio (sampling rate de cada canal/10)- SOLO LOS DE LOS CANALES ADC
    # [frecuencia*canales], puede tener cada canal diferente frecuencia [xcanales*f1+xcanales*f2]
    #Tamaño del paquete =2+a+10
    #  Tamaño del paquete=2+2*(500*32)/10+10=3212=>0x c8c
    #  el byte más significativo: 12 (0xC)
    #  el byte menos significativo: 140 (0x8C) 
    #  (2 bytes)    
        140, 12 
        ]
elif int(freq)==250:
    muestras=50
    actual_freq=4
    comnd_ComDirecta=[
    17, 126, 0, 0, 0, 0, 0, 0, 0, 0, 
    250, 0, 250, 0, 250, 0, 250, 0, 250, 0, 250, 0, 250, 0, 250, 0, 
    250, 0, 250, 0, 250, 0, 250, 0, 250, 0, 250, 0, 250, 0, 250, 0,
    250, 0, 250, 0, 250, 0, 250, 0, 250, 0, 250, 0, 250, 0, 250, 0,  
    250, 0, 250, 0, 250, 0, 250, 0, 250, 0, 250, 0, 250, 0, 250, 0,  
    10, 0, 10, 0, 10, 0, 10, 0, 10, 0, 10, 0, 
    2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2,  
    2, 2, 2, 2, 2, 2, 2, 2,  
    2, 2, 2, 2, 2, 2, 2, 2,
    50, 50, 50, 50, 50, 50, 
    25, 0, 
    76, 6
    ]
elif int(freq)==100:
    muestras=20
    actual_freq=10
    comnd_ComDirecta=[ 
    17, 126, 0, 0, 0, 0, 0, 0, 0, 0, 
   100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 
    100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 
    100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 
    100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 
    10, 0, 10, 0, 10, 0, 10, 0, 10, 0, 10, 0, 
    5, 5, 5, 5, 5, 5, 5, 5, 
    5, 5, 5, 5, 5, 5, 5, 5, 
    5, 5, 5, 5, 5, 5, 5, 5, 
    5, 5, 5, 5, 5, 5, 5, 5, 
    50, 50, 50, 50, 50, 50, 
    10, 0, 
    140, 2 
    ]


elif int(freq)==50:
    muestras=10
    actual_freq=20
    comnd_ComDirecta=[
    17, 126, 0, 0, 0, 0, 0, 0, 0, 0, 
    50, 0, 50, 0, 50, 0, 50, 0, 50, 0, 50, 0, 50, 0, 50, 0, 
    50, 0, 50, 0, 50, 0, 50, 0, 50, 0, 50, 0, 50, 0, 50, 0,
    50, 0, 50, 0, 50, 0, 50, 0, 50, 0, 50, 0, 50, 0, 50, 0,  
    50, 0, 50, 0, 50, 0, 50, 0, 50, 0, 50, 0, 50, 0, 50, 0,  
    10, 0, 10, 0, 10, 0, 10, 0, 10, 0, 10, 0, 
    10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10,
    50, 50, 50, 50, 50, 50, 
    5, 0, 
    76, 1
    ]

elif int(freq)==20:
    muestras=4
    actual_freq=50     #4 bytes,2 muestras, 2*50=100 muestras piechart
    comnd_ComDirecta=[
        17, 126, 0, 0, 0, 0, 0, 0, 0, 0, 
        20, 0, 20, 0, 20, 0, 20, 0, 20, 0, 20, 0, 20, 0, 20, 0, 
        20, 0, 20, 0, 20, 0, 20, 0, 20, 0, 20, 0, 20, 0, 20, 0,
        20, 0, 20, 0, 20, 0, 20, 0, 20, 0, 20, 0, 20, 0, 20, 0,   
        20, 0, 20, 0, 20, 0, 20, 0, 20, 0, 20, 0, 20, 0, 20, 0,
        10, 0, 10, 0, 10, 0, 10, 0, 10, 0, 10, 0, 
        25, 25, 25, 25, 25, 25, 25, 25,
        25, 25, 25, 25, 25, 25, 25, 25,
        25, 25, 25, 25, 25, 25, 25, 25,
        25, 25, 25, 25, 25, 25, 25, 25,
        50, 50, 50, 50, 50, 50, 
        2, 0, 
        140, 0
        ]

ser.flushInput()
ser.flushOutput()
while (ser.in_waiting!=0):
    pass
    
ser.write(comnd_ComDirecta)

#Primero ack del comando 0x11, xfd y x08
flag_ack=True
while flag_ack: 
    ack=ser.read(1)
    if ack== b'\x11':
        ack = ser.read(1)
        if ack== b'\xfd':
            ack = ser.read(1)
            if ack== b'\x08':       
                flag_ack=False
print('ya tiene ack')

etiquetas = ["Delta","Theta", "Alpha", "Beta", "Gamma"]
colores=['#EC937B', '#C4F880', '#B6F3EC', '#CAB6F3', '#F6C0DF']


if len(canales_lectura)==2:
    # Dibujo gráfico en blanco, solo su posición
    fig, axarr = plt.subplots(2,figsize=(7,7))
    axarr[0].set_position([0.065,0.3,0.4,.5])
    axarr[1].set_position([0.55,0.3,0.4,0.5])
    lista_global =  [[] for i in range(32)]

    def update():
        global etiquetas,colores
        global actual_freq, lista_global
        global canales_lectura,muestras

        # Comprobación preámbulo
        lista_global_aux =  [[] for i in range(32)]
        for veces in range(actual_freq):
            flag=True
            while flag: 
                preambulo=ser.read(1)
                if preambulo== b'\xfd':
                    preambulo = ser.read(1)
                    if preambulo== b'\x03':
                        flag=False
            canales=ser.read(10)

            #Obtención datos EEG con su formato
            for j in range (32):
                canal_ac=ser.read(muestras)
                list_canal_ac.append([canal_ac])
                list_aux=list()
                for k in range(muestras):
                    if k%2==0:
                        aux=int.from_bytes([canal_ac[k],canal_ac[k+1]], byteorder='little', signed=True)
                        list_aux.append(aux)
                lista_global_aux[j].append(list_aux)

        for aa in range(len(lista_global_aux)):
            lista_global[aa].append(lista_global_aux[aa])

        #Bandas de frecuencia, FFT
        for can in range(len(canales_lectura)):
            
            eeg_bands = {'Delta': (0, 4),
                        'Theta': (4, 8),
                        'Alpha': (8, 12),
                        'Beta': (12, 30),
                        'Gamma': (30, 45)}
                    
            flat_list = []
            for sublist in lista_global_aux[canales_lectura[can]]:
                for item in sublist:
                    flat_list.append(item)
            fft_freq = np.fft.fft(flat_list)
            N = len(flat_list)
            f_valores = (np.abs(fft_freq)[:N // 2] * 1 / N)**2
            f = np.linspace(0, 100, len(f_valores))

            eeg_band_fft = dict()
            for band in eeg_bands:  
                freq_ix = np.where((f >= eeg_bands[band][0]) & 
                                (f <= eeg_bands[band][1]))[0]
                
                eeg_band_fft[band] = np.mean(f_valores[freq_ix])


            df = pd.DataFrame(columns=['band', 'val'])
            df['band'] = eeg_bands.keys()
            df['val'] = [eeg_band_fft[band] for band in eeg_bands]

            if math.isnan(eeg_band_fft['Delta']):
                eeg_band_fft['Delta']=0
            if math.isnan(eeg_band_fft['Theta']):
                eeg_band_fft['Theta']=0
            if math.isnan(eeg_band_fft['Alpha']):
                eeg_band_fft['Alpha']=0
            if math.isnan(eeg_band_fft['Beta']):
                eeg_band_fft['Beta']=0
            if math.isnan(eeg_band_fft['Gamma']):
                eeg_band_fft['Gamma']=0

            suma_bandas=eeg_band_fft['Delta']+eeg_band_fft['Theta']+eeg_band_fft['Alpha']+eeg_band_fft['Beta']+eeg_band_fft['Gamma']

            # Potencia relativa
            Delta=(eeg_band_fft['Delta']/suma_bandas)*100
            Theta=(eeg_band_fft['Theta']/suma_bandas)*100
            Alpha=(eeg_band_fft['Alpha']/suma_bandas)*100
            Beta=(eeg_band_fft['Beta']/suma_bandas)*100
            Gamma=(eeg_band_fft['Gamma']/suma_bandas)*100

            #Actualización del gráfico
            axarr[can].clear()
            axarr[can].bar(etiquetas,[Delta, Theta, Alpha,Beta, Gamma], align='center', alpha=0.5,color=colores)
            axarr[can].set_title( "Canal " + str(canales_lectura[can]),fontsize=16)
        fig.canvas.draw_idle()
        update()
    
    # Hilo y cierro puerto de forma segura
    t1 = threading.Thread(target=update)
    t1.start()
    plt.show()
    compr=True
    while(compr):
        if not(t1.is_alive()):
            print("Cierro el puerto")
            comnd_ComDirectaEnd=[23]
            ser.write(comnd_ComDirectaEnd)
            ser.close()
            if guardado=="down":
                for a in range(len(lista_global)):
                    with open("Datos/"+str(freq)+"Hz_Canal_" + str(a) + ".txt", 'w') as f:
                        for b in range(len(lista_global[a])): 
                            for item in lista_global[a][b]:
                                for c in range(len(item)):
                                    f.write("%s\n" % item[c])
                        f.close()
            compr=False
       
else:
    # Análogo para un solo gráfico
    lista=[[0,0,0,0,0]]
    fig, axarr = plt.subplots(figsize=(5,5))

    axarr.bar(etiquetas,lista[0],align='center', alpha=0.5,color=colores)
    axarr.set_position([0.25,0.4,.5,.5])
    axarr.set_title( "Canal " + str(canales_lectura[0]),fontsize=16)

    lista_global =  [[] for i in range(32)]
        
    def update():
        global lista, etiquetas, actual_freq, lista_global
        global canales_lectura,muestras

        lista_global_aux =  [[] for i in range(32)]
        for veces in range(actual_freq):
            flag=True
            while flag: 
                preambulo=ser.read(1)
                if preambulo== b'\xfd':
                    preambulo = ser.read(1)
                    if preambulo== b'\x03':
                        flag=False
            canales=ser.read(10)

            for j in range (32):
                canal_ac=ser.read(muestras)
                list_canal_ac.append([canal_ac])
                list_aux=list()
                for k in range(muestras):
                    if k%2==0:
                        aux=int.from_bytes([canal_ac[k],canal_ac[k+1]], byteorder='little', signed=True)
                        list_aux.append(aux)
                lista_global_aux[j].append(list_aux)

        for aa in range(len(lista_global_aux)):
            lista_global[aa].append(lista_global_aux[aa])

        for can in range(len(canales_lectura)):
            
            eeg_bands = {'Delta': (0.1, 4),
                        'Theta': (4, 8),
                        'Alpha': (8, 12),
                        'Beta': (12, 30),
                        'Gamma': (30, 45)}
            flat_list = []
            for sublist in lista_global_aux[canales_lectura[can]]:
                for item in sublist:
                    flat_list.append(item)
            fft_freq = np.fft.fft(flat_list)
            N = len(flat_list)
            f_valores = (np.abs(fft_freq)[:N // 2] * 1 / N)**2
            f = np.linspace(0, 100, len(f_valores))
            eeg_band_fft = dict()
            for band in eeg_bands:  
                freq_ix = np.where((f >= eeg_bands[band][0]) & 
                                (f <= eeg_bands[band][1]))[0]
                
                eeg_band_fft[band] = np.mean(f_valores[freq_ix])

            df = pd.DataFrame(columns=['band', 'val'])
            df['band'] = eeg_bands.keys()
            df['val'] = [eeg_band_fft[band] for band in eeg_bands]


            if math.isnan(eeg_band_fft['Delta']):
                eeg_band_fft['Delta']=0
            if math.isnan(eeg_band_fft['Theta']):
                eeg_band_fft['Theta']=0
            if math.isnan(eeg_band_fft['Alpha']):
                eeg_band_fft['Alpha']=0
            if math.isnan(eeg_band_fft['Beta']):
                eeg_band_fft['Beta']=0
            if math.isnan(eeg_band_fft['Gamma']):
                eeg_band_fft['Gamma']=0

            suma_bandas=eeg_band_fft['Delta']+eeg_band_fft['Theta']+eeg_band_fft['Alpha']+eeg_band_fft['Beta']+eeg_band_fft['Gamma']

            Delta=(eeg_band_fft['Delta']/suma_bandas)*100
            Theta=(eeg_band_fft['Theta']/suma_bandas)*100
            Alpha=(eeg_band_fft['Alpha']/suma_bandas)*100
            Beta=(eeg_band_fft['Beta']/suma_bandas)*100
            Gamma=(eeg_band_fft['Gamma']/suma_bandas)*100

            axarr.clear()
            axarr.bar(etiquetas,[Delta, Theta, Alpha,Beta, Gamma], align='center', alpha=0.5,color=colores)
            axarr.set_title( "Canal " + str(canales_lectura[0]),fontsize=16)
            fig.canvas.draw_idle()
            update()

    t1 = threading.Thread(target=update)
    t1.start()
    plt.show()
    compr=True
    while(compr):
        if not(t1.is_alive()):
            print("Cierro el puerto")
            comnd_ComDirectaEnd=[23]
            ser.write(comnd_ComDirectaEnd)
            ser.close() 
            if guardado=="down":
                for a in range(len(lista_global)):
                    with open("Datos/"+str(freq)+"Hz_Canal_" + str(a) + ".txt", 'w') as f:
                        for b in range(len(lista_global[a])): 
                            for item in lista_global[a][b]:
                                for c in range(len(item)):
                                    f.write("%s\n" % item[c])
                        f.close()
            compr=False
    