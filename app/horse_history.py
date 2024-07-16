import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np

horse_history_data = None

course_mapping = {
    "A": 1,
    "A+2": 2,
    "A+3": 3,
    "B": 4,
    "B+2": 5,
    "B+3": 6,
    "C": 7,
    "C+3": 8,
    "NA": 9,
    "NA+2": 10,
    "NB": 11,
    "NB+2": 12,
    "AWT": 13
}

g_mapping = {
    'G': 2.75,
    'GF': 2.5,
    'GD': 2.75,
    'GY': 3,
    'Y': 3.25,
    'S': 3.25,
    'WS': 3,
    'FT': 2,
    'WF': 2.5,
    'YS': 3.5,
    'H': 4
}

def getHorseHistory(filename, horse_data):
    global horse_history_data
    horse_history_data = pd.read_csv(filename, parse_dates=['date'], date_format='%d/%m/%y')
    horse_history_data = horse_history_data.drop(horse_history_data[horse_history_data["finish_time"]=="--"].index)
    horse_history_data = horse_history_data.drop(horse_history_data[horse_history_data["weight"]=="--"].index)
    

    horse_history_data["month"] = horse_history_data["date"].dt.month

    #process location_run
    horse_history_data["course_location"] = horse_history_data["location_run"].apply(lambda x: x.split('/')[0].strip())
    horse_history_data["track"] = horse_history_data["location_run"].apply(lambda x: x.split('/')[1].strip()) 
    horse_history_data["course"] = horse_history_data["location_run"].apply(extractCourse)
    
    horse_history_data["weight"] = horse_history_data["weight"].astype("int")

    horse_history_data["finish_time_ms"] = horse_history_data["finish_time"].apply(lambda x: None if x == "--" else (int(x.split(".")[0]) * 60 + int(x.split(".")[1])) * 1000 + int(x.split(".")[2]) * 10)
    horse_history_data["speed_m_s"] = horse_history_data["distance"] / horse_history_data["finish_time_ms"] * 1000
    horse_history_data["distance_km"] = horse_history_data["distance"].astype("int") / 1000

    # Fill in horse information
    horse_history_data["horse_country"] = horse_history_data["horse_id"].map(horse_data["country"].to_dict())
    horse_history_data["horse_age"] = horse_history_data["horse_id"].map(horse_data["age"].to_dict())
    horse_history_data["horse_age"] = horse_history_data["date"].dt.year - 2024 + horse_history_data["horse_age"]
    horse_history_data["horse_owner"] = horse_history_data["horse_id"].map(horse_data["owner"].to_dict())
    horse_history_data["horse_import_type"] = horse_history_data["horse_id"].map(horse_data["import_type"].to_dict())
    horse_history_data["horse_color"] = horse_history_data["horse_id"].map(horse_data["color"].to_dict())
    horse_history_data["horse_sex"] = horse_history_data["horse_id"].map(horse_data["sex"].to_dict())
    horse_history_data["horse_sire"] = horse_history_data["horse_id"].map(horse_data["sire"].to_dict())
    horse_history_data["horse_dam"] = horse_history_data["horse_id"].map(horse_data["dam"].to_dict())
    horse_history_data["horse_dam_sire"] = horse_history_data["horse_id"].map(horse_data["dam_sire"].to_dict())
    return horse_history_data.copy()

def extractCourse(loc_run):
    parts = loc_run.split('/')
    if len(parts) >= 3:
        course = parts[2].replace("\"", "").strip()
    elif parts[1].strip() == 'AWT':
        course = "AWT"
    else:
        course = None
    return course

__labelEncoders = {}
def __getLabelEncoder(field):
    global __labelEncoders
    if not field in __labelEncoders:
        __labelEncoders[field] = LabelEncoder()

    return __labelEncoders[field]
    

def encodeCourseLocation(course_location, fit=True):
    global horse_history_data
    le = __getLabelEncoder("course_location")
    if fit:
        le.fit(horse_history_data["course_location"])

    return le.transform(course_location)
    
def encodeWithLabelEncoder(data, field, fit=True):
    le = __getLabelEncoder(field)
    if fit:
        le.fit(data)
    return le.transform(data) 

def getMedianRank(field):
    return horse_history_data.groupby(field)["speed_m_s"].median().rank()

def encodeWithMedianRank(data, field):
    global horse_history_data
    return data.map(getMedianRank(field).to_dict())
    
def prepareData(race_data):
    global horse_history_data
    global course_mapping
    
    data = race_data.copy()

    # Remove foreign races
    data = data[(data["course_location"] == "ST") | (data["course_location"] == "HV")]

    data["G"] = data["G"].map(g_mapping)
    data["course"] = data["course"].map(course_mapping)

    fieldsToEncodeWithMedian = ['race_class', 'dr', 'trainer', 'jockey', 'horse_country', 'horse_owner',
                                'horse_import_type', 'horse_color', 'horse_sex', 
                                'horse_sire', 'horse_dam', 'horse_dam_sire' , 
                                'course']

    for field in fieldsToEncodeWithMedian:
        data[field] = encodeWithMedianRank(data[field], field)

    data["gear"] = data["gear"].map(lambda x: 0 if x == "--" else 1)
    data["track"] = encodeWithLabelEncoder(data["track"], 'track') 
    
    return data
    


# def preProcess_bak(horse_history_data, horse_data):
#     horse_race_data = horse_history_data.copy()

#     # Drop features
#     col_to_drop = ["date", "result", "location_run", "running_position", "finish_time"]
#     horse_race_data = horse_race_data.drop(col_to_drop, axis=1)

#     from scipy import stats

#     # Calculate the Z-scores
#     z_scores = np.abs(stats.zscore(horse_race_data["speed_m_s"]))
#     outlier_mask = (z_scores > 3)
#     horse_race_data = horse_race_data[~outlier_mask]
#     return horse_race_data
