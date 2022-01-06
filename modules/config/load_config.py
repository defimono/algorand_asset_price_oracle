import os


def load_config():
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
