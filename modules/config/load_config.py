import json
import os

from modules.config.logger import logger
from modules.get_secret import get_secret

import os
os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "/home/dallin/.aws/credentials"
os.environ["AWS_DEFAULT_PROFILE"] = "ss-dev"

def load_config():
    aws_secret_name = os.environ['SECRET_NAME']
    aws_region = os.environ['AWS_REGION']

    secret_string = get_secret(aws_secret_name, aws_region)
    secret = json.loads(secret_string)

    logger.info(secret)

    config_dict = {
        "oracle_app_id": os.environ['ORACLE_APP_ID'],
        "admin_wallet_address": secret.get("ADMIN_WALLET_ADDRESS"),
        "admin_private_key": secret.get("ADMIN_PRIVATE_KEY"),
        "admin_mnemonic": secret.get("ADMIN_WALLET_ADDRESS"),
        "algod_address": os.environ['ALGOD_ADDRESS'],
        "algod_token": os.environ['ALGOD_KEY'],
        "algod_chain": os.environ['ALGOD_CHAIN'],
    }

    return config_dict
