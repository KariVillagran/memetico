# -*- coding: utf-8 -*-
import glob
import os
import errno
from hv import HyperVolume
import matplotlib.pyplot as plt
import funciones
from nsga2func import Solucion
from nsga2func import NSGA2



class Metrics:

	def __init__(self, directorio):
		#nombre del directorio donde se encuentran los resultados
		self.directorio = directorio
		#Carpetas con los resultados
		self.folders = []
		#Lista de listas que contiene las fronteras de cada ejecucion (incluido elementos repetidos)
		self.paretoFrontiers = []
		#Lista de listas que contiene las fronteras de cada ex sin repetidos
		self.nonRepParetoFrontiers = []
		#Combinacion de todas las fronteras
		self.mergedNonRepFrontiers = []
		#Todas las Fronteras 'mergeds' son unidas en una sola, se aplica FND-Sort y se agregan a esta lista solo las no-dominadas
		self.fndsFrontier = []
		#Se supone que es una lista con listas dentro, del tamano de len(folders) en donde cada una tiene los valores
		#normalizados de cada ejecucion para calcular HV
		self.hyperVolumeResults = []
		#Lista con los porcentajes de participacion de cada frontera con respecto al total de elementos de la frontera merged
		self.participation = []
		self.numFacilites = 0
		#Lista de listas en donde se encuentran todas las fronteras optimas para los casos de tamanio 10 instancia.
		#IMPORTANTE!!! posiciones = [10-1rl, 10-1uni, 10-2rl, 10-2uni, 10-3rl, 10-3uni, 10-4rl, 10-5rl]
		self.paretoOptimas = []
		#Aca guardo los max y min de cada instancia
		self.maxMinInstance = []




	def openParetOptimas(self):
		path = '/home/rsandova/Desktop/Tesis/Memetico/AM/PO/'
		carpetas = os.listdir(path)
		carpetas.sort()
		for file in carpetas:
			po = []
			print "Abriendo Pareto-Optimal set de instancia: ", file
			new_path = path + file
			try:
				with open(new_path) as f:
					for line in f:
						linea = line.split()
						linea = [float(i) for i in linea]
						po.append(linea)
						#print linea
			except IOError as exc:
				if exc.errno != errno.EISDIR:
					raise
			self.paretoOptimas.append(po)
		#print len(self.paretoOptimas)
		return True


	def openArchivos(self):
		path = self.directorio
		carpetasRun = os.listdir(path)
		cantCarpetas = len(carpetasRun)
		self.folders = carpetasRun[:]
		print carpetasRun
		for i in range(cantCarpetas):
			fronteraComplete = []
			frontera = []
			new_path = ""
			new_path = path + "/" + carpetasRun[i] + "/" + "pareto.csv"
			print new_path
			try:
				with open(new_path) as f:
					for lines in f:
						for line in f:
							costosFlujo = []
							#print line
							linea = line.strip().split(",")
							if len(linea) != 0:
								costosFlujo.append(float(linea[0]))
								costosFlujo.append(float(linea[1]))
								#print costosFlujo
								fronteraComplete.append(costosFlujo)
								if costosFlujo not in frontera:
									frontera.append(costosFlujo)
				self.nonRepParetoFrontiers.append(frontera)
				self.paretoFrontiers.append(fronteraComplete)				
				#print len(self.paretoFrontiers)
			except IOError as exc:
				if exc.errno != errno.EISDIR:
					raise		
		return True

	def poMaxMin(self):
		for i in range(len(self.paretoOptimas)):
			lista, listaObj1, listaObj2, maxMinValues, aux, aux2 = [], [], [], [], [], []
			for results in self.paretoOptimas[i]:
				if results not in lista:
					lista.append(results)
			for elements in lista:
				listaObj1.append(elements[0])
				listaObj2.append(elements[1])
			listaObj1.sort()
			listaObj2.sort()
			aux.append(float(listaObj1[0])), aux.append(float(listaObj1[len(listaObj1)-1]))
			maxMinValues.append(aux)
			aux2.append(float(listaObj2[0])), aux2.append(float(listaObj2[len(listaObj2)-1]))
			maxMinValues.append(aux2)
			self.maxMinInstance.append(maxMinValues)
		for i in range(len(self.maxMinInstance)):
			for pares in self.maxMinInstance[i]:
				print pares, i





	def obtenerMaxMin(self):
		lista, listaObj1, listaObj2, maxMinValues, aux, aux2 = [], [], [], [], [], []
		for i in range(len(self.nonRepParetoFrontiers)):
			for results in self.nonRepParetoFrontiers[i]:
				if results not in lista:
					lista.append(results)

		self.mergedNonRepFrontiers = lista[:]		
		#print "largo merged: ", len(self.mergedNonRepFrontiers)
		for elements in lista:
			listaObj1.append(elements[0])
			listaObj2.append(elements[1])
		listaObj1.sort()
		listaObj2.sort()
		aux.append(float(listaObj1[0])), aux.append(float(listaObj1[len(listaObj1)-1]))
		maxMinValues.append(aux)
		aux2.append(float(listaObj2[0])), aux2.append(float(listaObj2[len(listaObj2)-1]))
		maxMinValues.append(aux2)
		return maxMinValues

	def computeHyperVolume(self, maxMinValues):
		minObj1, maxObj1 = maxMinValues[0][0], maxMinValues[0][1]
		minObj2, maxObj2 = maxMinValues[1][0], maxMinValues[1][1]
		#print minObj1, maxObj1, minObj2, maxObj2
		difObj1 = maxObj1 - minObj1
		difObj2 = maxObj2 - minObj2
		#Se guarda en esta lista debido a que los resultados iran dentro del objeto... en normalizedValues...
		normalizados = []
		for i in range(len(self.nonRepParetoFrontiers)):
			normValues = []
			for elemento in self.nonRepParetoFrontiers[i]:
				#print elemento
				values = []
				cost1 = elemento[0]
				cost2 = elemento[1]
				valueObj1 = (cost1 - minObj1)/difObj1
				valueObj2 = (cost2 - minObj2)/difObj2
				values.append(valueObj1), values.append(valueObj2)
				normValues.append(values)
			#print "valores normalizados"
			#for value in normValues:
			#	print value
			normalizados.append(normValues)

			#self.normalizedValues.append(normValues)
		referencePoint = [1,1]
 		for i in range(len(normalizados)):
 			hv = HyperVolume(referencePoint)
 			volume = hv.compute(normalizados[i])
 			self.hyperVolumeResults.append(volume)
 		print "Valores de HV para cada run: ", self.hyperVolumeResults	
 		return 1

 	def computeParticipationLevel(self):
 		listaContador = []
 		contador= 0
 		for i in range(len(self.nonRepParetoFrontiers)):
 			contador = 0
 			#print i
 			for elemento in self.nonRepParetoFrontiers[i]:
 				if elemento in self.fndsFrontier:
 					contador += 1
 				#print elemento
 			listaContador.append(contador)	
 		for cantidad in listaContador:
 			cantAux = float(cantidad)/float(len(self.fndsFrontier))
 			self.participation.append(cantAux)
 		print "porcentajes de participacion: ", self.participation


 	def grafiqueFrontera(self):
 		listaSolC1, listaSolC2 = [], []
 		for i in range(len(self.fndsFrontier)):
 			print  self.fndsFrontier[i]
 			listaSolC1.append(self.fndsFrontier[i][0])
 			listaSolC2.append(self.fndsFrontier[i][1])
 		plt.plot(listaSolC1, listaSolC2, 'ro')
		plt.ylabel('Costo Flujo 2')
		plt.xlabel('Costo Flujo 1')
		plt.show()

	def calculeFinalFrontier(self):
		poblacion = []
		nsga2 = NSGA2(2, 1.0, 1.0)
		largo = len(self.mergedNonRepFrontiers)
		for i in range(len(self.mergedNonRepFrontiers)):
			#print self.mergedNonRepFrontiers[i]
			sol = Solucion(self.numFacilities)
			sol.costoFlujo[0] = self.mergedNonRepFrontiers[i][0]
			sol.costoFlujo[1] = self.mergedNonRepFrontiers[i][1]
			poblacion.append(sol)

			#print  self.mergedNonRepFrontiers[i]
		#print len(poblacion)	
		fronteras = nsga2.fastNonDominatedSort(poblacion)
		poblacion = nsga2.ordenPostBusqueda(poblacion, fronteras, largo)
		for elem in poblacion:
			if elem.rank == 1:
				self.fndsFrontier.append(elem.costoFlujo)
			#print elem.costoFlujo, elem.rank
		

	
	def writeResults(self, salida):
		outputFile = salida + ".csv"




	

if __name__ == "__main__":

    # Example:
    direct = '/home/rsandova/Desktop/Tesis/Memetico/AM/ResultadosCY/'
    carpetas = os.listdir(direct)
    print carpetas
    myMetr = Metrics(direct)
    myMetr.openParetOptimas()
    myMetr.poMaxMin()



    #for i in range(1,len(carpetas)+1):
    #	print i 
    #	direct = '/home/rsandova/Desktop/Tesis/Memetico/AM/ResultadosCY/resultsMem' + str(i)
    #	metrics = Metrics(direct)
    #	metrics.numFacilities = input ("numFac: ")
    #	metrics.openArchivos()
    #	maxMin = metrics.obtenerMaxMin()
    #	metrics.computeHyperVolume(maxMin)
    #	metrics.calculeFinalFrontier()
    #	#metrics.grafiqueFrontera()
    #	metrics.computeParticipationLevel()
		