# -*- coding: utf-8 -*-

import funciones
import random
import numpy as np
import copy
import itertools
import datetime
import os
from hv import HyperVolume
#import matplotlib.pyplot as plt

class Solucion:

	def __init__(self, numFacilities):
		self.numFacilities = numFacilities
		#self.numObjetivos = 2
		self.costoFlujo = []
		for _ in range(1,3):
			self.costoFlujo.append(None) 
		self.solution = []
		self.rank = 10000
		self.numSolDominantes = 0
		self.setSolDominadas = []
		self.crowdedDistance = 0.0
		self.visitado = 0
		self.tabuList = []

	def costoAsignacion(self):
		self.costoFlujo[0] = 0.0
		self.costoFlujo[1]= 0.0
		for i in range(self.numFacilities):
			for j in range(self.numFacilities):
				self.costoFlujo[0] = self.costoFlujo[0] + funciones.matrixFlujoUno[i*(self.numFacilities)+j]*funciones.matrixDistancia[self.solution[i]*(self.numFacilities)+self.solution[j]]
				self.costoFlujo[1] = self.costoFlujo[1] + funciones.matrixFlujoDos[i*(self.numFacilities)+j]*funciones.matrixDistancia[self.solution[i]*(self.numFacilities)+self.solution[j]]
		#print "Costo F1: ", self.costoFlujo[0]
		#print "Costo F2: ", self.costoFlujo[1]

	def costoAsignacionMovida(self, r, s ):
		#self.costoFlujo[0] = 0.0
		#self.costoFlujo[1] = 0.0
		costos = [0.0,0.0]
		for k in range(self.numFacilities):
			if k != r and k != s:
				costos[0] += (funciones.matrixFlujoUno[s*self.numFacilities+k] - funciones.matrixFlujoUno[r*self.numFacilities+k])*(funciones.matrixDistancia[self.solution[s]*self.numFacilities+self.solution[k]] - funciones.matrixDistancia[self.solution[r]*self.numFacilities+self.solution[k]]) + (funciones.matrixFlujoUno[s*self.numFacilities+k] - funciones.matrixFlujoUno[r*self.numFacilities+k])*(funciones.matrixDistancia[self.solution[s]*self.numFacilities+self.solution[k]] - funciones.matrixDistancia[self.solution[r]*self.numFacilities+self.solution[k]])										
				costos[1] += (funciones.matrixFlujoDos[s*self.numFacilities+k] - funciones.matrixFlujoDos[r*self.numFacilities+k])*(funciones.matrixDistancia[self.solution[s]*self.numFacilities+self.solution[k]] - funciones.matrixDistancia[self.solution[r]*self.numFacilities+self.solution[k]]) + (funciones.matrixFlujoDos[s*self.numFacilities+k] - funciones.matrixFlujoDos[r*self.numFacilities+k])*(funciones.matrixDistancia[self.solution[s]*self.numFacilities+self.solution[k]] - funciones.matrixDistancia[self.solution[r]*self.numFacilities+self.solution[k]])						  
		return costos
		#print "Costo Movida F1: ", self.costoFlujo[0]
		#print "Costo Movida F2: ", self.costoFlujo[1]
	def costoAsignacionParcial(self, locationNew ):
		largoK = len(self.solution)
		self.costoFlujo[0] =  0.0
		self.costoFlujo[1] =  0.0
		
		indexNew = self.solution.index(locationNew)
		for i in range(largoK-1):
			self.costoFlujo[0] += funciones.matrixFlujoUno[i*self.numFacilities+largoK]*funciones.matrixDistancia[self.solution[i]*(self.numFacilities)+self.solution[indexNew]] + funciones.matrixFlujoUno[i*self.numFacilities+largoK]*funciones.matrixDistancia[self.solution[i]*(self.numFacilities)+self.solution[indexNew]] 
			self.costoFlujo[1] += funciones.matrixFlujoDos[i*self.numFacilities+largoK]*funciones.matrixDistancia[self.solution[i]*(self.numFacilities)+self.solution[indexNew]] + funciones.matrixFlujoDos[i*self.numFacilities+largoK]*funciones.matrixDistancia[self.solution[i]*(self.numFacilities)+self.solution[indexNew]] 
		#print "costos: "
		#print self.costoFlujo[0], 
		#print self.costoFlujo[1]
			





class NSGA2:

	def __init__(self, numObjectives, mutationRate, crossoverRate):
		self.numObjectives = numObjectives
		self.mutationRate = mutationRate
		self.crossoverRate = crossoverRate
		self.directorio = None
		self.hyperVol = None

		

	def runAlgorithm(self, poblacion, tamPob, generaciones, alpha, indCX, indMUT, start):
		
		startTime = start
		tiempo = funciones.convertTime(startTime)
		self.directorio = "results/Results_"+tiempo
		os.makedirs(self.directorio)

		nextPobla = self.makeNewPob(poblacion, indCX, indMUT, tamPob)
		nombreArchivo = self.directorio + "/generaciones.csv"
		nArchivo = open(nombreArchivo, 'w' )	
		counter = 1
		archiveHyperVolume = []
		for i in range(1,generaciones+1):
			print "++++++++++++++++++++++++++++++++++++++++++++++++++++++"
			print "Generation Number: ", i,
			print "from a Total of ", generaciones
			print "++++++++++++++++++++++++++++++++++++++++++++++++++++++"
			pobCombinada = []
			print "Extending Populations into Combined Population. . ."
			pobCombinada.extend(poblacion)
			pobCombinada.extend(nextPobla)

			print "Largo poblacion:" ,len(poblacion)
			print "largo bextPobla: ", len(nextPobla)
			print "Largo Combinada:", len(pobCombinada)
			#for elem in pobCombinada:
			#	print elem.solution, elem.costoFlujo[0], elem.costoFlujo[1], elem.rank,elem.crowdedDistance
			print "Fast Non-Dominated Sorting of Combined Population. . . " 
			#np.asarray(pobCombinada)
			fronteras = self.fastNonDominatedSort(pobCombinada)
			del poblacion[:]
			poblacion = self.ordenPostBusqueda(pobCombinada, fronteras, tamPob)
			print "Tamaño poblacion: ", len(poblacion)
			nArchivo.write("Generacion: " + str(i) + "\n")
			for j in range(len(poblacion)):
				nArchivo.write(""+ str(poblacion[j].costoFlujo[0]) + ", " + str(poblacion[j].costoFlujo[1]) + ", " + str(poblacion[j].rank) + ", " +  str(poblacion[j].crowdedDistance) +"\n")
				

			if counter != 1:
				poblacion = self.makeNewPob(poblacion, indCX, indMUT, tamPob)
				print len(poblacion)
				print "Fast Non-Dominated Sorting of new population. . .  "
				fronteras = self.fastNonDominatedSort(poblacion)
				#print "la cantidad de fronteras es: ", len(fronteras)
				poblacion = self.ordenPostBusqueda(poblacion, fronteras, tamPob)
			
			print "Local Search is beggining. . . "	
			nextPobla = self.paretoLocalSearch(poblacion, tamPob, alpha)
			print "Local Search has ended."
			
			if counter == generaciones:
				print "ULTIMA GENERACION!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
				
				
				pobCombi = []
				normalizedValues = []
				pobCombi.extend(poblacion)
				pobCombi.extend(nextPobla)
				#print len(poblacion)
				#print len(nextPobla)
				front =	self.fastNonDominatedSort(pobCombi)
				pobCombi = self.ordenPostBusqueda(pobCombi, front, tamPob)
				#print len(pobCombi)
				#print tamPob
				for elem in pobCombi:
					#pardeFlujos = []
					#pardeFlujos.append(elem.costoFlujo[0])
					#pardeFlujos.append(elem.costoFlujo[1])
					#print elem.costoFlujo	
					archiveHyperVolume.append(elem.costoFlujo)
					#archiveHyperVolume.append(pardeFlujos)
				normalizedValues = self.normalizarValores(poblacion, tamPob)	
				ref = [1,1]
				hv = HyperVolume(ref)
				volume = hv.compute(normalizedValues)
				#print archiveHyperVolume
					
					#print elem.costoFlujo[0], elem.costoFlujo[1]
				#print archiveHyperVolume
				#print len(archiveHyperVolume)
			counter += 1
			#print "NEXTPOBLA"
			#for elem in nextPobla:
			#	print elem.solution, elem.costoFlujo[0], elem.costoFlujo[1], elem.rank, elem.crowdedDistance


			#print "largo resultado LS: ", len(nextPobla)
			#nextPobla = self.paretoLoc(poblacion, tamPob, cantIteraciones)
		stopTime = datetime.datetime.now()
		final = stopTime - startTime
		nArchivo.seek(0)
		nArchivo.write("Final time of Execution: " + str(final) + "\n")
		nArchivo.close()
		print "Algorithm finished in: " , str(final)

	def normalizarValores(self, poblacion, tamPob):
		maxMin = []
		for n_obj in range(0,self.numObjectives):
			objValues = []
			poblacion = self.sortCostoAssignacion(poblacion, n_obj)
			for elem in poblacion:
				print elem.solution, elem.costoFlujo
			minValue = poblacion[0].costoFlujo[n_obj]
			maxValue = poblacion[tamPob-1].costoFlujo[n_obj]
			objValues.append(minValue)
			objValues.append(maxValue)
			maxMin.append(objValues)
			print "obj2"
		minObj1 = maxMin[0][0]
		maxObj1 = maxMin[0][1]
		minObj2 = maxMin[1][0]
		maxObj2 = maxMin[1][1]
		difObj1 = maxObj1 - minObj1
		difObj2 = maxObj2 - minObj2
		poblacion_SR = []
		soluciones = []
		for elemento in poblacion:
			if elemento.solution not in soluciones:
				poblacion_SR.append(elemento)
				soluciones.append(elemento.solution)
		del soluciones[:]
		print "pob sin repetidos"
		#for elem in poblacion_SR:
		#	print elem.solution, elem.costoFlujo

		#print minObj1, maxObj1, minObj2, maxObj2 
		
		normValues = []
		for elemento in poblacion_SR:
			values = []
			cost1 = elemento.costoFlujo[0]
			cost2 = elemento.costoFlujo[1]
			valueObj1 = (cost1 - minObj1 )/difObj1
			valueObj2 = (cost2 - minObj2)/difObj2
			values.append(valueObj1)
			values.append(valueObj2)
			normValues.append(values)
		print "valores normalizados"
		#for value in normValues:
		#	print value
		return normValues

	def ordenPostBusqueda(self, poblacion, fronteras, tamPob):
		
		del poblacion[:]
		for front in fronteras:
			self.crowdingDistanceAssignment(front)
			for elem in front:
				poblacion.append(elem)
		self.sortCrowding(poblacion)
		if len(poblacion) >= tamPob:
			poblacion = poblacion[:tamPob]
		#for elemento in poblacion:
			#print elemento.solution, elemento.rank
		return poblacion
		#Viejo
#		del poblacion[:]
#		for frontera in fronteras:
#			frontera = self.crowdingDistanceAssignment(frontera)
			#print "Largo de la frontera: ", len(fronteras)
#			for elemento in frontera:
				#print elemento.solution
#				poblacion.append(elemento)
#			if len(frontera)==0:
#					break	

#		self.sortCrowding(poblacion)
		#if len(poblacion) >= tamPob:

#		poblacion = poblacion[:tamPob]
		#else: 
			#print "SOMETHING IS WRONG!! "
#		return poblacion

	def modifiedPLS(self, poblacion, tamPob, alphaVec):
		archive, solutionArchive, vecindad, soluciones, listaVecinos, solucionAux = [], [], [], [], [], []
		numFac = poblacion[0].numFacilities
		for solucion in poblacion:
			if solucion.rank == 1:
				archive.append(solucion)
				solucion.visitado = 0
		while self.contadorVisitados(archive):
			for elemento in archive:
				solutionArchive.append(elemento.solution)
			solSeleccionada = self.seleccionar(archive)
			if alphaVec >= 0.9:
				vecindad = self.generoVecinos(solSeleccionada, numFac)
			else:
				vecindad = self.generarAlphaVecinos(solSeleccionada, alphaVec)
			vecindad.append(solSeleccionada)
			solucionAux.append(solSeleccionada.solution)
			fronteras = self.fastNonDominatedSort(vecindad)
			vecindad = self.ordenPostBusqueda(vecindad, fronteras, tamPob)
			for vecino in vecindad:
				if vecino.rank == 1:
					soluciones.append(vecino.solution)
					listaVecinos.append(vecino)
			if solSeleccionada.solution in soluciones:
				solSeleccionada.visitado = 1
				for elementoVecino in listaVecinos:
					if elementoVecino in solucionAux:
						continue
					else:
						if elementoVecino.solution in solutionArchive:
							elementoVecino.visitado = 1
							archive.append(elementoVecino)
							self.fastNonDominatedSort(archive)
							archive = self.actualizarArchive(archive)
						else:
							archive.append(elementoVecino)
							self.fastNonDominatedSort(archive)
							archive = self.actualizarArchive(archive)
				
				del listaVecinos[:]			
			
			elif solSeleccionada.solution not in soluciones:
				archive.remove(solSeleccionada)
				for elementoVecino in listaVecinos:
					if elementoVecino.solution in solutionArchive:
						elementoVecino.visitado = 1
						archive.append(elementoVecino)
						self.fastNonDominatedSort(archive)
						archive = self.actualizarArchive(archive)
					else:
						archive.append(elementoVecino)
						self.fastNonDominatedSort(archive)
						archive = self.actualizarArchive(archive)					
				del listaVecinos[:]
			tamanoPonderar = tamPob*0.1
			if len(archive)	>= tamanoPonderar*tamPob:
				print "Population size bigger than setted: ", len(archive),
				print "Reducing Size. . ."
				fronteras = self.fastNonDominatedSort(archive)
				archive = self.ordenPostBusqueda(archive, fronteras, tamPob)
				for elem in archive:
					print elem.visitado, 
			del solutionArchive[:]			
		return archive		

	def memoryBasedPLS(self, poblacion, tamPob):
		#Defino variables para almacenar soluciones
		archive ,archive_aux ,LS_archive, solutionArchive, vecindad, soluciones, listaVecinos, solucionAux = [], [], [], [], [], [], [], []
		numFac = poblacion[0].numFacilities	
		#Para cada solucion de la poblacion cuyo rank sea 1, debo agregarla al archive_aux, que contiene todas las soluciones pero solo 
		#usa las no repetidas para la LS
		for solucion in poblacion:
			if solucion.rank == 1:
				archive_aux.append(solucion)
		#Calculo su crowding de cada individuo y sort por dicho valor		
		archive_aux = self.crowdingDistanceAssignment(archive_aux)
		archive_aux = self.sortCrowding(archive_aux)
		#aqui elimino los repetidos	
		#for elemento in archive_aux:
		#	print elemento.solution, elemento.costoFlujo[0], elemento.costoFlujo[1], elemento.rank, elemento.crowdedDistance 
		for elemento in archive_aux:
			if elemento.solution not in soluciones:
				archive.append(elemento)
				soluciones.append(elemento.solution)
		del soluciones[:]
		#crear funcion para eliminar repetidos
		#print "Sin repetir"
		#for elemento in archive:
		#	print elemento.solution, elemento.costoFlujo[0], elemento.costoFlujo[1], elemento.rank, elemento.crowdedDistance 
		#Setear tamanio archive... como justificar tamaño seleccionado. 
		#SOlo para probar se utiliza que el tamano del archive sea como maximo el 10% del tamPob . Ej: Tam pob: 100 --> tam Archive = 10
		tamArchive = int(round(tamPob*0.2))
		print tamArchive
		#En caso que sea mayor a un 20% del tamanio de la poblacion es necesario reducir!
		#TRASPASAR A FUNCION! IGUAL QUE LA PARTE DE REPETIDAS!
		if len(archive) > tamArchive:
			print "MAYOR! A REDUCIR"
			#Si es mayor, elijo los miembros random (CAMBIAR Y PREGUNTAR SI HACERLO POR crowding distance)
			aux, aux_solution = [], []
			for i in range(tamArchive):
				elem = random.choice(archive)
				while elem.solution in aux_solution:
					elem = random.choice(archive)
				aux.append(elem)
				aux_solution.append(elem.solution)
				elem.visitado = 0
			del archive[:]
			archive = aux[:]
			del aux[:]
		#for elemento in archive:
		#	print elemento.solution, elemento.costoFlujo[0], elemento.costoFlujo[1], elemento.rank, elemento.crowdedDistance, elemento.visitado 
		
		while self.contadorVisitados(archive):
			solSeleccionada = self.seleccionar(archive)
			




	def generate_One_Neighbor(self, solucion, posiciones ):
		pos_Aux = []
		posiciones = []
		#Selecciono las posiciones, no pueden ser iguales
		posRandom1 = random.randint(0, numFac-1)
		posRandom2 = random.randint(0, numFac-1)
		while posRandom1 == posRandom2:
			posRandom2 = random.randint(0, numFac-1)
		posAux.append(posRandom1), posAux.append(posRandom2)
		while ((posAux in posiciones) or posAux.reverse() in posiciones):
			posRandom1 = random.randint(0, numFac-1)
			posRandom2 = random.randint(0, numFac-1)
			while posRandom1 == posRandom2:
				posRandom2 = random.randint(0, numFac-1)
			del posAux[:]	
			posAux.append(posRandom1), posAux.append(posRandom2)
		#Aca si o si deberia tener un par [rand1,rand2] que no esten en la lista de soluciones,
		# que contiene todos los movimientos hechos hasta ahora
		vecino = Solucion(numFac)
		vecino = self.swap(solucion, posAux[0], posAux[1], numFac)
		#Entonces genero el primer vecino, ahora debo iterar este proceso hasta encontrar dominante

	def buscarDominante(self, solucion):
		numFac = solucion.numFacilities
		posiciones = []
		vecino = Solucion(numFac)
		resultado = self.generate_One_Neighbor(solucion, posiciones)
		
		iterator = 0
		#Mientras el vecino NO domine a la solucion: Hay 3 casos... 
		#1.- si el vecino domina a la solucion no entra al while y pasa directo a ser agregada
		#2.- si la solucion domina al vecino 
		while not(funciones.dominance(vecino, solucion)):
			
			if funciones.dominance(solucion, vecino):
				posiciones.append(posAux)
			else:
				pass





	def paretoLocalSearch(self, poblacion, tamPob, alphaVec):
		archive, solutionArchive, vecindad, soluciones, listaVecinos, solucionAux = [], [], [], [], [], []
		numFac = poblacion[0].numFacilities
		#print "largo pob: ", len(poblacion)
		#Para cada solucion de la poblacion, si la solucion tiene rank 1 la agrego a mi archive
		#Ademas seteo su bit de visita en 0.
		for solucion in poblacion:
			#print solucion.solution
			if solucion.rank == 1:
				archive.append(solucion)
				solucion.visitado = 0
				#print solucion.solution
		#Mientras no esten todos los elementos del archive visitados
		while self.contadorVisitados(archive):
			#Para cada elemento en el archivo, agrego sus vectores solucion a un vector para 
			#.verificar que si se agregan elementos repetidos sea con el bit de visitado en 1.
			for elemento in archive:
				solutionArchive.append(elemento.solution)
			#Selecciono una solucion cuyo bit de visita sea 0.	
			#print "seleccionando y  obteniendo vecinos"
			solSeleccionada = self.seleccionar(archive)
			#Genero la vecindad TOTAL de la solucion seleccionada
			if alphaVec >= 0.9:
				vecindad = self.generoVecinos(solSeleccionada, numFac)
			else:
				vecindad = self.generarAlphaVecinos(solSeleccionada, alphaVec)
			#Agrego el elemento a la vecindad para analizarla con respecto a ND-Sort y Crowding
			vecindad.append(solSeleccionada)
			#Agrego para comprobar que este
			solucionAux.append(solSeleccionada.solution)
			#Realizo el proceso de FND Sort y luego ordeno por crowding distance de los vecinos
			#. con el fin de obtener solo los mejores vecinos, los cuales seran agregados al archive
			fronteras = self.fastNonDominatedSort(vecindad)
			vecindad = self.ordenPostBusqueda(vecindad, fronteras, tamPob)
			#Para cada vecino en la vecindad, selecciono solo los con ranking 1, los agrego tanto
			#. a la lista de listas con soluciones y a la lista de vecinos a agregar al archive.
			
			for vecino in vecindad:
				#print vecino.solution, vecino.costoFlujo[0], vecino.costoFlujo[1], vecino.rank, vecino.crowdedDistance
				
				if vecino.rank == 1:
					soluciones.append(vecino.solution)
					listaVecinos.append(vecino)
					#print "vecino a agregar: "
					#print vecino.solution, vecino.rank
			#print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
			#Si la solSeleccionada esta en las mejores soluciones, la agrego y su bit de visita en 1.
			#print "Se agregaran ", len(listaVecinos), "elementos"
			#print "agregando nuevas soluciones"
			if solSeleccionada.solution in soluciones:
				#print "esta!!!!!"
				solSeleccionada.visitado = 1
				#Ahora todos los elementos del vecindario deben ser agregados excepto la solucion 
				for elementoVecino in listaVecinos:
					#Si es la solSeleccionada, continuo
					if elementoVecino.solution in solucionAux:
						continue
					#Si no
					else:
						#Si el elementoVecino ya esta en el archive, lo agrego pero con bit de visitado en 1
						if elementoVecino.solution in solutionArchive:
							elementoVecino.visitado = 1
							#archive.append(elementoVecino)
							#Aqui tengo una duda... siempre que la solucion ya esta en el archive, hare un ordenamiento no dominada?
							#Deberia solo setear su bit de visita en 0, en otra parte debería ordenarlo, solo cuando se agregan...
							#REVISAR!!!!
							#self.fastNonDominatedSort(archive)
							#archive = self.actualizarArchive(archive)

						#Si no esta, simplemente lo agrego
						else:
							#Aca se justifica por que lo estoy agregando.... bien, 
							archive.append(elementoVecino)
							self.fastNonDominatedSort(archive)
							archive = self.actualizarArchive(archive)
				
				del listaVecinos[:]			
			
			elif solSeleccionada.solution not in soluciones:
				#print "NO esta !!"
				archive.remove(solSeleccionada)
				for elementoVecino in listaVecinos:
					if elementoVecino.solution in solutionArchive:
						elementoVecino.visitado = 1
						#archive.append(elementoVecino)
						#self.fastNonDominatedSort(archive)
						#archive = self.actualizarArchive(archive)
					else:
						archive.append(elementoVecino)
						self.fastNonDominatedSort(archive)
						archive = self.actualizarArchive(archive)					
				del listaVecinos[:]
			tamanoPonderar = tamPob*0.1
			if len(archive)	>= tamanoPonderar*tamPob:
				print "Population size bigger than setted: ", len(archive),
				print "Reducing Size. . ."
				fronteras = self.fastNonDominatedSort(archive)
				archive = self.ordenPostBusqueda(archive, fronteras, tamPob)
				for elem in archive:
					print elem.visitado,
			else:
				self.fastNonDominatedSort(archive)
				archive = self.actualizarArchive(archive)



			#print "elementos del archive: "
			#contador = 0
			#for elemento in archive:
			#	print elemento.solution, contador, elemento.visitado
			#	contador +=1
			#print "len Archive: ", len(archive)
				
			del solutionArchive[:]			
		#Debo chequear si el archive resultante es menor al tamanio de la poblacion,
		#. si esto se cumple es necesario generar mutaciones dentro de los mejores elementos 
		#. de la poblacion para llenar con mutaciones de buenas soluciones
		#. REVISARRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR!!!
		return archive			

	def actualizarArchive(self, archive):
		newArchive = []
		for elemento in archive:
			if elemento.rank == 1:
				newArchive.append(elemento)
		return newArchive	


	def contadorVisitados(self, archive):
		contador = 0
		for solucion in archive:
			if solucion.visitado == 1:
				contador += 1
				#print "contador del contadorVisitados", 
				#print contador
				if contador == len(archive):
					return False
				
			else:
				return True

	def ready(self, archive):
		contador = 0
		contadorVisita = 0
		listaSolVis = []
		for elemento in archive:
			listaAux = []
			listaAux.append(elemento.solution)
			listaAux.append(elemento.visitado)
			listaSolVis.append(listaAux)
		#print len(listaSolVis)
		i = 0
		largo = len(listaSolVis)	
		while contador != largo:
			#print len(listaSolVis)
			if len(listaSolVis) == 0:
				contador +=1
				break
			else:
				elemSolVis = random.choice(listaSolVis)
			#print "soy elemSolVis: ",
			#print elemSolVis
			if elemSolVis[1] == 1:
				contadorVisita += 1
				listaSolVis.remove(elemSolVis)
				#print "soy listaSolVis: ", listaSolVis
			elif elemSolVis[0] == 0:
				listaSolVis.remove(elemSolVis)
			contador += 1
		if contadorVisita == len(archive):
			#print "True"
			return False
		else:
			return True	




	def sortRanking(self, poblacion):
		for i in range(len(poblacion)-1, -1,-1):
			for j in range(1,i+1):
				sol1 = poblacion[j-1]
				sol2 = poblacion[j]
				if sol1.rank > sol2. rank:
					poblacion[j-1] = sol2
					poblacion[j] = sol1
		return poblacion

	def sortCostoAssignacion(self, poblacion, objetivo):
		#print "Iniciando sortCostoAsignacion. . ."
		for i in range(len(poblacion)-1,-1,-1):
			for j in range(1,i+1):
				sol1 = poblacion[j-1]
				sol2 = poblacion[j]
				if objetivo ==0:
					if sol1.costoFlujo[0] > sol2.costoFlujo[0]:
						poblacion[j-1] = sol2
						poblacion[j] = sol1
				elif objetivo ==1:
					if sol1.costoFlujo[1] > sol2.costoFlujo[1]:
						poblacion[j-1] = sol2
						poblacion[j] = sol1
		return poblacion

	def sortCrowding(self, poblacion):
		#print "Iniciando sortCrowding. . ."
		for i in range(len(poblacion)-1, -1, -1):
			for j in range(1,i+1):
				sol1 = poblacion[j-1]
				sol2 = poblacion[j]
				if (crowdedComparisonOperator(sol1, sol2) < 0):
					poblacion[j-1] = sol2
					poblacion[j] = sol1
		return poblacion

	def createNewPob(self, poblacion, indiceCX, indiceMut):
	
		print "Creating a new Population. . . "
		numFac = poblacion[0].numFacilities
		new_pob, rankedPop, restPop = [], [], []
		for elemento in poblacion:
			if elemento.rank == 1:
				rankedPop.append(elemento)
				new_pob.append(elemento)
			else:
				restPop.append(elemento)
		#AQUI SETEO EL % DE RANDOM
		indiceRand = 0.2
		indiceCruz = 1 - indiceRand
		largoRestante = len(poblacion)-len(new_pob)
		cantidadCX = int(round(largoRestante * indiceCruz))
		cantidadRand = int(round(largoRestante*indiceRand))
		for i in range(1, cantidadCX+1):
			child = Solucion(numFac)
			solSeleccionadas = [None, None]
			for i in range(2):
				sol1 = random.choice(rankedPop)
				sol2 = random.choice(restPop)
				if crowdedComparisonOperator(sol1, sol2) > 0:
					solSeleccionadas[i] = sol1
				else: 
					solSeleccionadas[i] = sol2
			if indiceCX == 1:
				if random.random() < self.crossoverRate:
					child = self.sequentialConstructiveCrossover(solSeleccionadas[0], solSeleccionadas[1])
			elif indiceCX == 2:
				if random.random() < self.crossoverRate:
					child = self.onePointCrossover(solSeleccionadas[0], solSeleccionadas[1])
			if indiceMut == 1:
				if random.random() < self.mutationRate:
					child = self.twOptSearch(child)
			elif indiceMut == 2:
				if random.random() < self.mutationRate:
					child = self.threExchangeMutation(child)
			new_pob.append(child)
		for i in range(1, cantidadRand+1):
			randomChild = Solucion(numFac)
			randomChild = funciones.generarSolucionRandom(randomChild, numFac)
			randomChild.costoAsignacion()
			new_pob.append(randomChild)
		del rankedPop[:]
		del restPop[:]

		return new_pob


	def makeNewPob(self, poblacion, indiceCX, indiceMUT, tamPob):
		print "Creating a new Population. . ."
		new_pob = []
		while len(new_pob) != tamPob:
			child = Solucion(poblacion[0].numFacilities)
			solSeleccionadas = [None, None]
			for i in range(2):
				sol1 = random.choice(poblacion)
				sol2 = random.choice(poblacion)
				if crowdedComparisonOperator(sol1, sol2) > 0:
					solSeleccionadas[i] = sol1
				else:
					solSeleccionadas[i] = sol2
			if indiceCX == 1:
				if random.random() < self.crossoverRate:
					child = self.sequentialConstructiveCrossover(solSeleccionadas[0], solSeleccionadas[1])
			elif indiceCX == 2:
				if random.random() < self.crossoverRate:
					child = self.onePointCrossover(solSeleccionadas[0], solSeleccionadas[1])
			if indiceMUT == 1:
				if random.random() < self.mutationRate:
					child = self.twOptSearch(child)
			elif indiceMUT == 2:
				if random.random() < self.mutationRate:
					child = self.threExchangeMutation(child)

			new_pob.append(child)
			for elem in new_pob:
				elem.costoAsignacion()
		return new_pob				

	def fastNonDominatedSort(self, poblacion):
		#print "Iniciando  Fast Non-Dominated-Sort"
		matrixFrontera = []
		fronteras = []
		for sol in poblacion:
			sol.rank = 0
		for solP in poblacion:
			for solQ in poblacion:
				if solP == solQ:
					continue
				if funciones.dominance(solP,solQ):
					solP.setSolDominadas.append(solQ)
				elif funciones.dominance(solQ,solP):
					solP.numSolDominantes += 1
			if solP.numSolDominantes == 0:
				solP.rank = 1
				fronteras.append(solP)
		matrixFrontera.append(fronteras)		
		cont_front = 1
		while len(fronteras) != 0:
			nextFront = []
			for solP in fronteras:
				for solQ in solP.setSolDominadas:
						solQ.numSolDominantes -= 1
						if solQ.numSolDominantes == 0:
							solQ.rank = cont_front+1
							nextFront.append(solQ)
			cont_front +=1
			#fronteras = nextFront[:]
			if(len(fronteras) == 0):
				continue
			else:
				matrixFrontera.append(fronteras)
			fronteras = nextFront[:]

		return matrixFrontera

	def crowdingDistanceAssignment(self,frontera):
		#print "Iniciando Crowded Distance Assignment. . ."
		largo = len(frontera)
		for sol in frontera:
			sol.crowdedDistance = 0.0
		for n_obj in range(0,self.numObjectives):
			frontera = self.sortCostoAssignacion(frontera, n_obj)
			if largo == 1:
				frontera[0].crowdedDistance = 0.0
			elif largo == 2:
				frontera[0].crowdedDistance = 2.0
				frontera[1].crowdedDistance = 2.0	
			else:
				frontera[0].crowdedDistance = float('Inf')
				frontera[largo-1].crowdedDistance = float('Inf')
				for i in range(1,largo-1):
					#pass
					#print frontera[i].crowdedDistance,
					#print frontera[i+1].costoFlujo[n_obj]
					if frontera[largo-1].costoFlujo[n_obj] - frontera[0].costoFlujo[n_obj] == 0:
						frontera[i].crowdedDistance = 0.0
					else: 
						frontera[i].crowdedDistance += (frontera[i+1].costoFlujo[n_obj] - frontera[i-1].costoFlujo[n_obj])/(frontera[largo-1].costoFlujo[n_obj] - frontera[0].costoFlujo[n_obj])
		return frontera
		

	def onePointCrossover(self,sol,other):
		#print "One Point Crossover beggining"
		numFac = sol.numFacilities
		child = Solucion(numFac)
		#sol.costoAsignacion(), other.costoAsignacion()
		#print "sol1: ",sol.solution, sol.costoFlujo[0], sol.costoFlujo[1]
		#print "Sol2:", other.solution, other.costoFlujo[0], other.costoFlujo[1]
		posRestringidas, posLibres, objPendiente  = [], [], []
		rangoA,rangoB = random.randint(0, numFac-1), random.randint(2, numFac-2)
		rangoC = rangoA+rangoB
		for x in range(rangoA,rangoC):
			indice = x%numFac
			elemento = sol.solution[indice]
			child.solution.insert(indice, elemento)
			posRestringidas.append(indice)
		for x in range(len(sol.solution)):
			if x not in posRestringidas:
				posLibres.append(x)
		for x in range(numFac):
			elem = other.solution[x]
			if elem in child.solution:
				continue
			else:
				objPendiente.insert(x, elem)
		cont = 0
		for x in posLibres:	
			child.solution.insert(x,objPendiente[cont])
			cont +=1
		#print "child: ", 
		child.costoAsignacion()
		#print child.solution, child.costoFlujo[0], child.costoFlujo[1]
		
		#print "One Point Crossover Finished"
		return child

	def sequentialConstructiveCrossover(self, sol, other):
		numFac = sol.numFacilities
		child = Solucion(numFac)
		soluciones = []
		soluciones.append(sol), soluciones.append(other)
		#print soluciones[0].solution, soluciones[1].solution
		sol.costoAsignacion(), other.costoAsignacion()
		#print "Costos iniciales de sol : ", sol.costoFlujo[0], sol.costoFlujo[1]
		#print "Costos iniciales de other: ", other.costoFlujo[0], other.costoFlujo[1]
		aux = random.choice(soluciones)
		locationP = aux.solution[0]
		#print aux.solution
		
		child.solution.insert(0, locationP)
		childAux1 = Solucion(numFac)
		childAux2 = Solucion(numFac)

		while len(child.solution) != len(sol.solution):

			nextElem = self.findNextLoc(soluciones[0], child, locationP, numFac)
			nextElem2 = self.findNextLoc(soluciones[1], child, locationP, numFac)

			childAux1.solution = child.solution[:]
			childAux2.solution = child.solution[:]


			childAux1.solution.append(nextElem)
			childAux2.solution.append(nextElem2)

			#print childAux1.solution, childAux2.solution
			childAux1.costoAsignacionParcial(nextElem)
			childAux2.costoAsignacionParcial(nextElem2)

			if funciones.dominance(childAux1, childAux2):
				
				child.solution = childAux2.solution[:]
				locationP = nextElem2
				del childAux1.solution[:]
				del childAux2.solution[:]

			elif funciones.dominance(childAux2, childAux1):
				child.solution = childAux1.solution[:]
				locationP = nextElem
				del childAux1.solution[:]
				del childAux2.solution[:]

			else:
				child.solution = childAux1.solution[:]
				locationP = nextElem
				del childAux1.solution[:]
				del childAux2.solution[:]

		child.costoAsignacion()		
		return child

	def findNextLoc(self, sol, child, locationP, numFac):
		index = sol.solution.index(locationP)
		#print "indice de location P: ", index
		for x in range(index+1, index+len(sol.solution)):
			elemento = sol.solution[x%numFac]
			if elemento in child.solution:
				continue
			else:
				return elemento
		

		
	def adaptiveMutation(self, sol, poblacion):
		raise "NOT IMPLEMENTED YET"

	

	def threExchangeMutation(self, sol):
		numFac = sol.numFacilities	
		posicionUno = random.randint(0,numFac-1)
		posicionDos = random.randint(0,numFac-1)
		while posicionUno == posicionDos:
			posicionDos = random.randint(0,numFac-1)
		posicionTres = random.randint(0,numFac-1)
		while posicionTres == posicionDos or posicionTres == posicionUno:
			posicionTres = random.randint(0,numFac-1)
		
		elementoPosUno = sol.solution[posicionUno]
		elementoPosDos = sol.solution[posicionDos]
		elementoPosTres = sol.solution[posicionTres]
 		
		solSwapeada = Solucion(numFac)
		solSwapeada.solution = sol.solution[:]
		
		a, b, c = solSwapeada.solution.index(elementoPosUno), solSwapeada.solution.index(elementoPosDos), solSwapeada.solution.index(elementoPosTres)
		
		solSwapeada.solution[b], solSwapeada.solution[a] = solSwapeada.solution[a], solSwapeada.solution[b]
		solSwapeada.solution[b], solSwapeada.solution[c] = solSwapeada.solution[c], solSwapeada.solution[b]

		solSwapeada.costoAsignacion()

		return solSwapeada

	def twOptSearch(self,sol):
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

	def binaryTournament(self,poblacion):
		participantes = random.sample(poblacion, 2)
		best = None
		for solParticipante in participantes:
			if (best is None) or self.crowdedComparisonOperator(solParticipante, best) == 1:
				best = solParticipante
		return best



	def seleccionar(self, archive):
		sol = random.choice(archive)
		while sol.visitado == 1:
			sol = random.choice(archive)
		return sol


	def generarAlphaVecinos(self, sol, alpha):
		numFac = sol.numFacilities
		tamVecindario = (numFac*(numFac-1))/2
		cantVecinos = tamVecindario*alpha
		cantVecinos = int(round(cantVecinos))
		vecindad, posiciones = [], []
		for i in range(cantVecinos):
			posAux = []
			posRandom1 = random.randint(0, numFac-1)
			posRandom2 = random.randint(0, numFac-1)
			while posRandom1 == posRandom2:
				posRandom2 = random.randint(0, numFac-1)
			posAux.append(posRandom1), posAux.append(posRandom2)
			while ((posAux in posiciones) or posAux.reverse() in posiciones):
				posRandom1 = random.randint(0, numFac-1)
				posRandom2 = random.randint(0, numFac-1)
				while posRandom1 == posRandom2:
					posRandom2 = random.randint(0, numFac-1)
				posAux.append(posRandom1), posAux.append(posRandom2)
			posiciones.append(posAux)
			vecino = Solucion(numFac)
			vecino = self.swap(sol, posRandom1, posRandom2, numFac)
			costos = sol.costoAsignacionMovida(posRandom1, posRandom2)
			vecino.costoFlujo[0] = sol.costoFlujo[0] - costos[0]
			vecino.costoFlujo[1] = sol.costoFlujo[1] - costos[1]
			vecindad.append(vecino)

		#print len(vecindad)	
		#for elem in vecindad:
		#	print elem.solution, elem.costoFlujo[0], elem.costoFlujo[1]
		return vecindad	

	def generoVecinos(self, sol, numFac):
		vecindad, soluciones = [], []
		for i in range(numFac):
			for j in range(numFac):
				if i != j:
					vecino = Solucion(numFac)
					vecino = self.swap(sol, i, j, numFac)
					if vecino.solution not in soluciones:
						soluciones.append(vecino.solution)
						costos = sol.costoAsignacionMovida(i,j)
						vecino.costoFlujo[0] = sol.costoFlujo[0] - costos[0]
						vecino.costoFlujo[1] = sol.costoFlujo[1] - costos[1]
						vecindad.append(vecino)
						#print vecino.solution
		del soluciones[:]
		#print len(vecindad)
		return vecindad

	def swap(self, sol, posicionUno, posicionDos, numFac):
		elementoPosUno = sol.solution[posicionUno]
		elementoPosDos = sol.solution[posicionDos]
		
		solSwapeada = Solucion(numFac)
		solSwapeada.solution = sol.solution[:]
		#solSwapeada = copy.deepcopy(sol)
		a, b = solSwapeada.solution.index(elementoPosUno), solSwapeada.solution.index(elementoPosDos)
		solSwapeada.solution[b], solSwapeada.solution[a] = solSwapeada.solution[a], solSwapeada.solution[b]
		return solSwapeada			





def crowdedComparisonOperator(sol, otherSol):
	if (sol.rank < otherSol.rank) or \
		((sol.rank == otherSol.rank) and (sol.crowdedDistance > otherSol.crowdedDistance)):
		return 1
	else: 
		return -1
















