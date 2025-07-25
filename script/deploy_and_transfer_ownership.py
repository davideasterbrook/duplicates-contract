from moccasin.boa_tools import VyperContract
from moccasin.config import get_active_network, get_config
from script.deploy_duplicates import deploy as deploy_duplicates
import boa

active_network = get_active_network()


def get_owner_address() -> str:
    if hasattr(active_network, 'extra_data') and 'owner_address' in active_network.extra_data:
        owner_address = active_network.extra_data["owner_address"]
        print(f"Using network-specific owner address: {owner_address}")
    else:
        config = get_config()
        owner_address = config.extra_data["owner_address"]
        print(f"Using global owner address: {owner_address}")
    return owner_address


def moccasin_main() -> VyperContract:
    duplicates_contract: VyperContract = deploy_duplicates()

    print("#" * 80)
    print(f"Duplicates Contract deployed: {duplicates_contract.address}")
    print("#" * 80)

    owner_address = get_owner_address()
    print(f"Transferring ownership to {owner_address}")
    duplicates_contract.transfer_ownership(owner_address)

    print(f"Contract owner: {duplicates_contract.owner()}")

    return duplicates_contract
