import pandas as pd

# Prepare horse data
def getHorseData(filename):
    horse_data = pd.read_csv(filename, index_col="horseID")
    horse_data["age"] = horse_data["country_age"].apply(lambda x: x.split('/')[1])
    horse_data["age"] = horse_data["age"].astype('int')

    horse_data["country"] = horse_data["country_age"].apply(lambda x: x.split('/')[0].strip())
    horse_data["country"] = horse_data["country"].astype('category')

    horse_data["color"] = horse_data["color_sex"].apply(lambda x: x.split('/')[0].strip())
    horse_data["color"] = horse_data["color"].astype('category')

    horse_data["sex"] = horse_data["color_sex"].apply(lambda x: x.split('/')[-1])
    horse_data["sex"] = horse_data["sex"].astype('category')

    horse_data = horse_data.drop(axis=1, columns=["color_sex", "country_age", "url"])

    horse_data["import_type"] = horse_data["import_type"].astype('category')
    return horse_data