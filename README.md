# Predicting Horse Racing Performance with Machine Learning
The goal of this project is to predict the finish time by providing the race and horse information

# Lib used and version
The program is written and run in python3 and the following library is used:
1. Pandas
2. Numpy
3. sklearn
4. seaborn
5. dash
6. selienium 

# Folder structure
There are two main folder in this project:
1. **app** - Contains the application and model training module
2. **data_gathering** - Contains the code that grab the horse and horse race data from the internet

# How to use:
## To grab the data:
```
cd data_gathering
python3 horse_graber.py
```

## To run the program with finding optimal model
```
cd app
make optimal
```

## To run the application with the optimal model found previously:
```
cd app
make run
```