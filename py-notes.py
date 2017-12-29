#!/usr/bin/python
#
#	TAREA 4: py-notes
#	Lenguajes de Programacion / 2016-2
#	Integrantes: hmelo - gsepulve
#
#	ARCHIVO MAIN
#	main del programa
#
#---------------------------------------------------------------------------------------------------------------------

#MODULOS NECESARIOS

import re
import os
import sys
from libs import libCommands
from libs import libAux
from libs import libStyles

#---------------------------------------------------------------------------------------------------------------------

#MAIN DEL PROGRAMA

print("-----------------------------------------------")
print("|------------Bienvenido a Py-notes------------|")
print("-----------------------------------------------")
print("")
print("Py-notes es un programa para gestionar notas.\nPara entender el uso de cada comando porfavor leer README.md")
print("")
print("\tComandos del programa:\n\t- dir\n\t- create\n\t- show\n\t- edit\n\t- delete\n\t- find\n\t- exit")
print("")
print("Directorio actual: "+str(os.getcwd())+", el cual contiene "+str(libAux.total_notes())+" nota(s)")

while True:

	comando = raw_input(">>> ")

	#Salir del programa
	if  re.match(r"exit",comando):
		sys.exit()

	#Comandos del programa
	elif re.match(r"dir",comando):
		libCommands._dir_(comando)
	elif re.match(r"create",comando):
		libCommands._create_(comando)
	elif re.match(r"show",comando):
		libCommands._show_(comando)
	elif re.match(r"edit",comando):
		libCommands._edit_(comando)
	elif re.match(r"delete",comando):
		libCommands._delete_(comando)
	elif re.match(r"find",comando):
		libCommands._find_(comando)
	else:
		print(libStyles.styles.WARNING+"[!] Comando invalido"+libStyles.styles.END)