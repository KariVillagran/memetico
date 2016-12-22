# -*- coding: utf-8 -*-

import funciones
import random
import numpy as np
import copy
import itertools
import matplotlib.pyplot as plt

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
		self.costoFlujo[0] = 0.0
		self.costoFlujo[1] = 0.0
		for k in range(self.numFacilities):
			if k != r and k != s:
				self.costoFlujo[0] += (funciones.matrixFlujoUno[s*self.numFacilities+k] - funciones.matrixFlujoUno[r*self.numFacilities+k])*(funciones.matrixDistancia[self.solution[s]*self.numFacilities+self.solution[k]] - funciones.matrixDistancia[self.solution[r]*self.numFacilities+self.solution[k]]) + (funciones.matrixFlujoUno[s*self.numFacilities+k] - funciones.matrixFlujoUno[r*self.numFacilities+k])*(funciones.matrixDistancia[self.solution[s]*self.numFacilities+self.solution[k]] - funciones.matrixDistancia[self.solution[r]*self.numFacilities+self.solution[k]])										
				self.costoFlujo[1] += (funciones.matrixFlujoDos[s*self.numFacilities+k] - funciones.matrixFlujoDos[r*self.numFacilities+k])*(funciones.matrixDistancia[self.solution[s]*self.numFacilities+self.solution[k]] - funciones.matrixDistancia[self.solution[r]*self.numFacilities+self.solution[k]]) + (funciones.matrixFlujoDos[s*self.numFacilities+k] - funciones.matrixFlujoDos[r*self.numFacilities+k])*(funciones.matrixDistancia[self.solution[s]*self.numFacilities+self.solution[k]] - funciones.matrixDistancia[self.solution[r]*self.numFacilities+self.solution[k]])						  
		#print "Costo Movida F1: ", self.costoFlujo[0]
		#print "Costo Movida F2: ", self.costoFlujo[1]			


class NSGA2:

	def __init__(self, numObjectives, mutationRate, crossoverRate):
		self.numObjectives = numObjectives
		self.mutationRate = mutationRate
		self.crossoverRate = crossoverRate

	def runAlgorithm(self, poblacion, tamPob, generaciones, cantIteraciones):
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
			#print "la cantidad de fronteras es: ", len(fronteras)

			del poblacion[:]

			for frontera in fronteras:
				if len(frontera)==0:
					break
				frontera = self.crowdingDistanceAssignment(frontera)
				for elem in frontera:
					poblacion.append(elem)

				if len(poblacion) >= tamPob:
					break
			self.sortCrowding(poblacion)
			if len(poblacion) > tamPob:
				del poblacion[tamPob:]
			
			nArchivo.write("Generacion: " + str(i) + "\n")
			for i in range(len(poblacion)):
				if i == generaciones:
					nArchivo.write("" +str(poblacion[i].solution)+ ", " + str(poblacion[i].costoFlujo[0]) + ", " + str(poblacion[i].costoFlujo[1]) + ", " + str(poblacion[i].rank) + "\n")
				else:
					nArchivo.write(""+ str(poblacion[i].costoFlujo[0]) + ", " + str(poblacion[i].costoFlujo[1]) + ", " + str(poblacion[i].rank) + "\n")
				
	
			if i == generaciones:
				break
				#funciones.graficarPob(poblacion)
			else:
				print "Comenzando Local Search. . ."
				nextP = self.paretoLS(poblacion, tamPob, cantIteraciones)
				nextPobla = self.makeNewPob(nextP)

		return poblacion

	def paretoLS(self, poblacion, tamPob, cantidadIteraciones):
		
		archive = []
		contador = 0
		numFac = poblacion[0].numFacilities
		for solucion in poblacion:
			if solucion.rank == 1:
				archive.append(solucion)
				solucion.visitado = 0
				#print solucion.solution
		solSeleccionada = self.seleccionar(archive)
		#print "solucion seleccionada: ", solSeleccionada.solution
		#print "costo de la solucion seleccionada en obj 1: ", solSeleccionada.costoFlujo[0],
		#print "costo de la solucion seleccionada en obj 2: ",  solSeleccionada.costoFlujo[1]
		while contador != cantidadIteraciones:
			#print "Generando Vecinos"
			vecindad = self.generoVecinos(solSeleccionada, numFac)
			for vecino in vecindad:
				#print "solucion vecina: ", vecino.solution
				#print "costo de la solucion vecina en obj 1: ", vecino.costoFlujo[0],
				#print "costo de la solucion vecina en obj 2: ",  vecino.costoFlujo[1]
				if funciones.dominance(vecino, solSeleccionada):
					#print "el vecino domina a la solucion seleccionada"
					
					archive = self.addAndUpdate(vecino, archive)
					
					#print "se agrega al archive y  se actualiza "
				elif funciones.dominance(solSeleccionada, vecino):
					#print "la solucion seleccionada domina al vecino"
					
					continue
				else:

					#print "ninguna se domina!"
					archive = self.addAndUpdate(vecino, archive)
					#print "se agrega al archive y  se actualiza "

			archive = np.array(archive)
			archive = np.unique(archive)
			archive = archive.tolist()
			solSeleccionada.visitado = 1
			contador += 1
			print contador
			if len(archive) >= tamPob:
				self.crowdingDistanceAssignment(archive)
				self.sortCrowding(archive)
				del archive[tamPob:]
			solSeleccionada = self.seleccionar(archive)
			#print "nueva solucion seleccionada. ", solSeleccionada.solution
		#Deberia ordenarlas por crowding ?
		newArchive = []
		newArchive.extend(archive)
		newArchive.extend(poblacion)
		
		print "poblacion:"
		for elem in poblacion:
			print elem.solution
		print "archive: "
		for elem in archive:
			print elem.solution
		print "new Archive:"
		for elem in newArchive:
			print elem.solution

		print "tamPob", tamPob
		print "len pobla:",len(poblacion)
		print "len archive",len(archive)
		#newArchive = self.fastNonDominatedSort(newArchive)
		#newArchive = np.array(newArchive)
		#newArchive = np.unique(newArchive)
		#newArchive = newArchive.tolist()
		#nuevoArchive = []
		print "FND SORTING ARCHIVE"
		print "len newArchive antes del del: ", len(newArchive)
		del newArchive[tamPob:]
		print "len newArchive",len(newArchive)
		return newArchive
		#Tengo que tomar la poblacion resultante del nsga2, tomarla y sacar solo las soluciones de la primera frontera y agregarlas
		#Al archivo que debe ser del mismo tamao que la poblacion resultante.
		#Selecciono una solucion del archivo 'solSeleccionada' 
		#mientras no se hayan visitado todas las soluciones del archivo se debe continuar. 
			#para cada solucion vecina del solSeleccionada
				#exploro su vecindario
				#si solucuionVecinadelaSeleccionada no es dominada por ninguna solucion del archivo:
					#debo chequear tambien si esta solucion domina a alguna.
					#Debo chequear el largo del archivo... ¿que pasa si esta lleno? o supera el tamao de m poblacion? 
					#la agrego al archivo (OJo: AGREGAR AL ARCHIVO DEBE CHEQUEAR SI ESA SOLUCION NUEVA DOMINA A ALGUNA QUE YA ESTA EN EL ARCHIVIO)
					#seteo su bit de visita en falso	
			#seteo el bit de visita en True de solSeleccionada
			#t = t  + 1 ... esto puede ser un contador, puede servir para algo... 
			#sol Seleccionada elegirDelArchivo(): Funcion que elige una solucion con el bit de visita en Falso del archivo.
					#Debo considerar las soluciones generadas en la iteracion pasada. 		 		



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
		print "Iniciando sortCostoAsignacion. . ."
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
		print "Iniciando sortCrowding. . ."
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
		print "Inicio FND-Sort"
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
		print "Crowded Distance Assignment"
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


	def addAndUpdate(self, solucion, archive):
		#print "comienzo addAndUpdate"
		archiveActualizado = []
		archiveActualizado.append(solucion)
		#print "solucion a analizar: ", solucion.solution
		#print "costo de la solucion obj 1: ", solucion.costoFlujo[0],
		#print "costo solucion obj 2: ",  solucion.costoFlujo[1]
		for elemento in archive:
			#print "solucion a comparar: ", elemento.solution
			#print "costo sol obj 1: ", elemento.costoFlujo[0],
			#print "costo sol obj 2: ",  elemento.costoFlujo[1] 
			#Si encuentro una solucion vecina dominada por mi solucion inicial, continuo
			if funciones.dominance(solucion, elemento):
				#print "la solucion a analizar domina a la solucion a comparar"
				continue
			elif funciones.dominance(elemento, solucion):
				#print "la solucion a comparar domina a la solucion a analizar"
				continue
			#Si encuentro una solucion que es no-dominada por esta nueva solucion ND agregada:
			else:
				#print "ninguna se domina!" 
				archiveActualizado.append(elemento)
				#print "se agrega al archive"
		archiveActualizado = np.array(archiveActualizado)
		archiveActualizado = np.unique(archiveActualizado)
		archiveActualizado = archiveActualizado.tolist()		
		#print "termino addAndUpdate"
		return archiveActualizado

	def contadorVisitados(self, archive, tamPob):
		contador = 0
		for solucion in archive:
			if solucion.visitado == 1:
				contador += 1
				if contador == tamPob:
					return False
				print "contador del contadorVisitados", 
				print contador
			else:
				return True

	def generoVecinos(self, sol, numFac):
		vecindad, soluciones = [], []

		#numFac = solucion.numFacilities
		for i in range(numFac):
			for j in range(numFac):
				if i != j:
					vecino = Solucion(numFac)
					vecino = self.swap(sol, i, j, numFac)
					if vecino.solution not in soluciones:
						soluciones.append(vecino.solution)
						vecino.costoAsignacion()
						vecindad.append(vecino)
						#print "vecino:", 
						#print vecino.solution
		del soluciones[:]
		#print len(vecindad)
		return vecindad


	def swap(self, sol, posicionUno, posicionDos, numFac):
		elementoPosUno = sol.solution[posicionUno]
		elementoPosDos = sol.solution[posicionDos]
		solSwapeada = copy.deepcopy(sol)
		a, b = solSwapeada.solution.index(elementoPosUno), solSwapeada.solution.index(elementoPosDos)
		solSwapeada.solution[b], solSwapeada.solution[a] = solSwapeada.solution[a], solSwapeada.solution[b]
		return solSwapeada			




def crowdedComparisonOperator(sol, otherSol):
	if (sol.rank < otherSol.rank) or \
		((sol.rank == otherSol.rank) and (sol.crowdedDistance > otherSol.crowdedDistance)):
		return 1
	else: 
		return -1
















