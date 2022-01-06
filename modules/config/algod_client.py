from algosdk.v2client import algod

from modules.config.load_config import load_config
from modules.config.logger import logger


def initialize_algod_client(address, token):
    logger.info("Initializing Algod Client")

    headers = {
        "X-API-Key": token,
    }

    algod_client = algod.AlgodClient(token, address, headers)

    return algod_client
