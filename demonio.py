import subprocess
import time
import sys

#Seeds para parametrizacion de % genetic y LS
#seeds = [1013197, 1013203, 1013227, 1013237,1013239, 1013249,1013263, 1013267,1013279, 1013291,
#		 1013321,1013329,1013377,1013399,1013401,1013429,1013431,1013471,1013477,1013501,
#		 1012993, 1012997, 1013003, 1013009, 1013029, 1013041, 1013053, 1013063, 1013143, 1013153]


seeds = [1017227, 1017277, 1017293, 1017299, 1017301, 1017307, 1017311, 1017319, 1017323, 1017329,
		1017347,1017353,1017361,1017371,1017377,1017383,1017391,1017437,1017439,1017449,
		1017473,1017479,1017481,1017539,1017551,1017553,1017559,1017607,1017613,1017617]


#prueba = [1012993, 1012997, 1013003, 1013009, 1013029]

#print len(seeds)
#Ejemplo: instances/KC10-2fl-1rL.dat
exe = sys.argv[1]

params = sys.argv[2]

#print exe
for i in range(20):
	print "+++++++++++++++++++"

	print "Running Process:  " +  str(i)
	print "+++++++++++++++++++"
	lineaCom = "python main.py " + str(exe) + " Metodos/" + str(params) + " "  + str(seeds[i]) 
	print lineaCom
	p = subprocess.Popen(lineaCom, shell=True)
	p.communicate()
	time.sleep(10)

print lineaCom
print "Memetic Algorithm Finished" 