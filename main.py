# -*- coding: utf-8 -*-
import funciones
from nsga2func import Solucion
from nsga2func import NSGA2
import nsga2func
import math
import time, sys, random, datetime
from random import randint
from itertools import cycle
#from PyGMO import *

#import numpy as np
import matplotlib.pyplot as plt

global matrixDistancia, matrixFlujoUno, matrixFlujoDos
global numFac
matrixDistancia = []
matrixFlujoUno = []
matrixFlujoDos = []


def main():

	numFac = funciones.distribuirMatrices(funciones.lectura())
	start = datetime.datetime.now()
	nsga2 = NSGA2(2, 0.1, 1.0)
	P = []
	funciones.crearPoblacion(P,100, numFac)
	#for elemento in P:
	#	elemento.costoAsignacion()
	fronteras= nsga2.fastNonDominatedSort(P)
	P = nsga2.ordenPostBusqueda(P, fronteras, 100)
	#for front in fronteras:
	#	nsga2.crowdingDistanceAssignment(front)
	#nsga2.sortCrowding(P)
	#P = nsga2.ordenPostBusqueda(P, front, 75)
		
	#for elemento in P:
	#	print elemento.solution, elemento.costoFlujo[0], elemento.costoFlujo[1], elemento.rank

	#newPob = nsga2.makeNewPob(P, 1, 1, 75)
	#fronteras = nsga2.fastNonDominatedSort(newPob)
	#for front in fronteras:
	#	nsga2.crowdingDistanceAssignment(front)
	#nsga2.sortCrowding(newPob)

	#for elemento in newPob:
	#	print elemento.solution, elemento.costoFlujo[0], elemento.costoFlujo[1], elemento.rank, elemento.crowdedDistance
	#print "memorybased"
	#ls = nsga2.memoryBasedPLS(newPob, 75)

	#P = nsga2.sortRanking(P)

	#for elemento in P:
	#	print elemento.solution


	#print "Trabajo escrito de tesis"

	#nsga2.createNewPob(P, 1, 2, 0.2)
	#print "Solucion : ", P[0].solution, P[0].costoFlujo[0], P[0].costoFlujo[1]
	#print "y su vecindario, con alpha = 0.3"
	#nsga2.generarAlphaVecinos(P[0], 0.6)
	#Cada parametro es: 
	#tamanio Pob, GENERACIONES, ALPHA(VECINOS A GENERAR), indiceCX (1=Seq, 2=Onepoint), indiceMUT (1=2opt, 2=3opt)
	
	nsga2.runAlgorithm(P,100, 5, 0.35, 2, 2, start)






if __name__ == '__main__':
	main()


