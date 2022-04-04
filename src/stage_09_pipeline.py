import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
import random
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from src.stage_07_ct_and_model_selection import ct
from src.stage_06_train_test_split import x , y , x_train , y_train
import joblib
from sklearn.model_selection import cross_val_score
from imblearn.combine import SMOTETomek

STAGE = "PIPELINE" ## <<< change stage name 

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
        # Creating pipeline with new parameters after optained from gridsearchcv
        pipeline = Pipeline([
                            ('columnTransformer', ct),
                            ('resample', SMOTETomek()),
                            ('model', RandomForestClassifier(bootstrap = True,
                                                            max_depth = 50,
                                                            max_features = 'sqrt',
                                                            min_samples_leaf = 4,
                                                            min_samples_split = 10,
                                                            n_estimators = 6))
                            ])
        logging.info(f'Final Pipeline created {pipeline}')
    except Exception as e:
        logging.exception(f'Error in creating final pipeline : {e}')


    try:
        accuracy_scores = cross_val_score(pipeline, x, y,
                                        scoring=params['final_pipeline']['scoring_accuracy'],
                                        cv=params['final_pipeline']['cv'],
                                        n_jobs=params['final_pipeline']['n_jobs'])
        logging.info(f'accuracy_scores are {accuracy_scores}')
        
        f1_scores = cross_val_score(pipeline, x, y,
                                    scoring=params['final_pipeline']['scoring_f1'],
                                    cv=params['final_pipeline']['cv'],
                                    n_jobs=params['final_pipeline']['n_jobs'])
        logging.info(f'f1_scores are {f1_scores}')
    except Exception as e:
        logging.exception(f'Error in scores : {e}')

    try:
        pipeline.fit(x_train, y_train)
        logging.info('Pipeline Trained succesfully')
    except:
        logging.exception(f'Error while training : {e}')

    if os.path.exists(pipeline_dir)==False:
        pipeline_dir = create_directories(config['data']['pipeline_dir'])
        pipeline_joblib = os.path.join(pipeline_dir,
                                    config['data']['pipeline_file'])
        joblib.dump(pipeline, pipeline_joblib)  
        logging.info(f"Trained pipeline is saved at : {pipeline_dir}")
        return pipeline
    else:
        logging.info(f'Trained Pipeline already present in {pipeline_dir}')



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