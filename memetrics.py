import glob
import os
import errno

class Metrics:
	def __init__(self, directorio):
		self.directorio = directorio
		self.folders = []
		self.paretoFrontiers = []
		self.nonRepParetoFrontiers = []
		self.combinedParetoFrontier = []
		self.mergedNonRepFrontiers = []
		#Se supone que es una lista con listas dentro, del tamano de len(folders) en donde cada una tiene los valores
		#normalizados de cada ejecucion para calcular HV
		self.normalizedValues = []




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
			#print new_path
			try:
				with open(new_path) as f:
					for lines in f:
						for line in f:
							costosFlujo = []
							linea = line.strip().split(",")
							costosFlujo.append(float(linea[0]))
							costosFlujo.append(float(linea[1]))
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

	def obtenerMaxMin(self):
		lista, listaObj1, listaObj2, maxMinValues, aux, aux2 = [], [], [], [], [], []
		for i in range(len(self.nonRepParetoFrontiers)):
			for results in self.nonRepParetoFrontiers[i]:
				if results not in lista:
					lista.append(results)
		self.mergedNonRepFrontiers = lista[:]		
		for elements in lista:
			listaObj1.append(elements[0])
			listaObj2.append(elements[1])
		listaObj1.sort()
		listaObj2.sort()
		aux.append(listaObj1[0]), aux.append(listaObj1[len(listaObj1)-1])
		maxMinValues.append(aux)
		aux2.append(listaObj2[0]), aux2.append(listaObj2[len(listaObj2)-1])
		maxMinValues.append(aux2)
		return maxMinValues

	def normalizeValues(self, maxMinValues):
		minObj1, maxObj1 = maxMinValues[0][0], maxMinValues[0][1]
		minObj2, maxObj2 = maxMinValues[1][0], maxMinValues[1][1]
		print minObj1, maxObj1, minObj2, maxObj2




if __name__ == "__main__":

    # Example:
    direct = '/home/rsandova/Desktop/Tesis/Memetico/AM/Pruebas'
    metrics = Metrics(direct)
    metrics.openArchivos()
    maxMin = metrics.obtenerMaxMin()
    metrics.normalizeValues(maxMin)

	