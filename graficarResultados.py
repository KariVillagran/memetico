import numpy as np 
import matplotlib.pyplot as plt 
import sys

def lectura():
	archivo = sys.argv[1]
	generacion = sys.argv[2]
	resultados = open(archivo, 'r')
	generacionCorrecta = "Generacion: " + generacion
	#print generacionCorrecta
	linea = []
	listaSolC1 = []
	listaSolC2 = []
	for line in resultados:
		if generacionCorrecta in line:
			#print "ENCONTRADA!"
			for new_line in resultados:
				linea = new_line.strip().split(",")
				print linea
				#print "Agregando a listaCosto1: ", linea[0]
				listaSolC1.append(linea[0])
				#print "Agregando a listaCosto2: ", linea[1]
				listaSolC2.append(linea[1])
		else:
			pass
			#print "NOT YET FOUND"
	
	plt.plot(listaSolC1, listaSolC2, 'ro')
	plt.ylabel('Costo Flujo 2')
	plt.xlabel('Costo Flujo 1')
	plt.show()

	return 1

lectura()