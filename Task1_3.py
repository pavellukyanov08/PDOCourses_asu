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
        with open(filename, 'rb') as file:
            content = file.read()
        return hashlib.md5(content).hexdigest()

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
        previous_block_index = len(os.listdir(self.blockchain_dir)) - 1
        previous_block_filename = os.path.join(self.blockchain_dir, f"block_{previous_block_index}.json")
        previous_hash = self.get_hash(previous_block_filename)

        new_block_data = {
            "index": previous_block_index + 1,
            "date": date,
            "previous_hash": previous_hash,
            "buyer": buyer,
            "seller": seller,
            "price": price
        }

        new_block_data["block_hash"] = hashlib.md5(json.dumps(new_block_data).encode()).hexdigest()
        new_block_filename = os.path.join(self.blockchain_dir, f"block_{new_block_data['index']}.json")
        self.write_block(new_block_data, new_block_filename)

        print(f"New block {new_block_data['index']} has been created")

    def view_block(self, block_index):
        """Viewing the contents' block by number"""
        filename = os.path.join(self.blockchain_dir, f"block_{block_index}.json")
        if not os.path.exists(filename):
            print(f"Block with number {block_index} does not exist")
            return

        with open(filename, 'r') as file:
            block_data = json.load(file)
            print(json.dumps(block_data, indent=4))

    def search_block(self, field, value):
        """Searching for blocks containing the specified data in a specific field"""
        for filename in os.listdir(self.blockchain_dir):
            with open(os.path.join(self.blockchain_dir, filename), 'r') as file:
                block_data = json.load(file)
                if block_data.get(field) == value:
                    print(f"Found match in {block_data['index']} block")
                    print(json.dumps(block_data, indent=4))
                    return
        print(f"Value '{value}' by field '{field}' not found")

    def verify_block(self, block_index):
        """Checking the hash of an arbitrary block"""
        current_block_filename = os.path.join(self.blockchain_dir, f"block_{block_index}.json")
        next_block_filename = os.path.join(self.blockchain_dir, f"block_{block_index + 1}.json")

        # checking for the next block
        if not os.path.exists(next_block_filename):
            print(f"Block {block_index + 1} not found. It's impossible to verify integrity of the block {block_index}")
            return

        # getting the hash current block
        calculated_hash = self.get_hash(current_block_filename)

        # comparing with the hash, stored in the next block
        with open(next_block_filename, 'r') as file:
            next_block_data = json.load(file)
            if next_block_data["previous_hash"] == calculated_hash:
                print(f"The hash of the block {block_index} has been verified")
            else:
                print(f"The hash of the block {block_index} doesn't match with the hash of the previous block {block_index + 1}")


blockchain = Blockchain()

blockchain.create_genesis_block()
blockchain.create_new_block("2024-11-13", "Alice", "Library", 100)
blockchain.create_new_block("2024-11-14", "Bob", "Library", 150)

blockchain.search_block("buyer", "Bob")

blockchain.verify_block(1)






