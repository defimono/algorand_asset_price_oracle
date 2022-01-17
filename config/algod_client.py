from algosdk.v2client import algod

from config.load_app_config import app_config


def initialize_algod_client():
    algod_address = app_config.get("algod_address")
    algod_token = app_config.get("algod_token")

    headers = {
        "X-API-Key": algod_token,
    }

    return algod.AlgodClient(algod_token, algod_address, headers)


algod_client = initialize_algod_client()
