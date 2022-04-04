import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
import random
from src.stage_01_get_data import df

STAGE = "TRAIN-TEST-SPLIT" ## <<< change stage name 

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
        x = df.drop(columns=['salary'] ,axis=1)
        y = df['salary']

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0,stratify=y)
        
    except Exception as e:
        logging.exception(f'Error Occured while train-test split : {e}')

    try:
        x.rename(columns = {
            'workclass_ Local-gov' : 'local_gov' ,
            'hours-per-week' : 'hours_per_week',
            'marital-status_single' : 'marital_status_single',
            'workclass_ Private' : 'private' ,
            'workclass_ Self-emp-inc' : 'self_emp_inc' ,    
            'workclass_ Self-emp-not-inc' : 'self_emp_not_inc' ,
            'workclass_ State-gov' : 'state_gov' ,
            'workclass_ Without-pay' : 'without_pay' ,
            'occupation_ Craft-repair' : 'craft_repair' ,
            'occupation_ Exec-managerial' : 'exec_managerial' ,
            'occupation_ Farming-fishing' : 'farming_fishing' ,
            'occupation_ Handlers-cleaners' : 'handlers_cleaners' ,
            'occupation_ Machine-op-inspct' : 'machine_op_inspct' ,
            'occupation_ Other-service' : 'other' ,
            'occupation_ Prof-specialty' : 'prof_specialty' ,
            'occupation_ Protective-serv' : 'protective_serv' ,
            'occupation_ Sales' : 'sales' ,
            'occupation_ Tech-support' : 'tech_support' ,
            'occupation_ Transport-moving' : 'transport_moving' ,
            'occupation_others' : 'others' ,
            'sex_ Male' : 'male' ,
            'country_ El-Salvador' : 'el_salvador' ,
            'country_ Germany' : 'germany' ,
            'country_ India' : 'india' ,
            'country_ Mexico' : 'mexico' ,
            'country_ Philippines' : 'philippines' , 
            'country_ Puerto-Rico' : 'puerto_rico' ,
            'country_ United-States' : 'united_states' 
            },inplace=True)
    except Exception as e:
        logging.exception(f'Error Occured while renaming columns : {e}')


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