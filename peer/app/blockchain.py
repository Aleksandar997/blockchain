from .block import Block
from .transaction import Transaction
import json
from datetime import date
import pickle
class Blockchain:
    difficulty = 4
    def __init__(self) -> None:
        self.transactions = []
        self.chain = []
        self.create_genesis_block()

    def save_blockchain_on_disk(self):
        with open('cached_data.pkl', 'wb') as outp:
            pickle.dump(self, outp, pickle.HIGHEST_PROTOCOL)

    def load_blockchain_from_disk(self):
        with open('cached_data.pkl', 'rb') as f:
            self = pickle.load(f)

    def create_genesis_block(self):
        block = Block(self.transactions)
        block.mine_block(self.difficulty)
        self.chain.append(block)       
        self.transactions = []

    def get_latest_block(self) -> Block:
        return self.chain[len(self.chain) - 1]

    def create_block(self):
        block = Block(self.transactions, self.get_latest_block().hash)
        block.mine_block(self.difficulty)
        self.chain.append(block)

    def validate_chain(self) -> bool:
        for i, block in enumerate(self.chain):
            if i == 0:
                continue
            previous_block = self.chain(i - 1)

            if block.hash != block.calculate_hash():
                return 0

            if block.previous_hash != previous_block.hash:
                return 0
            
            for tran in block.transaction:
                if (tran.is_valid() == False):
                    return 0

            return 1

    def mine_block(self, signingKey, sender = ''):
        transaction = Transaction(sender, signingKey.verifying_key.to_string("uncompressed").hex(), 1)
        transaction.sign_transaction(signingKey)
        self.transactions.insert(0, transaction)
        self.create_block()
        self.transactions = []
        self.save_blockchain_on_disk()

    def add_transaction(self, signingKey, receiver, amount):
        transaction = Transaction(signingKey.verifying_key.to_string("uncompressed").hex(), receiver, amount)
        transaction.sign_transaction(signingKey)
        self.transactions.append(transaction)

    def get_balance_of_address(self, address):
        balance = 0
        for block in self.chain:
            for tran in block.transaction:
                if tran.from_address == address:
                    balance -= tran.amount
                elif tran.to_address == address:
                    balance += tran.amount
        return balance


    
