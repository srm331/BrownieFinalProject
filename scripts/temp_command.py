
from brownie import DigitalRightsNFT, accounts

def main():
    if len(DigitalRightsNFT) == 0:
        acct = accounts[0]
        DigitalRightsNFT.deploy({'from': acct})

    contract = DigitalRightsNFT[-1]
    tx = contract.mintNFT('sfer', 'wr', 'ere', 10000000000000000000, {'from': accounts[0]})
