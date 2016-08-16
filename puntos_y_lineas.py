#!/usr/bin/python
# -*- coding: utf-8 -*-
import turtle
import re  

#variable globales
cuadros = {} #acá estarán los datos de cada cuadro del tablero
aristas = {} #acá estarán todas las aristas del tablero referenciadas al cuadro que corresponden
trazo = 0
jugadorActivo = 1
jugadores = {}
jugadores[1] = {}
jugadores[2] = {}
jugadores[1]['id'] = 1
jugadores[2]['id'] = 2
jugadores[1]['color'] = "red"
jugadores[2]['color'] = "blue"
turtle

# Retorna la fila de la matriz a la que corresponde un cuadro
# Parametro (x): corresponde al indice del cuadrado
def switch(x):
	y = 0
	if  x < 9:
		y = 1
	elif x < 18:
		y = 2
	elif x < 27:
		y = 3
	elif x < 36:
		y = 4
	elif x < 45:
		y = 5
	elif x < 54:
		y = 6
	elif x < 63:
		y = 7
	elif x < 72:
		y = 8
	elif x < 81:
		y = 9

	return y

# Retorna las coordenadas de todas las aristas de un cuadro
# Parametro (y): corresponde al columna del cuadrado
# Pareametro (x): corresponde a la fila en que se encuentra el cuadrado
def nueva_coordenada(y, x):
	a1 = x
	a2 = y
	a3 = x 
	a4 = y + 1
	b1 = x
	b2 = y + 1
	b3 = x + 1
	b4 = y + 1
	c1 = x + 1
	c2 = y
	c3 = x + 1
	c4 = y + 1
	d1 = x
	d2 = y
	d3 = x + 1
	d4 = y
	ai = str(a1) + "," + str(a2)
	ad = str(a3) + "," + str(a4)
	bi = str(b1) + "," + str(b2)
	bd = str(b3) + "," + str(b4)
	ci = str(c1) + "," + str(c2)
	cd = str(c3) + "," + str(c4)
	di = str(d1) + "," + str(d2)
	dd = str(d3) + "," + str(d4)

	return ai, ad, bi, bd, ci, cd, di, dd

# Crea la estructura del juego, un direccionario que contiene: Nº Cuadrado y sus 4 aristas
# También crea un diccionario de aristas que contiene: 'estado' (para saber si está marcada) y 'padre' para verificar a que cuadrados corresponde
# Parametro (ancho), (altura): utilizados para calcular la cantidad de cuadros del tablero
def crea_estructura(ancho, altura):
	global cuadros, aristas
	x = 0
	y = 0 
	aux = 0 # lleva el indice de la columna
	totalCuadros = (ancho-1) * (altura-1)
	for i in range(totalCuadros):
		aux += 1
		cuadros[i] = {}
		cuadros[i]['nombre'] = i
		cuadros[i]['dueno'] = 0
		x = switch(i)
		cuadros[i]['marcadas'] = 0
		cuadros[i]['aristas'] = {}
		cuadros[i]['aristas']['a'] = {}
		cuadros[i]['aristas']['b'] = {}
		cuadros[i]['aristas']['c'] = {}
		cuadros[i]['aristas']['d'] = {}
		cuadros[i]['aristas']['a'][1], cuadros[i]['aristas']['a'][2], cuadros[i]['aristas']['b'][1], cuadros[i]['aristas']['b'][2], cuadros[i]['aristas']['c'][1], cuadros[i]['aristas']['c'][2], cuadros[i]['aristas']['d'][1], cuadros[i]['aristas']['d'][2] = nueva_coordenada(aux, x)
		if aux == 9:
			aux = 0
	for i in cuadros:
		for j in cuadros[i]['aristas']:
			arista = cuadros[i]['aristas'][j][1] + "-" + cuadros[i]['aristas'][j][2]
			if aristas.has_key(arista):
				if not i in aristas[arista]['padres']:
					aristas[arista]['padres'].append(i)
			else:
				aristas[arista] = {}
				aristas[arista]['estado'] = 0
				aristas[arista]['padres'] = []
				aristas[arista]['padres'].append(i)

# Crea la estructura de datos del juego, y además crea el tablero inicial
def dibujar_tablero(distancia, ancho, altura):
	global cuadros, aristas, turtle, trazo
	trazo = distancia
	crea_estructura(ancho, altura)
	turtle.setup(700,700) # Crea el tablero de 700px 700px
	turtle.setworldcoordinates(-10,600,600,-10) # Cambia las coordenadas desde el origen 0,0 (centro) a la esquina superior derecha
	turtle.title("JUEGO: Lineas y Puntos")
	for i in range(1,ancho+1):
		# Imprime los numeros del 1 al 10 de las filas y columnas
		turtle.speed(20)
		turtle.penup()
		turtle.setpos(0, i * distancia+5)
		turtle.pencolor('#6a6a6a')
		turtle.write(i, False, "right", ("arial",16))
		turtle.setpos(i * distancia+5, 0)
		turtle.write(i, False, "right", ("arial",16))
		for j in range(1, ancho+1):
			# Imprime loos puntos de la fila
			turtle.speed(20)
			turtle.penup()
			turtle.pencolor("#585866")
			turtle.setpos(j * distancia, i * distancia)
			turtle.dot(8)
	turtle.home()
	x = turtle.xcor()
	y = turtle.ycor()
	return x, y 

# Pide las coordenadas para jugar
def pedir_cordenadas():
	global jugadorActivo, jugadores
	terminado = 0
	patron = re.compile(r'^\d{1,2}\,\d{1,2}\,[a|d]{1}$')  
	coordenadas = ""
	x = 0
	y = 0
	d = ''
	print ""
	print "TURNO PARA: %s" % (jugadores[jugadorActivo]["nombre"].upper())
	while terminado == 0:
		coordenadas = raw_input("    - Ingrese coordenadas (x,y,direccion): ")
		if not patron.match(coordenadas) == None:
			array_coordenadas = coordenadas.split(",")
			x = int(array_coordenadas[0])
			y = int(array_coordenadas[1])
			d = array_coordenadas[2]
			if (x > 0 and x <= 10) and (y > 0 and y <= 10):
				if not (x == 10 and d == "d"):
					if not (y == 10 and d == "a"):
						terminado = 1
					else:
						print "ERROR: Desde la posicion Y = 10, NO es posible avanzar hacia abajo."
				else:
					print "ERROR: Desde la posicion X = 10, NO es posible avanzar hacia la derecha."
			else:
				print "ERROR: Las coordenadas (X,Y) pueden contener valores entre 1 y 10."
				print "       Usted ingresó (%s, %s)" % (str(x), str(y))
		else:
			print "ERROR: Formato de coordenadas no valido. Coordenadas X,Y,Direccion."
	return x,y,d

# Dada una arista, verifica si ésta completa un cuadrado
def verificar_cuadrado(arista):
	global aristas, cuadros, jugadorActivo, jugadores, trazo
	contador = 0
	pinta_cuadro = 0
	retorno = 1
	for i in range (len(aristas[arista]['padres'])):
		n = aristas[arista]['padres'][i]
		for j in cuadros[n]["aristas"]:
			aristaActual = cuadros[n]["aristas"][j][1] + "-" + cuadros[n]["aristas"][j][2]
			contador = contador + aristas[aristaActual]["estado"]
		if contador == 4:
			cuadros[n]["dueno"] = jugadores[jugadorActivo]["id"]
			pinta_cuadro = 1
			turtle.fillcolor(jugadores[jugadorActivo]["color"])
			turtle.begin_fill()
			for k in ["a", "b", "c", "d"]:
				if ( k== "d" or k == "c"):
					turtle.speed(2)
					coor = cuadros[n]["aristas"][k][2].split(",")
					x = int(coor[0])
					y = int(coor[1])
					turtle.penup()
					turtle.goto(x*trazo, y*trazo)
					coor = cuadros[n]["aristas"][k][1].split(",")
					x = int(coor[0])
					y = int(coor[1])
					turtle.pendown()
					turtle.goto(x*trazo, y*trazo)
				else:
					coor = cuadros[n]["aristas"][k][1].split(",")
					x = int(coor[0])
					y = int(coor[1])
					turtle.penup()
					turtle.goto(x*trazo, y*trazo)
					coor = cuadros[n]["aristas"][k][2].split(",")
					x = int(coor[0])
					y = int(coor[1])
					turtle.pendown()
					turtle.goto(x*trazo, y*trazo)
			turtle.end_fill()
			turtle.fillcolor("black")
			turtle.penup()
			turtle.goto(0, 0)
			turtle.pencolor("black")
		contador = 0
	if pinta_cuadro == 1:
		retorno = 2
	return retorno

# Dibuja una linea y verifica si cierra un cuadrado
def dibujar_linea(xpos, ypos):
	global cuadros, aristas, turtle, trazo, jugadorActivo, jugadores
	estado = 0 #0: arista ya ocupada | 1: arista marcada
	x2 = 0
	y2 = 0
	while estado == 0:
		x1,y1,d = pedir_cordenadas()
		if d == 'd':
			x2 = x1 + 1
			y2 = y1
			arista = str(x1) + "," + str(y1) + "-" + str(x2) + "," + str(y2)
		elif d == 'a':
			x2 = x1 
			y2 = y1 + 1
			arista = str(x1) + "," + str(y1) + "-" + str(x2) + "," + str(y2)
		else:
			print "ERROR: Ocurrio un error inesperado."
		if aristas[arista]['estado'] == 0:
			aristas[arista]['estado'] = 1
			turtle.penup()
			turtle.speed(3)
			turtle.goto(x1*trazo,y1*trazo)
			turtle.pencolor("black")
			turtle.pendown()
			turtle.pensize(3)
			turtle.goto(x2*trazo,y2*trazo)
			turtle.penup()
			turtle.goto(0,0)
			estado = verificar_cuadrado(arista)
		else:
			print "ERROR: La linea que ingresaste, ya se encuentra marcada. Intenta nuevamente"
	return estado

# Realiza un resumen de la partida
def resumen_partida():
	global cuadros, aristas, jugadores, jugadorActivo
	cuadros_jugador1 = 0
	cuadros_jugador2 = 0
	total_cuadros = 0
	cuadros_disponibles = 0
	total_aristas = 0
	total_ocupadas = 0
	aristas_disponibles = 0
	fin = 0
	ganador = 0
	for i in cuadros:
		total_cuadros += 1
		if cuadros[i]["dueno"] == 1:
			cuadros_jugador1 += 1
		elif cuadros[i]["dueno"] == 2:
			cuadros_jugador2 += 1

	cuadros_disponibles = total_cuadros - (cuadros_jugador1 + cuadros_jugador2)
	print " -------------------------------------------------------"
	print "|  RESUMEN CUADROS :\t\t\t\t\t|"
	print "|  %s: %s \t\t\t\t\t\t|" % (jugadores[1]["nombre"].upper(), str(cuadros_jugador1))
	print "|  %s: %s \t\t\t\t\t\t|" % (jugadores[2]["nombre"].upper(), str(cuadros_jugador2))
	print "|  DISPONIBLES PARA CERRAR: %s\t\t\t\t|" % (str(cuadros_disponibles))
	for j in aristas:
		total_aristas += 1
		if aristas[j]["estado"] == 1:
			total_ocupadas += 1
	aristas_disponibles = total_aristas - total_ocupadas
	print "|  LINEAS MARCADAS: %s | LINEAS DISPONIBLES: %s\t\t|" % (str(total_ocupadas), str(aristas_disponibles) )
	print " -------------------------------------------------------"
	if cuadros_disponibles == 0:
		fin = 1
	if cuadros_jugador1 > cuadros_jugador2:
		ganador = 1
	elif cuadros_jugador1 < cuadros_jugador2:
		ganador = 2
	return fin, ganador

# Lleva el control de las partidas y de los turnos
def control_partida(xpos, ypos):
	global turtle, jugadorActivo, jugadores
	jugadores[1]["nombre"] = raw_input("Ingrese el nombre del jugador Nro 1: ")
	jugadores[2]["nombre"] = raw_input("Ingrese el nombre del jugador Nro 2: ")
	juegoTerminado = 0 # 0: el juego continúa, 1: juego terminado
	ganador = 0
	print ""
	print " NOTA: El ingreso de coordenadas se hace en el formato:"
	print "       CoordenadaX,CoordenadaY,Direccion (d:derecha|a:abajo)"
	print "       EJ: 7,2,a"
	print ""
	
	while juegoTerminado == 0:
		estado = dibujar_linea(xpos, ypos)
		if (estado == 1 and jugadorActivo == 1):
			jugadorActivo = 2
		elif (estado == 1 and jugadorActivo == 2):
			jugadorActivo = 1
		elif estado == 2:
			print "COMPLETASTE UN CUADRO, TIENES UN TURNO EXTRA"
		else:
			print "ERROR: Ocurrio un error inesperado."
		juegoTerminado, ganador = resumen_partida()
	if not ganador == 0:
		print ""
		print ""
		print "¡EL GANADOR ES: %s!" % (jugadores[ganador]["nombre"])
	else:
		print "EMPATE..."

# Funcion principal
def main():
	global turtle
	print "BIENVENIDO AL JUEGO PUNTOS Y LINEAS"
	xpos, ypos = dibujar_tablero(50,10,10)
	control_partida(xpos, ypos)
	print "JUEGO TERMINADO"
	turtle.done()

main()


