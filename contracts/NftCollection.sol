// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title NftCollection
 * @dev ERC-721 compatible NFT contract with minting, transfers, approvals, and metadata support
 */
contract NftCollection {
    // ============ Events ============
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId);
    event ApprovalForAll(address indexed owner, address indexed operator, bool approved);

    // ============ State Variables ============
    string public name;
    string public symbol;
    uint256 public maxSupply;
    uint256 public totalSupply;
    bool public mintingPaused;

    address private _admin;
    string private _baseURI;

    mapping(uint256 => address) private _owners;
    mapping(address => uint256) private _balances;
    mapping(uint256 => address) private _approvals;
    mapping(address => mapping(address => bool)) private _operatorApprovals;

    // ============ Constructor ============
    constructor(
        string memory _name,
        string memory _symbol,
        uint256 _maxSupply,
        string memory baseURI
    ) {
        require(_maxSupply > 0, "Max supply must be greater than 0");
        name = _name;
        symbol = _symbol;
        maxSupply = _maxSupply;
        _baseURI = baseURI;
        _admin = msg.sender;
        totalSupply = 0;
        mintingPaused = false;
    }

    // ============ Access Control ============
    modifier onlyAdmin() {
        require(msg.sender == _admin, "Only admin can call this function");
        _;
    }

    // ============ Core ERC-721 Functions ============
    
    /**
     * @dev Returns the number of tokens owned by address
     */
    function balanceOf(address owner) public view returns (uint256) {
        require(owner != address(0), "Address cannot be zero");
        return _balances[owner];
    }

    /**
     * @dev Returns the owner of tokenId
     */
    function ownerOf(uint256 tokenId) public view returns (address) {
        address owner = _owners[tokenId];
        require(owner != address(0), "Token does not exist");
        return owner;
    }
        return owner;
    }

    /**
     * @dev Mints new token (admin only)
     */
    function safeMint(address to, uint256 tokenId) public onlyAdmin {
        require(!mintingPaused, "Minting is paused");
        require(to != address(0), "Cannot mint to zero address");
        require(_owners[tokenId] == address(0), "Token already minted");
        require(totalSupply < maxSupply, "Max supply reached");

        _owners[tokenId] = to;
        _balances[to]++;
        totalSupply++;

        emit Transfer(address(0), to, tokenId);
    }

    /**
     * @dev Transfers token from one address to another
     */
    function transferFrom(
        address from,
        address to,
        uint256 tokenId
    ) public {
        require(_owners[tokenId] == from, "From address is not the owner");
        require(to != address(0), "Cannot transfer to zero address");
        
        require(
            msg.sender == from || msg.sender == _approvals[tokenId] || _operatorApprovals[from][msg.sender],
            "Not authorized to transfer"
        );

        // Clear approvals
        _approvals[tokenId] = address(0);

        // Update ownership
        _owners[tokenId] = to;
        _balances[from]--;
        _balances[to]++;

        emit Transfer(from, to, tokenId);
    }

    /**
     * @dev Safe transfer with optional data
     */
    function safeTransferFrom(
        address from,
        address to,
        uint256 tokenId,
        bytes memory data
    ) public {
        transferFrom(from, to, tokenId);
    }

    /**
     * @dev Safe transfer without data
     */
    function safeTransferFrom(
        address from,
        address to,
        uint256 tokenId
    ) public {
        safeTransferFrom(from, to, tokenId, "");
    }

    /**
     * @dev Approves address to transfer a specific token
     */
    function approve(address to, uint256 tokenId) public {
        address owner = _owners[tokenId];
        require(owner != address(0), "Token does not exist");
        require(msg.sender == owner || _operatorApprovals[owner][msg.sender], "Not authorized");

        _approvals[tokenId] = to;
        emit Approval(owner, to, tokenId);
    }

    /**
     * @dev Sets or revokes operator approval for all tokens
     */
    function setApprovalForAll(address operator, bool approved) public {
        require(operator != msg.sender, "Cannot approve yourself");
        _operatorApprovals[msg.sender][operator] = approved;
        emit ApprovalForAll(msg.sender, operator, approved);
    }

    /**
     * @dev Returns approved address for a token
     */
    function getApproved(uint256 tokenId) public view returns (address) {
        require(_owners[tokenId] != address(0), "Token does not exist");
        return _approvals[tokenId];
    }

    /**
     * @dev Returns if operator is approved for all tokens of owner
     */
    function isApprovedForAll(address owner, address operator) public view returns (bool) {
        return _operatorApprovals[owner][operator];
    }

    // ============ Metadata Functions ============
    
    /**
     * @dev Returns metadata URI for a token
     */
    function tokenURI(uint256 tokenId) public view returns (string memory) {
        require(_owners[tokenId] != address(0), "Token does not exist");
        return string(abi.encodePacked(_baseURI, toString(tokenId), ".json"));
    }

    /**
     * @dev Updates base URI (admin only)
     */
    function setBaseURI(string memory newBaseURI) public onlyAdmin {
        _baseURI = newBaseURI;
    }

    // ============ Admin Functions ============
    
    /**
     * @dev Pauses minting (admin only)
     */
    function pauseMinting() public onlyAdmin {
        mintingPaused = true;
    }

    /**
     * @dev Unpauses minting (admin only)
     */
    function unpauseMinting() public onlyAdmin {
        mintingPaused = false;
    }

    /**
     * @dev Burns token (reduces totalSupply)
     */
    function burn(uint256 tokenId) public {
        require(_owners[tokenId] == msg.sender, "Only token owner can burn");
        
        _balances[msg.sender]--;
        totalSupply--;
        
        delete _owners[tokenId];
        delete _approvals[tokenId];

        emit Transfer(msg.sender, address(0), tokenId);
    }

    // ============ Utility Functions ============
    
    /**
     * @dev Converts uint256 to string
     */
    function toString(uint256 value) internal pure returns (string memory) {
        if (value == 0) return "0";
        uint256 temp = value;
        uint256 digits;
        while (temp != 0) {
            digits++;
            temp /= 10;
        }
        bytes memory buffer = new bytes(digits);
        while (value != 0) {
            digits--;
            buffer[digits] = bytes1(uint8(48 + uint256(value % 10)));
            value /= 10;
        }
        return string(buffer);
    }

    /**
     * @dev Returns admin address
     */
    function getAdmin() public view returns (address) {
        return _admin;
    }
}
    }
}
