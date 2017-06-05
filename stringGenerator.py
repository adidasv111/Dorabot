# Author: Vardi Adi
#!/usr/bin/env python
import os
import sys
import argparse
import string
import multiprocessing
import random
import time

dir_path = os.path.dirname(os.path.realpath(__file__))
fileName = dir_path + "/data.txt"

def progressBar(prog):
	done = int(round(progressBar.barWidth*prog))
	bar = "Progress: [{0}] {1}%\n".format( "#"*done + "-"*(progressBar.barWidth-done), prog*100)
	sys.stdout.write(bar)
	sys.stdout.flush()
progressBar.barWidth = 20

def writeToFile(queue):
	'''writes strings to file'''
	file = open(fileName, 'wb')
	
	while True:
		next = queue.get()
		if next == 'end':
			print "end signal"
			break
		elif writeToFile.totalMem > writeToFile.neededMem:
			print "Memory needed exceeded"
			break;
		file.write(next)
		writeToFile.totalMem += sys.getsizeof(next)
		progressBar(float(writeToFile.totalMem) / writeToFile.neededMem)
		file.flush()
	file.close()
	print "totalMemory: ", writeToFile.totalMem
writeToFile.totalMem = 0
writeToFile.neededMem = 0

def generateString():
	'''generates one string'''
	l = random.randint(generateString.minL, generateString.maxL)
	str = ''.join(random.choice(generateString.availableChars) for _ in range(l)) + '\n'
	return str
generateString.availableChars = ''
generateString.minL = 0
generateString.maxL = 0

def generate4MB(arg, queue):	
	'''generates at least MBMB of strings'''
	strMBMB = ''.join(generateString() for _ in range(generate4MB.N))
	queue.put(strMBMB)
generate4MB.N = 0


def main(args):
	if args.minL > args.maxL:
		print "Error: maxL must be bigger than minL"
		sys.exit()

	startTime = time.time()

	# Set the parameters
	generateString.minL = args.minL
	generateString.maxL = args.maxL
	generateString.availableChars = string.ascii_lowercase + string.ascii_uppercase	# + .... to add other types of characters

	N = 2**22 / args.minL							# Average number of strings in 4MB (ignoring the 36 bytes overhead, which is negligeable out ou MB MB)
	generate4MB.N = N
	writeToFile.neededMem = args.memory*(2**30)

	qManager = multiprocessing.Manager()
	queue = qManager.Queue()    
	pool = multiprocessing.Pool(multiprocessing.cpu_count() + 2)

	# add writer to pool
	pool.apply_async(writeToFile, (queue,))

	print "Number of jobs: ",256*args.memory
	jobs = []
	for i in range(256*args.memory):
		job = pool.apply_async(generate4MB, (i, queue))
		jobs.append(job)

	progressBar(0)
	for job in jobs:
	    job.get()

	# end the writer when done
	queue.put('end')
	pool.close()
	completionTime = time.time() - startTime
	print "Completion Time [s]: ", completionTime
	

if __name__ == '__main__':
	# ---- Parse arguments ----
	parser = argparse.ArgumentParser(description='String Generator')#,formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('minL', type=int, help="Minimum string length")
	parser.add_argument('maxL', type=int, help="Maximum string length")
	parser.add_argument('memory', type=int, help="Amount of strings to generate in GBs")
	args = parser.parse_args(sys.argv[1:])


	sys.exit(main(args))