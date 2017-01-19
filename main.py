# -*- coding: utf-8 -*-
import funciones
from nsga2func import Solucion
from nsga2func import NSGA2
import nsga2func
import math
import time, sys, random, datetime
from random import randint
from itertools import cycle
#import numpy as np
#import matplotlib.pyplot as plt

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
	funciones.crearPoblacion(P,50, numFac)
	front = nsga2.fastNonDominatedSort(P)
	P = nsga2.sortRanking(P)

	#print "Solucion : ", P[0].solution, P[0].costoFlujo[0], P[0].costoFlujo[1]
	#print "y su vecindario, con alpha = 0.3"
	#nsga2.generarAlphaVecinos(P[0], 0.6)

	nsga2.runAlgorithm(P,50,5, start)






if __name__ == '__main__':
	main()


