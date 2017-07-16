# -*- coding: utf-8 -*-


import numpy as np
import os
from hv import HyperVolume
import datetime
import matplotlib as mpl
import shutil

#mpl.use('agg')
 
import matplotlib.pyplot as plt

#plt.switch_backend('Qt5Agg')  
plt.style.use('ggplot')
#Creo matriz con 15 elementos, distribuidos en dimensiones (3,5), es decir, 3 arreglos de tamaño 5 cada uno
a = np.arange(15).reshape(3,5)
#Creo array
b = np.array([6,7,8])
#Creo array con dimensiones y EDA que yo decida
c = np.array([(1,2,3), (1,4,3)], dtype = float)
# Funciones: 
# np.zero((3,4)) ---> Crea matriz con ceros
# np.ones((3,4)) ---> Crea matriz con unos
# np.empty((2,3)) --> Crea matriz con random float64
#Creo array que parte en 10 y va hasta el 30, en numeros de a 5. el resultado es d = [10,15,20,25]
d = np.arange(10,30,5)
#Para usar arange con numeros flotantes se usa linspace que recibe como argumento el numero de elementos que queremos, en vez de los 'pasos'
e = np.linspace(0, 2, 9 ) # ---> 9 numeros desde el 0 al 2 ==> [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
#Sirve harto para evaluar funciones en puntos, como por ejemplo: f = np.sin(e) --> Evalua l funcion seno en los valores de e

#b = np.arange(12).reshape(2,3,4) # --> Creo matriz con dos matrices de tamaño 3x4 
# se puede comparar cada elemento y pregutnar si es menor a cierto valor: Ej: d > 5 ==> array([True, True, True, True])
# A * B --> multiplicacion de elementos dentro de la matriz
# A.dot(B) --> multiplicacion matricial o np.dot(A,B)
#Sumas de elementos, minimos y maximos de un array de enteros o flotantes.
a = np.random.random((2,3))
a.sum() #---> suma de los elementos
a.min() # --> entrega el menor elmento
a.max() # --> Entrega el mayor elemento
#Creo matriz de 3x4 con num del 0 al 11
b = np.arange(12).reshape(3,4) # ==> [[0,1,2,3], [4,5,6,7], [8,9,10,11]]
#Suma de las columnas 
b.sum(axis =0) # [0 + 4 + 8 , 1 + 5 + 9, 2 + 6 + 10, 3 + 7 + 11]
b.sum(axis=1) #Suma de filas
b.cumsum(axis = 1) #Suma acumulativa de las filas (devuelve matriz del mismo tamanio ingtesado)

#Indexando, particionando e iterando
def resultsNSGA2(carpeta):
	dirs = os.listdir(carpeta)
	print carpeta
	print dirs
	theResults = []
	#delete
	#allValuesF1, allValuesF2 = [], []
	for i in range(len(dirs)):
		counter = 1
		strs = "Generacion: "
		dirc = carpeta + "/" + dirs[i] + '/pareto.csv'
		print "calculando valores para: " + dirs[i]
		f = open(dirc, 'r')
		#allLines debe almacenar todas las listas por cada generacion, con largo igual al numero de gen que hice
		allLines = []
		for line in f:
			listLine = []
			if counter != 1:
				line = line + strs
				osf = line.strip().split(",")
				aux = []
				val1 = float(osf[0])
				val2 = float(osf[1])
				aux.append(val1)
				aux.append(val2)
				listLine.append(aux)
			#delete
			#if val1 not in allValuesF1:
			# allValuesF1.append(val1)
			#if val2 not in allValuesF2:
			# allValuesF2.append(val2)
			#delete
			#print osf
			if strs in line:
			#print strs + str(counter)
				for line in f:
					linea = line.strip().split(",")
					#print linea
					if strs in linea[0]:
					#line = strs
						break
					if linea[3] != 0.0:
						aux = []
						val1 = float(linea[0])
						val2 = float(linea[1])
						aux.append(val1)
						aux.append(val2)
					if aux not in listLine:
						listLine.append(aux)
					#if val1 not in allValuesF1:
					# allValuesF1.append(val1)
					#if val2 not in allValuesF2:
					# allValuesF2.append(val2)
			counter += 1
			allLines.append(listLine)
		theResults.append(allLines)
		#for lines in listLine:
		# print lines       
		#o = input(". . . .")
		#print listLine
	print len(allLines)
	#theResults.append(allLines)
	print len(theResults)
	#h = input(" . . .")
	#allValuesF1.sort()
	#allValuesF2.sort()
	maxMin, ref1, ref2 = [], [], []
	#minObj1 = allValuesF1[0]
	#maxObj1 = allValuesF1[len(allValuesF1)-1]
	
	#ref1.append(minObj1), ref1.append(maxObj1)
	#minObj2 = allValuesF2[0]
	#maxObj2 = allValuesF1[len(allValuesF2)-1]
	#minObj2 = 642493898.0
	#maxObj2 = 1052456716.0
	#ref2.append(minObj2), ref2.append(maxObj2)
	#maxMin.append(ref1)
	#maxMin.append(ref2)

	#results = []
	#results.append(theResults)
	#results.append(maxMin)
	#print maxMin
	return theResults
	#print len(theResults)
	#return results
	#print len(allValues)

def computeHyperVolume(maxMinValues, fronteras, generacion):
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
		for j,frontera in enumerate(fronteras[i]):
		
			if j == generacion:
				for elemento in frontera:

				#h = input(". . . .")
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
	print "Valores de HV para cada run: ", listaHyperVol    
	print len(listaHyperVol)
	return listaHyperVol


def computeHyperVolumeIns(maxMinValues, fronteras, instance):
	minObj1, maxObj1 = maxMinValues[0][0], maxMinValues[0][1]
	minObj2, maxObj2 = maxMinValues[1][0], maxMinValues[1][1]
	#print minObj1, maxObj1, minObj2, maxObj2
	difObj1 = maxObj1 - minObj1
	difObj2 = maxObj2 - minObj2
	#Se guarda en esta lista debido a que los resultados iran dentro del objeto... en normalizedValues...
	listaHyperVol = []
	normalizados = []
	print len(fronteras)
	h = input("")
	listOfIndexes = []
	for i in range(len(fronteras)):
		print i
		if i == instance:
			print "largo", len(fronteras[i])
			#Cada 10 generaciones calculo HV, al final deberia tener 1300 valores de HV
			
			for j in range(1,len(fronteras[i])):
				normValues = []
				listOfIndexes.append(j)
				#print j
				#h = input("DEBERIA SER 13.000 SI ES ASÍ ESTOY BIEN")
				for elemento in fronteras[i][j]:
					#h = input(". . . .")
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
				normalizados.append(normValues)

		#print "valores normalizados"
		#for value in normValues:
		#   print value
				#normalizados.append(normValues)
		#self.normalizedValues.append(normValues)
	#h = input("")
	#en normValues tengo toda la caca
	print "len norm:" ,len(normalizados)
	#for i in range(len(normalizados)):
	##  print normalizados[i]
	# h = input(". . . .")
	referencePoint = [2,2]
	for i in range(len(normalizados)):
		print "Calculando HV . . . .", i 
		hv = HyperVolume(referencePoint)
		volume = hv.compute(normalizados[i])
		listaHyperVol.append(volume)
	#print volume
	#io = input(". . . .")
		
	results = []
	results.append(listOfIndexes)
	results.append(listaHyperVol)
	#print "Valores de HV para cada run: ", listaHyperVol    
	print len(listOfIndexes)
	print len(listaHyperVol)
	return results

def getPareto(values, instance):
	lista = []
	for i in range(len(values)):
		if i == instance:
			print len(values[i])
			for j in range(len(values[i])):
				lista.append(values[i][j])
				#if j == 1:
				#	lista.append(values[i][j])
				#elif j == 5:
				#	print "largo gen 500: " , len(values[i][j])
				#	lista.append(values[i][j])
				#elif j == 12999:
				#	lista.append(values[i][j])
	lista1 = lista[0]
	lista2 = lista[1]
	lista3 = lista[2]
	a, b, c, d,e,f = [], [], [], [], [], []
	for ls in lista1:
		a.append(ls[0])
		b.append(ls[1])
	for ls in lista2:
		c.append(ls[0])
		d.append(ls[1])
	for ls in lista3:
		e.append(ls[0])
		f.append(ls[1])
	return lista
	#aa = plt.plot(a, b, 'b+', label = "Gen 1" )
	#bb = plt.plot(c,d, 'g+', label = "Gen 5000")
	#cc = plt.plot(e, f, 'r', label = "Gen 13000")
	#dd = plt.plot(listaOfCosts[6], listaOfCosts[7], 'y', label = instanceList[3].nombre) 
	#plt.setp(aa, "linestyle", "none", "marker", "o")
	#plt.setp(bb, "linestyle", "none", "marker", "o")
	#plt.setp(cc, "linestyle", "none", "marker", "*")
	#plt.ylabel('Costo Flujo 2')
	#plt.xlabel('Costo Flujo 1')
	#plt.legend(loc = 'upper right')
	#plt.show()
		#print values[i][j]
	
		#o = input(". . .. ")


def plots(results):
	#print "entre"
	xAxis_1 = results[0][0:200]
	yAxis_1 = results[1][0:200]
	#xAxis_2 = results2[0]
	#yAxis_2 = results2[1]
	plt.plot(xAxis_1, yAxis_1, '-bo', label = "NSGA-II")
	#pl2 = plt.plot(xAxis_2, yAxis_2, '-go', label ="Gen3")
	#plt.setp(pl, "linestyle", "none", "marker", "*")
	plt.xlabel('Generaciones')
	plt.ylabel('HiperVolumen')
	plt.title(' Medicion Hipervolumen por generaciones ')
	plt.legend(loc = 'upper right')
	#plt.savefig('nsga2.png')
	plt.show()


def getMainNSGA2():
	cwd = os.getcwd()
	print cwd
	#result = "/Resultados"
	
	start = datetime.datetime.now()
	gen2 = '/NSGA2/resultsGen2'
	
	dors = cwd + gen2
	values = resultsNSGA2(dors)

	#getPareto(values, 11)
	#Max min de los gen2
	minObj1_g2 = 62171264.0
	maxObj1_g2 = 140629788.0
	minObj2_g2 = 29521532.0
	maxObj2_g2 = 140629788.0
	#[[62171264.0, 140629788.0], [29521532.0, 140629788.0]]
	maxMins, aux1, aux2 = [], [], []
	aux1.append(minObj1_g2), aux1.append(maxObj1_g2)
	aux2.append(minObj2_g2), aux2.append(maxObj2_g2)
	maxMins.append(aux1), maxMins.append(aux2)
	
	for i in range(20):
		results1 = computeHyperVolumeIns(maxMins, values, i)
		plots(results1)
	
	#sa = input("... ")
	gen3 = "/NSGA2/resultsGen3"

	directory = cwd + gen3
	valuesGen3 = resultsNSGA2(directory)

	#getPareto(valuesGen3, 10)
	#plot(valuesGen3)
	#max min de lso gen3
	minObj1_g3 = 719589618.0
	maxObj1_g3 = 1052456717.0
	minObj2_g3 = 642493898.0
	maxObj2_g3 = 1052456716.0
	maxiMins, ayud1, ayud2 = [], [], []
	ayud1.append(minObj1_g3), ayud1.append(maxObj1_g3)
	ayud2.append(minObj2_g3), ayud2.append(maxObj2_g3)
	maxiMins.append(ayud1), maxiMins.append(ayud2)

	for i in range(20):
		results2 = computeHyperVolumeIns(maxiMins, valuesGen3, i)
		plots(results2)

	finish = datetime.datetime.now()
	total = finish - start
	print "execution time: ", total
	#plot(results1, results2)
	return 1


def obtainResults(carpetas, directory):
	theResults = []
	allValuesF1_1, allValuesF2_1 = [], []
	allValuesF1_2, allValuesF2_2 = [], []
	allValuesF1_3, allValuesF2_3 = [], []
	#3
	for i in range(1,len(carpetas)+1):
		carpeta = directory + "resultsMem" + str(i) + "/"
		#print carpeta
		listaResults = os.listdir(carpeta)
		#print listaResults
		#Aca almaceno los dos valores que devuelvo, es decir, listaDeFronteras y allvalues. 
		
		results = [] 
		listaDeFronterasINS = []
		
		for j in range(len(listaResults)):
			new_path = carpeta + listaResults[j]
			file = new_path + "/pareto.csv"
			fronteraRun = []
			print file
			try:
				with open(file) as f:
					for lines in f:
						costoFlujo = []
						linea = lines.split(",")
						crowding = float(linea[2])
						if crowding != 0.0:
							costoFlujo.append(float(linea[0]))
							costoFlujo.append(float(linea[1]))
						#Obtengo el costo y lo agrego a la lista de allvalues para obtener luego mayores y menores. 
							if i <= 11:
								if costoFlujo[0] not in allValuesF1_1:
									allValuesF1_1.append(costoFlujo[0])
								if costoFlujo[1] not in allValuesF2_1:
									allValuesF2_1.append(costoFlujo[1])
							elif i > 11 and i <= 22:
								if costoFlujo[0] not in allValuesF1_2:
									allValuesF1_2.append(costoFlujo[0])
								if costoFlujo[1] not in allValuesF2_2:
									allValuesF2_2.append(costoFlujo[1])
							elif i > 22 and i <= 33:
								if costoFlujo[0] not in allValuesF1_3:
									allValuesF1_3.append(costoFlujo[0])
								if costoFlujo[1] not in allValuesF2_3:
									allValuesF2_3.append(costoFlujo[1])

							if costoFlujo not in fronteraRun:
								fronteraRun.append(costoFlujo)
							#print costoFlujo
				#print len(fronteraRun)			
				listaDeFronterasINS.append(fronteraRun)
				#print len(listaDeFronterasINS)    
			#print linea
			except IOError as exc:
				if exc.errno != errno.EISDIR:
					raise
			#AQUI QUEDE ESTOY CONFUNDIDO... MEJOR DUERMO.
		theResults.append(listaDeFronterasINS)
		
	#print len(theResults)
	allValuesF1_1.sort(), allValuesF2_1.sort()
	allValuesF1_2.sort(), allValuesF2_2.sort()
	allValuesF1_3.sort(), allValuesF2_3.sort()
	#print allValuesF2_1
	
	minObj1 = allValuesF1_3[0]
	maxObj1 = allValuesF1_3[len(allValuesF1_3)-1]
	minObj2 = allValuesF2_3[0]
	maxObj2 = allValuesF2_3[len(allValuesF2_3)-1]
	#print minObj1, maxObj1, minObj2, maxObj2
	#15071714.0 25238352.0 6224236.0 14883234.0
	#601774990.0 908145682.0 541841820.0 898464818.0
	#11368.976593 11517.7483789 13148.1703743 13236.9167113
	return theResults
	#print new_path

	#print carpetas[i]

def getMeanSTD(listofHV):
	arr = np.array(listofHV)
	prom = np.mean(arr, axis = 0)
	std = np.std(arr, axis = 0)
	meanStandar = str(prom) + " +- " +  str(std)
	#print str(prom) + " +- " +  str(std)
	return meanStandar

def getData(results):
	cantInstancias = 2
	#listaHV1, listaHV2 = [], []
	allListaHV1, allListaHV2, allListaHV3 = [], [], []
	meanSTD = []
	for i in range(len(results)):
		if i < 11:
			maxMins = [ [15071714.0, 25238352.0 ], [6224236.0, 14883234.0]]
			listaHV1 = computeHV(maxMins,results[i])
			allListaHV1.append(listaHV1)
			std = getMeanSTD(listaHV1)
			#meanSTD.append(std)
		elif i >= 11 and i < 22:
			maxMins = [[601774990.0, 908145682.0], [541841820.0, 898464818.0]]
			listaHV2 = computeHV(maxMins,results[i])
			allListaHV2.append(listaHV2)
			std = getMeanSTD(listaHV2)
			#meanSTD.append(std)
		elif i >= 22 and i <= 33:
			maxMins = [ [11368.976593, 11517.7483789], [13148.1703743, 13236.9167113] ]
			listaHV3 = computeHV(maxMins, results[i])
			allListaHV3.append(listaHV3)
			std = getMeanSTD(listaHV3)
			meanSTD.append(std)
	
	f = open("resultados.csv", "w")		
	#print "resultados instancia KC20"
	for elem in allListaHV1:
		for e in elem:
			f.write(str(e) + "\n")
	#print "resultados instancia GAR60"
	for elem in allListaHV2:
		for e in elem:
			f.write(str(e)+ "\n")
	for elem in allListaHV3:
		for e in elem:
			f.write(str(e)+ "\n")
	f.close()
	#for mean,i in enumerate(meanSTD):
	#	print mean, i	
	#getBoxPlots(allListaHV1, "KC20-2fl-1rl")
	#getBoxPlots(allListaHV2, "Gar60-2fl-4rl")
	getBoxPlots(allListaHV3, "arabidopsis")


def getBoxPlots(allListaHV, instancia):
	fig = plt.figure(1, figsize=(9,6))

	ax = fig.add_subplot(111)
	##fill color
	bp = ax.boxplot(allListaHV, patch_artist = True)
	titulo = 'Instancia: ' + instancia
	fig.suptitle(titulo, fontsize = 20)
	plt.xlabel('Casos', fontsize = 16)
	plt.ylabel('HyperVolumen', fontsize = 16)

	ax.set_xticklabels(['Caso 1', 'Caso 2','Caso 3','Caso 4','Caso 5','Caso 6','Caso 7','Caso 8','Caso 9','Caso 10','Caso 11' ])
	##cambio el color
	ax.get_xaxis().tick_bottom()
	ax.get_yaxis().tick_left()
	for box in bp['boxes']:
		box.set(color = '#7570b3', linewidth=2)
		box.set(facecolor = '#1b9e77')
	#cambio	color y ancho de linea para "whiskers"
	for whisker in bp['whiskers']:
		whisker.set(color = '#7570b3', linewidth = 2)
	for cap in bp['caps']:
		cap.set(color = '#7570b3', linewidth= 2)
	for median in bp['medians']:
		median.set(color = '#b2df8a', linewidth= 2)	
	for flier in bp['fliers']:
		flier.set(marker = 'o', color = '#e7298a', alpha = 0.5)

	name = 'fig-' + instancia + '.png'
	fig.savefig(name, bbox_inches = 'tight')

	#plt.show()



def computeHV(maxMinValues, fronteras):
	minObj1, maxObj1 = maxMinValues[0][0], maxMinValues[0][1]
	minObj2, maxObj2 = maxMinValues[1][0], maxMinValues[1][1]
	#print minObj1, maxObj1, minObj2, maxObj2
	difObj1 = maxObj1 - minObj1
	difObj2 = maxObj2 - minObj2
	#Se guarda en esta lista debido a que los resultados iran dentro del objeto... en normalizedValues...
	listaHyperVol = []
	normalizados = []
	for i in range(len(fronteras)):
		#print i
		normValues = []
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
		normalizados.append(normValues)
	referencePoint = [2,2]
	for i in range(len(normalizados)):
		hv = HyperVolume(referencePoint)
		volume = hv.compute(normalizados[i])
		listaHyperVol.append(volume)
	#print "Valores de HV para cada run: ", listaHyperVol    
	return listaHyperVol	

def preProcessData(dirs, carpetas):
	out = open("BIO133.dat", 'w')
	out.write("133")
	out.write("\n")
	carpetas.sort()
	for i in range(len(carpetas)):
		print carpetas[i]
		path = dirs + "/" + carpetas[i]
		print path

		try:
			with open(path) as f:
				f.next()
				for lines in f:
					#print lines
					stre = ",".join(lines.split(',')[1:])
					new_str = stre.replace(",", " ")
					out.write(new_str)
					#print new_str
					#os = input(". . . .")	
		
		except IOError as exc:
			if exc.errno != EISDIR:
				raise
		out.write("\n")
		#o = input(". . . .")
		#print path
	out.close()
		
def gerResultCasos():
	cwd = os.getcwd()
	carpeta = "/ResultadosCASOS/"
	path = cwd + carpeta
	dirs = os.listdir(path)
	results = obtainResults(dirs, path)
	data = getData(results)

def selectCarpetas(dirs, cwd, carpetas):
	#carpetas = ['MB-MOMA-1', 'MB-MOMA-2','MB-MOMA-3','MB-MOMA-5','MB-MOMA-6','MB-MOMA-7', 'MB-MOMA-8', 'MB-MOMA-9', 'MB-MOMA-11', 'MB-MOMA-12' ]
	#print dirs
	resultsMem = 'resultsMem'
	for carp in dirs:
		#print carp
		if carp in carpetas:
			path = str(cwd) + "/" + str(carp)
			elements = os.listdir(path)
			for elem in elements:
				if elem == 'KC':
					new_path = str(path) + "/" + str(elem) + "/"
					result = os.listdir(new_path)
					result.sort()
					npList = np.arange(0,480,30)
					lista = list(npList)
					counter = 0
					print counter
					memCounter = 0
					for elem in result:
						counter +=1	
						papath = str(new_path) + str(elem)
						print papath
						destiny = str(path)+ "/"  + resultsMem + str(memCounter) + "/" + str(elem)
						print destiny
						shutil.move(papath, destiny)
						if counter in lista:
							print counter
							memCounter +=1
							#a = input("....")
					
				if elem == 'GAR':
					new_path = str(path) + "/" + str(elem) + "/"
					result = os.listdir(new_path)
					result.sort()
					npList = np.arange(0,300,30)
					lista = list(npList)
					counter = 0
					print counter
					memCounter = 16
					for elem in result:
						counter +=1	
						papath = str(new_path) + str(elem)
						print papath
						destiny = str(path) + "/" + resultsMem + str(memCounter) + "/" + str(elem)
						shutil.move(papath, destiny)
						print destiny
						if counter in lista:
							print counter
							memCounter +=1
							#a = input("....")

						

						


					#print "GAR"
				
			#print path
			#for i in range(1,26):
def convertMBMOMA(ins):
	print ins
	cwd = '/home/rsandova/Desktop/Tesis/Resultados/Julio2017/ResultadosConfiguraciones'
	dirs = os.listdir(cwd)
	print dirs
	numCarp = input("Numero de carpetas:")
	#2
	carpetas = []
	for i in range(numCarp):
		carpeta = raw_input("Ingrese Carpeta: ")
		carpetas.append(carpeta)
	#print carpetas
	selectCarpetas(dirs, cwd, carpetas)



if __name__ == "__main__":
	
	#Funcion para obtener resultados de NSGA2.
	getMainNSGA2()



	#Funcion para traer casos de los resultados.
	#getResultCasos()
	
	#print dirs
	
	#cwd = os.getcwd()
	#carpeta = "/biological/arabidopsis"
	#path = cwd + carpeta
	#dirs = os.listdir(path)
	#print dirs
	#preProcessData(path,dirs)

	#cwd = os.getcwd()
	
	#Funcion de conversion MB-MOMA.
	#ls = convertMBMOMA("Empezando a ordenar...")
	
	

	#valores = computeHyperVolume(maxMins, values, 25999)
	#for i, val in enumerate(valores):
	# print val, i
	

	#sbatch --array=0-9 punto.sh
	
	#valores.sort()
	#print "sorted"
	#for i, val in enumerate(valores):
	# print val, i
	#median = np.median(np.array(valores))
	#print "LA MEDIANA ES. . .", median
	#Selected = 11. 
	#Selected2 = 10