import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
import random
from src.stage_01_get_data import df
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from src.stage_07_ct_and_model_selection import ct
from src.stage_06_train_test_split import x , y

STAGE = "HYPERPARAMETER TUNING" ## <<< change stage name 

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
        # We choose Random Forest
        pipeline = Pipeline([
                        ('columnTransformer', ct),
                        ('model', RandomForestClassifier())
                            ])
    except Exception as e:
        logging.exception(f'Error in creating initial pipeline : {e}')


    # for model_rf    
    params = {  'model__n_estimators'     : params['hyperparameter_tuning_params']['model__n_estimators'] ,
                'model__max_features'     : params['hyperparameter_tuning_params']['model__max_features'] ,
                'model__max_depth'        : params['hyperparameter_tuning_params']['model__max_depth'] ,
                'model__min_samples_split': params['hyperparameter_tuning_params']['model__min_samples_split'] ,
                'model__min_samples_leaf' : params['hyperparameter_tuning_params']['model__min_samples_leaf'] ,
                'model__bootstrap'        : params['hyperparameter_tuning_params']['model__bootstrap'] 
            }
    logging.info('params defined')

    try:
        random_search = RandomizedSearchCV(pipeline,
                                            param_distributions=params,
                                            scoring=params['hyperparameter_tuning']['scoring'],
                                            n_jobs=params['hyperparameter_tuning']['n_jobs'],
                                            cv=params['hyperparameter_tuning']['cv'])
        random_search.fit(x, y)
        logging.info(random_search.best_params_)
        logging.info(random_search.best_score_)
    except Exception as e:
        logging.exception(f'Error in tuning the parameters : {e}')



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