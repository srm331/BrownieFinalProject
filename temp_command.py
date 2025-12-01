
from brownie import DigitalRightsNFT, accounts
contract = DigitalRightsNFT[-1]
tx = contract.mintNFT('sunset', 'sunset beautiful', 'Creator Dace', 1000000000000000000, {'from': accounts[0]})
print(f'NFT Minted! Token ID: {tx.return_value}')
