from algosdk.future import transaction
from algosdk.future.transaction import wait_for_confirmation

from config.algod_client import initialize_algod_client
from config.load_app_config import app_config
from config.logger import logger
from modules.helpers.compile import compile_program
from modules.helpers.configure_state_params import configure_state_params
from smart_contracts.clear_state_program import clear_state_program
from smart_contracts.oracle import oracle


def deploy(action="deploy", app_index=0):
    try:
        algod_client = initialize_algod_client()
        admin_address = app_config.get("admin_address")
        admin_private_key = app_config.get("admin_private_key")

        application_approval_teal = oracle()

        application_clear_teal = clear_state_program()

        logger.info("Deploying stateful smart contract...")

        # compile program to binary
        approval_program_compiled = compile_program(application_approval_teal)

        # compile program to binary
        clear_state_program_compiled = compile_program(application_clear_teal)

        global_schema, local_schema = configure_state_params(
            local_ints=0,
            local_bytes=0,
            global_ints=3,
            global_bytes=3
        )

        # declare on_complete as NoOp
        on_complete = transaction.OnComplete.NoOpOC.real

        # get node suggested parameters
        params = algod_client.suggested_params()

        txn = ""

        if action == "deploy" and app_index == 0:
            txn = transaction.ApplicationCreateTxn(
                admin_address,
                params,
                on_complete,
                approval_program_compiled,
                clear_state_program_compiled,
                global_schema,
                local_schema
            )
        elif action == "update" and app_index != 0:
            txn = transaction.ApplicationUpdateTxn(
                admin_address,
                params,
                app_index,
                approval_program_compiled,
                clear_state_program_compiled
            )

        # sign transaction
        signed_txn = txn.sign(admin_private_key)

        tx_id = signed_txn.transaction.get_txid()

        # send transaction
        algod_client.send_transactions([signed_txn])

        # await confirmation
        wait_for_confirmation(algod_client, tx_id, 5)

        # display results
        transaction_response = algod_client.pending_transaction_info(tx_id)

        app_id = transaction_response['application-index']

        logger.info('Oracle successfully deployed with app_id: {}'.format(app_id))

        return app_id

    except Exception as error:
        logger.error('{}'.format(error))
