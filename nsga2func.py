# -*- coding: utf-8 -*-

import funciones
import random
import numpy as np
import copy
import itertools
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


class NSGA2:

	def __init__(self, numObjectives, mutationRate, crossoverRate):
		self.numObjectives = numObjectives
		self.mutationRate = mutationRate
		self.crossoverRate = crossoverRate

	def runAlgorithm(self, poblacion, tamPob, generaciones):
		print "tamPob INICIAL: ",tamPob
		for sol in poblacion:
			sol.costoAsignacion()
		lastIteration = generaciones-1	
		nextPobla = self.makeNewPob(poblacion)
		for sol in nextPobla:
			sol.costoAsignacion()
		nombreArchivo = "generaciones.csv"
		nArchivo = open(nombreArchivo, 'w' )	
		for i in range(1,generaciones+1):
			print "+++++++++++++++++++"
			print "Iteracion: ", i,
			print "de un total de ", generaciones
			print "+++++++++++++++++++"
			pobCombinada = []
			pobCombinada.extend(poblacion)
			pobCombinada.extend(nextPobla)

			fronteras = self.fastNonDominatedSort(pobCombinada)
			
			poblacion = self.ordenPostBusqueda(pobCombinada, fronteras, tamPob)


			nArchivo.write("Generacion: " + str(i) + "\n")
			for i in range(len(poblacion)):
				nArchivo.write(""+ str(poblacion[i].costoFlujo[0]) + ", " + str(poblacion[i].costoFlujo[1]) + ", " + str(poblacion[i].rank) + ", " +  str(poblacion[i].crowdedDistance) +"\n")
				
	
			if i == generaciones:
				break
				#funciones.graficarPob(poblacion)
			else:
				
				poblacion = self.makeNewPob(poblacion)
				fronteras = self.fastNonDominatedSort(poblacion)
				#print "la cantidad de fronteras es: ", len(fronteras)
				poblacion = self.ordenPostBusqueda(poblacion, fronteras, tamPob)
				print "Comenzando Local Search. . ."	
				nextPobla = self.paretoLocalSearch(poblacion, tamPob)
				#print "largo resultado LS: ", len(nextPobla)
				#nextPobla = self.paretoLoc(poblacion, tamPob, cantIteraciones)
		return poblacion

	def ordenPostBusqueda(self, poblacion, fronteras, tamPob):
		del poblacion[:]
		for frontera in fronteras:
			if len(frontera)==0:
				break
			frontera = self.crowdingDistanceAssignment(frontera)
			for elemento in frontera:
				poblacion.append(elemento)

			if len(poblacion) >= tamPob:
				break	
		self.sortCrowding(poblacion)
		if len(poblacion) >= tamPob:
			del poblacion[tamPob:]
		return poblacion


	def paretoLocalSearch(self, poblacion, tamPob):
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
			vecindad = self.generoVecinos(solSeleccionada, numFac)
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
				if vecino.rank == 1:
					soluciones.append(vecino.solution)
					listaVecinos.append(vecino)
					#print "vecino a agregar: "
					#print vecino.solution
			#Si la solSeleccionada esta en las mejores soluciones, la agrego y su bit de visita en 1.
			#print "Se agregaran ", len(listaVecinos), "elementos"
			#print "agregando nuevas soluciones"
			if solSeleccionada.solution in soluciones:
				#print "esta!!!!!"
				solSeleccionada.visitado = 1
				#Ahora todos los elementos del vecindario deben ser agregados excepto la solucion 
				for elementoVecino in listaVecinos:
					#Si es la solSeleccionada, continuo
					if elementoVecino in solucionAux:
						continue
					#Si no
					else:
						#Si el elementoVecino ya esta en el archive, lo agrego pero con bit de visitado en 1
						if elementoVecino.solution in solutionArchive:
							elementoVecino.visitado = 1
							archive.append(elementoVecino)
						#Si no esta, simplemente lo agrego
						else:
							archive.append(elementoVecino)
				del listaVecinos[:]			
			
			elif solSeleccionada.solution not in soluciones:
				#print "NO esta !!"
				archive.remove(solSeleccionada)
				for elementoVecino in listaVecinos:
					if elementoVecino.solution in solutionArchive:
						elementoVecino.visitado = 1
						archive.append(elementoVecino)
					else:
						archive.append(elementoVecino)
				del listaVecinos[:]
			tamanoPonderar = tamPob*0.1
			if len(archive)	>= tamanoPonderar*tamPob:
				print "Se supera el tamaño de poblacion, reduciendo tamaño", len(archive)
				fronteras = self.fastNonDominatedSort(archive)
				archive = self.ordenPostBusqueda(archive, fronteras, tamPob)
				del archive[tamPob:]
				for elem in archive:
					print elem.visitado,


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

	def makeNewPob(self, poblacion):
		print "Creando una nueva poblacion. . ."
		new_pob = []
		while len(new_pob) != len(poblacion):
			child = Solucion(poblacion[0].numFacilities)
			solSeleccionadas = [None, None]
			while solSeleccionadas[0] == solSeleccionadas[1]:
				for i in range(2):
					sol1 = random.choice(poblacion)
					sol2 = random.choice(poblacion)
					while sol1 == sol2:
						sol2 = random.choice(poblacion)
					if crowdedComparisonOperator(sol1, sol2) > 0:
						solSeleccionadas[i] = sol1
					else:
						solSeleccionadas[i] = sol2
			if random.random() < self.crossoverRate:
				child = self.onePointCrossover(solSeleccionadas[0], solSeleccionadas[1])

			if random.random() < self.mutationRate:
				child = self.twOptSearch(child)

			child.costoAsignacion()
			new_pob.append(child)

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
			fronteras = nextFront
			if(fronteras == []):
				continue
			else:
				matrixFrontera.append(fronteras)
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
		#print child
		#print "One Point Crossover Finished"
		return child

	def sequentialConstructiveCrossover(self, sol, other):
		raise "Not implemented yet"

	def adaptiveMutation(self, sol):
		raise "Not implemented yet"

		

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
















