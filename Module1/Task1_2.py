import json
import hashlib
import os


class Blockchain:
    def __init__(self, blockchain_dir="blocks"):
        self.blockchain_dir = blockchain_dir
        if not os.path.exists(self.blockchain_dir):
            os.mkdir(self.blockchain_dir)

    def get_hash(self, filename):
        """Calculating the hash for the block"""
        with open(filename, 'rb') as f:
            content = f.read()
        return hashlib.sha256(content).hexdigest()

    def write_block(self, block_data, filename):
        """Writing the block into the JSON-file"""
        with open(filename, 'w') as file:
            json.dump(block_data, file, indent=4)

    def create_genesis_block(self):
        """Creating the genesis-block"""
        genesis_data = {
            "index": 0,
            "date": "2024-11-10",
            "previous_hash": "0",
            "buyer": "Library Admin",
            "seller": "Customer",
            "price": "100$"
        }

        genesis_data["block_hash"] = hashlib.md5(json.dumps(genesis_data).encode()).hexdigest()
        self.write_block(genesis_data, os.path.join(self.blockchain_dir, "block_0.json"))
        print("Genesis block has been created")

    def create_new_block(self, date, buyer, seller, price):
        """Creating the new block with the specified data"""

        # Determining the number of the new block
        previous_block_index = len(os.listdir(self.blockchain_dir)) - 1
        previous_block_filename = os.path.join(self.blockchain_dir, f"block_{previous_block_index}.json")

        # Getting the hash the previous block
        previous_hash = self.get_hash(previous_block_filename)

        # The data of the new block
        new_block_data = {
            "index": previous_block_index + 1,
            "date": date,
            "previous_hash": previous_hash,
            "buyer": buyer,
            "seller": seller,
            "price": price
        }

        # Calculating the hash of the current block and saving it
        new_block_data["block_hash"] = hashlib.md5(json.dumps(new_block_data).encode()).hexdigest()
        new_block_filename = os.path.join(self.blockchain_dir, f"block_{new_block_data['index']}.json")
        self.write_block(new_block_data, new_block_filename)

        print(f"Block {new_block_data['index']} has been created")

    def view_block(self, block_index):
        """Viewing the contents' block by number"""
        filename = os.path.join(self.blockchain_dir, f"block_{block_index}.json")
        if not os.path.exists(filename):
            print(f"Block with number {block_index} does not exist")
            return

        with open(filename, 'r') as file:
            block_data = json.load(file)
            print(json.dumps(block_data, indent=4))


blockchain = Blockchain()
blockchain.create_genesis_block()  # Generating genesis-block

# Generating a new blocks
blockchain.create_new_block("2024-02-01", "Alice", "Library", 100)
blockchain.create_new_block("2024-03-01", "Bob", "Library", 150)

# Viewing the contents' block by number
blockchain.view_block(1)
blockchain.view_block(2)
