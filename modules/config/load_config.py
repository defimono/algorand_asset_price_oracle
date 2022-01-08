import json
import os

from modules.get_secret import get_secret


def load_config():
    aws_secret_name = os.environ['AWS_SECRET_NAME']
    aws_region = os.environ['AWS_REGION']

    secret_string = get_secret(aws_secret_name, aws_region)
    secret = json.loads(secret_string)

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
