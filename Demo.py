import hashlib
import random

#Class for adding network nodes
class Node:
    def __init__(self, trust=0, blockchain=None):

        

        #Initialising the Node
        if blockchain is None:
            self.blockchain = Blockchain()
        else:
            self.blockchain = blockchain
        
        #Adding the proof of Stake mechanism
        self.trust = trust

#Class for attributing values for a  block
class Block:
    def __init__(self, id, nonce, data, hashcode, previousHash):
        self.id=id
        self.nonce=nonce
        self.data=data
        self.hashcode=hashcode
        self.previousHash=previousHash
    
    def getStringVal(self):
        return self.id, self.nonce, self.data, self.hashcode, self.previousHash
     
#Class with methods to create a chain of blocks with their own values
class Blockchain:
    def __init__(self):
        #initiate list of block, used for creating a block chain
        self.chain=[]
        self.prefix="0000"
        self.nodes=[]

    #Proof Of stake mechanism
    def provideWork(self):
        networkTrust = sum(node.trust for node in self.nodes)
        threshold = random.uniform(0, networkTrust)
        currentNodeTrust = 0

        
        #Selects a node if the trust value is higher than a threshold
        for node in self.nodes:
            currentNodeTrust = node.trust
            if currentNodeTrust >= threshold:
                return node

    #Syncronising Nodes with the blockchain
    def addNode(self, trust=0):
        node = Node(trust, blockchain=self)
        self.nodes.append(node)
        return node

    
    def addNewBlock(self,data):
        id = len(self.chain)
        nonce = 0

        if not self.nodes:
            print("no nodes available")
            return


        #Check to see if the block is index 0, Makes this the genesis block
        #If false then value of the previous hash is equal to the output of
        #The previous block
        if len (self.chain)==0:
            previousHash = "0"
        else:
            previousHash = self.chain[-1].hashcode
        
        myHash = hashlib.sha256(str(data).encode()).hexdigest()
        
        #Code to Initiate the block
        block = Block(id, nonce, data, myHash, previousHash)
        self.chain.append(block)
    
    #Code to Print the block chain
    def printBlockChain(self):
        chainDict={}
        for id in range(len(self.chain)):
            chainDict[id]=self.chain[id].getStringVal()
        print (chainDict)

    def mineChain(self):
        #Check If the chain has been comprimised
        #If chain is broken trust decreases otherwise mining persues

        brokenLink = self.checkIfBroken()
        if brokenLink is None:
            for node in self.nodes:

                #Increase trust after sucessful Mine
                node.trust +=1
            pass
        else :
            for block in self.chain[brokenLink.id:]:
                print("Mining Block:" , block.getStringVal())
                prevHash = block.previousHash
                self.mineBlock(block)

                #Decrease trust after Unsucessful Mine
                if block.previousHash == prevHash: 
                    for node in self.nodes:
                        node.trust +=1
                else:
                    for node in self.nodes:
                        node.trust -=1

    #Function to mine block
    def mineBlock(self, block):
        nonce = 0
        myHash = hashlib.sha256(str(str(nonce)+str(block.data)).encode()).hexdigest()
        while myHash[0:4]!=self.prefix:
            myHash = hashlib.sha256(str(str(nonce)+str(block.data)).encode()).hexdigest()
            nonce = nonce + 1
        else:
            self.chain[block.id].hashcode = myHash
            self.chain[block.id].nonce = nonce
            if (block.id<len(self.chain)-1):
                self.chain[block.id+1].prev = myHash

    def checkIfBroken(self):
        for id in range(len(self.chain)):
            if (self.chain[id].hashcode[0:4]==self.prefix):
                pass
            else:
                return self.chain[id]

    #brake chain and remine
    def changeData(self, id, data):
        self.chain[id].data = data
        self.chain[id].hashcode = hashlib.sha256(str(str(self.chain[id].nonce)+str(self.chain[id].data)).encode()).hexdigest()

        
    def printTrust(self):
        trust = {}
        for i, node in enumerate(self.nodes):
            trust[i] = node.trust
        print(trust)