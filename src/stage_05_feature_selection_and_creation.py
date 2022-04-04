import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
import random
from src.stage_01_get_data import df


STAGE = "FEATURE SELECTON AND CREATION" ## <<< change stage name 

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
        # Form coln name capital_gain_or_loss with capital-gain and capital-loss
        df['capital_gain_or_loss'] = df['capital-gain']-df['capital-loss']
        logging.info('New column "capital_gain_or_loss" form')
    except Exception as e:
        logging.exception(f'Error Occured in making new feature : {e}')

    try:
        df.drop(columns=['capital-gain','capital-loss','education-num','fnlwgt','race',
                    'relationship_ Not-in-family', 'relationship_ Other-relative',
                    'relationship_ Own-child', 'relationship_ Unmarried',
                    'relationship_ Wife'] ,axis=1, inplace=True)
        logging.info('Useless columns dropped')
    except Exception as e:
        logging.exception(f'Error Occured while droping useless column : {e}')


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