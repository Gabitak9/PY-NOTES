TAREA 4 / LENGUAJES DE PROGRAMACIÓN / 2016-2
========================================

INTEGRANTES
-------------
- **Gabriela Sepúlveda Bravo**
	- **Usuario DI**: gsepulve
	- **Rol**: 201573012-1
- **Harold Melo Montani** 
	- **Usuario DI**: hmelo
	- **Rol**: 201573098-9

CONSIDERACIONES DE LA TAREA: py-notes.py
------------------
- El usuario sabe utilizar de forma correcta los comandos. De todas manera si el comando es mal ejecutado, el programa avisará al usuario o en su defecto, no realizará ninguna acción.
- La tarea contiene una carpeta llamada `notes`, en donde se pueden encontrar varias notas de prueba. Si bien todas las notas fueron agrupadas ahí, el programa no las guarda por defecto en ese directorio, si no que en el directorio indicado con el comando 'dir'.

SUPUESTOS
------------------
- Para evitar situaciones contradictorias con el nombre de las notas, es que se pide al usuario que cuando quiera ingresar el nombre de una, lo haga con **comillas simples**. Se asume que el usuario siempre ingresará los nombres de forma correcta.
Ej.
```
#(forma incorrecta)
>>> create nota 1 nota 2
#(forma correcta)
>>> create 'nota 1' 'nota 2'
```
*De esta forma evitamos situaciones contradictorias como que en el primer caso el programa no sepa si el usuario quiere 4 notas o tal vez 3 (nota 1, nota y 2), y así ...*

- De igual forma, las rutas deben ser ingresadas con su respectiva barra invertida inicial.
```
#(esto es una ruta)
/home/usuario
#(esto no es una ruta)
estonoes/unaruta
```
*De todas formas, gracias a una función proporcionada por el modulo os, es que podemos validar si la ruta ingresada es válida o no*

ESTRUCTURA DE LA TAREA Y ESTRATEGIA SEGUIDA
------------------
**Estructura**
```
tarea4LP-2016-2-gsepulve-hmelo/
	|-----README.md
	|-----py-notes.py
	|-----libs/
		|-----__init__.py
		|-----libCommands.py
		|-----libAux.py
		|-----libStyles.py
	|-----notes/ 			#notas de prueba
```

El paquete `libs/` contiene los módulos necesarios para ejecutar  `py-notes`. En cada uno de ellos está la documentacion necesaria para entenderlos, pero a modo de resumen:
-  `libCommands.py`: módulo que contiene las funciones asociadas a cada comando del lenguaje del programa. Aqui se incluyen los patrones utilizados.
-  `libAux.py`: módulo que contiene funciones auxiliares que utiliza el modulo libCommands.py.
-  `libStyles.py`: módulo que contiene las clases necesarias tanto para interpretar las etiquetas de los estilos, como para poder imprimir estos por pantalla.

**Estrategia**
- Básicamente se hace uso del **modulo re** para encontrar el comando ingresado y las distintas opciones dentro de él. Cada comando está subdivido en los distintos sub-casos posibles que puede ingresar el usuario, a los cuales el programa ingresa mediante condicionales y patrones encontrados.
- Se crearon patrones tanto para encontrar las distintas opciones, como para obtener de ellas los nombres de notas, tags, rutas o palabras a buscar.
- Con el **modulo os** es que manejamos el directorio y la eliminacion de archivos.

MODO DE EDICIÓN Y ESTILOS
------------------
- El programa hace uso del editor de textos `gedit` para editar las notas. SI el usuario desea crear notas con estilos, deberá utilizar las siguientes etiquetas:

|ESTILO|ETIQUETA|
|:---:|:---:|
|color rojo| `<red>texto rojo</>`
|color verde| `<green>texto verde</>`
|color amarillo| `<yellow>texto amarillo</>`
|color azul| `<blue>texto azul</>`
|color cyan| `<cyan>texto cyan</>` 
|negrita| `<bold>texto negrita</>`
|cursiva| `<cursive>texto cursiva</>`
|subrayado| `<underline>texto subrayado</>`

- Cabe destacar que si bien se pueden utilizar cuantas etiquetas distintas desee en una nota, **NO** puede combinarlas entre si. Ej. Lo siguiente no es posible  `<bold><red> texto no compatible </></>`  *(escribir algo en negrita y rojo al mismo tiempo)*

PROBANDO py-notes
------------------
- Para clonar el repositorio
```
git clone https://gitlab.labcomp.cl/gsepulve/tarea4LP-2016-2-hmelo-gsepulve
```

- Para iniciar py-notes
```
python py-notes.py
```
- Programa:
```
[Gabitak9@gabitak9 tarea4LP-2016-2-hmelo-gsepulve]$ python py-notes.py 
-----------------------------------------------
|------------Bienvenido a Py-notes------------|
-----------------------------------------------
Py-notes es un programa para gestionar notas.
Para entender el uso de cada comando porfavor leer enunciado documentacion en libCommands.py
	Comandos del programa:
	- dir
	- create
	- show
	- edit
	- delete
	- find
	- exit
Directorio actual: /home/Gabitak9/Documentos/INF253/Tareas/tarea4LP-2016-2-hmelo-gsepulve, el cual contiene 10 nota(s)
>>> create 'Prueba' edit with tags tag1 tag2
[!] NOMBRE(s) DE ARCHIVO(s): Prueba
[!] NOMBRE(s) DE TAG(s): tag1 tag2
[!] RUTA A GUARDAR: /home/Gabitak9/Documentos/INF253/Tareas/tarea4LP-2016-2-hmelo-gsepulve
[!] MODO DE EDICION: True
[!] 1 archivo(s) fue(ron) creado(s) con exito
>>> 
```