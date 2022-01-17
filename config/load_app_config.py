import os

from algosdk import account


def load_app_config():
    config = dict()

    config["admin_private_key"] = os.environ["ADMIN_PRIVATE_KEY"]
    config["admin_address"] = account.address_from_private_key(config["admin_private_key"])

    # Managed globally static app id's from foundation
    config["oracle_app_id"] = int(os.environ['ORACLE_APP_ID'])

    # Config for algo sdk client blockchain connection
    config["algod_address"] = os.environ['ALGOD_ADDRESS']
    config["algod_token"] = os.environ['ALGOD_KEY']
    config["algod_chain"] = os.environ['ALGOD_CHAIN']

    return config


app_config = load_app_config()
