# -*- coding: utf-8 -*-
def paretoLS(self, poblacion, tamPob, cantidadIteraciones):
		
		archive = []
		contador = 0
		numFac = poblacion[0].numFacilities
		#print "largo pob: ", len(poblacion)
		for solucion in poblacion:
			print solucion.solution
			if solucion.rank == 1:
				archive.append(solucion)
				solucion.visitado = 0
				#print solucion.solution
		solSeleccionada = self.seleccionar(archive)
		#print "solucion seleccionada: ", solSeleccionada.solution
		#print "costo de la solucion seleccionada en obj 1: ", solSeleccionada.costoFlujo[0],
		#print "costo de la solucion seleccionada en obj 2: ",  solSeleccionada.costoFlujo[1]
		contadorItera = 0
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
					#contadorItera = 0
					#print "se agrega al archive y  se actualiza "
				elif funciones.dominance(solSeleccionada, vecino):
					#print "la solucion seleccionada domina al vecino"
					#contador += 1
					#contadorItera += 1
					#print contadorItera
					continue
				else:
					
					#print "ninguna se domina!"
					archive = self.addAndUpdate(vecino, archive)
					#contadorItera = 0
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
		#print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		#print "elementos del archive: "
		#for elem in archive:
		#	print elem.solution
		newArchive = []
		newArchive.extend(archive)
		#print "Len con solo el archive: ", len(newArchive)
		newArchive.extend(poblacion)
		#print "len con archive y poblacion", len(newArchive)
		#print "poblacion:"
		#for elem in poblacion:
		#	print elem.solution
		#print "archive: "

		#print "new Archive:"
		#for elem in newArchive:
		#	print elem.solution

		#print "tamPob", tamPob
		#print "len pobla:",len(poblacion)
		#print "len archive",len(archive)
		
		del newArchive[tamPob:]
		#print "len newArchive",len(newArchive)
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
		#print "el archive esta compuesto por: "
		#for elem in archiveActualizado:
		#	print elem.solution,
		#print "termino addAndUpdate"
		return archiveActualizado


		#tamArchive = int(round(tamPob*0.2))
		#print tamArchive
		
		#En caso que sea mayor a un 20% del tamanio de la poblacion es necesario reducir!
		#TRASPASAR A FUNCION! IGUAL QUE LA PARTE DE REPETIDAS!
		
		#if len(archive) > tamArchive:
		#	print "MAYOR! A REDUCIR"
			#Si es mayor, elijo los miembros random (CAMBIAR Y PREGUNTAR SI HACERLO POR crowding distance)
		#	aux, aux_solution = [], []
		#	for i in range(tamArchive):
		#		elem = random.choice(archive)
		#		while elem.solution in aux_solution:
		#			elem = random.choice(archive)
		#		aux.append(elem)
		#		aux_solution.append(elem.solution)
		#		elem.visitado = 0
		#	del archive[:]
		#	archive = aux[:]
		#	del aux[:]
		#for elemento in archive:
		#	print elemento.solution, elemento.costoFlujo[0], elemento.costoFlujo[1], elemento.rank, elemento.crowdedDistance, elemento.visitado 
	