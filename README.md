# Duplicates NFT

An NFT project for creating duplicates of any ERC721 NFTs. The goal of this project is to learn and work with Vyper, write my first smart contract (and deploy it!) while providing some commentary on the ideas about the "value" of NFTs.

## Overview

This project demonstrates how to create "duplicate" NFTs that reference existing ERC721 tokens from popular collections like BAYC, Doodles, PudgyPenguins. The smart contract is written in Vyper and uses the snekmate library for ERC721 implementation.

## Prerequisites

- Python 3.11 or higher
- Git

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd duplicates_contract
```

2. Install dependencies using uv (recommended) or pip:
```bash
# Using uv (faster)
uv sync

# Or using pip
pip install -r requirements.txt
```

3. Set up your environment variables by creating a `.env` file:
```bash
cp example.env .env
# Edit .env with your configuration
```

## Project Structure

```
duplicates_nft_contract/
├── src/                          # Smart contract source code
│   ├── duplicates.vy            # Main duplicates NFT contract
│   ├── interfaces/              # Contract interfaces
│   └── mocks/                   # Mock contracts for testing
│       └── mock_erc721.vy
├── script/                      # Deployment and utility scripts
│   ├── deploy_duplicates.py     # Main deployment script
│   ├── deploy_and_transfer_ownership.py
│   ├── mint_multiple_tokens.py  # Batch minting script
│   ├── give_deployer_eth.py     # Test account funding
│   ├── reset_test_accounts.py   # Reset test environment
│   └── mocks/
│       └── deploy_mock_erc721.py
├── tests/                       # Test suite
│   ├── conftest.py             # Test configuration
│   └── test_duplicates.py      # Main test file
├── abis/                       # Contract ABIs
│   ├── duplicates.json         # Generated duplicates contract ABI
│   ├── bayc.json              # Bored Ape Yacht Club ABI
│   ├── doodle.json            # Doodles ABI
│   ├── autoglyphs.json        # Autoglyphs ABI
│   └── ppg.json               # PudgyPenguins ABI
├── out/                        # Compiled contract artifacts
├── lib/                        # Dependencies
├── moccasin.toml              # Moccasin configuration
├── pyproject.toml             # Python project configuration
└── README.md
```

## Tools

This project makes use of:
- **Moccasin**: Smart contract development framework for Vyper
- **Titanoboa**: Vyper interpreter and testing framework
- **Vyper**: Smart contract programming language
- **Snekmate**: Vyper smart contract library

## Usage

### Compiling Contracts

Compile the Vyper contracts:

```bash
mox compile
```

### Running Tests

Run the test suite:

```bash
# Run all tests
mox test

# Run specific test file
mox test tests/test_duplicates.py

# Run tests with verbose output
mox test -v
```

### Deployment

#### Local Development (Anvil)

1. Start a local Anvil node:
```bash
anvil
```

2. Deploy the contract:
```bash
mox run deploy_duplicates --network anvil
```

#### Mainnet Fork Testing

1. Start Anvil with mainnet fork:
```bash
anvil --fork-url $MAINNET_RPC_URL --chain-id 31337
```

2. Deploy to the fork:
```bash
mox run deploy_duplicates --network anvil-mainnet-fork
```

### Minting Duplicates

After deployment, you can mint duplicate NFTs:

```bash
# Mint multiple tokens
mox run mint_multiple_tokens --network anvil
```

## Smart Contract Features

The Duplicates NFT contract includes:

- **ERC721 Compliance**: Full ERC721 implementation using snekmate
- **Metadata Storage**: Tracks original contract address and token ID for each duplicate
- **Owner Controls**: Ownable pattern for administrative functions
- **Batch Operations**: Support for minting multiple duplicates
- **Gas Optimization**: Efficient storage and operations

## Network Configuration

The project supports multiple networks configured in `moccasin.toml`:

- **pyevm**: Local Python EVM for testing
- **anvil**: Local development network
- **anvil-mainnet-fork**: Mainnet fork for realistic testing


# Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

# Notes:
### Adding NFT Collections for easier local development

Collection's contract must be ERC721 compliant and make use of the tokenuri() function.

To add a new NFT collection for easier local development:

1. Fetch the contract ABI:
```bash
mox explorer get <CONTRACT_ADDRESS> --save --name <collection_name>
```

2. Add the contract configuration to `moccasin.toml`:
```toml
[networks.contracts]
<collection_name> = {abi = "abis/<collection_name>.json"}
```

3. Update the mainnet fork configuration with the contract address.

## Future work
- Improve testing
