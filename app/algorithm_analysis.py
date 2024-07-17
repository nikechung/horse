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

def getModel():
    global models
    name, model = models[5]
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

def findBestHyperParameter(model, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    param_test = {
        "n_estimators": list(range(100, 300, 100)),
        "learning_rate": [0.0, 0.1, 0.2],
        "max_depth": list(range(1, 3, 1)),
        "subsample": [0.0, 0.1, 0.2],
    }

    grid = GridSearchCV(estimator=model, param_grid=param_test, scoring='r2')
    grid.fit(X_train, y_train)
    best_model = grid.best_estimator_
    best_params = grid.best_params_
    grid.score
    y_pred = best_model.predict(X_test)
    score = r2_score(y_test, y_pred)
    print("Best params: ", best_params)
    print("Score: ", score)

    return best_params, score