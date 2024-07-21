# Predicting Horse Racing Performance with Machine Learning
In this project, a machine learning app will be developed to predict the finish time of a horse race based on the provided race and horse information. The data obtained from the Hong Kong Jockey Club will be utilized for this purpose.

## Libraries Used
The program is written and run in python3 and the following library is used:
1. Pandas
2. Numpy
3. sklearn
4. seaborn
5. dash
6. selienium 

## Project Setup Instruction
Open a terminal on the machine
```
# Clone repo
git clone https://github.com/nikechung/horse.git

# Navigate to repo
cd horse/app

# Install requirements
make install

# Run program
make run
```

## Folder Structure
There are two main folders in this project:
1. **app** - Contains the application and model training module
2. **data_gathering** - Contains the code that grab the horse and horse race data from the internet

## Part I: Data Collection 
Selenium will be used for web scraping to extract the list of horses.

For simplicity, the horses located in Hong Kong will be grabbed from the URL:https://racing.hkjc.com/racing/information/English/Horse/ListByLocation.aspx?Location=HK

For each horse, the URL for their horse detail will also be extracted. Whtih the horse detail URL, detailed information about the horse can be obtained.

### To grab the data:
```
cd data_gathering
python3 horse_graber.py
```
## Part II: Data Preprocessing 

### Missing or incomplete values
* Remove cancalled races and overseas races (finish_time or weight equal to "--")
* Remove missing values from dataset by using dropna()

### Tranform data
* Calculate the age of the horse when it participates in the race based on its current age and the year of the race.
* Calculate the speed based on the distance of the race and the horse's finish time.
* Label encoding: Mapping categories to integer values (e.g. "track")
* One-hot encoding: Creating binary columns for each unique category (e.g. "gear")
* Target encoding: Encoding the variable based on the target variable "speed"

### Feature engineering
* Create new feature "number of turns" for each race to provide more relevant and informative inputs.

### Remove outliers
By using Z-scores, remove data where the z-score of the speed.

## Part III: Feature Selection
Remove features that are not available to the user before the race(e.g. "horse_id", "result", "G").

Using heatmap to identify relations between 
Remove closely related vaiables using heatmap: "horse_owner", "horse_sire", "horse_dam_sire", "month".
```
cd app
make showHeatmap
```

Find out optimal r-squared score from all combinations using Linear Regression.

## Part IV: Model Selection
Find the algorithm with the highest score by calculating the r-squared scores of below algorithms:
* Linear Regression
* Random Forest Regression
* KNN Regression
* Decision Tree Regression
* Support Vector Regression
* Gradient Boosting Regression

## Part V: Model Evaluation
Using Coarse-tuning and Fine-tuning to turn the hyperparamters.

In Part IV, the gradient boosting regression algorithm was selected as the best algorithm. Then, the algorithm will be fine-tuned based on the following hyperparameters:
* loss
* learning_rate
* n_estimators
* max_depth
* subsample

### To run the program with finding optimal model
```
cd app
make optimal
```

## Part VI: Dash APP
A web-based data visualization applications, allow users to interact with it and get the predicted finish time by using the model in this project.

### To run the application with the optimal model found previously:
```
cd app
make run
```