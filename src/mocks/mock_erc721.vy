# pragma version 0.4.3


from snekmate.tokens import erc721
from snekmate.auth import ownable as ow


initializes: ow
initializes: erc721[ownable := ow]

exports: erc721.__interface__


NAME: constant(String[25]) = "Mock NFT"
SYMBOL: constant(String[5]) = "MNFT"
BASE_URI: public(constant(String[80])) = "MOCK://"
NAME_EIP712: constant(String[50]) = "Mock NFT"
VERSION_EIP712: constant(String[20]) = "1"


@deploy
def __init__():
    ow.__init__()
    erc721.__init__(NAME, SYMBOL, BASE_URI, NAME_EIP712, VERSION_EIP712)
    

@external
def mint():
    token_id: uint256 = erc721._counter
    erc721._counter = token_id + 1
    erc721._safe_mint(msg.sender, token_id, b"")
    erc721._set_token_uri(token_id, uint2str(token_id))