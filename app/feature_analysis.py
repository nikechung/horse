import itertools
import time
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from math import comb
import matplotlib.pyplot as plt
import seaborn as sns

# Get features
def getFeatures():
  return ['horse_color', 'horse_age', 'race_class', 'weight', 'dr', 'jockey', 'distance_km', 'quarter', 'horse_dam', 'no_of_turns']

# Using heatmap to identify relationships between variables
def createHeatmap(data):
  columns = ['distance_km', 'act_wt', 'month', 'quarter', 'track', 'course',
       'race_class', 'dr', 'trainer',
       'jockey', 'weight', 'gear',
       'horse_country', 'horse_age', 'horse_owner',
       'horse_import_type', 'horse_sex', 'horse_sire',
       'horse_dam', 'horse_dam_sire',
       'horse_color', 'speed_m_s']
  corr_matrix = data[columns].corr()

  plt.figure(figsize=(40,30))
  sns.heatmap(corr_matrix, annot=True, cmap="YlOrRd")
  plt.show()

# Search best feature combinations
def findBestFeatureCombinations(data, y, features):
  bestScore = 0
  bestFeatures = None
  startTime = time.time()
  speed = 0
  X = data[features]

  for i in range(2, len(features)):
    features, score, speed = __findBestFeatureCombinations(X, y, i, bestScore, speed)
    if score > bestScore:
        bestScore = score
        bestFeatures = features

  execution_time = time.time() - startTime
  print(f'Completed scanning in {int(execution_time / 60)} min {int(execution_time % 60)} s')
  print(f'Best Score: {bestScore:.4f} with features: {bestFeatures}')
  return bestFeatures, bestScore


def __findBestFeatureCombinations(X, y, combination, best_score = 0, speed = 0):
  best_features = None

  featuresCombinations = itertools.combinations(X.columns, combination)
  combinationCount = comb(len(X.columns), combination)

  now = time.asctime( time.localtime(time.time()) )

  print(f'Start checking {combination} feature combinations: {combinationCount} to check {now}')
  if speed != 0:
    eta = combinationCount / speed
    print(f'Estimate Completion Time: {int(eta / 60)} min {int(eta % 60)} s')
  j=0
  start_time = time.time()
  lastProgress = 0
  for features in featuresCombinations:
    j=j+1

    execution_time = (time.time() - start_time)
    if execution_time != 0:
        speed = j/execution_time
        eta = (combinationCount - j)/speed
        progress = int(j/combinationCount * 100)

        if execution_time - lastProgress >= 30:
            lastProgress = execution_time
            print(f'\tchecked {j} of {combination} combination ({progress}%) in {int(execution_time / 60)} min {int(execution_time % 60)} s (Estimate Completion Time: {int(eta / 60)} min {int(eta % 60)} s)')

    model = LinearRegression()
    x_train, x_test, y_train, y_test = train_test_split(X[list(features)], y, test_size=0.2, random_state=42)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    score = r2_score(y_test, y_pred)

    if score > best_score:
      best_score = score
      best_features = features
      print(f'\t{best_features}: {best_score:.3f}')

  execution_time = (time.time() - start_time)
  print(f'Complete checked {combinationCount} combination in  {int(execution_time / 60)} min {int(execution_time % 60)} s')
  return best_features, best_score, combinationCount / execution_time

