import hashlib
import datetime

class Block:
    def __init__(self, data, previous_hash):
        self.timestamp = datetime.datetime.now()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calc_hash()

    def calc_hash(self):
        sha = hashlib.sha256()

        # Hash the block's data and the previous block's hash
        hash_str = str(self.data).encode('utf-8') + str(self.previous_hash).encode('utf-8')

        sha.update(hash_str)

        return sha.hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [Block("Genesis Block", None)]

    def add_block(self, data):
        previous_hash = self.chain[-1].hash
        new_block = Block(data, previous_hash)
        self.chain.append(new_block)

    def print_chain(self):
        for block in self.chain:
            print("Timestamp: ", block.timestamp)
            print("Data: ", block.data)
            print("Previous Hash: ", block.previous_hash)
            print("Hash: ", block.hash)
            print()


if __name__ == "__main__":
  blockchain = Blockchain()

  blockchain.add_block("This is block 1")
  blockchain.add_block("This is block 2")
  blockchain.add_block("This is block 3")

  blockchain.print_chain()
