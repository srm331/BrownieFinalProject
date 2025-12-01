from brownie import DigitalRightsNFT, accounts

def main():
    account = accounts[0]
    
    print(f"Deploying from account: {account}")
    print(f"Account balance: {account.balance() / 1e18} ETH")
    
    contract = DigitalRightsNFT.deploy({'from': account})
    
    print(f"Contract deployed at: {contract.address}")
    print(f"Deployment successful!")
    
    return contract