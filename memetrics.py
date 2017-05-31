# -*- coding: utf-8 -*-
import glob
import os
import errno
from hv import HyperVolume
import matplotlib.pyplot as plt
import funciones
from nsga2func import Solucion
from nsga2func import NSGA2
import numpy



class Metrics:

	def __init__(self):
		#nombre del directorio donde se encuentran los resultados
		self.nombre = ""
		#Carpetas con los resultados
		self.folders = []
		#Lista de listas que contiene las fronteras de cada ejecucion (incluido elementos repetidos)
		self.paretoFrontiers = []
		#Lista de listas que contiene las fronteras de cada ex sin repetidos
		self.nonRepParetoFrontiers = []
		#Combinacion de todas las fronteras
		self.mergedNonRepFrontiers = []
		#Todas las Fronteras 'mergeds' son unidas en una sola, se aplica FND-Sort y se agregan a esta lista solo las no-dominadas
		self.listOFrontiers = []
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
		self.hyperVolumePO = []
		self.graspFrontier = []
		self.participation = []


	def openResults(self):
		direct = '/home/rsandova/Desktop/Tesis/Memetico/AM/literature/'
		carpetas = os.listdir(direct)
		carpetas.sort()
		print carpetas
		files = []
		for file in carpetas:
			results = []
			print "Abriendo Resultados de instancia: " , file
			files.append(file)
			new_path = direct + file
			try:
				with open(new_path) as f:
					for line in f:
						linea = line.split(",")
						linea = [float(i) for i in linea]
						results.append(linea)
						#print linea
			except IOError as exc:
				if errno != errno.EISDIR:
					raise
			self.graspFrontier.append(results)

	def openParetOptimas(self):
		path = '/home/rsandova/Desktop/Tesis/Memetico/AM/PO/'
		carpetas = os.listdir(path)
		carpetas.sort()
		files = []
		for file in carpetas:
			po = []
			print "Abriendo Pareto-Optimal set de instancia: ", file
			files.append(file)
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
		return files


	def openArchivos(self, directorio):
		#path = self.directorio
		#print directorio
		carpetasRun = os.listdir(directorio)
		cantCarpetas = len(carpetasRun)
		self.folders = carpetasRun[:]
		carpetasRun.sort()
		fronteras = []
		#print carpetasRun
		allFronts = []
		retorne = []
		for i in range(cantCarpetas):
			#fronteraComplete = []
			frontera = []
			new_path = ""
			new_path = directorio + "/" + carpetasRun[i] + "/" + "pareto.csv"
			#print new_path
			try:
				with open(new_path) as f:
					for lines in f:
						for line in f:
							costosFlujo = []
							#print line
							linea = line.strip().split(",")
							#print linea
							#break
							if len(linea) != 0:
								costosFlujo.append(float(linea[0]))
								costosFlujo.append(float(linea[1]))
								#fronteraComplete.append(costosFlujo)
								if costosFlujo not in frontera:
									frontera.append(costosFlujo)
								if costosFlujo not in allFronts:
									allFronts.append(costosFlujo)   
				fronteras.append(frontera)
				#self.paretoFrontiers.append(fronteraComplete)              
				#print len(self.paretoFrontiers)
			except IOError as exc:
				if exc.errno != errno.EISDIR:
					raise       
		#fronteras = self.nonRepParetoFrontiers[:]
		#for elemento in fronteras: 
			#print elemento

		retorne.append(fronteras)
		retorne.append(allFronts)
		#allFronts las contiene todas, para sacar el mayor y el menor. 
		return retorne

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
		#for i in range(len(self.maxMinInstance)):
		#   print i
		#   for pares in self.maxMinInstance[i]:
		#       print pares






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

	def computeHVforPO(self):
		for i in range(len(self.maxMinInstance)):
			#print i
			#print self.maxMinInstance[i]
			self.computeHVPO(self.maxMinInstance[i], self.paretoOptimas[i])
		print "Valores de HV para cada instancia: ", self.hyperVolumePO
			

	def computeHVPO(self, maxMinValues, frontera):
		minObj1, maxObj1 = maxMinValues[0][0], maxMinValues[0][1]
		minObj2, maxObj2 = maxMinValues[1][0], maxMinValues[1][1]
		#print minObj1, maxObj1, minObj2, maxObj2
		difObj1 = maxObj1 - minObj1
		difObj2 = maxObj2 - minObj2
		if difObj1 == 0:
			print "El valor de hyperVolume es: ", 4.0
			self.hyperVolumePO.append(4.0)
		#Se guarda en esta lista debido a que los resultados iran dentro del objeto... en normalizedValues...
		#normalizados = []
		else:

			normValues = []
			for elemento in frontera:
				
		
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
			#   print value
			#normalizados.append(normValues)

			#self.normalizedValues.append(normValues)
			referencePoint = [2,2]
			#for i in range(len(normalizados)):
			hv = HyperVolume(referencePoint)
			volume = hv.compute(normValues)
			self.hyperVolumePO.append(volume)
		for volume in self.hyperVolumePO:
			print "El HyperVolumen es: ", volume
		return 1                        



	def computeParticipationLevel(self, referencia):
		listaContador = []
		contador= 0
		for i in range(len(self.nonRepParetoFrontiers)):
			contador = 0
			#print i

			for elemento in self.nonRepParetoFrontiers[i]:
				#print elemento
				if elemento in referencia:
					contador += 1
				#print elemento
			listaContador.append(contador)  
		for cantidad in listaContador:
			cantAux = float(cantidad)/float(len(referencia))
			self.participation.append(cantAux)
		maxVal = max(self.participation)
		print "el mejor es: ", maxVal
		indice = self.participation.index(maxVal)
		print "y su indice es: ", indice
		print "porcentajes de participacion: ", self.participation
		return indice



	def grafiqueFrontera(self, po, best, indice, instances):
		listaSolC1, listaSolC2 = [], []
		listaObtC1, listaObtC2 = [], []
		for i in range(len(self.nonRepParetoFrontiers)):
			if i == best:
				for elem in self.nonRepParetoFrontiers[i]:
					#print elem
					#print  self.nonRepParetoFrontiers[i]
					listaSolC1.append(elem[0])
					listaSolC2.append(elem[1])
		
		for i in range(len(po)):
			if i == indice:
				for elem in po[i]:
					#print elem
					listaObtC1.append(elem[0])
					listaObtC2.append(elem[1])
		#for i in range(len(self.paretoOptimas)):

		#plt.legend()
		#print listaSolC1
		a = plt.plot(listaSolC1, listaSolC2, 'r+', label = 'NSGA2+QPLS')
		b = plt.plot(listaObtC1, listaObtC2, 'g-', label = 'mGRASP/MH')
		plt.title('Comparacion con instancia: ' + instances)
		plt.setp(a, "linestyle", "none", "marker", "o")
		plt.setp(b, "linestyle", "none", "marker", "*")
		plt.ylabel('Costo Flujo 2')
		plt.xlabel('Costo Flujo 1')
		plt.legend(loc = 'upper right')
		plt.show()
		#plt.plot(<X AXIS VALUES HERE>, <Y AXIS VALUES HERE>, 'line type', label='label here')
		#plt.plot(<X AXIS VALUES HERE>, <Y AXIS VALUES HERE>, 'line type', label='label here')
		#plt.title('title')


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
		

	def getMaxMin(self,allFronts):
		costoF1 = []
		costoF2 = []
		maxMinIns = []
		aux1, aux2 = [], []
		for elemento in allFronts:
			costoF1.append(elemento[0])
			costoF2.append(elemento[1])
		costoF1.sort()
		costoF2.sort()
		#print costoF1[0], costoF1[len(costoF1)-1]
		#print costoF2[0], costoF1[len(costoF2)-1]
		aux1.append(costoF1[0]), aux1.append(costoF1[len(costoF1)-1])
		aux2.append(costoF2[0]), aux2.append(costoF2[len(costoF2)-1])
		maxMinIns.append(aux1)
		maxMinIns.append(aux2)
		return maxMinIns

		#print elemento


def obtainResults(carpetas):
	instanceList = [ Metrics() for i in range(len(carpetas))]
	#break
	for i in range(len(carpetas)):
		mejores = []
		mergedFronts = []
		listaHV = []
		allListaHV = []
		allMerged = []
		metodo = direct + "/" + carpetas[i]
		instanceList[i].nombre = carpetas[i]
		#print instanceList[i].nombre
		subcarp = os.listdir(metodo)
		for j in range(len(subcarp)):
			datos = metodo + "/resultsMem" + str(j)
			metrics = Metrics()
			resultados = metrics.openArchivos(datos)
			#resultaos[0] correspodne a la lista con cada run para la instancia en cuestion. y resultados[1] es spolo una lista con todos los merges
			#metrics.mergeResultados(fronteras)
			listaHV = resultados[0]
			mergedFronts = resultados[1]
			#listaHV = fronteras[:]
			#mergedFronts = allFronts[:]
			#mm = maxmin
			allListaHV.append(listaHV)
			allMerged.append(mergedFronts)
			mm = metrics.getMaxMin(mergedFronts)
			mejores.append(mm)
		#aqui saco el mejor de los mejores de la lista y entrego solo uno, no la lista completa. duh
		#print len(mejores)
		#print mejores
		#instanceList[i].getTrueMaxMin(mejores)

		instanceList[i].listOFrontiers = allListaHV[:]
		instanceList[i].mergedNonRepFrontiers = allMerged[:]
		instanceList[i].maxMinInstance = mejores[:]
		#break
		#print instanceList[i].maxMinInstance
		#print "++++++++++++++++++++++"
		#print instanceList[i].mergedNonRepFrontiers
		
		#print len(instanceList[i].maxMinInstance)
		#print len(instanceList[i].mergedNonRepFrontiers)
		#print len(instanceList[i].listOFrontiers)
		
		#hola = input("asdasd")
				#print instanceList[i].nombre
		#print len(instanceList[i].listOFrontiers)
		
		#for j in range(len(instanceList[i].listOFrontiers)):
		#   print len(instanceList[i].listOFrontiers[j])
		
			#print j
			#print instanceList[i].listOFrontiers[j]
		#print len(instanceList[i].maxMinInstance)
		#print len(instanceList[i].mergedNonRepFrontiers)
		#print input(" ")
	return instanceList

def getMaxMinMetodos(instanceList):
	globalMaxMinMetodos = []
	for j in range(len(instanceList[0].maxMinInstance)):
		maxMinMetodos = []
		listMinObj1, listMaxObj1, listMinObj2, listMaxObj2 = [], [], [], []
		aux, aux1 = [], []
		maxMin = []
		#print "soy j", j
		#print instanceList[0].maxMinInstance[j]
		for i in range(len(instanceList)):
			#print "                soy i: ", instanceList[i].nombre
			maxMinMetodos.append(instanceList[i].maxMinInstance[j])
			#print instanceList[i].maxMinInstance[j]
			listMinObj1.append(instanceList[i].maxMinInstance[j][0][0])
			listMaxObj1.append(instanceList[i].maxMinInstance[j][0][1])
			listMinObj2.append(instanceList[i].maxMinInstance[j][1][0])
			listMaxObj2.append(instanceList[i].maxMinInstance[j][1][1])
		listMinObj1.sort()
		listMaxObj1.sort()
		listMinObj2.sort()
		listMaxObj2.sort()
		#print listMinObj1
		#print "+++++++++++++++++++++++++++++"
		
		
		largo = len(listMaxObj1)
		aux.append(listMinObj1[0]), aux.append(listMaxObj1[largo-1])
		aux1.append(listMinObj2[0]), aux1.append(listMaxObj2[largo-1])
		maxMin.append(aux)
		maxMin.append(aux1)
		#print "Menores objetivo 1" ,listMinObj1
		#print "Mayores Objetivo 1", listMaxObj1
		#print "Menores Objetivo 2", listMinObj2
		#print "mayores Objetivo 2", listMaxObj2
		globalMaxMinMetodos.append(maxMin)
		#print ".............................."
	for i in range(len(globalMaxMinMetodos)):
		print globalMaxMinMetodos[i]    
	return globalMaxMinMetodos

def computeHyperVolume(maxMinValues, fronteras):
	minObj1, maxObj1 = maxMinValues[0][0], maxMinValues[0][1]
	minObj2, maxObj2 = maxMinValues[1][0], maxMinValues[1][1]
	#print minObj1, maxObj1, minObj2, maxObj2
	difObj1 = maxObj1 - minObj1
	difObj2 = maxObj2 - minObj2
	#Se guarda en esta lista debido a que los resultados iran dentro del objeto... en normalizedValues...
	listaHyperVol = []
	normalizados = []
	#print len(fronteras)
	#h = input("")
	for i in range(len(fronteras)):
		normValues = []
		#print i
		for elemento in fronteras[i]:
			
			#print elemento

			values = []
			cost1 = elemento[0]
			cost2 = elemento[1]
			if difObj1 == 0:
				valueObj1 = 0
			else:
				valueObj1 = (cost1 - minObj1)/difObj1
			if difObj2 == 0:
				valueObj2 = 0
			else: 
				valueObj2 = (cost2 - minObj2)/difObj2
			values.append(valueObj1), values.append(valueObj2)
			normValues.append(values)
		#print "valores normalizados"
		#for value in normValues:
		#   print value
		normalizados.append(normValues)
			#self.normalizedValues.append(normValues)
	#h = input("")
	referencePoint = [2,2]
	for i in range(len(normalizados)):
		hv = HyperVolume(referencePoint)
		volume = hv.compute(normalizados[i])
		listaHyperVol.append(volume)
	#print "Valores de HV para cada run: ", listaHyperVol    
	return listaHyperVol

def ordenarMergedFronts(mergedFronts, numFac):
	nsga2 = NSGA2(2, 0.1, 1.0)
	pob, poblacion = [], []
	for elem in mergedFronts:
		sol = Solucion(numFac)
		sol.costoFlujo = elem[:]
		pob.append(sol)
		#print sol.costoFlujo
	fronteras = nsga2.fastNonDominatedSort(pob)
	pob = nsga2.ordenPostBusqueda(pob, fronteras, len(pob))
	for elem in pob:
		if elem.rank == 1:
			poblacion.append(elem)
	return poblacion

def grafiqueFrontera(listPoblacion, po, instance, instanceList):
	#listaSolC1, listaSolC2 = [], []
	#listaObtC1, listaObtC2 = [], []
	listaOfCosts = []
	listaObtC1, listaObtC2 = [], []
	for i in range(len(listPoblacion)):
		listaCost1, listaCost2 = [], []
		#print i
		for solucion in listPoblacion[i]:
			#print solucion.costoFlujo
			listaCost1.append(solucion.costoFlujo[0])
			listaCost2.append(solucion.costoFlujo[1])
		listaOfCosts.append(listaCost1)
		listaOfCosts.append(listaCost2)
	#print len(listaOfCosts)
	a = plt.plot(listaOfCosts[0], listaOfCosts[1], 'b+', label = instanceList[0].nombre )
	b = plt.plot(listaOfCosts[2], listaOfCosts[3], 'g+', label = instanceList[1].nombre)
	c = plt.plot(listaOfCosts[4], listaOfCosts[5], 'c', label = instanceList[2].nombre)
	d = plt.plot(listaOfCosts[6], listaOfCosts[7], 'y', label = instanceList[3].nombre)	
	if len(po) == 0:
		pass	
	else:
		for elem in po:
			#print "elemento: ", elem
			listaObtC1.append(elem[0])
			listaObtC2.append(elem[1])
		e = plt.plot(listaObtC1, listaObtC2, 'r', label = 'Pareto Optima')
		plt.setp(e, "linestyle", "none", "marker", "*")
	
	plt.title('Comparacion con instancia: ' + instance)
	plt.setp(a, "linestyle", "none", "marker", "o")
	plt.setp(b, "linestyle", "none", "marker", ".")
	plt.setp(c, "linestyle", "none", "marker", "8")
	plt.setp(d, "linestyle", "none", "marker", "o")
		
	plt.ylabel('Costo Flujo 2')
	plt.xlabel('Costo Flujo 1')
	plt.legend(loc = 'upper right')
	plt.show()

		#plt.plot(<X AXIS VALUES HERE>, <Y AXIS VALUES HERE>, 'line type', label='label here')
		#plt.plot(<X AXIS VALUES HERE>, <Y AXIS VALUES HERE>, 'line type', label='label here')
		#plt.title('title')

def computeParticipationLevel(referencia):
	listaContador = []
	contador= 0
	for i in range(len(self.nonRepParetoFrontiers)):
		contador = 0
		#print i
		for elemento in self.nonRepParetoFrontiers[i]:
			#print elemento
			if elemento in referencia:
				contador += 1
			#print elemento
		listaContador.append(contador)  
	for cantidad in listaContador:
		cantAux = float(cantidad)/float(len(referencia))
		self.participation.append(cantAux)
	maxVal = max(self.participation)
	print "el mejor es: ", maxVal
	indice = self.participation.index(maxVal)
	print "y su indice es: ", indice
	print "porcentajes de participacion: ", self.participation
	return indice

def computeParticipation(poblations, representative):
	listaContador = []
	participation = []
	for i in range(len(poblations)):
		#print i
		contador = 0
		for solucion in poblations[i]:
			if solucion.costoFlujo in representative:
				contador += 1
				#print solucion.costoFlujo
		listaContador.append(contador)
	for cantidad in listaContador:
		cantAux = float(cantidad)/float(len(representative))
		participation.append(cantAux)
	print participation	

def getParetoRepresentative(pobMetodos):
	nsga2 = NSGA2(2, 0.1, 1.0)
	auxRepresentative = []
	pob = []
	paretoRepresentative = []
	for i in range(len(pobMetodos)):
		for elemento in pobMetodos[i]:
			pob.append(elemento)
	fronteras = nsga2.fastNonDominatedSort(pob)
	pob = nsga2.ordenPostBusqueda(pob, fronteras, len(pob))
	for elem in pob:
		if elem.rank == 1:
			#print elem.costoFlujo, elem.rank
			paretoRepresentative.append(elem.costoFlujo)
	return paretoRepresentative

def getMeanSTD(listofHV):
	arr = numpy.array(listofHV)
	prom = numpy.mean(arr, axis = 0)
	std = numpy.std(arr, axis = 0)
	print str(prom) + " +- " +  str(std)
					#print listofHV

def computeCoverage(pobEvaluada, pobMetodos, indice):
	cov = []
	for j in range(len(pobMetodos)):
		if indice != j:
			for sols in pobEvaluada:
				for solus in pobMetodos[j]:
					pass
#			print frontera



if __name__ == "__main__":

	# Example:
	direct = '/home/rsandova/Desktop/Tesis/Memetico/AM/Resultados'
	carpetas = os.listdir(direct)
	#print carpetas
	instancias = '/home/rsandova/Desktop/Tesis/Memetico/AM/instances'
	inst = os.listdir(instancias)
	inst.sort()
		
	allMaxMin = []
	myMetr = Metrics()
	myMetr.openParetOptimas()
	myMetr.poMaxMin()
	
	#for i in range(len(myMetr.maxMinInstance)):
		#print(myMetr.maxMinInstance[i])
	#print "paretoOptimas, ", myMetr.paretoOptimas
	#myMetr.computeHVforPO()

	graspMetr = Metrics()
	graspMetr.openResults()

	cwd = os.getcwd()
	result = "/Resultados"
	direct = cwd + result
	carpetas = os.listdir(direct)
	#print carpetas

	#Lista de listas que contiene los mejores de cada ejecucion (indice)
	mejoresDeMejores = []
	#Aqui obtengo todos los datos por cada ejecucion para cada metodo y se almacenan en instanceList,
	#En donde instanceList[i] --> Corresponde a los datos para el metodo 'i' que sería cada uno de los metodo en cuestion
	instanceList = obtainResults(carpetas)
	#Aqui obtengo los maxmin de todAs las instancias.
	#Este metodo devuelve una lista de largo 'x' (cantidad de instancias) en donde cada posicion corresponde a un arreglo de dos arreglos.
	#Del tipo [[minObj1, MaxObj1], [MinObj2, MaxObj2]]
	for i in range(len(instanceList)):
		print instanceList[i].nombre
	allMaxMin = getMaxMinMetodos(instanceList)
	#print len(allMaxMin)
	#pobMetodos = []
	for i in range(len(allMaxMin)):
		pobMetodos = []
		combined = []
		print "Resultados para Mem" + str(i)
		for j in range(len(instanceList)):
			if i < 8:
				print instanceList[j].nombre
				if i == 3:
					listofHV = computeHyperVolume(allMaxMin[i], instanceList[j].listOFrontiers[i])
					getMeanSTD(listofHV)
					pob = ordenarMergedFronts(instanceList[j].mergedNonRepFrontiers[i], 10)
					pobMetodos.append(pob)
					
				listofHV = computeHyperVolume(myMetr.maxMinInstance[i], instanceList[j].listOFrontiers[i])
				getMeanSTD(listofHV)
				#print listofHV
				pob = ordenarMergedFronts(instanceList[j].mergedNonRepFrontiers[i], 10)
				pobMetodos.append(pob)	
			else:
				print instanceList[j].nombre
				listofHV = computeHyperVolume(allMaxMin[i], instanceList[j].listOFrontiers[i])
				getMeanSTD(listofHV)
				pob = ordenarMergedFronts(instanceList[j].mergedNonRepFrontiers[i], 20)
				pobMetodos.append(pob)
		print "pobMetodos: ", len(pobMetodos)		

		if i < 8:
			computeParticipation(pobMetodos, myMetr.paretoOptimas[i])
			#for i in range(len(pobMetodos)):
			#	computeCoverage(pobMetodos[i], pobMetodos, i)
			grafiqueFrontera(pobMetodos, myMetr.paretoOptimas[i], inst[i], instanceList )
		else:
			paretoRep = getParetoRepresentative(pobMetodos)
			aporteFrontera = computeParticipation(pobMetodos, paretoRep)
			#computeCoverage(pobMetodos)
			grafiqueFrontera(pobMetodos, [], inst[i], instanceList)


		h = input("")



	#for i in range(1,9):
	#   print i
	#   direct = '/home/rsandova/Desktop/Tesis/Memetico/AM/ResultadosCY/resultsMem' + str(i)
	#   metrics = Metrics(direct)
	#   metrics.numFacilities = input("Numfac: ")
	#   metrics.openArchivos()
	#   metrics.computeHyperVolume(myMetr.maxMinInstance[i-1])
	#   best = metrics.computeParticipationLevel(myMetr.paretoOptimas[i-1])
	#   metrics.grafiqueFrontera(myMetr.paretoOptimas,best, i-1, instances[i-1])
	#

	#for i in range(9,11):
	#   print i
	#   direct = '/home/rsandova/Desktop/Tesis/Memetico/AM/ResultadosCY/resultsMem' + str(i)
	#   metrics = Metrics(direct)
	#   metrics.numFacilities = input("NumFac: ")
	#   metrics.openArchivos()
	#   metrics.grafiqueFrontera(graspMetr.graspFrontier, 3, k, "")
	#   k+=1


	#for i in range(1,len(carpetas)+1):
	#   print i 
	#   direct = '/home/rsandova/Desktop/Tesis/Memetico/AM/ResultadosCY/resultsMem' + str(i)
	#   metrics = Metrics(direct)
	#   metrics.numFacilities = input ("numFac: ")
	#   metrics.openArchivos()
	#   maxMin = metrics.obtenerMaxMin()
	#   metrics.computeHyperVolume(maxMin)
	#   metrics.calculeFinalFrontier()
	#   #metrics.grafiqueFrontera()
	#   metrics.computeParticipationLevel()