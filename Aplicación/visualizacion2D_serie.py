
# Script que ejecuta la viisualización 2D en el modo serie

import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

#Lectura parámetros
canales_lectura=[]
freq=sys.argv[1]
guardado=sys.argv[2]
for c in range(3,len(sys.argv)):
    canales_lectura.append(int(sys.argv[c]))

canales_lectura.sort()
dicc_canales= dict()

for a in range(len(canales_lectura)):
    dicc_canales.update({int(canales_lectura[a]):a})

list_ac = [[] for i in range(32)]
list_canal_ac= list()

### Lista de pueros disponibles:
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
aux_port=""
for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
        aux_port = str(port)
   
#Configura y abre el puerto serie:     
import serial
ser=serial.Serial()
ser.port= str(aux_port)
ser.baudrate=1000000
ser.open()
if int(freq)==500:
    muestras=100
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


#Para dibujar creo ventana, título e inicializo listas
win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('EEG')
graficos=list()
curve = list()
data = list() 
ptr = np.empty(len(canales_lectura))
#Creo los  plots, los organizo y creo las listas necesarias
for canal in range(len(canales_lectura)):
    curve.append([])
    data.append(np.empty(100))

for canal in range(len(canales_lectura)):
    if canal % 4 ==0:
        win.nextRow()
    graficos.append(win.addPlot())
    graficos[canal].setDownsampling(mode='peak')
    graficos[canal].setClipToView(True)
    graficos[canal].setRange(xRange=[-100, 0])
    graficos[canal].setLimits(xMax=0)
    curve[canal] = graficos[canal].plot()
    ptr[canal] = 0
    
#Dibuja datos
def update2(lista,indice):
    global data, ptr
    
    for aaa in range(len(lista)):
        data[indice][int(ptr[indice])] = lista[aaa]
        ptr[indice] += 1
    if ptr[indice] >= data[indice].shape[0]:
        tmp = data[indice]
        data[indice] = np.empty(data[indice].shape[0] * 2)
        data[indice][:tmp.shape[0]] = tmp
    curve[indice].setData(data[indice][:int(ptr[indice])])
    curve[indice].setPos(-int(ptr[indice]), 0)



def update():  
    global canales_lectura,muestras, dicc_canales
    flag=True
    while flag: 
        preambulo=ser.read(1)
        if preambulo== b'\xfd':
            preambulo = ser.read(1)
            if preambulo== b'\x03':
                flag=False
    
    canales=ser.read(10)
    #Lectura datos
    for j in range (32):
        canal_ac=ser.read(muestras)
        list_canal_ac.append([canal_ac])
        list_aux=list()
        for k in range(muestras):
            if k%2==0:
                aux=int.from_bytes([canal_ac[k],canal_ac[k+1]], byteorder='little', signed=True)
                list_aux.append(aux) 

        for w in range(len(list_aux)):
            list_ac[j].append(list_aux[w])

        if j in canales_lectura:
            update2(list_aux,dicc_canales[j])

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start()
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

#Cierro puerto de forma segura
comnd_ComDirectaEnd=[23]
ser.write(comnd_ComDirectaEnd)

ser.close()

#Guardado de datos
if guardado=='down':
    for aa in range(len(list_ac)):     
        with open("Datos/"+str(freq)+"Hz_Canal_" + str(aa) + ".txt", 'w') as f: 
            for item in list_ac[aa]:
                f.write("%s\n" % item)
            f.close()