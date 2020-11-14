@ECHO OFF
ECHO Comenzando con la instalacion de la aplicacion web...
SET Eleccion="N"
ECHO Si introduces cualquier otra letra se asumira que dispone de todas las bibliotecas instaladas.
SET /P Eleccion="Dispone de todas las bibliotecas instaladas [S/N]?"
if "%Eleccion%"=="N" (
ECHO ======================
ECHO INSTALANDO BIBLIOTECAS
ECHO ======================
pip install numpy
pip install Flask
pip install PyQtGraph
pip install mne
pip install serial
pip install tkinter
)
ECHO Lanzando la aplicacion...
START python app.py
timeout 3
start chrome http://127.0.0.1:5000/