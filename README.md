# Data-Mining
Various projects related to Data Mining

Curse of Dimensionality
This demonstrates through a curve how distance amongst data points becomes insignificant as the number of dimensions increases

Movie Recommendation System
This project has two implementations for a recommendation algorithm.
The first one is a Naive Algorithm which averages the ratings for a movie not seen.
The second algorithm "Recommendation.py" uses a model which factors in the age and gender to generate predictions using K Nearest Neighbours (K=100)

Decision-Tree-Classification-System
This system builds a decision tree classifier for the given data set and predicts accuracy using 10 fold cross validation. 
The file names correspond to data sets from UC Irvine Machine learning repository.
Performance is best for ordinal and nominal attributes, though continuous attributes give an acceptable accuracy.
To use the scripts follow the pattern given below
e.g. cmd> python "DecisionTree.py" 'filePathForData' 'classColumnIndex #starts at 0' 'ImpurityMeasure #1 – GINI #2 – Information Gain'
