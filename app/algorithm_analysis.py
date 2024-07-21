from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV
from sklearn.metrics import r2_score

models = [("Linear Regression", LinearRegression()),
            ("Random Forest Regression", RandomForestRegressor()),
            ("KNN Regression", KNeighborsRegressor()),
            ("Decision Tree", DecisionTreeRegressor()),
            ("SVR", SVR()),
            ("Gradient Boosting Regression", GradientBoostingRegressor())]

# Selected model with best performance
def getModel():
    global models
    model = GradientBoostingRegressor(loss='huber', learning_rate=0.1, n_estimators=300, max_depth=3, subsample=0.8)
    return model

def findBestAlgorithm(X, y):
    global models
    bestScore = 0
    bestAlgoName = None
    bestAlgo = None
    print('finding best algorithm')
    for name, model in models:
        score = cross_val_score(model, X, y, scoring='r2').mean()
        print(f'\tchecked {name}: {score}')
        if score > bestScore:
            bestAlgoName = name
            bestScore = score
            bestAlgo = model

    print(f'best Algo: {bestAlgoName} with score {bestScore}')
    return bestAlgo, bestScore

# search best hyperparameter by coarse tuning
def findBestHyperParameterCoarseTune(model, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    param_test = {
        "loss": ["squared_error", "absolute_error", "huber", "quantile"],
        "learning_rate": [0.001, 0.01, 0.1, 0.2],
        "n_estimators": [100, 200, 300],
        "max_depth": [3, 5, 7],
        "subsample": [0.1, 0.5, 1.0]
    }

    grid = GridSearchCV(estimator=model, param_grid=param_test, scoring='r2', n_jobs=-1, verbose=10)
    grid.fit(X_train, y_train)
    best_model = grid.best_estimator_
    best_params = grid.best_params_
    y_pred = best_model.predict(X_test)
    score = r2_score(y_test, y_pred)
    print("Best params: ", best_params)
    print("Score: ", score)

    return best_params, score

# search best hyperparameter by fine tuning
def findBestHyperParameterFindTune(model, X, y):
    # 1st find tuning:
    # param_test = {
    #     "learning_rate": [0.05, 0.1, 0.15],
    #     "n_estimators": [250, 300, 350],
    #     "max_depth": [2, 3, 4],
    #    "subsample": [0.3, 0.4, 0.5]
    #}
    # Best params:  {'learning_rate': 0.1, 'loss': 'huber', 'max_depth': 3, 'n_estimators': 300, 'subsample': 0.5}
    # Score:  0.7809316995858007
    # 

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    param_test = {
        # "learning_rate": [0.05, 0.1, 0.15],
        # "n_estimators": [250, 300, 350],
        # "max_depth": [2, 3, 4],
        "subsample": [0.6, 0.7, 0.8, 0.9]
    }

    grid = GridSearchCV(estimator=model, param_grid=param_test, scoring='r2', n_jobs=-1, verbose=10)
    grid.fit(X_train, y_train)
    best_model = grid.best_estimator_
    best_params = grid.best_params_
    y_pred = best_model.predict(X_test)
    score = r2_score(y_test, y_pred)
    print("Best params: ", best_params)
    print("Score: ", score)

    return best_params, score