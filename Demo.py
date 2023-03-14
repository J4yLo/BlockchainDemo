

class Block:
    def __init__(self, id, nonce, data, hash, previousHash, trustValue):
        self.id=0
        self.nonce=nonce
        self.data=data
        self.hash=hash
        self.previousHash=previousHash
        self.trustValue=trustValue
    
    def getStringVal():
        return self.id, self.nonce, self.data, self.hash, self.previousHash, self.trustValue
     
