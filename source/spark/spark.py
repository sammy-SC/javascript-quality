from pyspark import SparkContext
import pandas as pd
import sklearn
import numpy as np
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC

# Print settings
pd.options.display.width = 200
pd.set_option('display.float_format', lambda x: '%.2f' % x)


# Constants
APP_NAME = "Javascript package classificator"


def pipeline_with_classifier(classifier):
    estimators = []
    estimators.append(('standardize', sklearn.preprocessing.StandardScaler()))
    estimators.append(('forest', classifier))
    pipeline = Pipeline(estimators)

    return pipeline


# Main functionality
def main(sc):
    print('starting')
    # filepath = '/Users/samuelsusla/Developer/jmq/data/data.csv'
    filepath = '/home/ubuntu/jmq/data/data.csv'
    dataframe = pd.read_csv(filepath, delimiter=',')
    dataset = dataframe.values

    X = dataset[:, 0:7]
    Y = np.zeros([len(X)])

    sum = 0
    for i, e in enumerate(dataset[:, 12]):
        if e > 73:
            sum += 1
            Y[i] = 1

    X_broadcasted = sc.broadcast(X)
    Y_broadcasted = sc.broadcast(Y)
    print('broadcasted')

    def mapIt(e):
        print('calculating: ', e[0])

        seed = 7
        np.random.seed(seed)
        kfold = sklearn.cross_validation.KFold(n=len(X_broadcasted.value), n_folds=10, random_state=seed)

        pipeline = pipeline_with_classifier(e[1])
        results = cross_val_score(pipeline, X_broadcasted.value, Y_broadcasted.value, cv=kfold)

        return (e[0], results.mean() * 100)

    def reduceIt(a, b):
        print('reducing: {} and {}'.format(a, b))
        if a[1] > b[1]:
            return a
        else:
            return b

    classifiers = [
        ('RandomForestClassifier', RandomForestClassifier()),
        ('KNN with uniform weights', KNeighborsClassifier()),
        ('KNN with distance weights', sklearn.neighbors.KNeighborsClassifier(weights='distance')),
        ('SVC', SVC()),
        ('Ada boost classifier', AdaBoostClassifier()),
    ]

    classifiers = sc.parallelize(classifiers)
    result = classifiers.map(mapIt).reduce(reduceIt)
    print(result)


if __name__ == "__main__":
    sc = SparkContext()

    main(sc)
