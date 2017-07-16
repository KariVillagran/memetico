# -*- coding: utf-8 -*-
import sys
from funciones import Parametros
from nsga2func import Solucion
from nsga2func import NSGA2
import funciones
import nsga2func
import math
import time, sys, random, datetime
from random import randint
from itertools import cycle

global matrixDistancia, matrixFlujoUno, matrixFlujoDos
global numFac
matrixDistancia, matrixFlujoUno, matrixFlujoDos = [], [], []


def main():
	numFac = funciones.distribuirMatrices(funciones.lectura())
	
	instancia = sys.argv[1]
	#Read parameters
	data = funciones.readParameters()
	params = Parametros(data)
	#Get Seed
	seed = sys.argv[3]
	random.seed(seed)
	#Set Time
	direct = sys.argv[4]

	start = datetime.datetime.now()
	#Create NSGA2
	nsga2 = NSGA2(2, params.mutRate, params.cxRate)

	P = []
	P = funciones.crearPoblacion(P, params.tamPob, numFac)

	#print "Trabajo escrito de tesis"
	
	
	#Runnning Algorithm
	if params.init == "True":
		initPobla = nsga2.initAlgorithm(P, params.tamPob)
		nsga2.runAlgorithm(params.algorithm, initPobla, params.tamPob, params.cxOp , params.k , params.limitSearch, start, params.finishLimit, params.evalPerGen, params.pobStrategy, params.searchStrategy, instancia, direct)	
	else:
		nsga2.runAlgorithm(params.algorithm, P, params.tamPob, params.cxOp , params.k , params.limitSearch, start, params.finishLimit, params.evalPerGen, params.pobStrategy, params.searchStrategy, instancia, direct)
	
#a = [i for i in range(numFac)]
if __name__ == '__main__':
	main()


