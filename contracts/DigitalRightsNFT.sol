// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DigitalRightsNFT {
    struct CreativeWork {
        string title;
        string description;
        string creator;
        uint256 price;
        address owner;
        bool forSale;
    }
    
    mapping(uint256 => CreativeWork) public creativeWorks;
    mapping(address => uint256[]) public ownerToTokenIds;
    
    uint256 public tokenCounter;
    
    event NFTMinted(uint256 indexed tokenId, string title, address indexed creator);
    event NFTBought(uint256 indexed tokenId, address indexed buyer, uint256 price);
    event NFTListed(uint256 indexed tokenId, uint256 price);
    
    constructor() {
        tokenCounter = 0;
    }
    
    function mintNFT(
        string memory _title,
        string memory _description,
        string memory _creator,
        uint256 _price
    ) public returns (uint256) {
        uint256 newTokenId = tokenCounter;
        
        creativeWorks[newTokenId] = CreativeWork({
            title: _title,
            description: _description,
            creator: _creator,
            price: _price,
            owner: msg.sender,
            forSale: false
        });
        
        ownerToTokenIds[msg.sender].push(newTokenId);
        tokenCounter++;
        
        emit NFTMinted(newTokenId, _title, msg.sender);
        
        return newTokenId;
    }
    
    function listNFTForSale(uint256 _tokenId, uint256 _price) public {
        require(creativeWorks[_tokenId].owner == msg.sender, "You don't own this NFT");
        require(_price > 0, "Price must be greater than 0");
        
        creativeWorks[_tokenId].price = _price;
        creativeWorks[_tokenId].forSale = true;
        
        emit NFTListed(_tokenId, _price);
    }
    
    function buyNFT(uint256 _tokenId) public payable {
        CreativeWork storage work = creativeWorks[_tokenId];
        
        require(work.forSale, "This NFT is not for sale");
        require(msg.value >= work.price, "Insufficient payment");
        require(work.owner != msg.sender, "You already own this NFT");
        
        address previousOwner = work.owner;
        
        payable(previousOwner).transfer(msg.value);
        
        _removeTokenFromOwner(previousOwner, _tokenId);
        
        work.owner = msg.sender;
        work.forSale = false;
        
        ownerToTokenIds[msg.sender].push(_tokenId);
        
        emit NFTBought(_tokenId, msg.sender, work.price);
    }
    
    function _removeTokenFromOwner(address _owner, uint256 _tokenId) private {
        uint256[] storage tokens = ownerToTokenIds[_owner];
        for (uint256 i = 0; i < tokens.length; i++) {
            if (tokens[i] == _tokenId) {
                tokens[i] = tokens[tokens.length - 1];
                tokens.pop();
                break;
            }
        }
    }
    
    function getMyNFTs() public view returns (uint256[] memory) {
        return ownerToTokenIds[msg.sender];
    }
    
    function getAllNFTs() public view returns (uint256[] memory) {
        uint256[] memory allTokens = new uint256[](tokenCounter);
        for (uint256 i = 0; i < tokenCounter; i++) {
            allTokens[i] = i;
        }
        return allTokens;
    }
    
    function getNFTDetails(uint256 _tokenId) public view returns (
        string memory title,
        string memory description,
        string memory creator,
        uint256 price,
        address owner,
        bool forSale
    ) {
        CreativeWork memory work = creativeWorks[_tokenId];
        return (
            work.title,
            work.description,
            work.creator,
            work.price,
            work.owner,
            work.forSale
        );
    }
}