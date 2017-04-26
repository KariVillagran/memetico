import subprocess
import time

for i in range(5):
	print "+++++++++++++++++++"

	print "Running Process:  " + str(i)
	print "+++++++++++++++++++"
	p = subprocess.Popen("python main.py instances/KC10-2fl-1uni.dat", shell=True)
	p.communicate()
	time.sleep(5)

print "Memetic Algorithm Finished" 