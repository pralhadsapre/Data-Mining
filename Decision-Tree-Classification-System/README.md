# Decision-Tree-Classification-System
Data Mining System for Classification

This system builds a decision tree classifier for the given data set and predicts accuracy using 10 fold cross validation. 
The file names correspond to data sets from UC Irvine Machine learning repository.
Performance is best for ordinal and nominal attributes, though continuous attributes give an acceptable accuracy.

To use the scripts follow the pattern given below
e.g. cmd> python "DecisionTree.py" 'filePathForData' 'classColumnIndex #starts at 0' 'ImpurityMeasure #1 – GINI #2 – Information Gain'
