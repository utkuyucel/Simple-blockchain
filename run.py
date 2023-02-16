import hashlib
import datetime
import uuid

class Transaction:
    def __init__(self, sender, recipient, amount, fee, transaction_type=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.fee = fee
        self.transaction_type = transaction_type

    def __str__(self):
        return f"Transaction(sender={self.sender}, recipient={self.recipient}, amount={self.amount}, fee={self.fee}, type={self.transaction_type})"

class Block:
    def __init__(self, transactions, previous_hash):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = datetime.datetime.now()
        self.nonce = 0
        self.hash = self.generate_hash()

    def generate_hash(self):
        block_contents = str(self.previous_hash) + str(self.timestamp) + str(self.transactions) + str(self.nonce)
        block_hash = hashlib.sha256(block_contents.encode())
        return block_hash.hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transaction_pool = []

    def add_transaction_to_pool(self, transaction):
        self.transaction_pool.append(transaction)

    def add_transactions_to_pool(self, transactions):
        self.transaction_pool.extend(transactions)

    def process_transaction_pool(self, reward, transaction_fee=0.01):
        if not self.transaction_pool:
            return

        # Create a coinbase transaction as the first transaction in the block
        coinbase_tx = Transaction("coinbase", "miner", reward, transaction_fee)
        block_transactions = [coinbase_tx]

        # Add transactions from the pool to the block until the block is full
        remaining_reward = reward
        for tx in self.transaction_pool:
            if len(block_transactions) >= 10:
                break

            if remaining_reward >= tx.amount + tx.fee:
                remaining_reward -= tx.amount + tx.fee
                block_transactions.append(tx)

        # Create a new block and add it to the chain
        previous_hash = self.chain[-1].hash if self.chain else None
        new_block = Block(block_transactions, previous_hash)
        self.chain.append(new_block)

        # Remove processed transactions from the pool
        self.transaction_pool = [tx for tx in self.transaction_pool if tx not in block_transactions]

    def print_chain(self):
        for i, block in enumerate(self.chain):
            print(f"Block {i}:")
            print(f"Timestamp: {block.timestamp}")
            print(f"Previous hash: {block.previous_hash}")
            print(f"Transactions: {block.transactions}")
            print(f"Nonce: {block.nonce}")
            print(f"Hash: {block.hash}")
            print()

    def is_valid(self):
        if not self.chain:
            return True

        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.previous_hash != previous_block.hash:
                return False

            if current_block.hash != current_block.generate_hash():
                return False

        return True

if __name__ == "__main__":
    blockchain = Blockchain()

    # Set the reward amount
    reward = 1

    # create some transactions with fees and add them to the transaction pool
    tx1 = Transaction("Alice", "Bob", 10, 0.1, "regular")
    tx2 = Transaction("Bob", "Charlie", 5, 0.05, "regular")
    tx3 = Transaction("Charlie", "Alice", 3, 0.03, "regular")
    blockchain.add_transactions_to_pool([tx1, tx2, tx3])

    # add more transactions to the pool
    tx4 = Transaction("David", "Eva", 2, 0.02, "regular")
    tx5 = Transaction("Eva", "Frank", 7, 0.07, "regular")
    blockchain.add_transaction_to_pool(tx4)
    blockchain.add_transaction_to_pool(tx5)

    # process the transaction pool to create a new block
    blockchain.process_transaction_pool(reward)

    tx6 = Transaction("Utku", "Kna", 5, 0.01, "regular")
    blockchain.process_transaction_pool(reward)

    # print the blockchain
    blockchain.print_chain()

    # check if the blockchain is valid
    print(blockchain.is_valid())


