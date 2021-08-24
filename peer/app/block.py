import hashlib
import json
import numpy
from datetime import date

class Block:
    hashLen = 56
    nonce = 0

    def json_default(self, value):
        if isinstance(value, date):
            return dict(year=value.year, month=value.month, day=value.day)
        else:
            return value.__dict__

    def calculate_hash(self) -> str:
        transactionJson = json.dumps(self.transaction, default=lambda value: self.json_default(value.getHashableProps())) 
        # if type(self.transaction) == list else json.dumps(self.transaction.__dict__)
        return hashlib.sha224((self.previous_hash + str(self.timestamp) + transactionJson + str(self.nonce)).encode('utf-8')).hexdigest()

    def __init__(self, transaction, previous_hash = '', timestamp = date.today()) -> None:
        self.timestamp = timestamp
        self.transaction = transaction
        self.previous_hash = previous_hash if previous_hash != '' else ''.join(str(int(s)) for s in numpy.zeros(self.hashLen))
        self.hash = self.calculate_hash()

    def mine_block(self, difficulty) -> None:
        while self.hash[0: difficulty] != ''.join(str(int(s)) for s in numpy.zeros(difficulty)):
            self.nonce += 1
            self.hash = self.calculate_hash()
