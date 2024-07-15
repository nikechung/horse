import itertools

from horse import getHorseData
from horse_history import getHorseHistory, preProcess
import itertools
import time
from math import comb
import feature_analysis 

horse_data = getHorseData('../horses.csv')
horseHistory = getHorseHistory('../horses_history.csv')
horse_race_data = preProcess(horseHistory, horse_data)


features =[ "horse_sex", "horse_color", "horse_age", 'race_class', "horse_import_type",
           "horse_country", "weight",  "G", "dr", "trainer", "jockey", "distance", "act_wt",
            "course_location", "track", "course", "month", "horse_sire", "horse_dam", "horse_dam_sire"]
d = horse_race_data.dropna()
y = d['speed_m_s']
x = d[features]

bestScore = 0
bestFeatures = None
startTime = time.time()
speed = 0

for i in range(2, len(features)):
  features, score, speed = feature_analysis.forward_stepwise(x, y, i, bestScore, speed)
  if score > bestScore:
      bestScore = score
      bestFeatures = features

execution_time = time.time() - startTime
print(f'Completed scanning in {int(execution_time / 60)} min {int(execution_time % 60)} s')
print(f'Best Score: {bestScore:.4f} with features: {bestFeatures}')
