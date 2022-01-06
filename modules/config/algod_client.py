from algosdk.v2client import algod

from modules.config.logger import logger


def initialize_algod_client(address, token):
    logger.info("Initializing Algod Client")

    headers = {
        "X-API-Key": token,
    }

    return algod.AlgodClient(token, address, headers)
