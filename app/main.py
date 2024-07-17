from horse import getHorseData
from horse_history import getHorseHistory, prepareData
import algorithm_analysis
import feature_analysis
import app
import sys


horse_data = getHorseData('../horses.csv')
horse_race_history = getHorseHistory('../horses_history.csv', horse_data)
horse_race_data = prepareData(horse_race_history)

d = horse_race_data.dropna()
y = d['speed_m_s']

if '--find_optimal_features' in sys.argv:
    features =[ "horse_sex", "horse_color", "horse_age", 'race_class', "horse_import_type",
           "horse_country", "weight",  "G", "dr", "trainer", "jockey", "distance", 
            "track", "course", "month", "horse_sire", "horse_dam", "horse_dam_sire", 'no_of_turns']
    optimal_features, score = feature_analysis.findBestFeatureCombinations(horse_race_data, y, features)
else:
    optimal_features = feature_analysis.getFeatures()

X = d[optimal_features] 

if '--find_algorithm' in sys.argv:
    model, score = algorithm_analysis.findBestAlgorithm(X, y)
else:
    model = algorithm_analysis.getModel() 

model.fit(X, y)
app.run(model)