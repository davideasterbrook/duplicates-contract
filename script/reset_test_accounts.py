from moccasin.config import get_active_network
import boa


active_network = get_active_network()


def test_account_setup(address: str = None):
    import requests

    if address:
        account = address
    else:
        account = boa.env.eoa
    code = boa.env.get_code(account)

    if code:
        if active_network.is_local_or_forked_network():
            boa.env.set_code(account, b"")  # Only works in simulation mode
            print(f"Reset {account} to clean EOA state")
        else:
            # Use anvil RPC to reset account code
            payload = {
                "jsonrpc": "2.0",
                "method": "anvil_setCode",
                "params": [str(account), "0x"],
                "id": 1
            }
            response = requests.post("http://127.0.0.1:8545", json=payload)
            print(f"Reset {account} to EOA via anvil RPC: {response.json()}")
    else:
        print(f"{account} already clean EOA")


def moccasin_main():
    test_account_setup("0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266")
    test_account_setup("0x70997970C51812dc3A010C7d01b50e0d17dc79C8")

