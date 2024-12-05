import json
import hashlib
import os
from datetime import datetime


class Blockchain:
    def __init__(self, blockchain_dir):
        self.blockchain_dir = blockchain_dir
        if not os.path.exists(self.blockchain_dir):
            os.makedirs(self.blockchain_dir)

    def _calculate_hash(self, block):
        block_string = json.dumps(block, sort_keys=True)
        return hashlib.md5(block_string.encode()).hexdigest()

    def write_block(self, block, filename):
        with open(filename, "w") as f:
            json.dump(block, f, indent=3)

    def create_block(self, previous_hash, block_number):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        block = {
            "block_number": block_number,
            "previous_hash": previous_hash,
            "block_hash": "",
            "timestamp": timestamp
        }
        block["block_hash"] = self._calculate_hash(block)
        return block


class BlockchainWithMerge(Blockchain):
    def __init__(self, blockchain_dir):
        super().__init__(blockchain_dir)

    def validate_and_merge_chain(self, short_chain_dir):
        short_chain_files = sorted(os.listdir(short_chain_dir), key=lambda x: int(x.split('_')[1].split('.')[0]))

        for file_name in short_chain_files:
            with open(os.path.join(short_chain_dir, file_name), "r") as f:
                block = json.load(f)

            if not self.is_block_in_chain(block):
                self.write_block(block, os.path.join(self.blockchain_dir, file_name))
                print(f"Block {block['block_number']} added to the main chain.")
            else:
                print(f"Block {block['block_number']} already exists in the main chain.")

    def is_block_in_chain(self, block):
        for file_name in os.listdir(self.blockchain_dir):
            with open(os.path.join(self.blockchain_dir, file_name), "r") as f:
                existing_block = json.load(f)
                if existing_block["block_hash"] == block["block_hash"]:
                    return True
        return False


# Task 1
blockchain_dir = "blockchain_data"
bc = Blockchain(blockchain_dir)

genesis_block = bc.create_block("0", 0)
bc.write_block(genesis_block, os.path.join(blockchain_dir, "block_0.json"))

# Добавление блоков в разные цепочки (ветвление)
block_1 = bc.create_block(genesis_block["block_hash"], 1)
bc.write_block(block_1, os.path.join(blockchain_dir, "block_1.json"))

# Ветка 1
block_2a = bc.create_block(block_1["block_hash"], 2)
bc.write_block(block_2a, os.path.join(blockchain_dir, "block_2a.json"))

# Ветка 2
block_2b = bc.create_block(block_1["block_hash"], 2)
bc.write_block(block_2b, os.path.join(blockchain_dir, "block_2b.json"))

# Ветка 1
block_3a = bc.create_block(block_2a["block_hash"], 3)
bc.write_block(block_3a, os.path.join(blockchain_dir, "block_3a.json"))

# Ветка 2
block_3b = bc.create_block(block_2b["block_hash"], 3)
bc.write_block(block_3b, os.path.join(blockchain_dir, "block_3b.json"))


# Task 2
bc_with_merge = BlockchainWithMerge(blockchain_dir)

short_chain_dir = "blockchain_data_short"
if not os.path.exists(short_chain_dir):
    os.makedirs(short_chain_dir)
bc_with_merge.validate_and_merge_chain(short_chain_dir)