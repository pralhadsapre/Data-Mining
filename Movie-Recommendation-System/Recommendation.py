# Data Mining Assignment - Recommendation System
# Developed by Pralhad

import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial.distance as dist
import heapq as hq
import math

baseFiles = ['u1.base', 'u2.base', 'u3.base', 'u4.base', 'u5.base']
testFiles = ['u1.test', 'u2.test', 'u3.test', 'u4.test', 'u5.test']
userProfileFile = 'u.user'
fileIndex = 0

# 1 is for Euclidean
# 2 is for Manhattan
# 3 is for Chebyshev or Lmax
distanceMetric = 2

kNeighbours = 100

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
suggestionAvg = [[0.0 for x in range(totalMovies)] for x in range(totalUsers)]

nearestNeighbours = {}

f1 = open(baseFiles[fileIndex],'r')
# o = open('suggestions_matrix_chebyshev.txt', 'w')

for line in f1:
	elements = line.split('\t', 3)
	elements[3] = elements[3].split('\n', 1)[0]
	
	if int(elements[2]) > maxRating:
		maxRating = int(elements[2])
	
	documentMatrix[int(elements[0])][int(elements[1])] = int(elements[2])

f1.close()
print "%s file read" %baseFiles[fileIndex]

f2 = open(userProfileFile, 'r')

for line in f2:
	elements = line.split('|', 4)
	elements[3] = elements[3].split('\n', 1)[0]
	
	# 0th index is for age
	userProfileMatrix[int(elements[0])][0] = int(elements[1])

	if int(elements[1]) > maxUserAge:
		maxUserAge = int(elements[1])
	
	# 1st index is for gender
	if str.lower(elements[2]) == 'm':
		# represents males
		userProfileMatrix[int(elements[0])][1] = 0
	else:
		userProfileMatrix[int(elements[0])][1] = 1

f2.close()
print "user profile data loaded"

comparisonDump = [[0 for x in range(totalUsers)] for x in range(totalUsers)]


############################################################################################################
# Building distance metrics

for user in range(1, totalUsers):
	for anotherUser in range(1, totalUsers):
	
		overlappingVectorUser = []
		overlappingVectorAnotherUser = []
		
		if user != anotherUser:
			if comparisonDump[anotherUser][user] != 0:
			
				# implies that the distance was already computed between a certain (x, y) as (y, x)
				comparisonDump[user][anotherUser] = comparisonDump[anotherUser][user]
			else:
				for matchIndex in range(1, totalMovies):
					if documentMatrix[user][matchIndex] != 0 and documentMatrix[anotherUser][matchIndex] != 0:
						overlappingVectorUser.append(documentMatrix[user][matchIndex])
						overlappingVectorAnotherUser.append(documentMatrix[anotherUser][matchIndex])

				# appending additional dimensions of age and gender respectively
				overlappingVectorUser.append((userProfileMatrix[user][0] / 10))
				overlappingVectorUser.append(userProfileMatrix[user][1])
				
				overlappingVectorAnotherUser.append((userProfileMatrix[anotherUser][0] / 10))
				overlappingVectorAnotherUser.append(userProfileMatrix[anotherUser][1])

		if len(overlappingVectorUser) != 0:
			if distanceMetric == 1:
				# The first distance metric : Euclidean
				comparisonDump[user][anotherUser] = (len(overlappingVectorUser) / float(totalMovies - 1)) * (1.0 / (1 + dist.euclidean(overlappingVectorUser, overlappingVectorAnotherUser)))
				
			elif distanceMetric == 2:
				# The second distance metric : Manhattan
				# The caveat here is that cityblock distance is an int and hence the numerator should be 1.0 and not 1
				# Observation: This metric doesn't involve squaring and square root and thus is faster
				comparisonDump[user][anotherUser] = (len(overlappingVectorUser) / float(totalMovies - 1)) * (1.0 / (1 + dist.cityblock(overlappingVectorUser, overlappingVectorAnotherUser)))
				
			elif distanceMetric == 3:
				# The third distance metric : Chebyshev
				comparisonDump[user][anotherUser] = (len(overlappingVectorUser) / float(totalMovies - 1)) * (1.0 / (1 + dist.chebyshev(overlappingVectorUser, overlappingVectorAnotherUser)))
				
				
	print "Distance amongst %d and others computed" % (user)
	
	nearestNeighbours[user] = []
	# Get the top k nearest neighbours
	for nearest in hq.nlargest(kNeighbours, comparisonDump[user]):
		nearestNeighbours[user].append([comparisonDump[user].index(nearest), nearest])
	
	# o.write(str(nearestNeighbours[user]) + "\n")


############################################################################################################
# Building suggestions based on k nearest neighbours

print "Building suggestions"

totalSuggestionsMade = 0

for user in range(1, totalUsers):
	for neighbour in range(kNeighbours):
	
		for l in range(1, totalMovies):
		
			# this statement means neighbour has seen a movie which user has not seen
			if documentMatrix[user][l] == 0 and documentMatrix[nearestNeighbours[user][neighbour][0]][l] != 0:
				
				if suggestionMatrix[user][l] == 0:
					totalSuggestionsMade += 1
				
				# Logic for weighted mean
				# suggestionMatrix[user][l] += (documentMatrix[nearestNeighbours[user][neighbour][0]][l] * nearestNeighbours[user][neighbour][1])
				# suggestionAvg[user][l] += nearestNeighbours[user][neighbour][1]
				
				# Logic used for normal mean
				suggestionMatrix[user][l] += documentMatrix[nearestNeighbours[user][neighbour][0]][l]
				suggestionAvg[user][l] += 1
	
	print "Suggestions built for %d" %user
	
for user in range(1, totalUsers):
	for movie in range(1, totalMovies):
		if suggestionMatrix[user][movie] != 0:
			suggestionMatrix[user][movie] = round(suggestionMatrix[user][movie] / float(suggestionAvg[user][movie]))
	
	
	# o.write(str(user) + " is suggested " + str(suggestionMatrix[user]) + "\n")
	
# o.close()


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
print "%d nearestNeighbours were used" %kNeighbours

if distanceMetric == 1:
	print "Distance metric used was Euclidean"
elif distanceMetric == 2:
	print "Distance metric used was Manhattan"				
elif distanceMetric == 3:
	print "Distance metric used was Chebyshev"
					
print "Sum of distance amongst predictions and test data is %d" %testAbsDiffSum
print "Sum of all ratings found is %d" %testRatingsFound
print "Total suggestions made by system were %d" %totalSuggestionsMade
print "%d predictions were spot on" %spotOn

print "The mean absolute distance is %f" % ((float(testAbsDiffSum) / testRatingsFound))