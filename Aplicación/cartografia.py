
# Script que ejecuta la cartográfia cerebral en el modo archivo

import numpy as np
from matplotlib import pyplot as plt
import mne
import sys

# Captura de la frecuencia seleciconada
freq=sys.argv[1]

biosemi_montage = mne.channels.make_standard_montage('biosemi32')
n_channels = len(biosemi_montage.ch_names)
fake_info = mne.create_info(ch_names=biosemi_montage.ch_names, sfreq=float(freq),
                            ch_types='eeg')

#Lectura de datos
datos_canales=[]
for can in range(32):
    aux=[]
    with open("Datos/" + freq + "Hz_Canal_" + str(can) + ".txt", "r" ) as f:
        for linea in f:
            aux.append(int(linea))
        datos_canales.append(aux)
        f.close()

dataFin = np.zeros((32,len(datos_canales[0])))

for i in range(32):
    for j in range(len(datos_canales[0])):
        dataFin[i,j]= datos_canales[i][j] * 1e-6

fake_evoked = mne.EvokedArray(dataFin, fake_info)
fake_evoked.set_montage(biosemi_montage)

#Se dibuja el gráfico
print("Se procede a dibujar el gráfico")
fake_evoked.plot_topomap(times = "interactive", ch_type='eeg', time_unit='s', time_format= "% 0.3f s", title="Cartografía cerebral",size =3)

