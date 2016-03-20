# Data Mining Assignment - Recommendation System
# Developed by Pralhad

# Naive Algorithm which averages all available values

import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial.distance as dist
import heapq as hq
import math

baseFiles = ['u1.base', 'u2.base', 'u3.base', 'u4.base', 'u5.base']
testFiles = ['u1.test', 'u2.test', 'u3.test', 'u4.test', 'u5.test']
userProfileFile = 'u.user'
fileIndex = 4

# For convenience the 0th indexed row and column are ignored
totalUsers = 943 + 1
totalMovies = 1682 + 1

# [[0 for x in range(cols_count)] for x in range(rows_count)]
documentMatrix = [[0 for x in range(totalMovies)] for x in range(totalUsers)]
userProfileMatrix = [[0 for x in range(2)] for x in range(totalUsers)]

maxUserAge = 0.0
maxRating = 0.0
maxGenders = 2.0
maxMovieRating = 5.0

suggestionMatrix = [[0.0 for x in range(totalMovies)] for x in range(totalUsers)]


f1 = open(baseFiles[fileIndex],'r')

for line in f1:
	elements = line.split('\t', 3)
	elements[3] = elements[3].split('\n', 1)[0]
	
	if int(elements[2]) > maxRating:
		maxRating = int(elements[2])
	
	documentMatrix[int(elements[0])][int(elements[1])] = int(elements[2])

f1.close()
print "%s file read" %baseFiles[fileIndex]

############################################################################################################
# Building naive suggestions by averaging all movies (columns)

totalSuggestionsMade = 0.0

for movie in range(1, totalMovies):
	count = 0
	average = 0.0
	for user in range(1, totalUsers):
		if documentMatrix[user][movie] != 0:
			average += documentMatrix[user][movie]
			count += 1
		
	if count > 0:
		average /= count
		
		for user in range(1, totalUsers):
			if documentMatrix[user][movie] == 0:
				totalSuggestionsMade += 1
				suggestionMatrix[user][movie] = round(average)

############################################################################################################
# Comparing the data with uX.test
f2 = open(testFiles[fileIndex],'r')
# o = open('kNearest_Manhattan.txt', 'w')

testRatingsFound = 0
testAbsDiffSum = 0.0
spotOn = 0

for line in f2:
	elements = line.split('\t', 3)
	elements[3] = elements[3].split('\n', 1)[0]
	
	# sanity check if the rating is available
	if suggestionMatrix[int(elements[0])][int(elements[1])] != 0:
		if int(elements[2]) == suggestionMatrix[int(elements[0])][int(elements[1])]:
			spotOn += 1
		testAbsDiffSum += abs(int(elements[2]) - suggestionMatrix[int(elements[0])][int(elements[1])])
		testRatingsFound += 1

f2.close()

print "%s file read" %testFiles[fileIndex]
					
print "Sum of distance amongst predictions and test data is %d" %testAbsDiffSum
print "Sum of all ratings found is %d" %testRatingsFound
print "%d predictions were spot on" %spotOn
print "Total suggestions made by system were %d" %totalSuggestionsMade
print "The mean absolute distance is %f" % ((float(testAbsDiffSum) / testRatingsFound))