# Autora: Claudia Gonzalo Gimeno
# Fecha: May-Dic, 2020

##################### Bibliotecas #######################
from flask import Flask, render_template, request
import  io, os, csv, sys
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import numpy as np
import pandas as pd
import threading,time


##################### Variable global #######################
method="Serie"

##################### Métodos gráficos.py #######################

#Lanzamiento del diagrama de sectores, modo archivo
def piechart_paralelo(canal):
    cad = 'python piechart.py ' 
    for datoschart in range(len(canal)):
        cad = cad + str("Procesos_internos/" + str(canal[datoschart]) + "_Canal.txt " )
    os.system(cad)

#Lanzamiento del gráfico de barras, modo archivo
def barchart_paralelo(canal):
    cad = 'python barchart.py '
    for datoschart in range(len(canal)):
        cad = cad + str("Procesos_internos/" + str(canal[datoschart]) + "_Canal.txt " )
    os.system(cad)

#Lanzamiento de la cartografía, modo archivo
def cartografia_paralelo(freq):
    cad = 'python cartografia.py '+str(freq)
    os.system(cad)

#Lanzamiento del gráfico visualización 2D, modo archivo
def visualizacion2D_paralelo(freq,canal):
    cad = 'python visualizacion2D.py '
    for datoschart in range(len(canal)):
        cad = cad + str("Datos/" + str(freq) + "Hz_Canal_" + str(canal[datoschart])+ ".txt " )
    os.system(cad)

#Lanzamiento de guardado de datos, modo serie
def guardado_paralelo(freq):
    cad = 'python guardado.py '+str(freq) 
    os.system(cad)

#Lanzamiento del gráfico visualización 2D, modo serie
def Visualizacion_serie_paralelo (freq,canal,guardado):
    cad = 'python visualizacion2D_serie.py '+ str(freq) + ' '+str(guardado)
    for x in range(len(canal)):
        cad = cad + ' '+ str(canal[x])
    os.system(cad)

#Lanzamiento del diagrama de sectores, modo serie
def Sectores_serie_paralelo (freq,canal,guardado):
    cad = 'python piechart_serie.py '+ str(freq) + ' '+str(guardado)
    for x in range(len(canal)):
        cad = cad + ' '+ str(canal[x])
    os.system(cad)

#Lanzamiento de gráfico de barras, modo serie
def Barras_serie_paralelo (freq,canal,guardado):
    cad = 'python barchart_serie.py '+ str(freq) + ' '+str(guardado)
    for x in range(len(canal)):
        cad = cad + ' '+ str(canal[x])
    os.system(cad)

    
app = Flask(__name__)

######################### Ruta raiz ##################################
#Selección entre modo serie y archivo

@app.route('/', methods=['GET', 'POST'])
def home():
    #Crea carpeta Datos y Procesos si no están ya creadas
    if not os.path.isdir("Datos"):
        os.mkdir("Datos")

    if not os.path.isdir("Procesos_internos"):
        os.mkdir("Procesos_internos") 

    return render_template("vista_inicial.html")


######################### /Seleccion ##################################
#Implementación de la funcionalidad dependiendo del modo elegido

@app.route('/Seleccion', methods=['GET', 'POST'])
def home12(): 
    global method
    if request.method == 'POST':
        method = request.form['select_mode']
    #Flag para detectar error en la entrada de parámetros
    flag_bool=True
    # El usuario selecciona el modo serie
    if method=="Serie":

        #Comprobación parámetros de entrada y lectura de parámetros
        if request.args:
            claves = list(request.args.keys())
            if 'Barra' in claves[0]:
                tipo_graf='Barras'
            elif 'Sectores' in claves[0]:
                tipo_graf='Sectores'
            elif 'Fourier' in claves [0]:
                tipo_graf='Fourier'
            elif 'Cartografia' in claves[0]:
                tipo_graf='Cartografia'
            elif 'Vi2d' in claves[0]:
                tipo_graf='Vi2d'     
            elif 'Guardado' in claves[0]:
                tipo_graf='Guardado'

            try:
                visua = request.args['visualizar']
            except:
                visua = None

            try:
                freq = request.args[tipo_graf + '_Frecuencia_ID']
            except:
                pass

            try:
                canales = request.args[tipo_graf + '_Canales_ID']
                canal=canales.split(',')
                for c in canal:
                    if int(c)>31 or int(c)<0:
                        flag_bool=False           
            except:
                canal=[]
                for i in range(32):
                    canal.append(i)
                pass

            #Vista error
            if not(flag_bool):
                return render_template("vista_error.html")

            #Creación de hilos para lanzar los gráficos paralelamente
            if tipo_graf=='Guardado':
                t1 = threading.Thread(target=guardado_paralelo,args=(freq,))
                t1.start() 
                return render_template("vista_serie.html")

            elif tipo_graf=='Vi2d':
                if len(canal)==2 or len (canal)==4  or len (canal)==1:
                    t1 = threading.Thread(target=Visualizacion_serie_paralelo,args=(freq,canal,visua,))
                    t1.start() 
                    return render_template("vista_serie.html")
                else:
                    return render_template("vista_error.html")

            elif tipo_graf=='Sectores':
                if len(canal)==2  or len (canal)==1:
                    t1 = threading.Thread(target=Sectores_serie_paralelo,args=(freq,canal,visua,))
                    t1.start() 
                    return render_template("vista_serie.html")
                else:
                    return render_template("vista_error.html")

            elif tipo_graf=='Barras':
                if len(canal)==2  or len (canal)==1:
                    t1 = threading.Thread(target=Barras_serie_paralelo,args=(freq,canal,visua,))
                    t1.start() 
                    return render_template("vista_serie.html")
                else:
                    return render_template("vista_error.html")
            
        else:   
            #Si no hay parámetros
            return render_template("vista_serie.html")

    else:
        # El usuario selecciona el modo archivo, análogo al modo serie
        if request.args:
            claves = list(request.args.keys())
            if 'Barra' in claves[0]:
                tipo_graf='Barras'
            elif 'Sectores' in claves[0]:
                tipo_graf='Sectores'
            elif 'Fourier' in claves [0]:
                tipo_graf='Fourier'
            elif 'Cartografia' in claves[0]:
                tipo_graf='Cartografia'
            elif 'Vi2d' in claves[0]:
                tipo_graf='Vi2d'               

            try:
                visua = request.args['visualizar']
            except:
                visua = None

            try:
                freq = request.args[tipo_graf + '_Frecuencia_ID']
            except:
                pass

            try:
                canales = request.args[tipo_graf + '_Canales_ID']
                canal=canales.split(',')
                for c in canal:
                    if int(c)>31 or int(c)<0:
                        flag_bool = False           
            except:                
                canal=[]
                for i in range(32):
                    canal.append(i)
                pass

            if not(flag_bool):
                return render_template("vista_error.html")

            # Creacción de hilos, incluye la repesentación tabulada de los datos
            if tipo_graf=='Cartografia':
                try:
                    datos_canales=[]
                    for can in range(32):
                        aux=[]
                        with open("Datos/" + freq + "Hz_Canal_" + str(can) + ".txt", "r" ) as f:
                            if visua=="down":
                                for linea in f:
                                    aux.append(int(linea))
                                datos_canales.append(aux)
                                f.close()
                            else:
                                f.close()

                    if visua=="down":
                        data_keys=["Canales"]
                        for a in range(len(datos_canales[0])):
                            data_keys.append("Dato " + str(a+1))

                        for elemen in range(len(datos_canales)):
                            datos_canales[elemen].insert(0,'Canal '+ str(canal[elemen]))
                except:
                    return render_template("vista_error.html")

                t1 = threading.Thread(target=cartografia_paralelo,args=(freq,))
                t1.start() 
                if visua=="down":       
                    return render_template("vista_archivo.html", data_keys=data_keys,data=datos_canales)
                else:
                    return render_template("vista_archivo.html")

            elif tipo_graf=='Vi2d':
                try:
                    datos_canales=[]
                    for can in range(len(canal)):
                        aux=[]
                        with open("Datos/" + freq + "Hz_Canal_" + str(can) + ".txt", "r" ) as f:
                            if visua=="down":
                                for linea in f:
                                    aux.append(int(linea))
                                datos_canales.append(aux)
                                f.close()
                            else:
                                f.close()

                    if visua=="down":
                        data_keys=["Canales"]
                        for a in range(len(datos_canales[0])):
                            data_keys.append("Dato " + str(a+1))

                        for elemen in range(len(datos_canales)):
                            datos_canales[elemen].insert(0,'Canal '+ str(canal[elemen]))
                except:
                    return render_template("vista_error.html")

                t1 = threading.Thread(target=visualizacion2D_paralelo,args=(freq,canal,))
                t1.start() 
                if visua=="down":      
                    #Añade la representación tabulada de los datos, data_keys: nombres columnas, datos_canales: datos EEG
                    return render_template("vista_archivo.html", data_keys=data_keys,data=datos_canales)
                else:
                    return render_template("vista_archivo.html")

            # Diagrama de sectores o gráfico de barras
            else:
                cadena=[]
                visual_final=[]
                if len(canal)==2  or len (canal)==1:
                    for can in range(len(canal)):
                        lista_valores = []
                        lista_valores_aux =[]
                        visual_aux=[]
                        contador_aux = 0
                        with open ("Datos/" + freq + "Hz_Canal_" + canal[can] + ".txt", "r" ) as f:
                            for linea in f:
                                lista_valores_aux.append(int(linea))
                                visual_aux.append(int(linea))
                                contador_aux = contador_aux + 1
                                #Division de los datos de 100 en 100
                                if contador_aux==99:
                                    contador_aux=0
                                    lista_valores.append(lista_valores_aux)
                                    lista_valores_aux=[]

                            visual_final.append(visual_aux)  
                            f.close()
                    
                      
                        cadena_aux=""      
                        #Bandas de frecuencia
                        eeg_bands = {'Delta': (0.1, 4),
                                    'Theta': (4, 8),
                                    'Alpha': (8, 12),
                                    'Beta': (12, 30),
                                    'Gamma': (30, 45)}
                        # FFT de losdatos
                        for i in range(len(lista_valores)):
                            
                            fft_freq = np.fft.fft(lista_valores[i])
                            N = len(lista_valores[i])
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

                            suma_bandas=eeg_band_fft['Delta']+eeg_band_fft['Theta']+eeg_band_fft['Alpha']+eeg_band_fft['Beta']+eeg_band_fft['Gamma']

                            # Potencia relativa
                            Delta=(eeg_band_fft['Delta']/suma_bandas)*100
                            Theta=(eeg_band_fft['Theta']/suma_bandas)*100
                            Alpha=(eeg_band_fft['Alpha']/suma_bandas)*100
                            Beta=(eeg_band_fft['Beta']/suma_bandas)*100
                            Gamma=(eeg_band_fft['Gamma']/suma_bandas)*100

                           
                            cadena_aux=cadena_aux + str(Delta) + "," + str(Theta) + "," + str(Alpha) + "," + str(Beta) + "," + str(Gamma) + ","
                        cadena.append(cadena_aux)
                
                    for datoschart in range(len(cadena)):
                        text_file = open("Procesos_internos/" + str(canal[datoschart]) + "_Canal.txt", "wt")
                        text_file.write(cadena[datoschart])
                        text_file.close()

                    if tipo_graf=='Sectores':
                        t1 = threading.Thread(target=piechart_paralelo,args=(canal,))
                        t1.start()
                    elif tipo_graf == 'Barras':
                        t1 = threading.Thread(target=barchart_paralelo,args=(canal,))
                        t1.start()

                    if visua=='down':
                        data_keys=["Canales"]
                        for a in range(len(visual_final[0])):
                            data_keys.append("Dato " + str(a+1))
                        for elemen in range(len(visual_final)):
                            visual_final[elemen].insert(0,'Canal '+ str(canal[elemen]))                    

                        return render_template("vista_archivo.html", data_keys=data_keys,data=visual_final)
                    else:
                        return render_template("vista_archivo.html")
                else:
                    return render_template("vista_error.html")
        else:
            return render_template("vista_archivo.html")




if __name__ == '__main__':
    app.run()



