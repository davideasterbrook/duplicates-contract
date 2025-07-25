from moccasin.boa_tools import VyperContract
from moccasin.config import get_active_network

from src.mocks import mock_erc721


def deploy_mock_erc721() -> VyperContract:
    mock_erc721_contract = mock_erc721.deploy()

    active_network = get_active_network()
    if active_network.has_explorer():
        result = active_network.moccasin_verify(mock_erc721_contract)
        result.wait_for_verification()

    return mock_erc721_contract


def moccasin_main():
    return deploy_mock_erc721()
