from pyteal import *


def oracle():
    """
    Requirements:
        Simply a small stateful smart contract written to on a cron (one every 5 minutes to start).
        Updates the price global state var with the current price x 10 ^ 2 fixed point
        example: 1.53 x 10 ^ 2 = 153 to convert into uint.
    """

    # security guards
    # ensure there is no close out address, this would be bad if on close out
    # a malicious actor routed funds.
    no_close_out_address = Txn.close_remainder_to() == Global.zero_address()

    # Make sure no rekey of smart contract
    no_rekey_address = Txn.rekey_to() == Global.zero_address()

    # Make sure no one forces a fee of like 100000 algos to blow account
    acceptable_fee = Txn.fee() <= Int(3000)

    # Only accept singular transactions
    is_single_tx = Global.group_size() == Int(1)

    is_admin = Txn.sender() == App.globalGet(Bytes("admin"))

    correct_group_index = Txn.group_index() == Int(0)

    application_call = Txn.type_enum() == TxnType.ApplicationCall

    current_price = Txn.application_args[1]

    fixed_point_accuracy = Txn.application_args[2]

    """
    Administrative function block, allowing the creator of the contract to be the admin
    """
    # Functions
    on_init = Seq([
        # This will set the creation of the contract as the admin in Global
        # State, they will have full control
        App.globalPut(Bytes("admin"), Txn.sender()),

        # Return 1, 0 is fail and 1 is success (reverse of unix)
        Return(Int(1))
    ])

    update_price = Seq([
        App.globalPut(Bytes("algo_usd_price"), Btoi(current_price)),
        App.globalPut(Bytes("fixed_point_accuracy"), Btoi(fixed_point_accuracy)),

        Return(Int(1))
    ])

    handle_noop = Cond(
        [And(
            is_admin,
            is_single_tx,
            no_rekey_address,
            no_close_out_address,
            acceptable_fee,
            application_call,
            Txn.application_args[0] == Bytes("update_price")
        ), update_price]
    )

    handle_optin = Seq([
        Assert(is_single_tx),

        Return(Int(1))
    ])

    handle_closeout = Seq([
        Return(Int(0))
    ])

    handle_update = Seq([
        Assert(is_admin),
        Assert(is_single_tx),
        Assert(no_rekey_address),
        Assert(no_close_out_address),
        Assert(acceptable_fee),
        Assert(correct_group_index),

        Return(Int(1))
    ])

    handle_delete = Seq([
        Assert(is_admin),
        Assert(is_single_tx),
        Assert(no_rekey_address),
        Assert(no_close_out_address),
        Assert(acceptable_fee),
        Assert(correct_group_index),

        Return(Int(1))
    ])

    program = Cond(
        [Txn.application_id() == Int(0), on_init],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop],
        [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_update],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_delete]
    )

    return compileTeal(program, Mode.Application, version=5)
