import  json
import os
import hashlib
from datetime import datetime


class Blockchain:
    def __init__(self, blocks_dir="blocks"):
        self.blocks_dir = blocks_dir
        if not os.path.exists(self.blocks_dir):
            os.mkdir(self.blocks_dir)

    def generate_genesis_block(self):
        genesis_block = {
            "index": 0,
            "date": str(datetime.now()),
            "previous_hash": "0",
            "transactions": [{"buyer": "System", "seller": "None", "amount": "0"}]
        }
        genesis_block["block_hash"] = self._calculate_hash(genesis_block)
        self.write_block(genesis_block, os.path.join(self.blocks_dir, "block_0.json"))


    def add_block(self, transactions):
        blocks = sorted(os.listdir(self.blocks_dir), key=lambda x: int(x.split('_')[1].split('.')[0]))
        last_block_path = os.path.join(self.blocks_dir, blocks[-1])
        with open(last_block_path, "r") as f:
            last_block = json.load(f)
            new_block = {
                "index": len(blocks),
                "date": str(datetime.now()),
                "previous_hash": last_block["block_hash"],
                "transactions": transactions
            }

            new_block["block_hash"] = self._calculate_hash(new_block)
            self.write_block(new_block, os.path.join(self.blocks_dir, f"block_{len(blocks)}.json"))


    def write_block(self, block_data, file_path):
        with open(file_path, "w") as f:
            json.dump(block_data, f, indent=4)


    def _calculate_hash(self, block_data):
        return hashlib.md5(json.dumps(block_data, sort_keys=True).encode()).hexdigest()


    def search_transaction(self, buyer, seller):
        for block_file in sorted(os.listdir(self.blocks_dir), key=lambda x: int(x.split('_')[1].split('.')[0])):
            with open(os.path.join(self.blocks_dir, block_file), "r") as f:
                block_data = json.load(f)
                for transaction in block_data["transactions"]:
                    if transaction["buyer"] == buyer and transaction["seller"] == seller:
                        return block_data
        return None


    def validate_blockchain(self):
        blocks = sorted(os.listdir(self.blocks_dir), key=lambda x: int(x.split('_')[1].split('.')[0]))
        for i in range(1, len(blocks)):
            with open(os.path.join(self.blocks_dir, blocks[i]), "r") as current_file:
                current_block = json.load(current_file)
            with open(os.path.join(self.blocks_dir, blocks[i - 1]), "r") as prev_file:
                prev_file = json.load(prev_file)
            if current_block["previous_hash"] != prev_file["block_hash"]:
                return False
        return True


blockchain = Blockchain()
blockchain.generate_genesis_block()

blockchain.add_block([{"buyer": "Alice", "seller": "Bob", "amount": 100}])

transaction = {"buyer": "Alice", "seller": "Bob", "amount": 100}
if blockchain.search_transaction(transaction["buyer"], transaction["seller"]):
    print("Error: the transaction already exists!")
else:
    blockchain.add_block([transaction])

if blockchain.validate_blockchain():
    print("Blockchain is numerical")
else:
    print("Blockchain is broken!")





