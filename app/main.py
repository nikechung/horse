import itertools

from horse import getHorseData
from horse_history import getHorseHistory, prepareData
import itertools
import time
from math import comb
import feature_analysis 
import algorithm_analysis
from sklearn.ensemble import GradientBoostingRegressor
import app

horse_data = getHorseData('../horses.csv')
horseHistory = getHorseHistory('../horses_history.csv', horse_data)
horse_race_data = prepareData(horseHistory)

d = horse_race_data.dropna()
y = d['speed_m_s']

features =[ "horse_sex", "horse_color", "horse_age", 'race_class', "horse_import_type",
           "horse_country", "weight",  "G", "dr", "trainer", "jockey", "distance", 
            "track", "course", "month", "horse_sire", "horse_dam", "horse_dam_sire", 'no_of_turns']
X = d[features]

# features, score = feature_analysis.findBestFeatureCombinations(X, y)
features = ['horse_color', 'horse_age', 'race_class', 'weight', 'G', 'dr', 'jockey', 'distance', 'month', 'horse_sire', 'horse_dam', 'no_of_turns']


X = d[features] 
# model, score = algorithm_analysis.findBestAlgorithm(X, y)
# algorithm_analysis.findBestHyperParameter(model, X, y)

model = GradientBoostingRegressor()
model.fit(X, y)
app.run()