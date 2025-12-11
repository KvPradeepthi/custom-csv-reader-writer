# ERC-721 NFT Smart Contract

## Overview

This is an ERC-721 compatible NFT smart contract implementation with comprehensive testing and Docker support. The contract enables secure minting, transferring, and management of unique tokens on the Ethereum blockchain.

## Features

- **ERC-721 Standard Compliance**: Implements core ERC-721 interface for non-fungible tokens
- **Secure Minting**: Admin-only minting with double-mint prevention
- **Safe Transfers**: Authorization checks for ownership and approvals
- **Token Approvals**: Individual token approval and operator approval mechanisms
- **Metadata Support**: tokenURI functionality for token metadata
- **Max Supply Control**: Configurable maximum token supply limit
- **Pause/Unpause**: Admin ability to pause/unpause minting
- **Token Burning**: Ability to burn tokens and reduce total supply
- **Comprehensive Tests**: Full test suite with edge case coverage

## Project Structure

```
.
├── contracts/
│   └── NftCollection.sol        # Main ERC-721 contract
├── test/
│   └── NftCollection.test.js    # Comprehensive test suite
├── package.json                  # Node.js dependencies
├── hardhat.config.js             # Hardhat configuration
├── Dockerfile                    # Docker configuration
├── .dockerignore                 # Docker ignore rules
└── NFT_README.md                # This file
```

## Installation

### Prerequisites
- Node.js 18+
- npm or yarn
- Docker (optional, for containerized testing)

### Local Setup

```bash
npm install
npx hardhat compile
```

## Testing

### Local Testing

```bash
npm test
# or
npx hardhat test
```

### Docker Testing

```bash
# Build Docker image
docker build -t nft-contract .

# Run tests in container
docker run nft-contract
```

## Contract Details

### Constructor

```solidity
constructor(
    string memory _name,
    string memory _symbol,
    uint256 _maxSupply,
    string memory baseURI
)
```

Initializes the contract with:
- `_name`: Token collection name
- `_symbol`: Token symbol
- `_maxSupply`: Maximum number of tokens that can be minted
- `baseURI`: Base URI for token metadata

### Core Functions

#### Minting
```solidity
function safeMint(address to, uint256 tokenId) public onlyAdmin
```
Mints a new token to the specified address. Only admin can mint.

#### Transfers
```solidity
function transferFrom(address from, address to, uint256 tokenId) public
function safeTransferFrom(address from, address to, uint256 tokenId) public
```
Transfers tokens with authorization checks.

#### Approvals
```solidity
function approve(address to, uint256 tokenId) public
function setApprovalForAll(address operator, bool approved) public
```
Manages token transfer permissions.

#### Metadata
```solidity
function tokenURI(uint256 tokenId) public view returns (string memory)
```
Returns the metadata URI for a token.

#### Admin Functions
```solidity
function pauseMinting() public onlyAdmin
function unpauseMinting() public onlyAdmin
function burn(uint256 tokenId) public
```

## Test Coverage

The test suite covers:

- **Initialization**: Contract configuration validation
- **Minting**: Successful minting, authorization checks, max supply enforcement
- **Transfers**: Token transfers, balance updates, authorization
- **Approvals**: Individual token approvals, operator approvals
- **Metadata**: tokenURI generation and retrieval
- **Edge Cases**: Double-minting prevention, zero address validation, pause/unpause

## Gas Optimization

The contract is optimized for:
- Minimal state writes
- Efficient data structures (mappings for O(1) lookups)
- Optimized compiler settings with 200 optimization runs

## Security Considerations

1. **Access Control**: Only admin can mint tokens
2. **Input Validation**: All addresses checked for zero address
3. **Invariant Enforcement**: Unique token IDs, ownership constraints
4. **Atomic Operations**: State changes are atomic to prevent inconsistencies
5. **Re-entrancy Protection**: No external calls in state-modifying functions

## Configuration

### Hardhat Config
- Solidity: ^0.8.20
- Optimizer: Enabled (200 runs)
- Chain ID: 31337 (Hardhat network)

### Dependencies
- @nomicfoundation/hardhat-toolbox: ^3.0.0
- hardhat: ^2.18.0
- chai: ^4.3.7
- @openzeppelin/contracts: ^4.9.3

## Running Tests

### All Tests
```bash
npm test
```

### Specific Test Suite
```bash
npx hardhat test --grep "Minting"
```

### With Gas Report
```bash
HTMLREPORT=true npx hardhat test
```

## Docker Workflow

1. **Build Image**
   ```bash
   docker build -t nft-contract:latest .
   ```

2. **Run Container**
   ```bash
   docker run nft-contract:latest
   ```

3. **View Logs**
   ```bash
   docker run nft-contract:latest npm test -- --reporter json
   ```

## License

MIT

## Author

KvPradeepthi
