# -*- coding: utf-8 -*-
import sys
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
	
	#Read parameters
	data = funciones.readParameters()
	#print data

	algorithm = data[0]
	cxOp = data[1]
	mutOp = data[2]
	cxRate = float(data[3])
	mutRate = float(data[4])
	tamPob = int(data[5])
	finishStrat = data[6]
	finishLimit = int(data[7])
	k = int(data[8])
	limitSearch = float(data[9])
	init = data[10]

	seed = sys.argv[3]
	random.seed(seed)

	start = datetime.datetime.now()
	nsga2 = NSGA2(2, mutRate, cxRate)
	P = []
	funciones.crearPoblacion(P,tamPob, numFac)
	
	
	for elemento in P:
		elemento.costoAsignacion()
	fronteras= nsga2.fastNonDominatedSort(P)
	P = nsga2.ordenPostBusqueda(P, fronteras, tamPob)

	#print "Trabajo escrito de tesis"

	#Cada parametro es: 
	#tamanio Pob, indiceCX (1=cycleCX, 2=OnepointCX), indiceMUT (3opt), numEvaluaciones
	numEvalua = 3000000
	nsga2.runAlgorithm(algorithm, P, tamPob, 1, k ,limitSearch, start, finishLimit)

	#a = [i for i in range(numFac)]


if __name__ == '__main__':
	main()


