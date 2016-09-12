'''
    Basic classification meant as baseline for further classification.

    Using average downloads as target we achieve accuracy rougly 59%.
    Which is by 9%  better than guessing
'''

import sys
import os
import pandas as pd
import numpy as np
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from source.helpers.db import fetch

FILE_NAME = 'data.csv'


def load_data_from_db_if_neccesarry():
    if os.path.isfile(FILE_NAME):
        print('skipping download')
        return

    result = fetch((
        "SELECT "
        "size, dependencies_count, mainteiners_count, "
        "contributors_count, has_tests, has_readme, "
        "stargazers_count, m_average_downloads.avg "
        "FROM repos AS r "
        "INNER JOIN m_average_downloads ON r.id = m_average_downloads.repo_id "
        "WHERE has_readme is not Null "
        "ORDER BY RANDOM();"
    ))

    X = np.array(result.fetchall(), dtype=np.float64)

    dataframe = pd.DataFrame.from_records(data=X)

    with open(FILE_NAME, 'w') as f:
        dataframe.to_csv(path_or_buf=f)


def prepare_data():
    dataframe = pd.read_csv(FILE_NAME, engine='python')
    dataset = dataframe.values
    dataset = dataset.astype('float32')
    X = dataset[:, 0:7]
    Y = dataset[:, 8]  # 7 is stars, 8 is average downloads

    return (X, Y)


if __name__ == '__main__':
    load_data_from_db_if_neccesarry()
    X, Y = prepare_data()

    Y_target = np.copy(Y)

    sum = 0
    for i, e in enumerate(Y_target):
        if e >= 73:
            sum += 1
            Y_target[i] = 1
        else:
            Y_target[i] = 0

    print('there are two classes: good with {} memebers and bad with {} members'.format(sum, Y.shape[0] - sum))
    print("Classes ratio: %.2f%%" % (sum / Y.shape[0] * 100))

    seed = 7
    np.random.seed(seed)

    estimators = []
    estimators.append(('standardize', sklearn.preprocessing.StandardScaler()))
    estimators.append(('forest', RandomForestClassifier()))
    pipeline = Pipeline(estimators)
    kfold = sklearn.cross_validation.KFold(n=len(X), n_folds=5, random_state=seed)
    print('Calculating')
    results = sklearn.cross_validation.cross_val_score(pipeline, X, Y_target, cv=kfold)
    print("Accuracy: %.2f%%" % (results.mean() * 100))
