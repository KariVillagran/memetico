# -*- coding: utf-8 -*-

import funciones
import random
import numpy as np
import copy
import itertools
import datetime
import os
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
		self.movimientos = []
		self.cyclePositions = []

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
		self.numberOfEvaluations = 0
		self.completado = False
			

	def checkNumEvalua(self, maxNE):
		if self.completado is False:
			return True
		else:
			return False


	def runAlgorithm(self, poblacion, tamPob, indCX, start, nEvalua):
		
		startTime = start
		tiempo = funciones.convertTime(startTime)
		self.directorio = "results/Results_"+tiempo
		os.makedirs(self.directorio)
		nextPobla = self.makeNewPob(poblacion, indCX, tamPob)
		self.numberOfEvaluations += tamPob
		nombreArchivo = self.directorio + "/generaciones.csv"
		nArchivo = open(nombreArchivo, 'w' )
		filePareto = self.directorio + "/pareto.csv"	
		counter = 1
		archiveHyperVolume = []
		#for i in range(1,generaciones+1):
		while self.checkNumEvalua(nEvalua):
			print "++++++++++++++++++++++++++++++++++++++++++++++++++++++"
			print "Generation Number: ", counter
			#print "from a Total of ", generaciones
			print "++++++++++++++++++++++++++++++++++++++++++++++++++++++"
			pobCombinada = []
			print "Extending Populations into Combined Population. . ."
			
			pobCombinada.extend(poblacion)
			pobCombinada.extend(nextPobla)

			print "Fast Non-Dominated Sorting of Combined Population. . . " 

			fronteras = self.fastNonDominatedSort(pobCombinada)
			poblacion = self.ordenPostBusqueda(pobCombinada, fronteras, tamPob)

			
			nArchivo.write("Generacion: " + str(counter) + "\n")
			for j in range(len(poblacion)):
				nArchivo.write(""+ str(poblacion[j].costoFlujo[0]) + ", " + str(poblacion[j].costoFlujo[1]) + ", " + str(poblacion[j].rank) + ", " +  str(poblacion[j].crowdedDistance) +"\n")
			
			if counter != 1:
				poblacion = self.makeNewPob(poblacion, indCX, tamPob)
				self.numberOfEvaluations += tamPob
				
				print "Fast Non-Dominated Sorting of new population. . .  "
				fronteras = self.fastNonDominatedSort(poblacion)
				#print "la cantidad de fronteras es: ", len(fronteras)
				poblacion = self.ordenPostBusqueda(poblacion, fronteras, tamPob)
			
			print "Local Search is beggining. . . "	
			nextPobla = self.memoryBasedPLS(poblacion, tamPob, 10)
			print "Local Search has ended."
			#for elemento in nextPobla:
				#print elemento.solution, elemento.costoFlujo
			if self.numberOfEvaluations >= nEvalua:
				print "Evaluation limit reached... "
				print "Number of total fitness evaluation: ", self.numberOfEvaluations
				print "++++++++++++++++++++++++++++++++++++++++++++++++++++++"
				print "Resumen: P = ", tamPob, "nEval = ", nEvalua
				fPareto = open(filePareto, 'w')
				pobCombi = []
				pobCombi.extend(poblacion)
				pobCombi.extend(nextPobla)
				
				for elemento in pobCombi:
					if elemento.rank == 1:
						fPareto.write(""+ str(elemento.costoFlujo[0]) + ", " + str(elemento.costoFlujo[1]) + ", " + str(elemento.crowdedDistance) + ", " + str(elemento.rank) + "\n")
				fPareto.close()

				self.completado = True		
			counter += 1
		
		stopTime = datetime.datetime.now()
		final = stopTime - startTime
		nArchivo.seek(0)
		nArchivo.write("Final time of Execution: " + str(final) + "\n")
		nArchivo.close()
		print "Algorithm finished in: " , str(final)


	def ordenPostBusqueda(self, poblacion, fronteras, tamPob):
		
		del poblacion[:]
		for front in fronteras:
			self.crowdingDistanceAssignment(front)
			for elem in front:
				poblacion.append(elem)
		self.sortCrowding(poblacion)
		if len(poblacion) > tamPob:
			#print "es mayor"
			poblacion = poblacion[:tamPob]
		#for elemento in poblacion:
			#print elemento.solution, elemento.rank
		return poblacion

	def memoryBasedPLS(self, poblacion, tamPob, numEntrantes):
		#Defino variables para almacenar soluciones
		archive ,archive_aux ,LS_archive, solutionArchive, vecindad, soluciones, listaVecinos, solucionAux = [], [], [], [], [], [], [], []
		numFac = poblacion[0].numFacilities	
		#Aqui se almacenan los vecinos dominantes obtenidos en la busqueda... 
		paretoArchive = []
		#aqui se almacenan los vecinos candidatos no-dominantes obtenidos en la busqueda
		candidatesNonDom = []
		#Aqui se almacenan los que entran al archive...
		vecinosNDAceptados = []
		#Para cada solucion de la poblacion cuyo rank sea 1, debo agregarla al archive_aux, que contiene todas las soluciones pero solo 
		#usa las no repetidas para la LS
		for solucion in poblacion:
			#if solucion.rank == 1:
			archive_aux.append(solucion)
		#Calculo su crowding de cada individuo y sort por dicho valor		
		archive_aux = self.crowdingDistanceAssignment(archive_aux)
		archive_aux = self.sortCrowding(archive_aux)
		#aqui elimino los repetidos	
		#for elemento in archive_aux:
		#	print elemento.solution, elemento.costoFlujo[0], elemento.costoFlujo[1], elemento.rank, elemento.crowdedDistance 
		for elemento in archive_aux:
			if elemento.solution not in soluciones:
				elemento.visitado = 0
				archive.append(elemento)
				soluciones.append(elemento.solution)
		del soluciones[:]
		#print "Elementos en el archive: "
		#for elemento in archive:
		#	print elemento.solution, elemento.costoFlujo
		#crear funcion para eliminar repetidos
		#print "Sin repetir"
		#for elemento in archive:
		#	print elemento.solution, elemento.costoFlujo[0], elemento.costoFlujo[1], elemento.rank, elemento.crowdedDistance 
		
		#Setear tamanio archive... como justificar tamaño seleccionado. 
		#SOlo para probar se utiliza que el tamano del archive sea como maximo el 10% del tamPob . Ej: Tam pob: 100 --> tam Archive = 10
		# ACA DEFINO TAMANIO DEL ARCHIVE, PERO POR AHORA NO LO USO. SE VA A CODIGO VIEJO

		#Tengo el archive listo, falta un t.
		t = 0
		#Mientras no haya visitado todas las soluciones del archive...
		while self.contadorVisitados(archive):
			#Selecciono una solucion no visitada
			#print "el archivo de entrada es..."
			#for elemento in archive:
			#	print elemento.solution, elemento.costoFlujo, elemento.visitado
			solSeleccionada = self.seleccionar(archive)
			#print "La sol seleccionada es: ",solSeleccionada.solution, solSeleccionada.costoFlujo
			#Obtengo un vecino dominante
			vecinosObtenidos = self.buscarDominante(solSeleccionada)

			#print "Los elementos en el vecinos obtenidos son:"
			#for elemento in vecinosObtenidos[1]:
			#	print elemento.solution
			#print "tamanio del vector de vecinosObtenidos: ", len(vecinosObtenidos[1])
			#Ahora debo comparar al vecino dominante con las soluciones en el archive, si el vecino es no-weakly-dominante con todas
			#las soluciones del archivo... entonces ahi agrego al vecino y elimino a la solucion de donde la obtuve. 
			vecino = Solucion(numFac)
			vecino = vecinosObtenidos[0]
			#print "El vecino obtenido es: ", vecino.solution, vecino.costoFlujo
			if len(vecinosObtenidos) > 1:
				for i in range(1,len(vecinosObtenidos)):
					candidatesNonDom.append(vecinosObtenidos[i])
			
			#print "candidates nondom deberian ser los mismos que en vecinso obtenidos"
			#for elemento in candidatesNonDom:
			#	print elemento.solution

			#Luego de estas ultimas 4 lineas ya tendre al vecino candidato para el PARETO ARCHIVE
			# y las 'x' nuevas soluciones candidatas para poblar el archive... 	
			#Primer caso... agrego el vecino a la pareto-archive solo si es no dominante con esta...
			
			#Caso 1.1: Si dentro de la busqueda no se encuentra un vecino dominante, es decir, se retorna la misma solucion...
			# entonces se setea el bit de visita de SolSeleccionada en 1 y se continua la búsqueda
			if solSeleccionada.solution == vecino.solution:
				#print "El vecino es igual a la solucion seleccionada..."
				solSeleccionada.visitado = 1
			#Caso 1.2: Si se encuentra un vecino dominante entonces se debe comparar el vecino con el Pareto-archive. Solo si el vecino es no-dominado
			# con el archive, se agrega, si se encuentra un elemento del archive que es dominado por el vecino, se elimina.
			#Y si un elemento del archive domina al vecino se debe eliminar, y continuar la busqueda. 
			else:
				#La variable question es la pregunta para ver si se puede agregar el vecino al archive
				question = self.checkArchive(vecino, paretoArchive)
				#Si es True, entonces debo agregar el vecino al archive y eliminar todos los elementos dominados por este
				# Debo chequear que el vecino no se encuentre en el archivo, si el vecino ya esta ingresado no se agrega. 
				if question:
					paretoArchive = self.updateArchive(vecino, paretoArchive)
					#PARAMETRO QUE DEBO REVISAR... COMO SABER CUANTOS INGRESO AL ARCHIVE....
					if len(candidatesNonDom)>1:
						if len(candidatesNonDom) < numEntrantes:
							archive = self.filtrarRepetidos(archive, candidatesNonDom)
						else:
							filtro = self.obtenerAlphaRandom(candidatesNonDom, numEntrantes)
							archive = self.filtrarRepetidos(archive, filtro)
						
													

				#Si es False, continuo la busqueda.
				else:
				#	print "No puedo agregarlo, continuo..."
					solSeleccionada.visitado = 1
				#print "elementos en el archive actualizados..."
				#for elemento in paretoArchive:
				#	print elemento.solution, elemento.costoFlujo
				#print "fin elementos archivo actualizado..."
		#print evaluations
		return paretoArchive

	def obtenerAlphaRandom(self, candidates, numEntrantes):
		filtro = []
		for i in range(numEntrantes):
			elemento = random.choice(candidates)
			candidates.remove(elemento)
			filtro.append(elemento)
		return filtro



	def filtrarRepetidos(self, archive, filtro):
		archiveSolution = []
		contRepetidos = 0
		for elemento in archive:
			archiveSolution.append(elemento.solution)
		for candidato in filtro:
			if candidato.solution in archiveSolution:
				contRepetidos += 1
			else:
				archive.append(candidato)
		#print "la cantidad de elementos repetidos y que no se agregaron es: ", contRepetidos
		return archive


					

	def updateArchive(self, solucion, archive):
		updatedArchive = []
		counter = 0
		if len(archive)==0:
			updatedArchive.append(solucion)
			return updatedArchive
		else:
			for elemento in archive:
				if funciones.dominance(solucion, elemento):
					counter += 1
				else:
					updatedArchive.append(elemento)
		updatedArchive.append(solucion)
		#print "la cantidad de elementos que domina es: ", counter
		return updatedArchive

			
	

	#Con esta funcion solo chequeo si la solucion a agregar es no-dominado por el resto del archive.
	def checkArchive(self, solucion, archive):
		contador = 0
		soluciones = []
		if len(archive) == 0:
			return True
		for elemento in archive:
			if elemento.solution not in soluciones:
				soluciones.append(elemento.solution)
		if solucion.solution in soluciones:
			return False

		for elemento in archive:
			#Si encuentro un elemento dentro del archive que domina a la solucion candidata se acaba la busqueda y no se puede agregar el vecino
 			if funciones.dominance(elemento, solucion):
 				#print "False"
 				return False
 			#Si la solucion domina a algun elemento 	
 			else:
 				contador += 1

 		if contador == len(archive):
 			#print "True"
 			return True

			
	def generate_One_Neighbor(self, solucion, posiciones ):
		numFac = solucion.numFacilities
		posAux = []
		#Selecciono las posiciones, no pueden ser iguales
		posRandom1 = random.randint(0, numFac-1)
		posRandom2 = random.randint(0, numFac-1)
		while posRandom1 == posRandom2:
			posRandom2 = random.randint(0, numFac-1)
		posAux.append(posRandom1), posAux.append(posRandom2)
		posAuxRev = posAux[::-1]
		
		while ((posAux in posiciones) or posAuxRev in posiciones):
			#print "UPS! Las posiciones a cambiar ya estan repetidas...:", posAux
			#print "Posiciones ya utilizadas, se generan nuevamente . . ."
			posRandom1 = random.randint(0, numFac-1)
			posRandom2 = random.randint(0, numFac-1)
			while posRandom1 == posRandom2:
				posRandom2 = random.randint(0, numFac-1)
			del posAux[:]	
			posAux.append(posRandom1), posAux.append(posRandom2)
			posAuxRev = posAux[::-1]
		#Aca si o si deberia tener un par [rand1,rand2] que no esten en la lista de soluciones,
		# que contiene todos los movimientos hechos hasta ahora
		#print "Las posiciones a cambiar:", posAux
		vecino = Solucion(numFac)
		vecino = self.swap(solucion, posAux[0], posAux[1], numFac)
		costos = solucion.costoAsignacionMovida(posAux[0], posAux[1])
		vecino.costoFlujo[0] = solucion.costoFlujo[0] - costos[0]
		vecino.costoFlujo[1] = solucion.costoFlujo[1] - costos[1]
		vecino.movimientos.append(posAux[0])
		vecino.movimientos.append(posAux[1])
		#Entonces genero el primer vecino, ahora debo iterar este proceso hasta encontrar dominante
		return vecino

	def buscarDominante(self, solucion):
		numFac = solucion.numFacilities
		posiciones = []
		vecino = Solucion(numFac)
		vecino = self.generate_One_Neighbor(solucion, posiciones)
		self.numberOfEvaluations +=1
		iterator = 1
		tamVecindario = (numFac*(numFac-1))/2
		searchLimit = int(round(tamVecindario*0.95))
		vecinosNoDom = []
		vecino_DomYCandidatos = []
		#Mientras el vecino NO domine a la solucion: Hay 3 casos... 
		#1.- si el vecino domina a la solucion no entra al while y pasa directo a ser agregada
		#2.- si la solucion domina al vecino entonces agrego la posicion generada
		while not(funciones.dominance(vecino, solucion)):
			#Si la solucion domina al vecino, se agregan las posiciones utilizadas
			if funciones.dominance(solucion, vecino):
				#print "La solucion domina al vecino", vecino.solution, vecino.costoFlujo
				posiciones.append(vecino.movimientos)
				vecino = self.generate_One_Neighbor(solucion, posiciones)
				self.numberOfEvaluations +=1
				iterator += 1
				if iterator >= searchLimit:
					break
			else:
				#print "El vecino y la solucion son no-dominadas entre si", vecino.solution, vecino.costoFlujo
				posiciones.append(vecino.movimientos)
				vecino_DomYCandidatos.append(vecino)
				vecino = self.generate_One_Neighbor(solucion, posiciones)
				self.numberOfEvaluations +=1
				iterator += 1
				if iterator >= searchLimit:
					break
		if iterator >= searchLimit:
			vecino_DomYCandidatos.insert(0,solucion)
			#print "no se encontraron resultados e iterator es: ", iterator
			return vecino_DomYCandidatos
		#print "El vecino dominantes es: ", vecino.solution, vecino.costoFlujo
		#print "y se encontro en la iteracion: ", iterator	
		vecino_DomYCandidatos.insert(0, vecino)
		return vecino_DomYCandidatos


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


	def makeNewPob(self, poblacion, indiceCX, tamPob):
		print "Creating a new Population. . ."
		new_pob = []
		#childs = []
		while len(new_pob) != tamPob:
			#print "new_pob vs tamPOb:", len(new_pob), tamPob
			#child = Solucion(poblacion[0].numFacilities)
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
					childs = self.cycleCrossover(solSeleccionadas[0], solSeleccionadas[1])
				if random.random() < self.mutationRate:
					for chil in childs:
						chil = self.threExchangeMutation(chil)
				for chil in childs:
					new_pob.append(chil)
					if len(new_pob) == tamPob:
						break
			elif indiceCX == 2:
				child = Solucion(poblacion[0].numFacilities)
				if random.random() < self.crossoverRate:
					child = self.onePointCrossover(solSeleccionadas[0], solSeleccionadas[1])
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
			fronteras = nextFront[:]
			if(len(fronteras) == 0):
				continue
			else:
				matrixFrontera.append(fronteras)
			#fronteras = nextFront[:]

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
		

	def cycleCrossover(self, sol, other):
		numFac = sol.numFacilities
		child1 = Solucion(numFac)
		child2 = Solucion(numFac)
		auxSolution = []
		for elemen in sol.solution:
			auxSolution.append(elemen)
		child1.solution = [None for i in range(numFac)]
		child2.solution = [None for i in range(numFac)]
		
		cycles = []
		childs =  []
		#Posicion inicial de donde parte el operador
		firstPos = 0
		#Bandera para asegurarse que la insercion sobre lso hijos es reversa 
		flag = True
		auxSolution[firstPos] = -1
		while len(cycles) != len(sol.solution):
			#Tomo la "firstPos" que solo en un principio es 0. luego debe ir iterando
			elem1 = sol.solution[firstPos]
			elem2 = other.solution[firstPos]
			cycle = []
			cycle.append(elem1), cycle.append(elem2)
			cyclePos = []
			if flag:
				cyclePos.append(firstPos), cyclePos.append(elem1), cyclePos.append(elem2)
			else:
				cyclePos.append(firstPos), cyclePos.append(elem2), cyclePos.append(elem1)
			cycles.append(cyclePos)
			auxSolution[firstPos] = -1
			if elem1 != elem2:
				while cycle[0] != cycle[len(cycle)-1]:
					cyclePos = []
					firstPos = sol.solution.index(cycle[len(cycle)-1])
					elem1 = sol.solution[firstPos]
					elem2 = other.solution[firstPos]
					cycle.append(elem2)
					if flag:
						cyclePos.append(firstPos), cyclePos.append(elem1), cyclePos.append(elem2)
					else:
						cyclePos.append(firstPos), cyclePos.append(elem2), cyclePos.append(elem1)
					cycles.append(cyclePos)
					auxSolution[firstPos] = -1
				#Selecciono nueva posicion
				for elem in auxSolution:
					if elem != -1:
						firstPos = auxSolution.index(elem)
						break
			else:
				for elem in auxSolution:
					if elem != -1:
						firstPos = auxSolution.index(elem)
						break
			if flag:
				flag = False
			else: 
				flag = True	
		for listaPosElem in cycles:
			child1.solution[listaPosElem[0]] = listaPosElem[1] 
			child2.solution[listaPosElem[0]] = listaPosElem[2]
		childs.append(child1)
		childs.append(child2)
		return childs

				



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
















