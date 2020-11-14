

# Script que ejecuta la viisualización 2D en el modo archivo

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import sys

#Lectura de parámetros
rutas = []
for rut in range(1,len(sys.argv)):
    rutas.append(sys.argv[rut])

#Lectura de datos
datos = []
datos_aux=[]
for ind in range(len(rutas)):
    datos_aux=[]
    with open(str(rutas[ind]), "r") as f:
        for linea in f:
            datos_aux.append(int(linea))
        f.close()
    datos.append(datos_aux)

#Inicialización gráfico
win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('EEG')
graficos=list()
curve = list()
data = list() 
ptr = np.empty(len(datos))
#Creo los 32 plots, los organizo y creo las listas necesarias
for canal in range(len(datos)):
    curve.append([])
    data.append(np.empty(500))

for canal in range(len(datos)):
    if canal % 4 ==0:
        win.nextRow()
    graficos.append(win.addPlot())
    graficos[canal].setDownsampling(mode='peak')
    graficos[canal].setClipToView(True)
    graficos[canal].setRange(xRange=[-500, 0])
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
    
# Lee los datos de entrada y los organiza por listas   
def update():
    global datos    
    for indice in range(len(datos)):   
        update2(datos[indice][0:500],indice)
        datos[indice] = datos[indice][500:(len(datos[indice])-1)]    
    
    

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start()
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

