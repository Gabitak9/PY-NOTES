#!/usr/bin/python
#
#	TAREA 4: py-notes
#	Lenguajes de Programacion / 2016-2
#	Integrantes: hmelo - gsepulve
#
#	MODULO DE COMANDOS
#	este modulo contiene las funciones principales, asociadas a cada comando
#
#---------------------------------------------------------------------------------------------------------------------

#MODULOS NECESARIOS

import re
import os
import subprocess
import libStyles
import libAux

#---------------------------------------------------------------------------------------------------------------------

#PATRONES

#(nombres de notas)
_pat_names = re.compile(r"(?:'.*?')")
#(ruta)
_pat_route = re.compile(r"/[\w|\W]+")
#(tags) almacenados en group 'ntags'
_pat_tags_ruta = re.compile(r"(with tags)\s(?P<ntags>[\w+\s]+)(in)")
_pat_tags_sinruta = re.compile(r"(with tags)\s(?P<ntags>[\w+\s]+)")
#(name is) nombre almacenado en group 'name_exact'
_pat_nameis = re.compile(r"(name is)\s(?P<name_exact>[\w]+)\s?")
#(name contains) nombre almacenado en 'name_contains'
_pat_namecontains = re.compile(r"(name contains)\s(?P<name_contains>[\w]+)\s?")
#(tag is) tag almacenado en 'tag'
_pat_tagis = re.compile(r"(tag is)\s(?P<tag>[\w]+)\s?")
#(sorted by) la opcion esta en el grupo 2
_pat_sorted = re.compile(r"(sorted by)\s(names|tags|modified|creation)")

#(palabras especificas)
_pat_here = re.compile(r"here")
_pat_in = re.compile(r"in")
_pat_edit = re.compile(r"edit")
_pat_wtags = re.compile(r"with tags")
_pat_where = re.compile(r"all where")



#---------------------------------------------------------------------------------------------------------------------

#COMANDO dir
#
#	<dir> ::= "dir" ( "here" | <route> )
#	casos.
#		>>> dir here 		(ruta actual)
#		>>> dir /home/user 	(ruta valida)
#		>>> dir noexiste 	(ruta invalida)
#

def _dir_(comando):

	_comando = re.split(r"\s",comando)

	if _pat_here.match(_comando[1]):
		_dir_actual = os.getcwd() #Obtenemos el directorio actual
		os.chdir(_dir_actual) #Asignamos directorio actual
		print("[!] Asignado como directorio actual de trabajo: "+_dir_actual)
	else:
		if os.path.exists(_comando[1]): #Verificamos que el directorio ingresado exista
			os.chdir(_comando[1]) #Asignamos directorio dado por el usuario
			print("[!] Asignado como directorio actual de trabajo: "+_comando[1])
		else:
			print(libStyles.styles.WARNING+"[!] No se ingreso un directorio valido"+libStyles.styles.END)

#---------------------------------------------------------------------------------------------------------------------

#COMANDO create
#
#	<create> ::= "create" (<name> ["edit"] | <name> {<name>}) [<tags>] ["in" <route>]
#	<tags> ::= "with tags" (<tag-name> {<tag-name>})
#	casos.
#		>>> create 'nota1'						#crea una nota llamada nota1
#		>>> create 'nota1' edit 				#crea una nota llamada nota1 y editarla
#		>>> create 'nota1' with tags tag1		#crea una nota llamada nota1 con tags
#		>>> create 'nota1' in /ruta				#crea una nota llamada nota1 en ruta especificada
#		>>> create 'nota1' edit with tags tag1 in /route			#crea nota1 con todas las condiciones anteriores
#
#	ademas se pueden crear mas de una nota simultaneamente, para ello el usuario debera separar cada nota con un ' ' (espacio)
#	ejemplo:
#		>>> create 'nota1' 'nota2'				#crea una nota llamada nota1 y otra llamada nota2
#

def _create_(comando):

	#lista con nombres de notas
	_list_names = _pat_names.findall(comando)
	_list_names = libAux.replace(_list_names)

	#lista con ruta en posicion [0]
	_ruta = _pat_route.findall(comando)

	#verificamos que la  ruta exista y obtenemos los tags
	if _pat_route.search(comando):
		if os.path.exists(_ruta[0]):
			if _pat_in.search(comando):
				_list_tags = _pat_tags_ruta.search(comando)
				_list_tags = _list_tags.group('ntags')
				_list_tags = re.split(r"\s",_list_tags)
		else:
			print(libStyles.styles.WARNING+"[!] La ruta ingresada no es valida"+libStyles.styles.END)
			return None
	elif _pat_wtags.search(comando):
		_list_tags = _pat_tags_sinruta.search(comando)
		_list_tags = _list_tags.group('ntags')
		_list_tags = re.split(r"\s",_list_tags)

	_ruta_actual = os.getcwd() #guardamos la ruta actual para devolverla en caso de que fuera necesario

	#variable para administrar el modo edit
	_modo_edit = False

	#accedemos a cada caso
	if _pat_edit.search(comando):

		_modo_edit = True

		if _pat_wtags.search(comando):

			if _pat_in.search(comando):
				#asignamos ruta de trabajo
				os.chdir(_ruta[0])
				#creamos strings de tags
				_string_tags = " ".join(_list_tags)

			else:
				#creamos strings de tags
				_string_tags = " ".join(_list_tags)

		elif _pat_in.search(comando):
			#asignamos ruta de trabajo
			os.chdir(_ruta[0])
			#vaciamos tags
			_string_tags = ""

		else:
			#vaciamos tags
			_string_tags = ""

	elif _pat_wtags.search(comando):

		if _pat_in.search(comando):
			#asignamos ruta de trabajo
			os.chdir(_ruta[0])
			#creamos strings de tags
			_string_tags = " ".join(_list_tags)

		else:
			#creamos strings de tags
			_string_tags = " ".join(_list_tags)

	elif _pat_in.search(comando):
		#asignamos ruta de trabajo
		os.chdir(_ruta[0])
		#vaciamos tags
		_string_tags = ""

	else:
		#vaciamos tags
		_string_tags = ""

	#informacion
	print("[!] NOMBRE(s) DE ARCHIVO(s): "+" ".join(_list_names))
	print("[!] NOMBRE(s) DE TAG(s): "+_string_tags)
	print("[!] RUTA A GUARDAR: "+str(os.getcwd()))
	print("[!] MODO DE EDICION: "+str(_modo_edit))

	#creamos los archivos
	if _modo_edit == False:
		libAux.create_files(_list_names,_string_tags)
	else:	
		libAux.create_edit_files(_list_names,_string_tags)

	#devolvemos la ruta
	os.chdir(_ruta_actual)
	return 0

#---------------------------------------------------------------------------------------------------------------------

#COMANDO show
#
#	<show> ::= "show" (<name> | "all" <show-options>) ["in" <route>]
#	<show-options> ::=  [<where>] [<sort>]
#	<where> ::= "where" ( ("name" ("is"|"contains") <name>) | ("tag is" <tag-name>) )
#	<sort> ::= "sorted by" ("names" | "tags" | "modified" | "creation")
#	casos.
#		>>> show 'nota1'
#		>>> show 'nota1' in /ruta
#		>>>	show all where name is nota
#		>>> show all where name contains nota
#		>>>	show all where tag is tag1
#		>>> show all sorted by names
#		>>> show all sorted by tags
#		>>> show all sorted by modified
#		>>> show all sorted by creation
#		>>>	show all where name is nota in /ruta
#		>>> show all where name contains nota in /ruta
#		>>>	show all where tag is tag1 in /ruta
#		>>> show all sorted by names in /ruta
#		>>> show all sorted by tags in /ruta
#		>>> show all sorted by modified in /ruta
#		>>> show all sorted by creation in /ruta
#

def _show_(comando):
	
	#lista con nombres de notas
	_list_names = _pat_names.findall(comando)
	_list_names = libAux.replace(_list_names)

	#lista con ruta en posicion [0]
	_ruta = _pat_route.findall(comando)

	#verificamos que la ruta exista
	if _pat_route.search(comando):
		if os.path.exists(_ruta[0]):
			None
		else:
			print(libStyles.styles.WARNING+"[!] La ruta ingresada no es valida"+libStyles.styles.END)
			return None

	#guardamos la ruta actual para devolverla en caso de que fuera necesario
	_ruta_actual = os.getcwd()

	#caso con ruta ingresada
	if _pat_route.search(comando):

		#asignamos ruta de trabajo
		os.chdir(_ruta[0])

		#obtenemos una lista con todos los archivos del directorio de trabajo
		_list_files = os.listdir(_ruta[0])

		#creamos patron para filtrar solo archivos .txt
		_pat_txt = re.compile(r"\.txt")

		#caso where
		if _pat_where.search(comando):
			
			#si se ingreso con 'name is'
			if _pat_nameis.search(comando):
				#creamos patron
				_name_aux = _pat_nameis.search(comando)
				_name_aux = _name_aux.group('name_exact')
				_pat_aux = re.compile(r""+_name_aux+".txt")

				#buscamos en los archivos del directorio un match y imprimimos
				for i in _list_files:
					if re.match(_pat_aux,i) and _pat_txt.search(i):
						#imprimimos el archivo
						libAux.print_style(str(i))

			#si se ingreso con 'name contains'
			elif _pat_namecontains.search(comando):
				#creamos patron
				_name_aux = _pat_namecontains.search(comando)
				_name_aux = _name_aux.group('name_contains')
				#el patron ignorara mayusculas/minusculas para extender busqueda
				_pat_aux = re.compile(r""+_name_aux, re.IGNORECASE)

				#buscamos en los archivos del directorio un search y lo imprimimos
				for i in _list_files:
					if re.search(_pat_aux,i) and _pat_txt.search(i):
						#imprimimos el archivo
						libAux.print_style(str(i))

			#si se ingreso con 'tags in'
			elif _pat_tagis.search(comando):
				#creamos patron
				_tag_aux = _pat_tagis.search(comando)
				_tag_aux = _tag_aux.group('tag')
				_pat_aux = re.compile(r""+_tag_aux)

				#buscamos en los archivos del directorio si contienen el tag
				for i in _list_files:
					if libAux.is_tag_there(i,_pat_aux)  and _pat_txt.search(i):
						#imprimimos el archivo
						libAux.print_style(str(i))

			else:
				print(libStyles.styles.WARNING+"[!] Ingrese el comando de forma correcta"+libStyles.styles.END)

		#caso sorted
		elif _pat_sorted.search(comando):
			
			_option = _pat_sorted.search(comando)
			_option = _option.group(2)

			#opcion ordenar por nombre
			if _option == 'names':
				#ordenamos los archivos en forma alfabetica
				_list_files.sort()

				for i in _list_files:
					#buscamos archivos q sean notas y los imprimimos
					if _pat_txt.search(i):
						libAux.print_style(str(i))


			#opcion ordenar por tags
			elif _option == 'tags':
				
				#creamos un patron para obtener los tags de los archivos
				_pat_aux = re.compile(r"(TAGS:)\s(?P<tags>[\w+\s]+)")

				#obtenemos una lista con todos los tags existentes
				_list_aux = libAux.list_of_some(_list_files,_pat_aux)

				#los ordenamos alfabeticamente
				_list_aux.sort()

				print("[!] Tags encontrados: "+' '.join(_list_aux))

				for i in _list_aux:

					print(libStyles.styles.OK+"-------------------------------------------------------------------")
					print("NOTAS RELACIONADAS CON EL TAG: "+str(i))
					print("-------------------------------------------------------------------"+libStyles.styles.END)

					_pat_aux2 = re.compile(r""+str(i))

					for j in _list_files:

						if libAux.is_tag_there(j,_pat_aux2):

							#buscamos archivos q sean notas y los imprimimos
							if _pat_txt.search(j):
								libAux.print_style(str(j))

			#opcion ordenar por fecha de modificacion
			elif _option == 'modified':
								
				#creamos un patron para obtener las fechas de modificacion
				_pat_aux = re.compile(r"(ULTIMA MODIFICACION:)\s(?P<fecha>[\w+\s]+)\s(?P<hora>[\w]+\:[\w]+\:[\w]+)\s(?P<anio>[\w]+)")

				#obtenemos una lista con todos los tags existentes
				_list_aux = libAux.list_of_dates(_list_files,_pat_aux)

				#los ordenamos alfabeticamente
				_list_aux.sort()

				print("[!] Fechas de modificacion encontrados: "+' / '.join(_list_aux))

				for i in _list_aux:

					print(libStyles.styles.OK+"-------------------------------------------------------------------")
					print("NOTAS RELACIONADAS CON LA FECHA DE MODIFICACION: "+str(i))
					print("-------------------------------------------------------------------"+libStyles.styles.END)

					_pat_aux2 = re.compile(r""+str(i))

					for j in _list_files:

						if libAux.is_date_there(j,_pat_aux2,1):

							#buscamos archivos q sean notas y los imprimimos
							if _pat_txt.search(j):
								libAux.print_style(str(j))

			#opcion ordenar por fecha de creacion
			else:

				#creamos un patron para obtener las fechas de creacion
				_pat_aux = re.compile(r"(FECHA DE CREACION:)\s(?P<fecha>[\w+\s]+)\s(?P<hora>[\w]+\:[\w]+\:[\w]+)\s(?P<anio>[\w]+)")

				#obtenemos una lista con todos los tags existentes
				_list_aux = libAux.list_of_dates(_list_files,_pat_aux)

				#los ordenamos alfabeticamente
				_list_aux.sort()

				print("[!] Fechas de creacion encontrados: "+' / '.join(_list_aux))

				for i in _list_aux:

					print(libStyles.styles.OK+"-------------------------------------------------------------------")
					print("NOTAS RELACIONADAS CON LA FECHA DE CREACION: "+str(i))
					print("-------------------------------------------------------------------"+libStyles.styles.END)

					_pat_aux2 = re.compile(r""+str(i))

					for j in _list_files:

						if libAux.is_date_there(j,_pat_aux2,2):

							#buscamos archivos q sean notas y los imprimimos
							if _pat_txt.search(j):
								libAux.print_style(str(j))

		#caso con nombre
		else:

			#recorremos nombres ingresados
			for i in _list_names:
				#validamos que el archivo exista en la ruta especificada
				if (str(i)+'.txt' in os.listdir(_ruta[0])):
					#imprimimos el archivo
					libAux.print_style(str(i)+'.txt')

				else:
					print(libStyles.styles.WARNING+"[!] El archivo no se encuentra en la ruta especificada"+libStyles.styles.END)

		#devolvemos a la ruta actual
		os.chdir(_ruta_actual)

	#caso sin ruta
	else:

		#obtenemos una lista con todos los archivos del directorio de trabajo
		_list_files = os.listdir(os.getcwd())

		#creamos patron para filtrar solo archivos .txt
		_pat_txt = re.compile(r"\.txt")

		#caso where
		if _pat_where.search(comando):
			
			#si se ingreso con 'name is'
			if _pat_nameis.search(comando):
				#creamos patron
				_name_aux = _pat_nameis.search(comando)
				_name_aux = _name_aux.group('name_exact')
				_pat_aux = re.compile(r""+_name_aux+".txt")

				#buscamos en los archivos del directorio un match y imprimimos
				for i in _list_files:
					if re.match(_pat_aux,i) and _pat_txt.search(i):
						#imprimimos el archivo
						libAux.print_style(str(i))

			#si se ingreso con 'name contains'
			elif _pat_namecontains.search(comando):
				#creamos patron
				_name_aux = _pat_namecontains.search(comando)
				_name_aux = _name_aux.group('name_contains')
				#el patron ignorara mayusculas/minusculas para extender busqueda
				_pat_aux = re.compile(r""+_name_aux, re.IGNORECASE)

				#buscamos en los archivos del directorio un search y lo imprimimos
				for i in _list_files:
					if re.search(_pat_aux,i) and _pat_txt.search(i):
						#imprimimos el archivo
						libAux.print_style(str(i))

			#si se ingreso con 'tags in'
			elif _pat_tagis.search(comando):
				#creamos patron
				_tag_aux = _pat_tagis.search(comando)
				_tag_aux = _tag_aux.group('tag')
				_pat_aux = re.compile(r""+_tag_aux)

				#buscamos en los archivos del directorio si contienen el tag
				for i in _list_files:
					if libAux.is_tag_there(i,_pat_aux)  and _pat_txt.search(i):
						#imprimimos el archivo
						libAux.print_style(str(i))

		#caso sorted
		elif _pat_sorted.search(comando):
			
			_option = _pat_sorted.search(comando)
			_option = _option.group(2)

			#opcion de ordenar por nombres
			if _option == 'names':
				#ordenamos los archivos en forma alfabetica
				_list_files.sort()

				for i in _list_files:
					#buscamos archivos q sean notas y los imprimimos
					if _pat_txt.search(i):
						libAux.print_style(str(i))

			#opcion de ordenar por tags
			elif _option == 'tags':
				
				#creamos un patron para obtener los tags de los archivos
				_pat_aux = re.compile(r"(TAGS:)\s(?P<tags>[\w+\s]+)")

				#obtenemos una lista con todos los tags existentes
				_list_aux = libAux.list_of_some(_list_files,_pat_aux)

				#los ordenamos alfabeticamente
				_list_aux.sort()

				print("[!] Tags encontrados: "+' '.join(_list_aux))

				for i in _list_aux:

					print(libStyles.styles.OK+"-------------------------------------------------------------------")
					print("NOTAS RELACIONADAS CON EL TAG: "+str(i))
					print("-------------------------------------------------------------------"+libStyles.styles.END)

					_pat_aux2 = re.compile(r""+str(i))

					for j in _list_files:

						if libAux.is_tag_there(j,_pat_aux2):

							#buscamos archivos q sean notas y los imprimimos
							if _pat_txt.search(j):
								libAux.print_style(str(j))

			#opcion de ordenar por fecha de modificacion
			elif _option == 'modified':
								
				#creamos un patron para obtener las fechas de modificacion
				_pat_aux = re.compile(r"(ULTIMA MODIFICACION:)\s(?P<fecha>[\w+\s]+)\s(?P<hora>[\w]+\:[\w]+\:[\w]+)\s(?P<anio>[\w]+)")

				#obtenemos una lista con todos los tags existentes
				_list_aux = libAux.list_of_dates(_list_files,_pat_aux)

				#los ordenamos alfabeticamente
				_list_aux.sort()

				print("[!] Fechas de modificacion encontrados: "+' / '.join(_list_aux))

				for i in _list_aux:

					print(libStyles.styles.OK+"-------------------------------------------------------------------")
					print("NOTAS RELACIONADAS CON LA FECHA DE MODIFICACION: "+str(i))
					print("-------------------------------------------------------------------"+libStyles.styles.END)

					_pat_aux2 = re.compile(r""+str(i))

					for j in _list_files:

						if libAux.is_date_there(j,_pat_aux2,1):

							#buscamos archivos q sean notas y los imprimimos
							if _pat_txt.search(j):
								libAux.print_style(str(j))

			#opcion de ordenar por fecha de creacion
			else:

				#creamos un patron para obtener las fechas de creacion
				_pat_aux = re.compile(r"(FECHA DE CREACION:)\s(?P<fecha>[\w+\s]+)\s(?P<hora>[\w]+\:[\w]+\:[\w]+)\s(?P<anio>[\w]+)")

				#obtenemos una lista con todos los tags existentes
				_list_aux = libAux.list_of_dates(_list_files,_pat_aux)

				#los ordenamos alfabeticamente
				_list_aux.sort()

				print("[!] Fechas de creacion encontrados: "+' / '.join(_list_aux))

				for i in _list_aux:

					print(libStyles.styles.OK+"-------------------------------------------------------------------")
					print("NOTAS RELACIONADAS CON LA FECHA DE CREACION: "+str(i))
					print("-------------------------------------------------------------------"+libStyles.styles.END)

					_pat_aux2 = re.compile(r""+str(i))

					for j in _list_files:

						if libAux.is_date_there(j,_pat_aux2,2):

							#buscamos archivos q sean notas y los imprimimos
							if _pat_txt.search(j):
								libAux.print_style(str(j))

		#caso con nombre
		else:

			#recorremos nombres ingresados
			for i in _list_names:
				#validamos que el archivo exista en la ruta especificada
				if (str(i)+'.txt' in os.listdir(os.getcwd())):
					#imprimimos el archivo
					libAux.print_style(str(i)+'.txt')

				else:
					print(libStyles.styles.WARNING+"[!] El archivo no se encuentra en la ruta especificada"+libStyles.styles.END)

#---------------------------------------------------------------------------------------------------------------------

#COMANDO edit
#
#	<edit> ::= "edit" <name> ["in" <route>
#	casos.
#		>>> edit 'nota1'			#edicion del archivo en ruta actual
#		>>> edit 'nota1' in /ruta 	#edicion del archivo en ruta especificada
#	

def _edit_(comando):

	#lista con nombres de notas
	_list_names = _pat_names.findall(comando)
	_list_names = libAux.replace(_list_names)

	#lista con ruta en posicion [0]
	_ruta = _pat_route.findall(comando)

	#verificamos que la  ruta exista
	if _pat_route.search(comando):
		if os.path.exists(_ruta[0]):
			None
		else:
			print(libStyles.styles.WARNING+"[!] La ruta ingresada no es valida"+libStyles.styles.END)
			return None

	#guardamos la ruta actual para devolverla en caso de que fuera necesario
	_ruta_actual = os.getcwd()

	if _pat_in.search(comando):
		#asignamos ruta de trabajo
		os.chdir(_ruta[0])

		for i in _list_names:

			#validamos que el archivo exista en la ruta
			if (str(i)+'.txt' in os.listdir(_ruta[0])):
				#lanzamos el editor
				_EDITOR = subprocess.Popen(['gedit', str(i)+'.txt'])
				_EDITOR.wait()

				#editamos fecha de modificacion
				libAux.upload_state(str(i))
				print("[!] Archivo editado con exito")
			else:
				print(libStyles.styles.WARNING+"[!] El archivo no se encuentra en la ruta especificada"+libStyles.styles.END)

	else:

		for i in _list_names:

			#validamos que el archivo exista en la ruta
			if (str(i)+'.txt' in os.listdir(_ruta_actual)):
				#lanzamos el editor
				_EDITOR = subprocess.Popen(['gedit', str(i)+'.txt'])
				_EDITOR.wait()

				#editamos fecha de modificacion
				libAux.upload_state(str(i))
				print("[!] Archivo editado con exito")
			else:
				print(libStyles.styles.WARNING+"[!] El archivo no se encuentra en la ruta actual"+libStyles.styles.END)

	#volvemos a la ruta inicial de trabajo
	os.chdir(_ruta_actual)

#---------------------------------------------------------------------------------------------------------------------

#COMANDO delete
#
#	<delete> ::= "delete" ("all" [<where>] | <name>) ["in" <route>]
#	<where> ::= "where" ( ("name" ("is"|"contains") <name>) | ("tag is" <tag-name>) )
#	casos:
#		>>> delete 'nota1'
#		>>> delete 'nota1' in /ruta
#		>>> delete all where name is nota
#		>>> delete all where name contains nota
#		>>> delete all where tag is tag1
#		>>> delete all where name is nota in /ruta
#		>>> delete all where name contains nota in /ruta
#		>>> delete all where tag is tag1 in /ruta
#

def _delete_(comando):
	
	#lista con nombres de notas
	_list_names = _pat_names.findall(comando)
	_list_names = libAux.replace(_list_names)

	#lista con ruta en posicion [0]
	_ruta = _pat_route.findall(comando)

	#verificamos que la  ruta exista
	if _pat_route.search(comando):
		if os.path.exists(_ruta[0]):
			None
		else:
			print(libStyles.styles.WARNING+"[!] La ruta ingresada no es valida"+libStyles.styles.END)
			return None

	#guardamos la ruta actual para devolverla en caso de que fuera necesario
	_ruta_actual = os.getcwd()

	#si se accede con comando where
	if _pat_where.search(comando):
		
		#si se ingreso ruta
		if _pat_route.search(comando):
			#asignamos ruta de trabajo
			os.chdir(_ruta[0])

			#obtenemos una lista con todos los archivos del directorio de trabajo
			_list_files = os.listdir(_ruta[0])

			#si se ingreso con 'name is'
			if _pat_nameis.search(comando):
				#creamos patron
				_name_aux = _pat_nameis.search(comando)
				_name_aux = _name_aux.group('name_exact')
				_pat_aux = re.compile(r""+_name_aux+".txt")

				#buscamos en los archivos del directorio un match y lo borramos
				for i in _list_files:
					if re.match(_pat_aux,i):
						os.remove(str(i))

			#si se ingreso con 'name contains'
			elif _pat_namecontains.search(comando):
				#creamos patron
				_name_aux = _pat_namecontains.search(comando)
				_name_aux = _name_aux.group('name_contains')
				_pat_aux = re.compile(r""+_name_aux)

				#buscamos en los archivos del directorio un search y lo borramos
				for i in _list_files:
					if re.search(_pat_aux,i):
						os.remove(str(i))

			#si se ingreso con 'tags in'
			elif _pat_tagis.search(comando):
				#creamos patron
				_tag_aux = _pat_tagis.search(comando)
				_tag_aux = _tag_aux.group('tag')
				_pat_aux = re.compile(r""+_tag_aux)

				#buscamos en los archivos del directorio si contienen el tag
				for i in _list_files:
					if libAux.is_tag_there(i,_pat_aux):
						os.remove(str(i))

			else:
				print(libStyles.styles.WARNING+"[!] Ingrese el comando de forma correcta"+libStyles.styles.END)

			#devolvemos a la ruta actual
			os.chdir(_ruta_actual)

		#si no se ingreso ruta
		else:
			#obtenemos una lista con todos los archivos del directorio de trabajo
			_list_files = os.listdir(os.getcwd())

			#si se ingreso con 'name is'
			if _pat_nameis.search(comando):
				#creamos patron
				_name_aux = _pat_nameis.search(comando)
				_name_aux = _name_aux.group('name_exact')
				_pat_aux = re.compile(r""+_name_aux+".txt")

				#buscamos en los archivos del directorio un match y lo borramos
				for i in _list_files:
					if re.match(_pat_aux,i):
						os.remove(str(i))

			#si se ingreso con 'name contains'
			elif _pat_namecontains.search(comando):
				#creamos patron
				_name_aux = _pat_namecontains.search(comando)
				_name_aux = _name_aux.group('name_contains')
				_pat_aux = re.compile(r""+_name_aux)

				#buscamos en los archivos del directorio un search y lo borramos
				for i in _list_files:
					if re.search(_pat_aux,i):
						os.remove(str(i))

			#si se ingreso con 'tags in'
			elif _pat_tagis.search(comando):
				#creamos patron
				_tag_aux = _pat_tagis.search(comando)
				_tag_aux = _tag_aux.group('tag')
				_pat_aux = re.compile(r""+_tag_aux)

				#buscamos en los archivos del directorio si contienen el tag
				for i in _list_files:
					if libAux.is_tag_there(i,_pat_aux):
						os.remove(str(i))

			else:
				print(libStyles.styles.WARNING+"[!] Ingrese el comando de forma correcta"+libStyles.styles.END)

	#si no se accede con comando where
	else:

		#si se ingreso ruta
		if _pat_route.search(comando):
			#asignamos ruta de trabajo
			os.chdir(_ruta[0])

			for i in _list_names:
				#validamos que el archivo exista en la ruta especificada
				if (str(i)+'.txt' in os.listdir(_ruta[0])):
					#eliminamos el archivo
					os.remove(str(i)+'.txt')

					print("[!] Archivo eliminado con exito")

				else:
					print(libStyles.styles.WARNING+"[!] El archivo no se encuentra en la ruta especificada"+libStyles.styles.END)

			#devolvemos a la ruta actual
			os.chdir(_ruta_actual)

		#si no se ingreso ruta
		else:

			for i in _list_names:
				#validamos que el archivo exista en la ruta actual
				if (str(i)+'.txt' in os.listdir(_ruta_actual)):
					#eliminamos el archivo
					os.remove(str(i)+'.txt')

					print("[!] Archivo eliminado con exito")

				else:
					print(libStyles.styles.WARNING+"[!] El archivo no se encuentra en la ruta actual"+libStyles.styles.END)


#---------------------------------------------------------------------------------------------------------------------

#COMANDO find
#
#	<find> ::= "find" ("exact" | "some" ) <string>
#	casos.
#		>>> find exact esta frase exacta
#		>>> find some estas palabras sueltas
#

def _find_(comando):

	#separamos el comando
	_comando = re.split(r"\s",comando)

	#ingresamos a cada caso
	if _comando[1] == "exact":
		#obtenemos la frase
		_string_aux = libAux.search_sentence(_comando)

		#creamos un patron con la frase (El patron no distingue entre mayusculas y minusculas)
		_pat_aux = re.compile(r''+_string_aux, re.IGNORECASE)

		#funcion que busca el patron en los archivos del directorio de trabajo
		libAux.search_in_files(_pat_aux,_string_aux)

	elif _comando[1] == "some":
		#obtenemos las palabras
		_string_aux = libAux.search_words(_comando)

		#creamos un patron con las palabras (El patron no distingue entre mayusculas y minusculas)
		_pat_aux = re.compile(r''+_string_aux, re.IGNORECASE)

		#funcion que busca el patron en los archivos del directorio de trabajo
		libAux.search_in_files(_pat_aux,_string_aux)

	else:
		print(libStyles.styles.WARNING+"[!] Ingrese el comando de forma correcta"+libStyles.styles.END)
