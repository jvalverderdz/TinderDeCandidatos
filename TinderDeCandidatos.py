#-*- coding: utf-8 -*-
#TINDER DE CANDIDATOS
#Sistema para determinación manual de color de piel de candidatos
#Elaborado por: Javier Valverde para Python2

import csv
from Tkinter import *
from PIL import Image, ImageTk
import os
import tkMessageBox
import tkFileDialog

reload(sys)
sys.setdefaultencoding("utf-8")
sys.setrecursionlimit(11000)

nID_UNIQUE=2
nNOMBRE=1
nCONTROL=3

ventana = Tk()
ventana.title("Tinder de Candidatos")
ventana.state('zoomed')

val_Nombre = StringVar()
TXT_Nombre = Entry(ventana, textvariable=val_Nombre, state='readonly', width=50).grid(row=0,column=1)

val_Clave = StringVar()
TXT_Clave = Entry(ventana, textvariable=val_Clave, state='readonly', width=50).grid(row=1,column=1)

LBL_Color = Label(ventana, text="Color Observado:").grid(row=1,column=2)
val_Color= StringVar()
TXT_Color = Entry(ventana, textvariable=val_Color, width=20).grid(row=2,column=2)

TkPerla = ImageTk.PhotoImage(Image.open("Perla_Prueba.jpg"))
LBL_PerlaPrueba = Label(ventana, image=TkPerla).grid(row=2,column=0,rowspan=4)

TkFoto= ImageTk.PhotoImage(Image.open("default.jpg"))
LBL_Imagen = Label(ventana, image=TkFoto, width=800, height=600)
LBL_Imagen.grid(row=3,column=1,rowspan=4,columnspan=4)

headers=[]
datos=[]
def importarDatos():	#Importación de los datos que vamos a iterar
	global datos
	global headers
	direccionBase=str(tkFileDialog.askopenfilename())
	with open(direccionBase) as baseRaw:
		base = csv.reader(baseRaw)

		datos = [r for r in base]
		headers=datos[0]
		datos.pop(0)
		baseRaw.close()

contenidoDirectorio=[]
contenidoCarpetas=[]
def seleccionarDirectorio():	#Explorar la ruta de la carpeta de cada candidato para obtener las fotos que vamos a iterar. Comentar en la versión final
	global direccionDirectorio
	global contenidoDirectorio

	direccionDirectorio=str(tkFileDialog.askdirectory())
	contenidoDirectorio = os.listdir(direccionDirectorio)


def evaluar():	#Aqui ponemos los eventos del teclado que deciden qué le pasa a la foto y a la base
	global datos
	global val_Color
	global i


	if val_Color.get()!="":

		evaluacion=str(val_Color.get())
		datos[i][nCONTROL]=evaluacion
		val_Color.set("")
		i+=1
		iterarCarpetas()
		iterarFotos()
	else:
		return

i=0
contenidoCarpeta=[]
direccionCarpeta=""

def iterarCarpetas():
	global i
	global contenidoCarpeta
	global datos
	global direccionCarpeta
	global j

	if i<len(datos):
		if (datos[i][nCONTROL]==str("0") or datos[i][nCONTROL]==str("")):
			direccionCarpeta=(direccionDirectorio+"/"+str(datos[i][nID_UNIQUE]))
			val_Nombre.set(datos[i][nNOMBRE])
			val_Clave.set(datos[i][nID_UNIQUE])
			TkFoto= ImageTk.PhotoImage(Image.open("default.jpg"))
			LBL_Imagen.config(image=TkFoto)
			LBL_Imagen.image = TkFoto

			try:
				contenidoCarpeta=os.listdir(direccionCarpeta)
				j=0
			except WindowsError as we:
				try:
					tkMessageBox.showinfo("Error","La carpeta: "+str(datos[i][nID_UNIQUE])+" no ha sido encontrada.")
					datos[i][nCONTROL]=str("-1")

				except IndexError as ie:
					return
				saltar()
		else:
			saltar()
	else:
		final=tkMessageBox.askyesno("No más datos","Se ha llegado al final de la base. ¿Quiere comenzar de nuevo?")
		if final==True:
			saltar()
		else:
			terminar()
		
j=0
def iterarFotos():
	global j
	global contenidoCarpeta
	global LBL_Imagen
	global TkFoto
	global direccionCarpeta


	if len(contenidoCarpeta)==0:
		try:
			tkMessageBox.showinfo("Error", "No se han encontrado fotos en la carpeta: "+str(datos[i][nID_UNIQUE]))
			datos[i][nCONTROL]=str("-1")
		except IndexError as ie:
			return
		saltar()
	elif j<len(contenidoCarpeta):
		direccionFoto=direccionCarpeta+"/"+contenidoCarpeta[j]
		try:
			TkFoto= ImageTk.PhotoImage(Image.open(direccionFoto))
		except IOError as e:
			return
		LBL_Imagen.config(image=TkFoto)
		LBL_Imagen.image = TkFoto


def saltar():
	global i
	global val_Color
	
	i+=1
	val_Color.set("")

	iterarCarpetas()
	iterarFotos()

def siguienteFoto():
	global j
	global val_Color
	global contenidoCarpeta

	if j<len(contenidoCarpeta)-1:
		j+=1
	val_Color.set("")
	iterarFotos()

def guardar():
	global datos
	global headers
	global val_Color

	val_Color.set("")

	headers[0]=""

	datosOutput=datos

	if os.path.exists("Output")==False:
		os.mkdir("Output")

	version=1
	while os.path.exists("Output/Output"+str(version)+".csv")==True:
		version+=1

	with open("Output/Output"+str(version)+".csv", 'wb') as output:
	    wr = csv.writer(output, quoting=csv.QUOTE_ALL, lineterminator="\n")
	    wr.writerow(headers)
	    wr.writerows(datosOutput)

	tkMessageBox.showinfo("Archivo guardado","Archivo guardado con el nombre: Ouput"+str(version))

def terminar():
	if tkMessageBox.askyesno("Salir","¿Desea guardar y salir?") == True:
            guardar()
            ventana.destroy()
        else:
            return

def anteriorFoto():
	global j
	global val_Color

	if j>0:
		j-=1
	val_Color.set("")
	iterarFotos()

def corregir():
	global i
	global val_Color
	
	i-=1
	datos[i][nCONTROL]=str("0")
	val_Color.set("")

	iterarCarpetas()
	iterarFotos()


BTN_Siguiente = Button(ventana, text="Siguiente Foto (N)", command=siguienteFoto, width=40).grid(row=1,column=3)
BTN_Anterior = Button(ventana, text="Foto Anterior (B)", command=anteriorFoto,width=40).grid(row=2,column=3)
BTN_Evaluar = Button(ventana, text="Evaluar (ENTER)", command=evaluar,width=40).grid(row=0,column=3)
BTN_Saltar = Button(ventana, text="Saltar Observación (S)", command=saltar,width=40).grid(row=0,column=4)
BTN_Guardar = Button(ventana,text="Guardar (G)", command=guardar,width=40).grid(row=1,column=4)

def evSiguienteFoto(evento):
	siguienteFoto()
def evEvaluar(evento):
	evaluar()
def evSaltar(evento):
	saltar()
def evGuardar(evento):
	guardar()
def evTerminar(evento):
	terminar()
def evAnteriorFoto(evento):
	anteriorFoto()

ventana.bind("n", evSiguienteFoto)
ventana.bind("N", evSiguienteFoto)
ventana.bind("<Return>", evEvaluar)
ventana.bind("s", evSaltar)
ventana.bind("S", evSaltar)
ventana.bind("g", evGuardar)
ventana.bind("G", evGuardar)
ventana.bind("B", evAnteriorFoto)
ventana.bind("b", evAnteriorFoto)

tkMessageBox.showinfo("Antes de Iniciar","""Bienvenido al software evaluador de colores de piel.
Al cerrar esta ventana, debes elegir la base de datos en el explorador.
En seguida, debes elegir la carpeta donde se encuentran las fotos (puede ser la de Dropbox, si lo tienes vinculado a tu computadora, o donde se encuentren las carpetas descargadas.
Una vez hecho esto, estás listo para comenzar a evaluar colores de piel.
Cuando termines de hacerlo, presiona "Terminar" para que las evaluaciones se guarden en una base de datos.""")

importarDatos()
seleccionarDirectorio()
iterarCarpetas()
iterarFotos()

ventana.mainloop()

#Notas: El software puede presentar errores cuando tiene que iterar demasiadas fotos ya evaluadas antes de mostrar la primer foto.