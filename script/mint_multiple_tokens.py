from moccasin.boa_tools import VyperContract
from moccasin.config import get_active_network
import boa


active_network = get_active_network()


def mint(cc_contract: VyperContract, contract_address: VyperContract, index: int):
    print(f"Minting token using contract:{contract_address.address} and index: {index}")
    cc_contract.mint(contract_address.address, index)


def get_contract(contract_name: str) -> VyperContract:
    return active_network.manifest_named(contract_name)


def moccasin_main() -> VyperContract:
    # CHECK THE ACTUAL ACCOUNT USED
    account = boa.env.eoa
    print(f"🔍 Script account: {account}")
    print(f"🔍 Account balance: {boa.env.get_balance(account)}")

    duplicates_contract: VyperContract = get_contract("duplicates")

    # My address: 0x40A34D87eb243C0811e0FF0c42350152fe2d1198
    # Anvil: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
    # Anvil 2: 0x70997970C51812dc3A010C7d01b50e0d17dc79C8

    with boa.env.prank("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"):
        for i in range(20):
            mint(duplicates_contract, get_contract("bayc"), i)
            mint(duplicates_contract, get_contract("doodle"), i)
            mint(duplicates_contract, get_contract("ppg"), i)
