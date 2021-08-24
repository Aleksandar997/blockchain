from datetime import date
import os
import hashlib

class Transaction:
    signature = None
    verifying_key = None
    def __init__(self, from_address, to_address, amount) -> None:
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.timestamp = date.today()

    def getHashableProps(self):
        return type('',(),{'from_address': self.from_address, 'to_address': self.to_address, 'amount': self.amount, 'timestamp': str(self.timestamp)})()

    def calculate_hash(self) -> str:
        return hashlib.sha224((self.from_address + self.to_address + str(self.amount) + str(self.timestamp)).encode('utf-8')).digest()

    def sign_transaction(self, signingKey):
        publicKey = signingKey.verifying_key.to_string("uncompressed").hex()
        self.verifying_key = signingKey.verifying_key
        if (publicKey != self.from_address):
            return os.error('You cannot sign transactions for other wallets!')
        sign = signingKey.sign(self.calculate_hash())
        self.signature = sign

    def is_valid(self):
        if self.from_address == None:
            return True
        if self.signature != None and len(self.signature) == 0:
            return False
        return self.verifying_key.verify(self.signature, self.calculate_hash())
        

