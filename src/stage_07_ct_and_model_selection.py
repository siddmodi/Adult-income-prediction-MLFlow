import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
import random
from sklearn.preprocessing import StandardScaler , MinMaxScaler
from sklearn.model_selection import cross_val_score, KFold , StratifiedKFold
from sklearn.linear_model import LogisticRegression
from imblearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from imblearn.combine import SMOTETomek 
from imblearn.over_sampling import SMOTE
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from src.stage_01_get_data import df


STAGE = "COLUMN TRANSFORMER AND MODEL SELECTION" ## <<< change stage name 

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def main(config_path, params_path):
    ## read config files
    config = read_yaml(config_path)
    params = read_yaml(params_path)
    
    try:
        ct = ColumnTransformer([
                            ('std_scaling', StandardScaler(),['age','hours_per_week']),
                            ('min_max_scaling',MinMaxScaler(),['education','capital_gain_or_loss'])
                            ], remainder='passthrough')
        logging.info('Column transformer created')
    except Exception as e:
        logging.exception(f'Error Occured while creating column transformer : {e}')

    # comparing different classification models using sklearn pipeline
    models = [LogisticRegression(), SVC(), RandomForestClassifier(), XGBClassifier(),\
            DecisionTreeClassifier(), KNeighborsClassifier()]

    model_labels = ['LogisticReg', 'SVC', 'RandomForest', 'Xgboost','DecisionTree','KNN']
    accuracy_mean_scores = []
    try:
        for model in models:
            pipeline = Pipeline([
                                ('columnTransformer', ct),
                                ('resample', SMOTETomek()),
                                ('model', model)
                                 ])
            accuracy_mean = cross_val_score(pipeline, x, y,
                                            cv=params['initial_pipeline']['cv'], 
                                            scoring=params['initial_pipeline']['scoring']
                                            ,n_jobs=-1).mean()
            accuracy_mean_scores.append(accuracy_mean)
            logging.info(accuracy_mean_scores)

    except Exception as e:
        logging.exception(f'Error Occured while creating pipeline : {e}')

    

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main(config_path=parsed_args.config, params_path=parsed_args.params)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e