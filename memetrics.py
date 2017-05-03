import glob
import os
import errno

class Metrics:
	def __init__(self, directorio):
		self.directorio = directorio


	def openArchivos(self):
		path = self.directorio
		carpetasRun = os.listdir(path)
		cantCarpetas = len(carpetasRun)
		for i in range(cantCarpetas):
			new_path = ""
			new_path = path + "/" + carpetasRun[i] + "/" + "pareto.csv"
			#print new_path
			try:
				with open(new_path) as f:
					print f
			except IOError as exc:
				if exc.errno != errno.EISDIR:
					raise		


if __name__ == "__main__":

    # Example:
    direct = '/home/rsandova/Desktop/Tesis/Memetico/AM/Pruebas'
    metrics = Metrics(direct)
    metrics.openArchivos()
    
