import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np

horse_history_data = None

g_mapping = {
    'G': 2.75,
    'GF': 2.5,
    'GD': 2.75,
    'GY': 3,
    'Y': 3.25,
    'S': 3.25,
    'SL': 3.25,
    'WS': 3,
    'F': 2,
    'FT': 2,
    'WF': 2.5,
    'YS': 3.5,
    'WE': 3,
    'H': 4
}

def getHorseHistory(filename, horse_data):
    global horse_history_data
    horse_history_data = pd.read_csv(filename, parse_dates=['date'], date_format='%d/%m/%y')
    horse_history_data = horse_history_data.drop(horse_history_data[horse_history_data["finish_time"]=="--"].index)
    horse_history_data = horse_history_data.drop(horse_history_data[horse_history_data["weight"]=="--"].index)
    
    horse_history_data["month"] = horse_history_data["date"].dt.month

    #process location_run
    horse_history_data["location"] = horse_history_data["location_run"].apply(lambda x: x.split('/')[0].strip())
    horse_history_data["track"] = horse_history_data["location_run"].apply(lambda x: x.split('/')[1].strip()) 
    horse_history_data["course"] = horse_history_data["location_run"].apply(extractCourse)
    
    horse_history_data["weight"] = horse_history_data["weight"].astype("int")

    horse_history_data["finish_time_ms"] = horse_history_data["finish_time"].apply(lambda x: None if x == "--" else (int(x.split(".")[0]) * 60 + int(x.split(".")[1])) * 1000 + int(x.split(".")[2]) * 10)
    horse_history_data["speed_m_s"] = horse_history_data["distance"] / horse_history_data["finish_time_ms"] * 1000

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
    course = loc_run
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
    

def encodeWithLabelEncoder(data, field, fit=True):
    le = __getLabelEncoder(field)
    if fit:
        le.fit(data)
    return le.transform(data) 

def applyNoOfTurns(data):
    data["no_of_turns"] = 0
    data.loc[data["location"] == 'HV', 'no_of_turns'] = data.loc[data["location"] == 'HV']['distance'].map({
        1000: 1,
        1200: 2,
        1650: 3,
        1800: 3,
        2200: 4,
        2400: 4
    })

    data.loc[data["location"] == 'ST', 'no_of_turns'] =data.loc[data["location"] == 'ST']['distance'].map({
        1000: 0,
        1200: 1,
        1400: 1,
        1600: 1,
        1650: 1,
        1800: 1,
        2000: 2,
        2200: 2,
        2400: 2
    })


def getMedianRank(field):
    return horse_history_data.groupby(field)["speed_m_s"].median().rank()

def encodeWithMedianRank(data, field):
    global horse_history_data
    medianRank = getMedianRank(field).to_dict()
    # print(medianRank)
    return data.map(medianRank)
    
def prepareData(race_data):
    global horse_history_data
    global course_mapping
    
    data = race_data.copy()

    # Remove foreign races
    data = data[(data["location"] == "ST") | (data["location"] == "HV")]

    data["G"] = data["G"].map(g_mapping)

    fieldsToEncodeWithMedian = ['race_class', 'trainer', 'jockey', 'horse_country', 'horse_owner',
                                'horse_import_type', 'horse_color', 'horse_sex', 
                                'horse_sire', 'horse_dam', 'horse_dam_sire', 'course']

    for field in fieldsToEncodeWithMedian:
        data[field] = encodeWithMedianRank(data[field], field)

    data["gear"] = data["gear"].map(lambda x: 0 if x == "--" else 1)
    data["track"] = encodeWithLabelEncoder(data["track"], 'track') 

    applyNoOfTurns(data)
    
    return data
    