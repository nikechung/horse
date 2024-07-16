from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor


def findBestAlgorithm(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = [("Linear Regression", LinearRegression()),
            ("Random Forest Regression", RandomForestRegressor()),
            ("KNN Regression", KNeighborsRegressor()),
            ("Decision Tree", DecisionTreeRegressor()),
            ("Gradient Boosting Regression", GradientBoostingRegressor())]
    
    bestScore = 0
    bestAlgoName = None
    bestAlgo = None

    for name, model in models:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        score = r2_score(y_test, y_pred)

        if score > bestScore:
            bestAlgoName = name
            bestScore = score
            bestAlgo = model
    

    print(f'best Algo: {bestAlgoName} with score {bestScore}')
    return bestAlgo, bestScore