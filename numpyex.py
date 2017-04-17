# -*- coding: utf-8 -*-


import numpy as np

#Creo matriz con 15 elementos, distribuidos en dimensiones (3,5), es decir, 3 arreglos de tamaño 5 cada uno
a = np.arange(15).reshape(3,5)
#Creo array
b = np.array([6,7,8])
#Creo array con dimensiones y EDA que yo decida
c = np.array([(1,2,3), (1,4,3)], dtype = float)
# Funciones: 
#	np.zero((3,4)) ---> Crea matriz con ceros
#	np.ones((3,4)) ---> Crea matriz con unos
#	np.empty((2,3)) --> Crea matriz con random float64
#Creo array que parte en 10 y va hasta el 30, en numeros de a 5. el resultado es d = [10,15,20,25]
d = np.arange(10,30,5)
#Para usar arange con numeros flotantes se usa linspace que recibe como argumento el numero de elementos que queremos, en vez de los 'pasos'
e = np.linspace(0, 2, 9 ) # ---> 9 numeros desde el 0 al 2 ==> [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
#Sirve harto para evaluar funciones en puntos, como por ejemplo: f = np.sin(e) --> Evalua l funcion seno en los valores de e

b = np.arange(12).reshape(2,3,4) # --> Creo matriz con dos matrices de tamaño 3x4 
# se puede comparar cada elemento y pregutnar si es menor a cierto valor: Ej: d > 5 ==> array([True, True, True, True])
# A * B --> multiplicacion de elementos dentro de la matriz
# A.dot(B) --> multiplicacion matricial o np.dot(A,B)
#Sumas de elementos, minimos y maximos de un array de enteros o flotantes.
a = np.random.random((2,3))
#