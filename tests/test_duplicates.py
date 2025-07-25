# Test withdraw
# Test ownership blocks
# Possible to test maximum mints (stack overflow?)
# Test update of max price
# Test owner transfer?


import pytest
import boa
from src import duplicates
from src.mocks import mock_erc721


@pytest.fixture
def deploy_duplicates():
    duplicates_contract = duplicates.deploy()
    return duplicates_contract


@pytest.fixture
def deploy_mock_nft():
    mock_nft = mock_erc721.deploy()
    return mock_nft


def test_name(deploy_duplicates):
    assert deploy_duplicates.name() == "Duplicates NFT"


def test_symbol(deploy_duplicates):
    assert deploy_duplicates.symbol() == "DUPE"


def test_mint_emits_event(deploy_duplicates, deploy_mock_nft):
    # First mint a token on the mock NFT contract to reference
    mock_nft = deploy_mock_nft
    mock_nft.mint()

    # Mint a duplicate with payment
    duplicates_contract = deploy_duplicates
    minting_cost = duplicates_contract.minting_cost()

    # Test event emission using boa's event capture
    with boa.env.anchor():
        duplicates_contract.mint(mock_nft.address, 0, value=minting_cost)

        # Get events from the duplicates contract
        events = duplicates_contract.get_logs()

        # Verify Minted event
        # Second event is the Minted event
        event = events[1]

        assert event.token_id == 0
        assert event.minter == boa.env.eoa
        assert event.original_contract == mock_nft.address
        assert event.original_token_id == 0
        assert event.price_paid == minting_cost
