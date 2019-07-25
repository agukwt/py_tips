import pandas
import pprint
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier


def main():
    df = pandas.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wdbc.data',
                         header=None)

    X = df.loc[:, 2:].values
    y = df.loc[:, 1].values
    le = LabelEncoder()
    y = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1)

    rfc = RandomForestClassifier(random_state=0, verbose=1)
    param_grid = [
        {'n_estimators': [5, 10], 'max_depth': [5, 10]},
        {'max_features': [10, 20], 'class_weight': [None, 'balanced']},
    ]

    gs = GridSearchCV(
                estimator=rfc,
                param_grid=param_grid,
                scoring='roc_auc',
                cv=10,
                n_jobs=-1,
    )
    gs = gs.fit(X_train, y_train)
    print('gs.best_score_: {}'.format(gs.best_score_))

    # arrayの大きさが、cv(10)でなく8なのは、GridSearchの組合せ数(8)
    pprint.pprint(gs.cv_results_)
    # print('mean_train_score: {}'.format(gs.cv_results_["mean_train_score"]))
    # print('std_train_score: {}'.format(gs.cv_results_["std_train_score"]))
    # print('mean_test_score: {}'.format(gs.cv_results_["mean_test_score"]))
    # print('std_test_score: {}'.format(gs.cv_results_["std_test_score"]))

    clf = gs.best_estimator_
    clf.fit(X_train, y_train)
    print('Test auc: %.3f' % clf.score(X_test, y_test))


if __name__ == '__main__':
    main()
