#!/usr/bin/python
#
#	TAREA 4: py-notes
#	Lenguajes de Programacion / 2016-2
#	Integrantes: hmelo - gsepulve
#
#	MODULO DE FUNCIONES AUXILIARES
#	este modulo contiene funciones auxiliares
#
#---------------------------------------------------------------------------------------------------------------------

#MODULOS NECESARIOS

import re
import os
import time
import subprocess
import libStyles

#---------------------------------------------------------------------------------------------------------------------

#PATRONES

#(nombres de notas)
_pat_names = re.compile(r"(?:'.*?')")
_pat_namesder = re.compile(r"(?:'.*?')")
_pat_namesizq = re.compile(r"(?:'.*?')")
#(ruta)
_pat_route = re.compile(r"/[\w|\W]+")
#(tags) almacenados en group 'ntags'
_pat_tags = re.compile(r"^(with tags)\s(?P<ntags>[\w\s]+)")

 #(palabras especificas)
_pat_here = re.compile(r"here")
_pat_in = re.compile(r"in")
_pat_edit = re.compile(r"edit")
_pat_wtags = re.compile(r"with tags")

#---------------------------------------------------------------------------------------------------------------------

#Elimina las comillas simples (' ') de un string
def replace(l):

	l2 = []

	for i in l:
		j = i.replace("'","")
		l2.append(j)

	return l2

#Crea nota(s) con el formato del programa
def create_files(list_names,string_tags):

	for i in list_names:
		archivo = open(str(i)+'.txt','w')
		archivo.write('---------------------------------\n')
		archivo.write('\n')
		archivo.write('NOMBRE ARCHIVO: '+str(i)+'\n')
		archivo.write('TAGS: '+string_tags+'\n')
		archivo.write('FECHA DE CREACION: '+time.asctime()+'\n')
		archivo.write('ULTIMA MODIFICACION: no modificado\n')
		archivo.write('\n')
		archivo.write('---------------------------------\n')
		archivo.write('\n')
		archivo.write('>>NOTA:\n')
		archivo.write('\n')
		archivo.close

	print('[!] '+str(len(list_names))+' archivo(s) fue(ron) creado(s) con exito')
	return None

#Crea nota(s) con el formato del programa y luego accese al editor 'gedit' para escribir en ella
def create_edit_files(list_names,string_tags):

	for i in list_names:

		#creamos la base del archivo
		archivo = open(str(i)+'.txt','w')
		archivo.write('---------------------------------\n')
		archivo.write('\n')
		archivo.write('NOMBRE ARCHIVO: '+str(i)+'\n')
		archivo.write('TAGS: '+string_tags+'\n')
		archivo.write('FECHA DE CREACION: '+time.asctime()+'\n')
		archivo.write('ULTIMA MODIFICACION: no modificado\n')
		archivo.write('\n')
		archivo.write('---------------------------------\n')
		archivo.write('\n')
		archivo.write('>>NOTA:\n')
		archivo.write('\n')
		archivo.close()

		#lanzamos el editor
		_EDITOR = subprocess.Popen(['gedit', str(i)+'.txt'])
		_EDITOR.wait()

	print('[!] '+str(len(list_names))+' archivo(s) fue(ron) creado(s) con exito')
	return None

#Actualiza la fecha de ultima modificacion de una nota.
#	[!] Solo actualiza la fecha si el archivo se modifica mediante py-notes. Si se realiza externamente, la fecha de ultima modificacion no cambia.
def upload_state(nombre_archivo):

	archivo = open(nombre_archivo+'.txt','r')
	_list_lineas = archivo.readlines()
	archivo.close()

	archivo = open(nombre_archivo+'.txt','w')
	for linea in _list_lineas:

		linea_aux = linea.split()

		if 'ULTIMA' in linea_aux:
			archivo.write('ULTIMA MODIFICACION: '+time.asctime()+'\n')
		else:
			archivo.write(linea)

	archivo.close()
	return None

#Retorna un string con la frase a buscar para crear el patron
def search_sentence(lista):
	_list_aux = []

	for i in lista:

		if i != 'find' and i != 'exact':
			_list_aux.append(i)
		else:
			None

	return (" ".join(_list_aux))

#Retorna un string con las palabras a buscar para crear el patron
def search_words(lista):
	_list_aux = []

	for i in lista:

		if i != 'find' and i != 'some':
			_list_aux.append(i)
		else:
			None

	return ("|".join(_list_aux))

#Busca en los archivos, del directorio de trabajo, una palabra o frase. En caso de encontrarla, imprime el documento.
def search_in_files(_pat_aux,_string_aux):

	#obtenemos una lista con todos los archivos del directorio de trabajo
	_list_files = os.listdir(os.getcwd())

	#creamos patron para filtrar solo archivos .txt
	_pat_txt = re.compile(r"\.txt")

	for i in _list_files:

		#variable para controlar si se encontro o no la palabra
		_find = False

		if _pat_txt.search(i):

			#recorremos el archivo y buscamos en cada linea cn el patron
			archivo = open(i,'r')
			for linea in archivo:
				if _pat_aux.search(linea):
					_find = True
					break
			archivo.close()

			#Si se encontro el patron, se imprime la nota con el patron destacado
			if _find == True:
				archivo = open(i,'r')
				for linea in archivo:
					if _pat_aux.search(linea):
						#reemplazamos el patron en la linea con el estilo para destacar
						linea = _pat_aux.sub(libStyles.styles.HIGHLIGHT+_string_aux+libStyles.styles.END,linea)
						linea = linea.rstrip('\n')
						print(linea)
					else:
						linea = linea.rstrip('\n')
						print(linea)
				archivo.close()

	return None

#Retorna la cantidad de notas en el directorio actual
def total_notes():

	_list_files = os.listdir(os.getcwd())
	_contador = 0
	_pat_aux = re.compile(r"\.txt")

	for i in _list_files:
		if _pat_aux.search(i):
			_contador += 1

	return _contador

#Retorna True o False dependiendo si encuentra o no un tag asociado a una nota
def is_tag_there(nombre_archivo,_pat_aux):

	archivo = open(nombre_archivo,'r')
	tag = False

	#recorremos archivo en busca de la linea de tags
	for linea in archivo:
		linea_aux = re.split(r"\s",linea)

		#cuando encontramos la linea que contiene los tags
		if 'TAGS:' in linea_aux:
			#con el patron buscamos el tag en la linea
			if _pat_aux.search(linea):
				tag = True

	archivo.close()
	return tag

#Retorna True o False dependiendo si encuentra o no una fecha en la nota.
#1 para buscar fecha de modificacion
#0 para buscar fecha de creacion
def is_date_there(nombre_archivo,_pat_aux,estado):

	archivo = open(nombre_archivo,'r')
	date = False

	for linea in archivo:
		linea_aux = re.split(r"\s",linea)

		if estado == 1:
			#buscamos la linea que contiene fecha de modificacion
			if 'MODIFICACION:' in linea_aux:
				#con el patron buscamos el tag en la linea
				if _pat_aux.search(linea):
					date = True

		elif estado == 2:
			#buscamos la linea que contiene fecha de creacion
			if 'CREACION:' in linea_aux:
				#con el patron buscamos el tag en la linea
				if _pat_aux.search(linea):
					date = True

	archivo.close()
	return date

#Imprime una nota con estilos
def print_style(nombre_archivo):

	archivo = open(nombre_archivo, 'r')

	for linea in archivo:

		#caso de que encuentre etiqueta </red>
		if libStyles.pat_styles.RED.search(linea):
			#reemplazamos el patron en la linea con el estilo
			linea = libStyles.pat_styles.RED.sub(libStyles.styles.RED,linea)

		#caso de que encuentre etiqueta </green>
		if libStyles.pat_styles.GREEN.search(linea):
			#reemplazamos el patron en la linea con el estilo
			linea = libStyles.pat_styles.GREEN.sub(libStyles.styles.GREEN,linea)

		#caso de que encuentre etiqueta </yellow>
		if libStyles.pat_styles.YELLOW.search(linea):
			#reemplazamos el patron en la linea con el estilo
			linea = libStyles.pat_styles.YELLOW.sub(libStyles.styles.YELLOW,linea)

		#caso de que encuentre etiqueta </blue>
		if libStyles.pat_styles.BLUE.search(linea):
			#reemplazamos el patron en la linea con el estilo
			linea = libStyles.pat_styles.BLUE.sub(libStyles.styles.BLUE,linea)

		#caso de que encuentre etiqueta </cyan>
		if libStyles.pat_styles.CYAN.search(linea):
			#reemplazamos el patron en la linea con el estilo
			linea = libStyles.pat_styles.CYAN.sub(libStyles.styles.CYAN,linea)

		#caso de que encuentre etiqueta </bold>
		if libStyles.pat_styles.BOLD.search(linea):
			#reemplazamos el patron en la linea con el estilo
			linea = libStyles.pat_styles.BOLD.sub(libStyles.styles.BOLD,linea)

		#caso de que encuentre etiqueta </cursive>
		if libStyles.pat_styles.CURSIVE.search(linea):
			#reemplazamos el patron en la linea con el estilo
			linea = libStyles.pat_styles.CURSIVE.sub(libStyles.styles.CURSIVE,linea)

		#caso de que encuentre etiqueta </underline>
		if libStyles.pat_styles.UNDERLINE.search(linea):
			#reemplazamos el patron en la linea con el estilo
			linea = libStyles.pat_styles.UNDERLINE.sub(libStyles.styles.UNDERLINE,linea)

		#caso de que encuentre etiqueta </>
		if libStyles.pat_styles.END.search(linea):
			#reemplazamos el patron en la linea con el estilo
			linea = libStyles.pat_styles.END.sub(libStyles.styles.END,linea)

		#imprimimos la linea
		linea = linea.rstrip('\n')
		print(linea)

	archivo.close()

#Obtiene una lista de tags ordenados alfabeticamente
def list_of_some(lista_archivos,patron):

	lista_some = []

	#creamos patron para filtrar solo archivos .txt
	_pat_txt = re.compile(r"\.txt")

	for i in lista_archivos:
		#si el archivo es una nota
		if _pat_txt.search(i):

			archivo = open(i,'r')

			for linea in archivo:
				if patron.match(linea):

					_aux = patron.search(linea)
					_aux = _aux.group(2)
					_aux = re.split(r"\s",_aux)

					for j in _aux:

						if j not in lista_some and j != '':

							lista_some.append(j)

	return lista_some

#Obtiene una lista de fechas.
def list_of_dates(lista_archivos,patron):

	lista_some = []

	#creamos patron para filtrar solo archivos .txt
	_pat_txt = re.compile(r"\.txt")

	for i in lista_archivos:
		#si el archivo es una nota
		if _pat_txt.search(i):

			archivo = open(i,'r')

			for linea in archivo:
				if patron.match(linea):

					_aux = patron.search(linea)
					fecha = _aux.group('fecha')
					#anio = _aux.group('anio')

					_string_aux = str(fecha)#+' '+str(anio)

					if _string_aux not in lista_some:

						lista_some.append(_string_aux)

	return lista_some