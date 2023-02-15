import hashlib
import datetime
import uuid

class Transaction:
    def __init__(self, sender, receiver, amount, fee=0, timestamp=None):
        self.id = str(uuid.uuid4())
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.fee = fee
        self.timestamp = timestamp if timestamp else datetime.datetime.now()

    def is_valid(self):
        if self.amount <= 0:
            return False
        return True


class Block:
    def __init__(self, transactions, previous_hash):
        self.timestamp = datetime.datetime.now()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calc_hash()

    def calc_hash(self):
        sha = hashlib.sha256()

        # Hash the block's transaction data, previous block's hash, and nonce
        hash_str = str([t.__dict__ for t in self.transactions]).encode('utf-8') + \
                   str(self.previous_hash).encode('utf-8') + str(self.nonce).encode('utf-8')

        sha.update(hash_str)

        return sha.hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calc_hash()

        print("Block mined: ", self.hash)

    def has_valid_transactions(self):
        for transaction in self.transactions:
            if not transaction.is_valid():
                return False
        return True

class Blockchain:
    def __init__(self):
        self.chain = [Block([], None)]
        self.difficulty = 2
        self.transaction_pool = []

    def add_transaction_to_pool(self, transaction):
        self.transaction_pool.append(transaction)

    def add_transactions_to_pool(self, transactions):
        for transaction in transactions:
            self.transaction_pool.append(transaction)

    def process_transaction_pool(self, reward):
        transactions = self.transaction_pool.copy()
        self.transaction_pool.clear()

        # Create a new transaction for the reward
        reward_tx = Transaction("coinbase", reward, reward, timestamp=datetime.datetime.now())
        transactions.append(reward_tx)

        self.add_block(transactions)

    def add_block(self, transactions):
        previous_hash = self.chain[-1].hash

        new_block = Block(transactions, previous_hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def print_chain(self):
        for block in self.chain:
            print("Timestamp: ", block.timestamp)
            print("Transactions: ", [t.__dict__ for t in block.transactions])
            print("Previous Hash: ", block.previous_hash)
            print("Hash: ", block.hash)
            print()

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calc_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

            if not current_block.has_valid_transactions():
                return False

        return True


if __name__ == "__main__":
    blockchain = Blockchain()

    # Set the reward amount
    reward = 1

    # create some transactions with fees and add them to the transaction pool
    tx1 = Transaction("Alice", "Bob", 10, 0.1)
    tx2 = Transaction("Bob", "Charlie", 5, 0.05)
    tx3 = Transaction("Charlie", "Alice", 3, 0.03)
    blockchain.add_transactions_to_pool([tx1, tx2, tx3])

    # add more transactions to the pool
    tx4 = Transaction("David", "Eva", 2, 0.02)
    tx5 = Transaction("Eva", "Frank", 7, 0.07)
    blockchain.add_transaction_to_pool(tx4)
    blockchain.add_transaction_to_pool(tx5)

    # process the transaction pool to create a new block
    blockchain.process_transaction_pool(reward)

    # print the blockchain
    blockchain.print_chain()

    # check if the blockchain is valid
    print(blockchain.is_valid())
