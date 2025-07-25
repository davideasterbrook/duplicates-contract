import pytest
from moccasin.config import get_active_network
from eth_account import Account
import boa
from eth_utils import to_wei

BALANCE = to_wei(10, "ether")
COLLATERAL_AMOUNT = to_wei(10, "ether")

# ------------------------------------------------------------------
#                          SESSION SCOPED
# ------------------------------------------------------------------

@pytest.fixture(scope="session")
def active_network():
    return get_active_network()


@pytest.fixture(scope="session")
def mock_erc721(active_network):
    return active_network.manifest_named("mock_erc721")


# ------------------------------------------------------------------
#                         FUNCTION SCOPED
# ------------------------------------------------------------------
@pytest.fixture(scope="function")
def duplicates(active_network):
    return active_network.manifest_named("duplicates")


@pytest.fixture(scope="function")
def random_account_1():
    entropy = 13
    account = Account.create(entropy)
    boa.env.set_balance(account.address, BALANCE)
    # with boa.env.prank(account.address):
    #     weth.mock_mint()
    return account
