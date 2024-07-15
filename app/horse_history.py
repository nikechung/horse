import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np

def getHorseHistory(filename):
    horse_history_data = pd.read_csv(filename, parse_dates=['date'], date_format='%d/%m/%y')
    horse_history_data = horse_history_data.drop(horse_history_data[horse_history_data["finish_time"]=="--"].index)
    horse_history_data = horse_history_data.drop(horse_history_data[horse_history_data["weight"]=="--"].index)
    return horse_history_data

def get_feature_mapping_table(feature, values, encoded_values):
    mapping_table = pd.DataFrame({'Feature': feature, 'Value': values, 'Encoded Values': encoded_values})
    mapping_table = mapping_table.drop_duplicates()
    return mapping_table

def map_feature_labelencoder(data, col_name):
    le = LabelEncoder()
    return le.fit_transform(data[col_name])

def concat_mapping_to_table(table, data, col_name, values):
  return pd.concat([table, get_feature_mapping_table(col_name, data[col_name], values)], ignore_index=True)

def preProcess(horse_history_data, horse_data):
    le = LabelEncoder()
    horse_race_data = horse_history_data.copy()
    feature_mapping_table = pd.DataFrame()

    # Horse Race Details
    # Race date
    horse_race_data["month"] = horse_race_data["date"].dt.month
    horse_race_data["quarter"] = pd.cut(horse_race_data["month"], bins=[0,3,6,9,12], labels=[1,2,3,4])

    # location_run
    horse_race_data["course_location"] = horse_race_data["location_run"].apply(lambda x: x.split('/')[0].strip())
    horse_race_data["track"] = horse_race_data["location_run"].apply(lambda x: x.split('/')[1].strip())

    def extract_course(loc_run):
        parts = loc_run.split('/')
        if len(parts) >= 3:
            course = parts[2].replace("\"", "").strip()
        elif parts[1].strip() == 'AWT':
            course = "AWT"
        else:
            course = None
        return course
    horse_race_data["course"] = horse_race_data["location_run"].apply(extract_course)
    # horse_race_data["course"] = horse_race_data["location_run"].apply(lambda x:  x.split('/')[2].replace("\"", "").strip() if len(x.split('/')) >= 3 else None )
    # Remove foreign races
    horse_race_data = horse_race_data[(horse_race_data["course_location"] == "ST") |(horse_race_data["course_location"] == "HV")]
    # course_location mapping
    course_location_values = map_feature_labelencoder(horse_race_data, "course_location")
    feature_mapping_table = concat_mapping_to_table(feature_mapping_table, horse_race_data, "course_location", course_location_values)
    horse_race_data["course_location"] = course_location_values
    # track
    # horse_race_data["track"] = horse_race_data["track"].astype('category')
    track_values = map_feature_labelencoder(horse_race_data, "track")
    feature_mapping_table = concat_mapping_to_table(feature_mapping_table, horse_race_data, "track", track_values)
    horse_race_data["track"] = track_values
    # course mapping
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
    horse_race_data["course"] = horse_race_data["course"].map(course_mapping)

    # speed_m_s distance
    horse_race_data["finish_time_ms"] = horse_race_data["finish_time"].apply(lambda x: None if x == "--" else (int(x.split(".")[0]) * 60 + int(x.split(".")[1])) * 1000 + int(x.split(".")[2]) * 10)
    horse_race_data["speed_m_s"] = horse_race_data["distance"] / horse_race_data["finish_time_ms"] * 1000
    horse_race_data["speed_class"] = pd.cut(horse_race_data["speed_m_s"], bins=[0,15,16,17,18,30])
    horse_race_data["distance_km"] = horse_race_data["distance"].astype("int") / 1000

    # G mapping
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
    horse_race_data["G"] = horse_race_data["G"].map(g_mapping)

    # race_class
    race_class_values = horse_race_data["race_class"].map(horse_race_data.groupby('race_class')["speed_m_s"].median().rank().to_dict())
    feature_mapping_table = concat_mapping_to_table(feature_mapping_table, horse_race_data, "race_class", race_class_values)
    horse_race_data["race_class"] = race_class_values
    # dr
    dr_values = horse_race_data["dr"].map(horse_race_data.groupby('dr')["speed_m_s"].median().rank().to_dict())
    feature_mapping_table = concat_mapping_to_table(feature_mapping_table, horse_race_data, "dr", race_class_values)
    horse_race_data["dr"] = dr_values
    # trainer
    trainer_values = horse_race_data["trainer"].map(horse_race_data.groupby('trainer')["speed_m_s"].median().rank().to_dict())
    feature_mapping_table = concat_mapping_to_table(feature_mapping_table, horse_race_data, "trainer", trainer_values)
    horse_race_data["trainer"] = trainer_values
    # jockey
    jockey_values = horse_race_data["jockey"].map(horse_race_data.groupby('jockey')["speed_m_s"].median().rank().to_dict())
    feature_mapping_table = concat_mapping_to_table(feature_mapping_table, horse_race_data, "jockey", jockey_values)
    horse_race_data["jockey"] = jockey_values
    # Horse Weight (Declaration)
    horse_race_data["weight"] = horse_race_data["weight"].astype("int")
    horse_race_data["weight_class"] = pd.cut(horse_race_data["weight"], bins=[900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350], labels=[0,1,2,3,4,5,6,7,8])
    # Gear
    horse_race_data["gear"] = horse_race_data["gear"].map(lambda x: 0 if x == "--" else 1)

    # Horse Details
    # Country of Origin
    horse_race_data["horse_country"] = horse_race_data["horse_id"].map(horse_data["country"].to_dict())
    country_values = horse_race_data["horse_country"].map(horse_race_data.groupby('horse_country')["speed_m_s"].median().rank().to_dict())
    feature_mapping_table = concat_mapping_to_table(feature_mapping_table, horse_race_data, "horse_country", country_values)
    horse_race_data["horse_country"] = country_values
    # Age
    horse_race_data["horse_age"] = horse_race_data["horse_id"].map(horse_data["age"].to_dict())
    horse_race_data["horse_age"] = horse_race_data["date"].dt.year - 2024 + horse_race_data["horse_age"]
    # Owner
    horse_race_data["horse_owner"] = horse_race_data["horse_id"].map(horse_data["owner"].to_dict())
    owner_values = horse_race_data["horse_owner"].map(horse_race_data.groupby('horse_owner')["speed_m_s"].median().rank().to_dict())
    feature_mapping_table = concat_mapping_to_table(feature_mapping_table, horse_race_data, "horse_owner", owner_values)
    horse_race_data["horse_owner"] = owner_values
    # Import Type
    horse_race_data["horse_import_type"] = horse_race_data["horse_id"].map(horse_data["import_type"].to_dict())
    import_type_values = horse_race_data["horse_import_type"].map(horse_race_data.groupby('horse_import_type')["speed_m_s"].median().rank().to_dict())
    feature_mapping_table = concat_mapping_to_table(feature_mapping_table, horse_race_data, "horse_import_type", import_type_values)
    horse_race_data["horse_import_type"] = import_type_values
    # Color
    horse_race_data["horse_color"] = horse_race_data["horse_id"].map(horse_data["color"].to_dict())
    color_values = horse_race_data["horse_color"].map(horse_race_data.groupby('horse_color')["speed_m_s"].median().rank().to_dict())
    feature_mapping_table = concat_mapping_to_table(feature_mapping_table, horse_race_data, "horse_color", color_values)
    horse_race_data["horse_color"] = color_values

    # Sex
    horse_race_data["horse_sex"] = horse_race_data["horse_id"].map(horse_data["sex"].to_dict())
    sex_values = horse_race_data["horse_sex"].map(horse_race_data.groupby('horse_sex')["speed_m_s"].median().rank().to_dict())
    feature_mapping_table = concat_mapping_to_table(feature_mapping_table, horse_race_data, "horse_sex", sex_values)
    horse_race_data["horse_sex"] = sex_values
    # Sire
    horse_race_data["horse_sire"] = horse_race_data["horse_id"].map(horse_data["sire"].to_dict())
    sire_values = horse_race_data["horse_sire"].map(horse_race_data.groupby('horse_sire')["speed_m_s"].median().rank().to_dict())
    feature_mapping_table = concat_mapping_to_table(feature_mapping_table, horse_race_data, "horse_sire", sire_values)
    horse_race_data["horse_sire"] = sire_values
    # Dam
    horse_race_data["horse_dam"] = horse_race_data["horse_id"].map(horse_data["dam"].to_dict())
    dam_values = horse_race_data["horse_dam"].map(horse_race_data.groupby('horse_dam')["speed_m_s"].median().rank().to_dict())
    feature_mapping_table = concat_mapping_to_table(feature_mapping_table, horse_race_data, "horse_dam", dam_values)
    horse_race_data["horse_dam"] = dam_values
    # Dam Sire
    horse_race_data["horse_dam_sire"] = horse_race_data["horse_id"].map(horse_data["dam_sire"].to_dict())
    dam_sire_values = horse_race_data["horse_dam_sire"].map(horse_race_data.groupby('horse_dam_sire')["speed_m_s"].median().rank().to_dict())
    feature_mapping_table = concat_mapping_to_table(feature_mapping_table, horse_race_data, "horse_dam_sire", dam_sire_values)
    horse_race_data["horse_dam_sire"] = dam_sire_values

    # horse_race_data["track"] = le.fit_transform(horse_race_data["track"])
    # horse_race_data["course"] = horse_race_data["course"].map(horse_race_data.groupby('course')["speed_m_s"].median().rank().to_dict())

    # Drop features
    col_to_drop = ["date", "result", "location_run", "running_position", "finish_time"]
    horse_race_data = horse_race_data.drop(col_to_drop, axis=1)

    from scipy import stats

    # Calculate the Z-scores
    z_scores = np.abs(stats.zscore(horse_race_data["speed_m_s"]))
    outlier_mask = (z_scores > 3)
    horse_race_data = horse_race_data[~outlier_mask]
    return horse_race_data
