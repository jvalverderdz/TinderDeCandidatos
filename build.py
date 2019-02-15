import cx_Freeze
from cx_Freeze import setup, Executable
#import os

#os.environ['TCL_LIBRARY'] = "C:/Users/Javier/Anaconda3/pkgs/tk-8.6.7-hcb92d03_3/Library/lib/tcl8.6"
#os.environ['TK_LIBRARY'] = "C:/Users/Javier/Anaconda3/pkgs/tk-8.6.7-hcb92d03_3/Library/lib/tk8.6"

exe = Executable(
   script="TinderDeCandidatos.py",
   base="Win32GUI",
   targetName="Tinder de Candidatos.exe"
   )

build_exe_options = {'packages':['os','csv','Tkinter','tkMessageBox','tkFileDialog','PIL'],"include_files": ['Perla_Prueba.jpg', 'default.jpg']}

cx_Freeze.setup(
	name = "Software iterador de fotos",
	options = {'build_exe': build_exe_options},
	version = '2.0',
	description = 'Software para renombrar fotos de candidatos',
	executables = [exe])