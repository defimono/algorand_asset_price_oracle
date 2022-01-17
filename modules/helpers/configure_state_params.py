from algosdk.future import transaction


def configure_state_params(
        local_ints=0,
        local_bytes=0,
        global_ints=0,
        global_bytes=0):
    """
    General state configuration program, configure as the program needs.
    """
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)

    return global_schema, local_schema
