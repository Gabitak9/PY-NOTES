#!/usr/bin/python
#
#	TAREA 4: py-notes
#	Lenguajes de Programacion / 2016-2
#	Integrantes: hmelo - gsepulve
#
#	MODULO DE ESTILOS
#	este modulo es creado a partir de la informacion obtenida en 
#	http://misc.flogisoft.com/bash/tip_colors_and_formatting
#	
#	en el modo edicion el usuario debera utilizar las etiquetas 
#	mostradas en los comentarios. LAS ETIQUETAS NO PUEDEN COMBI-
#	NARSE ENTRE SI.
#
#---------------------------------------------------------------------------------------------------------------------

import re

#Clase de estilos

class styles:
	RED = "\033[31m"		#color rojo			etiqueta en modo edicion: <red> texto aqui </>
	GREEN = "\033[32m" 		#color verde		etiqueta en modo edicion: <green> texto aqui </>
	YELLOW = "\033[33m"		#color amarillo		etiqueta en modo edicion: <yellow> texto aqui </>
	BLUE = "\033[34m"		#color azul			etiqueta en modo edicion: <blue> texto aqui </>
	CYAN = "\033[36m"		#color cyan 		etiqueta en modo edicion: <cyan> texto aqui </>
	BOLD = "\033[1m"		#letra negrita 		etiqueta en modo edicion: <bold> texto aqui </>
	CURSIVE = "\033[3m"		#letra cursiva		etiqueta en modo edicion: <cursive> texto aqui </>
	UNDERLINE = "\033[4m"	#letra subrayada	etiqueta en modo edicion: <underline> texto aqui </>
	HIGHLIGHT = "\033[7m"	#letra resaltada
	WARNING = "\033[41m"	#letra para mensajes
	OK = "\033[44m"			#letra ok
	END = "\033[0m"			#cierre
 
#---------------------------------------------------------------------------------------------------------------------

#Clase de patrones de estilos

class pat_styles:
	RED = re.compile(r"\<red\>")
	GREEN = re.compile(r"\<green\>")
	YELLOW = re.compile(r"\<yellow\>")
	BLUE = re.compile(r"\<blue\>")
	CYAN = re.compile(r"\<cyan\>")
	BOLD = re.compile(r"\<bold\>")
	CURSIVE = re.compile(r"\<cursive\>")
	UNDERLINE = re.compile(r"\<underline\>")
	END = re.compile(r"\<\/\>")