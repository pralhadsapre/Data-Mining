# This program generates curves using Matplotlib to show the curse of dimensionality
# Developed by Pralhad

import random
import math
import matplotlib.pyplot as plt
# import numpy as np

maxDimensions = 100
averagingRuns = 20
nvalues = [100]
graphPlot = [0 for x in range(maxDimensions)]

for run in range(averagingRuns):
	for dimensions in range(1, maxDimensions + 1):

		# [[0 for x in range(cols_count)] for x in range(rows_count)]
		dataMatrix = [[0 for x in range(dimensions)] for x in range(nvalues[0])]

		for i in range(nvalues[0]):
			for j in range(dimensions):
				dataMatrix[i][j] = random.random()
			# print dataMatrix[i]
		
		dMax = 0.0
		dMin = 10.0
		euclideanSummation = 0.0

		for i in range(nvalues[0]):
			for j in range(i+1, nvalues[0]):
			
				euclideanSummation = 0.0
				
				for k in range(dimensions):
					if dataMatrix[i][k] == dataMatrix[j][k]:
						euclideanSummation = 0.0
						print "Similar random values found"
						break;
					else:
						euclideanSummation += (dataMatrix[i][k] - dataMatrix[j][k])**2
				
				if euclideanSummation != 0.0:
					# euclideanSummation = math.sqrt(euclideanSummation)
					
					if(euclideanSummation < dMin):
						dMin = euclideanSummation
						# print "new dMin %f" %dMin
					if(euclideanSummation > dMax):
						dMax = euclideanSummation
						# print "new dMax %f" %dMax
					

		# print "Minimum distance %f" % dMin
		# print "Maximum distance %f" % dMax
		
		# print ((dMax-dMin)/dMin)
		rk = math.log10(((dMax-dMin)/dMin))
		graphPlot[dimensions - 1] += rk
		
		print "generated r(k) for %d dimensions in run %d" %(dimensions, run)
		# print math.log10((dMax-dMin)/dMin)

		
for i in range(maxDimensions):
	graphPlot[i] /= averagingRuns

# print graphPlot
print "Values computed"
plt.plot(graphPlot)
plt.ylabel('r(k) function')
plt.xlabel('Dimensions')
plt.show()
# print "Random number generated"
	