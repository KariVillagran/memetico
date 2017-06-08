#%matplotlib inline

from PyGMO import *
from PyGMO.problem import base
from PyGMO import algorithm, island
from PyGMO import population
from math import sqrt

import matplotlib.pyplot as plt 
import numpy as np
import os
import csv

class multi_qap (base):

	def __init__(self, dim=10):
		#Constructor para la clase base, diciendo que clase de problema se trata
		super(multi_qap, self).__init__(dim)

		self.set_bounds(-5.12, 5.12)

	def _objfun_impl(self, x):
		f = sum([x[i] ** 2 for i in range(self.dimension)])

		return (f,)

	def human_readble_extra(self):	
		return "\n\t Problem dimension: " + str(self.__dim)


class problem_max(base):
	def __init__(self):
		super(problem_max, self).__init__(2)
		self.set_bounds(-10,10)
		self.best_x = [[1.0, -1.0], ]

	def _objfun_impl(self, x):
		f = -(1.0 - x[0])**2-100*(-x[0]**2 - x[1]) **2 -1.0
		return (f, )
	def _compare(self, f1,f2):
		return f1[0] > f2[0]

	def human_readble_extra(self):
		return "\n\t Maximization problem"

#Definicion de mo-problem. En este caso es necesario sobrecargar el constructor base con un tercer argumento, en donde se debe
#declarar la dimension de la funcion objetivo y luego retornar una tupla con mas de un elemento. 

class mo_problem(base):
	def __init__(self, dim=2):
		#Llamada al constructor base
		super(mo_problem, self).__init__(dim, 0, 2)
		self.set_bounds(0.0, 1.0)

	#Se reimplementa el metodo virtual que define la funcion objetivo	
	def _objfun_impl(self, x):
		f0 = x[0]
		g = 1.0 + 4.5 * x[1]
		f1 = g* (1.0 - sqrt(f0 / g))
		return (f0, f1, )

	def human_readble_extra(self):
		return "\n\t Multi-objective problem"


def obtainResults(carpetas, dirs):
	print dirs
	#print carpetas
	#carpetas.sort()
	allTimes = []
	#Este for va desde 0 hasta el largo de carpetas, que en este caso es 25. 
	for i in range(len(carpetas)):
		#print carpetas[i]
		metodo = dirs + "/resultsMem" + str(i)
		print metodo
		subcarp = os.listdir(metodo)
		cantCarp = len(subcarp)
		#print cantCarp
		tiempos = []
		for j in range(len(subcarp)):
			path = ""
			path = metodo + "/" + subcarp[j] + "/" + "generaciones.csv"
			try:
				with open(path) as file:
					lines = file.readline()
					time = lines.strip().split(":")
					#print time
					mins = 60*float(time[2])
					secs = float(time[3])
					total = mins + secs
					tiempos.append(total)
					#print "Se demoro : ", total, "segundos"
					#print times
			except IOError as exc:
				if exc.errno != errno.EISDIR:
					raise
		allTimes.append(tiempos)
	return allTimes	
	
def writeTimes(allTimes):
	listInstance = []
	meanSTD = []
	fin = []
	inst = "Mem"
	for i in range(len(allTimes)):
		instance = inst + str(i)
		print instance
		arreglo = np.array(allTimes[i])
		mean = np.mean(arreglo)
		std = np.std(arreglo)
		value = str(mean) + " (" + str(std) + ")"
		print value
		listInstance.append(instance)
		meanSTD.append(value)

	file = open('tiempos.csv', "wt")
	writer = csv.writer(file, delimiter = ' ')	
	for i in range(len(listInstance)):
		writer.writerow( (listInstance[i], meanSTD[i]) )
	#writer.writerow(listInstance)
	#writer.writerow(meanSTD)


if __name__ == "__main__":
	cwd = os.getcwd()
	carpeta = "/ResultsNSGA2"
	directory = cwd + carpeta
	resultsMems = os.listdir(directory)

	results = obtainResults(resultsMems, directory)
	writeTimes(results)	


















#prob = problem.zdt(1)
#pop = population(prob, 100)
#pop.compute_pareto_fronts()
#pop.plot_pareto_fronts()

#PAra mo_problem(base)
#prob = mo_problem()
#algo = algorithm.sms_emoa(gen = 2)
#pop = population(prob, 30)
#pop = algo.evolve(pop)

#F = np.array([ind.cur_f for ind in pop]).T
#plt.scatter(F[0], F[1])
#plt.xlabel("$f^{(1)}$")
#plt.ylabel("$f^{(2)}$")
#plt.show()

#Utilizado para problem_max(base)

#prob = problem_max()
#algo = algorithm.de(gen=20)
#isl = island(algo, prob, 20)
#isl.evolve(10)
#isl.join()

#print("Mejor individuo: ")
#print(isl.population.champion)

#print("Comparacion entre el mejor invididuo encontrado con la mejor fitness conocida: ")
#for best in prob.best_f:
#	print(best[0] - isl.population.champion.f[0])
#
#print("L2 distance to the best decision vector: ")
#for best in prob.best_x:
#	l2 = 0
#	for n in range(0, len(best)):
#		l2 += (best[n]  - isl.population.champion.x[n]) **2
#	l2 = sqrt(l2)
#	print (l2)

#best_f and best_x son metodos que retornan el mejor valor conocido de fitness y el vector de decision. 



#PAra clase multi_qap
#prob = multi_qap(dim = 10) #Creo un problema con dimension 10
#algo = algorithm.bee_colony(gen=500)
#isl = island(algo, prob, 20) #20 individuos por isla
#isl.evolve(1)
#isl.join()
#print(isl.population.champion.f)


