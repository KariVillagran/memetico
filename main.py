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
	seed = sys.argv[2]
	random.seed(seed)
	numFac = funciones.distribuirMatrices(funciones.lectura())
	start = datetime.datetime.now()
	nsga2 = NSGA2(2, 0.1, 1.0)
	P = []
	funciones.crearPoblacion(P,100, numFac)
	
	
	for elemento in P:
		elemento.costoAsignacion()
	fronteras= nsga2.fastNonDominatedSort(P)
	P = nsga2.ordenPostBusqueda(P, fronteras,100)





	#print "Trabajo escrito de tesis"


	#Cada parametro es: 
	#tamanio Pob, indiceCX (1=cycleCX, 2=OnepointCX), indiceMUT (3opt), numEvaluaciones

	numEvalua = 3000000
	
	nsga2.runAlgorithm(P,100, 1, start, numEvalua)

	#a = [i for i in range(numFac)]


if __name__ == '__main__':
	main()


