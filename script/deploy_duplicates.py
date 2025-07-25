from src import duplicates
from moccasin.boa_tools import VyperContract
from moccasin.config import get_active_network

active_network = get_active_network()


def deploy() -> VyperContract:
    contract: VyperContract = duplicates.deploy()

    return contract


def moccasin_main() -> VyperContract:
    duplicates_contract: VyperContract = deploy()
    print(f"Duplicates Contract deployed: {duplicates_contract.address}")
    return duplicates_contract
