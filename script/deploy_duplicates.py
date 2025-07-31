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

    if active_network.has_explorer() and not active_network.is_local_or_forked_network():
        print("Verifying contract on explorer...")
        result = active_network.moccasin_verify(duplicates_contract)
        result.wait_for_verification()

    print("#" * 80)
    print(f"Duplicates Contract deployed at: {duplicates_contract.address}")
    print("#" * 80)

    return duplicates_contract
