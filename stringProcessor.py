# Author: Vardi Adi
#!/usr/bin/env python
import os
import sys
import argparse
import string
import multiprocessing
import time
dir_path = os.path.dirname(os.path.realpath(__file__))
outputFileName = dir_path + "/processOutput.txt"

def progressBar(prog):
	done = int(round(progressBar.barWidth*prog))
	bar = "Progress: [{0}] {1}%\n".format( "#"*done + "-"*(progressBar.barWidth-done), prog*100)
	sys.stdout.write(bar)
	sys.stdout.flush()
progressBar.barWidth = 20

def expensiveFunc(string, queue):
	time.sleep(expensiveFunc.delay)
expensiveFunc.delay = 0

def writeToFile(queue):
	file = open(outputFileName, 'wb')
	
	while True:
		next = queue.get()
		if next == 'end':
		    break
		file.write(next)
		file.flush()
	file.close()

def main(args):
	startTime = time.time()

	# Set the parameters
	expensiveFunc.delay = args.timeDelay
	inputFile = args.inputFile

	qManager = multiprocessing.Manager()
	queue = qManager.Queue()    
	pool = multiprocessing.Pool(multiprocessing.cpu_count() + 2)

	# add writer to pool
	pool.apply_async(writeToFile, (queue,))

	nLines = sum(1 for line in open(inputFile,'r'))
	print "lines:",nLines

	jobs = []
	with open(inputFile, 'r') as f:
		for line in sorted(f):		# sort using sorted - can be extended to any other sorting algorithm
			job = pool.apply_async(expensiveFunc, (line, queue))
			jobs.append(job)
			queue.put(line)
			
	counter = 0
	for job in jobs:
		job.get()
		counter += 1
		progressBar(float(counter)/nLines)

	# end the writer when done
	queue.put('end')
	pool.close()

	completionTime = time.time() - startTime
	print "Completion Time [s]: ", completionTime


def isFileValid(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


if __name__ == '__main__':
	# ---- Parse arguments ----
	parser = argparse.ArgumentParser(description='String Generator')#,formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('timeDelay', type=int, help="time delay for each string (in seconds)")
	parser.add_argument('inputFile', type=lambda x: isFileValid(parser, x), help="Input file")
	args = parser.parse_args(sys.argv[1:])

	sys.exit(main(args))