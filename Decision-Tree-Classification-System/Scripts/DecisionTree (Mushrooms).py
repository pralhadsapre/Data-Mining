import sys
import math
from collections import Counter 
from operator import itemgetter

# The command line arguments are such
# 1 - Input data file
# 2 - Class Column Index
# 3 - Impurity Measure to use (1 - Gini, 2 - Entropy)

mapping = []
masterSet = []
dataSet = []
testSet = []
stringColumns = []

classIndex = int(sys.argv[2])
impurityMeasure = int(sys.argv[3])

nominalOrdinalThreshold = 20
impurityThreshold = 0.05

def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def printSomeData(dataSet):
	for x in range(10):
		print dataSet[x]

	# list = [row[0] for row in dataSet]
	# print list	

# Mushroom data set
def readFile(fileName, dataSet):
	dataFile = open(fileName, 'r')
	droppedRows = 0

	for line in dataFile:
		data = line.split(',')		
		data[len(data) - 1] = data[len(data) - 1].split('\n', 2)[0]

		# popping the missing attribute stalk root
		data.pop(11)		
		if '?' in data:
			# print data
			droppedRows += 1
		else:
			for x in range(len(data)):
				if isFloat(data[x]):
					data[x] = float(data[x])
				else:
					if x not in stringColumns and x != classIndex:
						stringColumns.append(x)
					data[x] = str(data[x])

			dataSet.append(data)
	
	print "%d rows dropped" %droppedRows
	dataFile.close()

# make column values into numbers
def assignNumbers(dataSet, columnNumber, mapping):
	for line in dataSet:
		if line[columnNumber] not in mapping:
			mapping.append(line[columnNumber])

		line[columnNumber] = int(mapping.index(line[columnNumber]))

def getDominantClass(dataChunk, classIndex):
	classCounts = Counter(sublist[classIndex] for sublist in dataChunk)
	classCounts = sorted(classCounts.iteritems(), key = lambda x: x[1], reverse = True)
	return classCounts[0][0]

def getGINI(dataChunk, classIndex):
	classCounts = Counter(sublist[classIndex] for sublist in dataChunk)
	classCounts = sorted(classCounts.iteritems())

	giniValue = 1

	for item in classCounts:
		giniValue -= ((item[1] / float(len(dataChunk))) ** 2)

	return giniValue


def getEntropy(dataChunk, classIndex):
	classCounts = Counter(sublist[classIndex] for sublist in dataChunk)
	classCounts = sorted(classCounts.iteritems())

	entropy = 0.0

	for item in classCounts:
		tempValue = item[1] / float(len(dataChunk))
		entropy -= (tempValue * math.log(tempValue, 2))
	
	return entropy

def getImpurity(dataChunk, classIndex):
	if impurityMeasure == 1:
		return getGINI(dataChunk, classIndex)
	else:
		return getEntropy(dataChunk, classIndex)

def getUniqueValuesWithIndexes(columnValues):
	classCounts = Counter(columnValues)	
	classCounts = sorted(classCounts.iteritems(), key = lambda x: x[0], reverse = False)
		
	previousIndex = 0
	valuesAndLastIndex = []
	for item in classCounts:
		singleItem = []
		singleItem.append(item[0])
		singleItem.append(item[1] + previousIndex)

		previousIndex = item[1]
		valuesAndLastIndex.append(singleItem)

	return valuesAndLastIndex

def findSplitPoint(dataChunk, classIndex):
	classNumber = -10
	startIndex = -10
	length = 0

	tempClassNumber = -10
	tempStartIndex = -10
	tempLength = 0

	for line in dataChunk:
		print "Do this later for continuous attributes"

# Class to contain the splitting condition
class ColumnSplitCondition(object):

	# classIndex = 0
	# columnIndex = 0
	# value = 0.0
	# giniValue = 0.0	

	def __init__(self, classIndex, columnIndex):
		self.columnIndex = columnIndex	
		self.classIndex = classIndex

		self.splitIndex = 0
		self.value = 0.0
		self.impurityValue = 0.0
		self.canSplit = False

	def chopDataSetForImpurity(self, dataChunk, index):
		chunkLeft = dataChunk[ : index]
		chunkRight = dataChunk[index: ]

		averagedImpurity = ((float(len(chunkLeft)) / len(dataChunk)) * getImpurity(chunkLeft, self.classIndex) + (float(len(chunkRight)) / len(dataChunk)) * getImpurity(chunkRight, self.classIndex))
		return averagedImpurity

	def computeBestSplitValue(self, dataChunk):

		minImpurity = 100
		value = 0.0
		splitIndex = 0
		dataChunk = sorted(dataChunk, key=lambda x: x[self.columnIndex])
		sortedValues = [row[self.columnIndex] for row in dataChunk]

		sortedValues = getUniqueValuesWithIndexes(sortedValues)
		
		if len(sortedValues) == 1:
			self.canSplit = False		
		else:
			for index in range(len(sortedValues) - 1):
				# print "Computing for %d out of %d column values" % (index, len(sortedValues) - 1)
				weightedImpurity = self.chopDataSetForImpurity(dataChunk, sortedValues[index][1])
				if weightedImpurity < minImpurity:
					splitIndex = sortedValues[index][1]
					minImpurity = weightedImpurity
					value = sortedValues[index][0]

			self.splitIndex = splitIndex
			self.impurityValue = minImpurity
			self.value = value
			self.canSplit = True

	def printCondition(self):
		print "Column: " + str(self.columnIndex) + " Value: " + str(self.value) + " Impurity: " + str(self.impurityValue)	

# Class which represents a tree node
class Node(object):

	# ColumnSplitCondition 
	# columnSplit = None
	# # Node 
	# left = None
	# right = None

	# dataSet = []
	# level = 0
	# classIndex = 0

	def __init__(self, dataSet, classIndex, level):		
		self.dataSet = dataSet
		self.classIndex = classIndex
		self.level = level

		self.columnSplit = None
		self.left = None
		self.right = None

		self.leaf = False
		self.classType = None
		self.impurity = getImpurity(self.dataSet, self.classIndex)

		if self.impurity <= impurityThreshold:
			self.makeLeaf()

		if len(self.dataSet) < (len(dataSet) * 0.05):
			self.makeLeaf()

	def makeLeaf(self):
		self.leaf = True
		self.classType = getDominantClass(self.dataSet, self.classIndex)

	def assignLeft(self, left):
		self.left = left

	def assignRight(self, right):
		self.right = right

	def generateDataSets(self, splitSets):

		if self.leaf == False:
			if self.computeBestColumnToSplit():
				dataChunk = sorted(self.dataSet, key=lambda x: x[self.columnSplit.columnIndex])		
				
				chunkLeft = dataChunk[ : self.columnSplit.splitIndex]
				chunkRight = dataChunk[self.columnSplit.splitIndex : ]				

				splitSets.append(chunkLeft)
				splitSets.append(chunkRight)
				return True
			else:
				self.makeLeaf()
				return False

		else:
			return False			

	def computeBestColumnToSplit(self):

		bestSplit = None

		splitConditions = []

		# print "Impurity : " + str(self.impurity)
		# # print self.dataSet
		# print "Level : " + str(self.level)
		for x in range(len(self.dataSet[0])):
			if x != self.classIndex:
				# print "Computing for column %d" % (x)
				split = ColumnSplitCondition(self.classIndex, x)
				split.computeBestSplitValue(self.dataSet)

				if not split.canSplit:
					continue

				splitConditions.append(split)
				if bestSplit is not None:
					if bestSplit.impurityValue > split.impurityValue:
						bestSplit = split
				else:
					bestSplit = split				

		self.columnSplit = bestSplit

		if self.columnSplit is not None:
			# self.columnSplit.printCondition()
			return True
		else:
			return False
			

	def printNodeInfo(self):
		# print self.dataSet
		print "Impurity : " + str(self.impurity)
		print self.leaf
		if self.leaf == True:
			print "Class: " + str(self.classType) + " Impurity : " + str(self.impurity) + " Level : " + str(self.level)		
		else:			
			print "Impurity : " + str(self.impurity) + " Level : " + str(self.level) 
			self.columnSplit.printCondition()

def buildDecisionTree():
	nodeQueue = []
	count = 0
	nodeQueue.append(rootNode)

	while len(nodeQueue) > 0:
		head = nodeQueue.pop(0)

		if(head.level < 50):

			# print "\n"
			# print "Iteration " + str(count)
			count += 1
			sets = []
			if head.generateDataSets(sets):

				# print "left chunk"
				# print sets[0]

				# print "right chunk"
				# print sets[1]

				left = Node(sets[0], classIndex, (head.level + 1))
				right = Node(sets[1], classIndex, (head.level + 1))		

				head.assignLeft(left)
				head.assignRight(right)
				
				nodeQueue.append(left)
				nodeQueue.append(right)
			else:
				dummy = 0
				# head.printNodeInfo()
		else:
			break	

	while len(nodeQueue) > 0:
		head = nodeQueue.pop(0)
		head.makeLeaf()

def printDecisionTree():
	print "\n"
	nodeQueue = []
	rootNode.printNodeInfo()
	nodeQueue.append(rootNode.left)
	nodeQueue.append(rootNode.right)
	print ""

	while len(nodeQueue) > 0:	
		head = nodeQueue.pop(0)
		head.printNodeInfo()
		print ""
		if head.left is not None:
			nodeQueue.append(head.left)
		if head.right is not None:
			nodeQueue.append(head.right)

def classifyRecords(testSet, root):
	temp = root	
	spotOn = 0
	errors = 0
	count = 0
	for record in testSet:
		temp = root
		while not temp.leaf:
			# temp.printNodeInfo()
			if record[temp.columnSplit.columnIndex] <= temp.columnSplit.value:
				temp = temp.left
			else:
				temp = temp.right

		if record[classIndex] == temp.classType:
			spotOn += 1
			# print "Classified %d record correctly" % (count + 1)
		else:
			errors += 1
			# print "Classified %d record incorrectly" % (count + 1)
		count += 1

	print "Classified correctly %d / %d" % (spotOn, len(testSet))
	return (spotOn, len(testSet))

def printStatistics():
	print "Dataset : " + str(sys.argv[1])
	print "Impurity measure : " + str("Gini" if impurityMeasure == 1 else "Information Gain")
	print "Accuracy was %d%%" % ((correctPredictions / totalPredictions) * 100)

readFile(sys.argv[1], dataSet)

# print stringColumns
for x in stringColumns:
	assignNumbers(dataSet, x, mapping)
	mapping = []

# printSomeData(dataSet)

masterSet = dataSet
window = 0
windowSize = float(len(masterSet)) / 10

correctPredictions = 0.0
totalPredictions = 0.0

while window < 10:
	dataSet = masterSet[0 : int(round(window * windowSize))] + masterSet[int(round((window + 1) * windowSize)) : ]
	testSet = masterSet[int(round(window * windowSize)) : int(round((window + 1) * windowSize))]

	# print len(dataSet)
	# print len(testSet)
	rootNode = Node(dataSet, classIndex, 0)
	buildDecisionTree()
	# printDecisionTree()
	stats = classifyRecords(testSet, rootNode)
	correctPredictions += stats[0]
	totalPredictions += stats[1]

	window += 1
	dataSet = []
	testSet = []

printStatistics()
