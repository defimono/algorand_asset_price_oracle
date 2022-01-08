import json

from algosdk import account
from algosdk.future import transaction
from algosdk.future.transaction import wait_for_confirmation
from dotenv import load_dotenv

from modules.config.algod_client import initialize_algod_client
from modules.config.load_config import load_config
from modules.config.logger import logger
import requests

load_dotenv()


def get_updated_price():
    """
    Query public API for ALGO price information. Will query, parse, and return a float representation pegged to USD.
    :return: float representation of price
    """
    url = "https://api.coinbase.com/v2/prices/ALGO-USD/buy"

    raw_response = requests.get(url)

    price_data = raw_response.json()

    real_price = price_data.get('data').get('amount')

    parsed_price = float(real_price)

    logger.info("Got real price from coinbase set to: ${}".format(parsed_price))

    return parsed_price


def call_noop(algod_client, app_id, private_key, app_args):
    """
    Call the update function in the deployed application with the new application TEAL
    :param algod_client: preconfigured algod client for desired chain (main, test, or beta)
    :param app_args: app args to pass to teal function inside smart contract on chain
    :param app_id: application id to update
    :param private_key: private key to authenticate and approve ourselves following the teal logic
    :return: raw transaction response of the update function
    """
    sender = account.address_from_private_key(private_key)

    logger.debug("Sender wallet: {}".format(sender))

    # get node suggested parameters
    params = algod_client.suggested_params()

    logger.debug("params: {}".format(params))

    # create unsigned transaction
    txn = transaction.ApplicationNoOpTxn(sender, params, app_id, app_args)

    logger.debug("txn: {}".format(txn))

    # sign transaction
    signed_txn = txn.sign(private_key)

    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    algod_client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(algod_client, tx_id, 10)


def lambda_handler(event, context):
    try:
        app_config = load_config()

        algod_address = app_config.get("algod_address")

        algod_token = app_config.get("algod_token")

        algod_client = initialize_algod_client(algod_address, algod_token)

        oracle_app_id = app_config.get("oracle_app_id")

        admin_private_key = app_config.get("admin_private_key")

        # get new price
        real_price = get_updated_price()

        # Real price is to fixed point to get round the issues with float in
        # teal
        price_fixed_point = int(real_price * 10 ** 2)

        logger.info(
            "Setting 2 digit fixed point price to: {} ".format(price_fixed_point))

        # call noop with new price and sign with service account
        # 2 meas we want two digits in the fixed point precision of the price
        app_args = ["update_price", price_fixed_point, 2]

        # Call the update operation in the published stateful algorand smart
        # contract
        call_noop(algod_client, oracle_app_id, admin_private_key, app_args)

        logger.info("Application update called successfully")

        # If called via API Gateway, return a formatted response body as
        # needed.
        response = {
            "statusCode": 200,
            "body": json.dumps(price_fixed_point)
        }

        return response

    except Exception as error:
        logger.error("{}".format(error))

        response = {
            "statusCode": 500,
            "body": json.dumps(error)
        }

        return response


if __name__ == "__main__":
    """
    Local development helper.
    """
    logger.info(lambda_handler(None, None))
