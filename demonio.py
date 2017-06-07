import subprocess
import time
import sys

seeds = [1013197, 1013203, 1013227, 1013237,1013239, 1013249,1013263, 1013267,1013279, 1013291,
		 1013321,1013329,1013377,1013399,1013401,1013429,1013431,1013471,1013477,1013501,
		 1012993, 1012997, 1013003, 1013009, 1013029, 1013041, 1013053, 1013063, 1013143, 1013153]

#prueba = [1012993, 1012997, 1013003, 1013009, 1013029]

#print len(seeds)
#Ejemplo: instances/KC10-2fl-1rL.dat
exe = sys.argv[1]

#print exe
for i in range(2):
	print "+++++++++++++++++++"

	print "Running Process:  " +  str(i)
	print "+++++++++++++++++++"
	lineaCom = "python main.py " + str(exe) + " parameters.dat " + str(seeds[i]) 
	print lineaCom
	p = subprocess.Popen(lineaCom, shell=True)
	p.communicate()
	time.sleep(5)

print "Memetic Algorithm Finished" 