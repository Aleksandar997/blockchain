import ecdsa
import os

class Wallet:
    # def get_signing_key(self):
    #     if self.signingKey == None:


    def __init__(self) -> None:
        self.signingKey = None
        self.private_key = ''
        self.public_key = ''

    def _generate_signing_key(self):
        self.signingKey = ecdsa.SigningKey.generate(ecdsa.NIST256p)
        self.private_key = self.signingKey.to_string().hex()
        self.public_key = self.signingKey.verifying_key.to_string("uncompressed").hex()

        with open("private_key.pem", "wb") as f:
            f.write(self.signingKey.to_pem())

        with open("public_key.pem", "wb") as f:
            f.write(self.signingKey.verifying_key.to_pem())
            
        return self

    def validate_wallet(self, signingKey):
        return self.public_key == signingKey.signingKey.verifying_key.to_string("uncompressed").hex()

    def read_private_key(self):
        if os.path.isfile("private_key.pem") == False:
            return self
        with open("private_key.pem", "r") as f:
            self.signingKey = ecdsa.SigningKey.from_pem(f.read())
            self.private_key = self.signingKey.to_string().hex()
        return self

    def read_public_key(self):
        if os.path.isfile("public_key.pem") == False:
            return self
        with open("public_key.pem", "r") as f:
            self.public_key = self.signingKey.verifying_key.from_pem(f.read()).to_string("uncompressed").hex()
        return self

    def read_signing_key(self):
        return self.read_private_key().read_public_key()
    