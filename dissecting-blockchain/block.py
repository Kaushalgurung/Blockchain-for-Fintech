import hashlib

from dataclasses import dataclass
from datetime import datetime
from re import T
from typing import List


@dataclass
class Block:
    def __init__(self, index: int, data: str, previous_block: str,  timestamp: datetime = None,):
        self.index = index
        self.timestamp = timestamp or datetime.now()
        self.data = data
        self.previous_block = previous_block

    def header_hash(self):
        """
        Generate block header hash
        """
        return hashlib.sha256(
            (
                str(self.index)
                + str(int(self.timestamp.timestamp()))
                + str(self.data)
                + str(self.previous_block or "")
            ).encode("utf-8")
        ).hexdigest()

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return "Block<{0}, {1}, Previous<{2}>, {3}, {4}>".format(
            self.index, self.header_hash(), self.previous_block, int(self.timestamp.timestamp()), self.data
        )


class Blockchain:
    def __init__(self, genesis=None, blocks=None):
        self.genesis = genesis or Block(0, "Genesis Block", None)
        self.blocks = ([Block(**block) for block in blocks] if blocks else None) or [self.genesis]

    def append_block(self, data: str):
        """
        Add new block to blockchain
        """
        block = Block(self.blocks[-1].index + 1, data, self.blocks[-1].header_hash())
        new_blockchain = self.blocks + [block]
        Blockchain.validate(new_blockchain)
        self.blocks = new_blockchain

    def get_last_block(self):
        return self.blocks[-1]

    def to_dict(self):
        return {
            "genesis": self.genesis.to_dict(),
            "blocks": [block.to_dict() for block in self.blocks]
        }

    def __str__(self):
        return "\n".join(str(block) for block in self.blocks)


    @classmethod
    def validate(cls, blocks: List[Block]) -> bool:
        """
        Validate given blockchain
        """
        for i in range(1, len(blocks)):
            if blocks[i - 1].header_hash() != blocks[i].previous_block:
                return False
        return True


if __name__ == "__main__":
    blockchain = Blockchain()

    # Add your code here
    blockchain.append_block("Blockchain")
    blockchain.append_block("Is")
    blockchain.append_block("Awesome")

    # Print the entire blockchain
    print("Orginal Blockchain:\n", blockchain)

    # Modify the 3rd block's data (index 2)
    blockchain.blocks[2].data = "Is very"
    print("\nBlockchain after modifying the 3rd block:\n", blockchain)

    # Validate the modified blockchain
    is_valid = Blockchain.validate(blockchain.blocks)
    print(f"\nIs the modified blockchain valid? {is_valid}")

    # Calculate the correct hash of the final block to make the blockchain valid
    if not is_valid:
        print("\nThe modified blockchain is invalid.")
        # Recalculate the correct hash for the last block by fixing the chain
        blockchain.blocks[2] = Block(2, "Is very", blockchain.blocks[1].header_hash())
        blockchain.blocks[3] = Block(3, "Awesome", blockchain.blocks[2].header_hash())
        print("\nThe blockchain is now repaired:")
        print(blockchain)
        print(f"\nHash of the final block after repair: {blockchain.get_last_block().header_hash()}")