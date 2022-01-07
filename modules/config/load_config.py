import os

from modules.config.logger import logger
from modules.get_secret import get_secret


def load_config():
    aws_secret_name = os.environ['SECRET_NAME']
    aws_region = os.environ['AWS_REGION']

    secret = get_secret(aws_secret_name, aws_region)

    logger.info(secret)

    config_dict = {
        "oracle_app_id": os.environ['ORACLE_APP_ID'],
        "admin_wallet_address": os.environ['ADMIN_WALLET_ADDRESS'],
        "admin_private_key": os.environ['ADMIN_PRIVATE_KEY'],
        "admin_mnemonic": os.environ['ADMIN_MNEMONIC'],
        "algod_address": os.environ['ALGOD_ADDRESS'],
        "algod_token": os.environ['ALGOD_KEY'],
        "algod_chain": os.environ['ALGOD_CHAIN'],
    }

    return config_dict
