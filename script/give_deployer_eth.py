from moccasin.config import get_active_network, get_config
import boa


def give_account_eth(amount: int = 5, address: str = None):
    account = boa.env.eoa

    if address:
        account = address
    else:
        account = boa.env.eoa

    active_network = get_active_network()
    if active_network.is_local_or_forked_network():
        print(f"Giving {account} {amount} ETH")
        boa.env.set_balance(account, amount * 10**18)
    else:
        # Transfer ETH from current EOA to the target account address
        current_balance = boa.env.get_balance(boa.env.eoa)
        transfer_amount = amount * 10**18

        if current_balance < transfer_amount:
            raise ValueError(f"Insufficient balance. Need {amount} ETH but only have {current_balance / 10**18} ETH")

        print(f"Transferring {amount} ETH from {boa.env.eoa} to {account}")

        # Send actual ETH transaction using boa's raw_call
        receipt = boa.env.raw_call(
            to_address=account,
            data=b"",  # Empty data for ETH transfer
            value=transfer_amount,
            gas=21000  # Standard ETH transfer gas
        )

        print(f"Transfer complete. Receipt: {receipt}")
        print(f"New balance of {account}: {boa.env.get_balance(account) / 10**18} ETH")

    return


def moccasin_main():
    config = get_config()
    deployer_address = config.extra_data["deployer_address"] 
    give_account_eth(address=deployer_address)
