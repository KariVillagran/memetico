from nsga2func import Solucion
from nsga2func import NSGA2
import random
import numpy as np
import matplotlib.pyplot as plt
import sys

global matrixDistancia, matrixFlujoUno, matrixFlujoDos
global numFac
matrixDistancia = []
matrixFlujoUno = []
matrixFlujoDos = []



def lectura():
	#archivo = raw_input("Ingrese nombre archivo: ")
	archivo = sys.argv[1]
	instancias = open(archivo, 'r')
	arreglo = []
	tamano = instancias.readline()
	arreglo.append(tamano)
	for line in instancias:
		for caract in line.split(' '):
			if caract == "":
				pass
			elif caract == "\n":
				pass
			else:
				num = caract
				arreglo.append(int(num))
	return arreglo

#DISTRIBUCION EN MATRICES DE FLUJO Y DISTANCIA, UTILES	
def distribuirMatrices(arreglo):
	numFac = int(arreglo[0])
	largoArray = len(arreglo)
	distribucion = numFac*numFac
	rangoMatrizD = distribucion
	rangoMatrizFU = distribucion*2
	rangoMatrizFD = distribucion*3
	for i in range(1,largoArray):
		if (0 < i and i <= rangoMatrizD):
			matrixDistancia.append(arreglo[i])
		elif (rangoMatrizD < i and i <= rangoMatrizFU):
			matrixFlujoUno.append(arreglo[i])
		elif (rangoMatrizFU < i and i <= rangoMatrizFD):
			matrixFlujoDos.append(arreglo[i])
		else:
			pass
	return numFac
#UTILES
def imprimeMatriz(arreglo):
	largo = len(arreglo)
	ancho = int(math.sqrt(largo))
	for i in range(ancho):
		for j in range(ancho):
			print arreglo[i*ancho+j],
			print " ",
		print "\n"

#ALGORITMO		
def generarSolucionRandom(sol, numFac):
	vectorObjetos = []
	vectorLocalidades = []
	for x in range(numFac):
		vectorObjetos.append(x)
		vectorLocalidades.append(x)
	while len(vectorObjetos) > 0:
		obj = random.choice(vectorObjetos)
		loc = random.choice(vectorLocalidades)
		sol.solution.insert(obj, loc)
		vectorObjetos.pop(vectorObjetos.index(obj)), vectorLocalidades.pop(vectorLocalidades.index(loc))
	return sol

#ALGORITMO
def crearPoblacion(poblacion, tamPoblacion, numFac):
	print "Creando poblacion inicial . . ."
	for x in range(tamPoblacion):
		if(x==0):
			solux = Solucion(numFac)
			generarSolucionRandom(solux, numFac)
			poblacion.append(solux)
		else:
			solux = Solucion(numFac)
			generarSolucionRandom(solux, numFac)
			while (solux in poblacion):
				generarSolucionRandom(solux, numFac)
			poblacion.append(solux)
	return poblacion
#ALGORITMO
def dominance(sol, otherSol):
	sF1 = sol.costoFlujo[0]
	sF2 = sol.costoFlujo[1]
	oF1 = otherSol.costoFlujo[0]
	oF2 = otherSol.costoFlujo[1]
	a,b = sF1 < oF1, sF2 < oF2
	c,d = sF1 <= oF1, sF2 <= oF2
	if (c and d) and (a or b):
		#print True
		return True
	else:
		#print False
		return False
#ALGORITMO
def strongDominance(sol, otherSol):
	sF1 = sol.costoFlujo[0]
	sF2 = sol.costoFlujo[1]
	oF1 = otherSol.costoFlujo[0]
	oF2 = otherSol.costoFlujo[1]
	a,b = sF1 < oF1, sF2 < oF2
	if(a and b):
		return True
	else:
		return False


def generarTodoVecindario(sol):
	raise "Not implemented yet"

def generarVecino(sol):
	numFac = sol.numFacilities
	posicionUno = random.randint(0,numFac-1)
	posicionDos = random.randint(0,numFac-1)
	while posicionUno == posicionDos:
		posicionDos = random.randint(0,numFac-1)
	#print "posiciones: ", 
	#print posicionUno, 
	#print posicionDos
	elementoPosUno = sol.solution[posicionUno]
	elementoPosDos = sol.solution[posicionDos]
	a, b = sol.solution.index(elementoPosUno), sol.solution.index(elementoPosDos)
	sol.solution[b], sol.solution[a] = sol.solution[a], sol.solution[b]
	#print "Solucion con cambio: ", 
	#print sol.solution
	return sol



def graficarPob(poblacion):
	listaSolC1, listaSolC2 = [], []
	for elem in poblacion:
		if elem.rank == 1:
			#elem.costoAsignacion()
			listaSolC1.append(elem.costoFlujo[0])
			listaSolC2.append(elem.costoFlujo[1])
	plt.plot(listaSolC1, listaSolC2, 'ro')
	plt.ylabel('Costo Flujo 2')
	plt.xlabel('Costo Flujo 1')
	plt.show()
	return 1

