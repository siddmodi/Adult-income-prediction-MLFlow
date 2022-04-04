import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
import random
from sklearn.preprocessing import OrdinalEncoder
import pandas as pd
from src.stage_01_get_data import df
from src.utils.feature_transformation import naming_as_others_for_less_frequent_valuea

STAGE = "ENCODING" ## <<< change stage name 

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
        edu = [' Preschool', ' 1st-4th', ' 5th-6th', ' 7th-8th', ' 9th', ' 10th',
        ' 11th', ' 12th', ' HS-grad', ' Prof-school', ' Some-college',
        ' Assoc-acdm', ' Assoc-voc',' Bachelors', ' Masters', ' Doctorate']
        ordi = OrdinalEncoder(categories=[edu])
        df['education'] = ordi.fit_transform(df[['education']])
        logging.info('Education column encoded') 

        # where salary is <=50K we subsitute 0 and where salary is >50K we subsitute 1
        df.replace(to_replace=[' <=50K', ' >50K'], value = [0, 1], inplace = True)
        logging.info('salary column encoded')

        # Convert values of marital status to only single and married
        df.replace(df['marital-status'].unique(),['single','married','single','single','single','married','single'],inplace=True)
        df = pd.get_dummies(df,columns=['marital-status'],drop_first=True)
        logging.info('marital-status column encoded')

        df = pd.get_dummies(df,columns=['workclass'],drop_first=True)
        logging.info('workclass column encoded')

        # naming less frequent occupation as others (having value counts less than 2% of total values)
        naming_as_others_for_less_frequent_value(df,'occupation',threshold=2)
        df = pd.get_dummies(df,columns=['occupation'],drop_first=True)
        logging.info('occupation column encoded')

        df = pd.get_dummies(df,columns=['relationship'],drop_first=True)
        logging.info('relationship column encoded')

        df = pd.get_dummies(df,columns=['sex'],drop_first=True)
        logging.info('sex column encoded')

        # naming less frequent countries as others (having value counts less than 0.3% of total values)
        naming_as_others_for_less_frequent_value(df,'country',threshold=0.3)
        df = pd.get_dummies(df,columns=['country'],drop_first=True)
        logging.info('country column encoded')

        # naming less frequent countries as others (having value counts less than 1% of total values)
        naming_as_others_for_less_frequent_value(df,'race',threshold=1)
        logging.info('race column encoded')

    except Exception as e:
        logging.exception(f'Error Occured : {e}')

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