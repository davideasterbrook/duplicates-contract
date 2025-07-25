# pragma version 0.4.3

from snekmate.tokens import erc721
from snekmate.auth import ownable as ow
from snekmate.tokens.interfaces import IERC721Metadata


initializes: ow
initializes: erc721[ownable := ow]

exports: (
    erc721.owner,
    erc721.balanceOf,
    erc721.ownerOf,
    erc721.getApproved,
    erc721.approve,
    erc721.setApprovalForAll,
    erc721.transferFrom,
    erc721.safeTransferFrom,
    # erc721.tokenURI, 
    erc721.totalSupply,
    erc721.tokenByIndex,
    erc721.tokenOfOwnerByIndex,
    erc721.burn,
    # erc721.safe_mint, 
    # erc721.set_minter,
    erc721.permit,
    erc721.DOMAIN_SEPARATOR,
    erc721.transfer_ownership,
    erc721.renounce_ownership,
    erc721.name,
    erc721.symbol,
    erc721.isApprovedForAll,
    erc721.is_minter,
    erc721.nonces,
)

NAME: constant(String[25]) = "Duplicates NFT"
SYMBOL: constant(String[5]) = "DUPE"
BASE_URI: constant(String[80]) = ""
NAME_EIP712: constant(String[50]) = "Duplicates NFT"
VERSION_EIP712: constant(String[20]) = "1"

# ------------------------------------------------------------------
#                              STRUCTS
# ------------------------------------------------------------------
struct token_metadata:
    contract_address: address
    external_id: uint256

# ------------------------------------------------------------------
#                             STORAGE
# ------------------------------------------------------------------
token_id_to_metadata: public(HashMap[uint256, token_metadata])
MAX_MINT_PRICE: public(uint256)

# ------------------------------------------------------------------
#                              EVENTS
# ------------------------------------------------------------------
event Minted:
    token_id: indexed(uint256)
    minter: indexed(address)
    original_contract: indexed(address)
    original_token_id: uint256
    price_paid: uint256

# ------------------------------------------------------------------
#                             CONSTRUCTOR
# ------------------------------------------------------------------
@deploy
def __init__():
    ow.__init__()
    erc721.__init__(NAME, SYMBOL, BASE_URI, NAME_EIP712, VERSION_EIP712)
    self.MAX_MINT_PRICE = 10**17  # Initialize to 0.1 ETH

# ------------------------------------------------------------------
#                        EXTERNAL FUNCTIONS
# ------------------------------------------------------------------
@external
@payable
def mint(contract_address: address, external_id: uint256):
    price_paid: uint256 = msg.value
    self._fund()
    token_uri: String[512] = self.get_external_uri(contract_address, external_id)
    token_id: uint256 = erc721._counter
    erc721._counter = token_id + 1
    self.token_id_to_metadata[token_id] = token_metadata(contract_address=contract_address, external_id=external_id)
    erc721._safe_mint(msg.sender, token_id, b"")
    
    log Minted(token_id=token_id, minter=msg.sender, original_contract=contract_address, original_token_id=external_id, price_paid=price_paid)
    

@external
def set_max_price(new_max_price: uint256):
    """
    Owner can update the maximum minting price cap
    """
    assert msg.sender == ow.owner, "Only owner can set max price"
    self.MAX_MINT_PRICE = new_max_price
    

@external
@view
def tokenURI(token_id: uint256) -> String[512]:
    metadata: token_metadata = self.token_id_to_metadata[token_id]
    return self.get_external_uri(metadata.contract_address, metadata.external_id)

@external
@view
def minting_cost() -> uint256:
    return self._minting_cost()

@external
def withdraw(gas_stipend: uint256 = 0):
    send(ow.owner, self.balance, gas=gas_stipend)

@external 
@payable 
def __default__():
    self._fund()

# ------------------------------------------------------------------
#                        INTERNAL FUNCTIONS
# ------------------------------------------------------------------
@internal
@view
def get_external_uri(contract_address: address, token_id: uint256) -> String[512]:
    external_uri: String[512] = staticcall IERC721Metadata(contract_address).tokenURI(token_id)
    return external_uri

@internal
@view
def _minting_cost() -> uint256:
    token_count: uint256 = erc721._counter
    if token_count < 100:  # First 100 tokens free
        return 0

    tier: uint256 = token_count // 1000
    base_price: uint256 = 10**15  # 0.0005 ETH in wei
    
    price: uint256 = base_price * (2 ** tier)
    
    if price > self.MAX_MINT_PRICE:
        return self.MAX_MINT_PRICE
    else:
        return price

@internal
@payable
def _fund():
    assert msg.value >= self._minting_cost()

