import os


def load_config():
    config_dict = {
        "oracle_address": os.environ['ORACLE_ADDRESS'],
        "oracle_private_key": os.environ['ORACLE_PRIVATE_KEY'],
        "algo_chain": os.environ['ALGO_CHAIN'],
    }

    return config_dict
