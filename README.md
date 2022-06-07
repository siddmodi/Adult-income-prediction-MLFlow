# Adult income prediction MLFlow

============ MLflow project ==============

## STEPS -

### STEP 01- Create a repository by using template repository

### STEP 02- Clone the new repository

### STEP 03- Create a conda environment after opening the repository in VSCODE

```bash
conda create --prefix ./env python=3.7 -y
```

```bash
conda activate ./env
```
OR
```bash
source activate ./env
```

### STEP 04- install the requirements
```bash
pip install -r requirements.txt
```

### STEP 05 - Create conda.yaml file -
```bash
conda env export > conda.yaml
```

### STEP 06- commit and push the changes to the remote repository

=============== **Explaination** ===================

Flask app to predict whether the individual income is more or less than $50k based on his/her mentioned details(Age,Education,Hours Per week,Marital Status,
Workclass,Occupation,Sex,Country,Capital Gain or Loss Amount)

we create a full fledged MLops pipeline to smoothen the process and defined all individual layer. We have data in cassandra database we take the data and store in
pandas dataframe for further process

We create 8 seprate stages for each step

1) Get data from cassandra database

2) Handling Missing values by sklearn SimpleImputer

3) Encode categorical columnsin integer form using ordinal encoding

4) Treatment of outlier using 99% quantile

5) Select features which are important for our prediction and drop useless column

6) Train 80% of data and rest 20% for testing and correct the naming convention

7) create column transformer of std.scaling and min-max scaling and select the best model using SMOTETomek cross validation and select with high accuracy

8) After choosing model tune the best parameters using randomized search cv

9) Create final pipeline with best model with best params and save it as joblib file for future prediction

We also consider the situation if we stuck anywhere by creating log files for each and every steps for each stage
