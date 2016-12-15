import funciones
from nsga2func import Solucion
from nsga2func import NSGA2
import nsga2func
import math
import time, sys, random
from random import randint
import numpy as np
import matplotlib.pyplot as plt

global matrixDistancia, matrixFlujoUno, matrixFlujoDos
global numFac
matrixDistancia = []
matrixFlujoUno = []
matrixFlujoDos = []


def main():
	
	numFac = funciones.distribuirMatrices(funciones.lectura())
	start = time.time()
	nsga2 = NSGA2(2, 0.1, 1.0)
	P = []
	pob = funciones.crearPoblacion(P,5, numFac)
	front = nsga2.fastNonDominatedSort(P)
	for elem in pob:
		print "Solucion s: ", 
		print elem.solution
		elem.costoAsignacion()
		sol1 = nsga2func.swap(elem, 2, 3)
		sol2 = nsga2func.swap(sol1, 3, 2)
		print "hola"
		print sol2.solution
		sol2.costoAsignacionMovida(2,3)
		sol2.costoAsignacion()

		break
		

	#for fron in front:
	#	nsga2.crowdingDistanceAssignment(fron)

	#nsga2.sortCrowding(P)

	#pob = nsga2.runAlgorithm(P,200,300)
	end = time.time()
	print "T =", end-start
	#funciones.graficarPob(pob)
	


if __name__ == '__main__':
	main()

