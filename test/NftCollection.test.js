const { expect } = require('chai');

describe('NftCollection', function () {
  let nftCollection;
  let owner, addr1, addr2, addr3;
  const NAME = 'My NFT Collection';
  const SYMBOL = 'MNFT';
  const MAX_SUPPLY = 1000;
  const BASE_URI = 'https://example.com/metadata/';

  beforeEach(async function () {
    [owner, addr1, addr2, addr3] = await ethers.getSigners();

    const NftCollection = await ethers.getContractFactory('NftCollection');
    nftCollection = await NftCollection.deploy(NAME, SYMBOL, MAX_SUPPLY, BASE_URI);
    await nftCollection.deployed();
  });

  describe('Initialization', function () {
    it('Should init', async function () {
      expect(await nftCollection.name()).to.equal(NAME);
      expect(await nftCollection.symbol()).to.equal(SYMBOL);
      expect(await nftCollection.maxSupply()).to.equal(MAX_SUPPLY);
    });
  });

  describe('Minting', function () {
    it('Should mint', async function () {
      await nftCollection.safeMint(addr1.address, 1);
      expect(await nftCollection.ownerOf(1)).to.equal(addr1.address);
      expect(await nftCollection.totalSupply()).to.equal(1);
    });

    it('Should emit Transfer', async function () {
      await expect(nftCollection.safeMint(addr1.address, 1))
        .to.emit(nftCollection, 'Transfer');
    });

    it('Should prevent non-admin', async function () {
      await expect(nftCollection.connect(addr1).safeMint(addr1.address, 1))
        .to.be.revertedWith('Only admin can call this function');
    });

    it('Should prevent zero address', async function () {
      await expect(nftCollection.safeMint(ethers.constants.AddressZero, 1))
        .to.be.revertedWith('Cannot mint to zero address');
    });
  });

  describe('Transfers', function () {
    beforeEach(async function () {
      await nftCollection.safeMint(addr1.address, 1);
    });

    it('Should transfer', async function () {
      await nftCollection.connect(addr1).transferFrom(addr1.address, addr2.address, 1);
      expect(await nftCollection.ownerOf(1)).to.equal(addr2.address);
    });
  });

  describe('Approvals', function () {
    beforeEach(async function () {
      await nftCollection.safeMint(addr1.address, 1);
    });

    it('Should approve', async function () {
      await nftCollection.connect(addr1).approve(addr2.address, 1);
      expect(await nftCollection.getApproved(1)).to.equal(addr2.address);
    });
  });

  describe('Metadata', function () {
    it('Should return tokenURI', async function () {
      await nftCollection.safeMint(addr1.address, 1);
      const uri = await nftCollection.tokenURI(1);
      expect(uri).to.equal(BASE_URI + '1.json');
    });
  });
});
