from src import duplicates
import boa
from moccasin.config import get_active_network

def estimate_deployment_gas():
    active_network = get_active_network()
    print(f"Estimating deployment gas on network: {active_network.name}")
    
    # Get current gas price from the network
    gas_price = boa.env.get_gas_price()
    
    # Deploy the contract to get gas estimation
    print("Deploying contract for gas estimation...")
    
    # Deploy and try to capture gas usage
    contract = duplicates.deploy()
    
    # Try different methods to get actual gas used
    actual_gas = None
    
    # Method 1: Check if deployment receipt is available
    try:
        if hasattr(contract, 'receipt') and contract.receipt:
            actual_gas = contract.receipt.gas_used
            print(f"Gas from receipt: {actual_gas:,}")
    except:
        pass
    
    # Method 2: Check deployment transaction
    try:
        if hasattr(contract, 'deploy_transaction') and contract.deploy_transaction:
            actual_gas = contract.deploy_transaction.gas_used
            print(f"Gas from deploy transaction: {actual_gas:,}")
    except:
        pass
    
    # Method 3: Estimate based on contract bytecode
    if actual_gas is None:
        try:
            # Get the deployed bytecode and estimate
            deployed_bytecode = boa.env.get_code(contract.address)
            if deployed_bytecode:
                # Rough gas estimation: 200 gas per byte + base cost
                bytecode_gas = len(deployed_bytecode) * 200
                creation_gas = 32000  # Base contract creation cost
                estimated_gas = bytecode_gas + creation_gas
                print(f"Estimated from bytecode size: {estimated_gas:,}")
            else:
                raise Exception("No bytecode found")
        except:
            # Final fallback for typical ERC721 deployment
            estimated_gas = 2500000  # Typical ERC721 with extensions
            print("Using typical ERC721 gas estimate (2.5M gas)")
    else:
        estimated_gas = actual_gas
    
    # Calculate costs
    estimated_cost_wei = estimated_gas * gas_price
    estimated_cost_eth = estimated_cost_wei / 10**18
    
    print("\n" + "="*60)
    print("DEPLOYMENT COST ESTIMATION")
    print("="*60)
    print(f"Contract address: {contract.address}")
    print(f"Estimated deployment gas: {estimated_gas:,}")
    print(f"Current gas price: {gas_price / 10**9:.2f} Gwei")
    print(f"Estimated cost: {estimated_cost_eth:.6f} ETH")
    print(f"Estimated cost: ${estimated_cost_eth * get_eth_price():.2f} USD (approximate)")
    
    if active_network.name == "anvil-mainnet-fork":
        print("\n⚠️  NOTE: This is a mainnet fork estimate.")
        print("   Actual mainnet costs may vary based on:")
        print("   - Current gas prices (check ethgasstation.info)")
        print("   - Network congestion")
        print("   - MEV/priority fees")
    
    print("="*60)
    
    return {
        'gas_estimate': estimated_gas,
        'gas_price_wei': gas_price,
        'cost_eth': estimated_cost_eth,
        'contract_address': contract.address
    }

def get_eth_price():
    """Get approximate ETH price in USD - simplified for estimation"""
    # This is a rough estimate - in production you'd fetch from an API
    return 3500  # Approximate ETH price

def moccasin_main():
    return estimate_deployment_gas()