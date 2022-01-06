import json

from algosdk import account
from algosdk.future import transaction
from algosdk.future.transaction import wait_for_confirmation
from dotenv import load_dotenv

from modules.config.load_config import load_config
from modules.config.logger import logger
import requests

load_dotenv()


def get_updated_price():
    url = "https://api.coinbase.com/v2/prices/ALGO-USD/buy"

    raw_response = requests.get(url)

    price_data = raw_response.json()

    real_price = price_data.get('data').get('amount')

    return float(real_price)


def call_noop(algod_client, app_id, private_key):
    """
    Call the update function in the deployed application with the new application TEAL
    :param algod_client: preconfigured algo client
    :param app_id: application id to update
    :param private_key: private key to authenticate and approve ourselves follwing the teal logic
    :param approval_teal: approval teal to replace the deployed teal with
    :param clear_teal: clear teal to replace the deployed clear teal with
    :return: raw transaction response of the update function
    """
    sender = account.address_from_private_key(private_key)

    # get node suggested parameters
    params = algod_client.suggested_params()

    app_args = ["update_price", price]

    # create unsigned transaction
    txn = transaction.ApplicationNoOpTxn(sender, params, app_id, app_args)

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    algod_client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(algod_client, tx_id, 10)


def main(event, context):
    config = load_config()

    # get new price
    real_price = get_updated_price()

    # Real price is to fixed point to get round the issues with float in teal
    price_fixed_point = int(real_price * 10 ** 2)

    # call noop with new price and sign with service account
    

    response = {
        "statusCode": 200,
        "body": json.dumps(price_fixed_point)
    }

    return response


if __name__ == "__main__":
    logger.info(main(None, None))
