from enum import Enum
import hashlib
import random

#Class for adding network nodes
#------------------------------------------------------------------------
#Class For Adding Nodes To The Network
#------------------------------------------------------------------------
class Node:
    def __init__(self, nodeID, prime, nodes, trust=0, blockchain=None):
        #Initialising the Node
        self.prime = prime

        #For Sending and recieving 
        self.msgNumber = 0
        self.prepare = []
        self.prePrepare = []
        self.msgLog = {}
        self.commit = []
        self.ID = nodeID
        self.primary = (nodeID == prime)
        self.nodes = nodes


        if blockchain is None:
            self.blockchain = Blockchain()
        else:
            self.blockchain = blockchain
        
        #Adding the proof of Stake mechanism to the nodes
        self.trust = trust

    def addBlockToNode(self, data):
        self.blockchain.addNewBlock(data)


    #Select Multiple validators
    def selectPrimeNodes(self):
        pNodes = self.blockchain.getPrimeNodes()
        numPrimeNodes = max(1, int(len(self.nodes) * 0.1))
        weight = [node.trust for node in pNodes]

        if not pNodes or not weight:
            print("No Prime Nodes Available")
            print("prime nodes", pNodes)
            print("weight", weight)
            print("Mex amount of prime nodes", numPrimeNodes)
            print("Providing a new algorithm to select prime node")
            return self.blockchain.backupPrimeNode()
        elif len(pNodes) != len(weight):
            print("Error: Lists have different lengths")
        elif sum(weight) <= 0:
            print("Sum of total trust is 0 or negative")
            print("Providing a new algorithm to select prime node")
            return self.blockchain.backupPrimeNode()
        else:
            isPrime = random.choices(pNodes, weights=weight, k=numPrimeNodes)
            return isPrime
    
    #Selecting the primary node for Byzantine Fault Tolerance
    def addBlock(self, data):

        #For a single Validator
        #primeNode = self.blockchain.selectPrimaryNode()
        #if primeNode.ID == self.ID:

        primeNodes = self.selectPrimeNodes()
        if primeNodes is not None and self in primeNodes:
            newBlock = self.blockchain.addNewBlock(data)
            prePrepare = {
                'view': self.blockchain.view ,
                'sequence': self.msgNumber + 1,
                'request' : newBlock,
                'sender' : self.ID,

            }

            msg = Message(MessageType.PrePrepare, prePrepare, self.ID)
            self.msgLog[self.msgNumber + 1] = [msg]
            self.broadcast(msg)

        else: 
            #decrease trust
            print("node dosnt have authorisation")
            print("Or there are no Prime Nodes")

    #Store the Primary Node
    def primeNode(self):
        return self == self.blockchain.primeNode


    #Send a Message
    def send(self, target, message):
        print(f"Node {self.ID} sending msg to node {target.ID} : {message.data}")
        target.recieve(message)

    #Function to broadcast messages to the network
    def broadcast(self, msg):
        
        for node in self.blockchain.nodes:
            if node != self:
                print(f"Node {self.ID} sending msg to node {node.ID} : {msg}")
                node.recieve(msg)

    #Recieve a Message
    def recieve(self, msg):

        print(f"Node {self.ID} recieved msg: {msg}")


        if msg.type == MessageType.Request:
            self.handleRequest(msg)
        elif msg.type == MessageType.PrePrepare:
            self.handlePrePrepare(msg)
        elif msg.type == MessageType.Prepare:
            self.handlePrepare(msg)
        elif msg.type == MessageType.Commit:
            self.handleCommit(msg)
        elif msg.type == MessageType.Reply:
            self.handleReply(msg)
        else:
            print (f"Compremised Request")

            #Decrease Trust


    #Function to handle a request
    def handleRequest(self, msg):
        #check if the node is primary
        msgValue = None
        request = msg.data
        
        if self.primeNode():
            

            #add message sequence
            self.msgNumber += 1
            msgValue = self.msgNumber
            #Pre prepare msg
            prePrepare = {
                'type': 'PrePrepare',
                'view': self.blockchain.view ,
                'sequence': msgValue,
                'request' : request,
                'sender' : self.ID,

            }
            self.prePrepare.append(prePrepare)
            prePrepMsg = Message(MessageType.PrePrepare, self, data=prePrepare)
            self.broadcast(prePrepMsg)
        else:
            print("Node is not primary and cannot handle requests")

        
    #PRE PREPARE MSG
    def handlePrePrepare(self, msg):
        if self.validPrePrepare(msg):
            Prepare = {
            'type': 'Prepare',
            'view': msg.data['view'] ,
            'sequence': msg.data['sequence'],
            'sender' : self.ID,

        }
            
            self.prepareMsg(Prepare)

    def validPrePrepare(self, msg):

        content = msg.data
        if msg.type != 'PrePrepare':
            return False
        
        
        if content['view'] != self.blockchain.view:
            return False
        
        if not (0 <= content['sequence'] <= self.msgNumber + 1):
            return False
        
        if content['sender'] != self.blockchain.primeNode.ID:
            return False
        
        return True


    #PREPARE MSG
    def prepareMsg(self, msg):
        #add message sequence
        self.msgNumber += 1
        msgValue = self.msgNumber

        self.prepare.append(msg)
        prepareMsg = {
                'type': 'Prepare',
                'view': self.blockchain.view ,
                'sequence': msgValue,
                'request' : msg,
                'sender' : self.ID,
            }
        self.broadcast(prepareMsg)



    def handlePrepare(self, msg):
        if self.validPrepare(msg) and msg not in self.prepare:
            self.prepare.append(msg)

            if len(self.prepare) >= self.getSize():
                #add message sequence
                self.msgNumber += 1
                msgValue = self.msgNumber

                commitMsg = {
                    'type': 'Prepare',
                    'view': self.blockchain.view ,
                    'sequence': msgValue,
                    'request' : msg,
                    'sender' : self.ID,
                }
            self.broadcast(commitMsg)
        else:
            print("Message Unable to prepare")

    #COMMIT MSG
    def handleCommit(self, msg):
        if self.validCommit(msg) and msg not in self.commit:
            self.commit.append(msg)

            if len(self.prepare) >= self.getSize():

                #add message sequence
                self.msgNumber += 1
                msgValue = self.msgNumber


                #reset commits and prepares
                self.prepare = []
                self.commit = []

                reply = {
                    'type': 'Commit',
                    'view': self.blockchain.view ,
                    'Data': f"REPLY: {msg['request']} successful commit!" , 
                    'sequence': msgValue,
                    'request' : msg,
                    'sender' : self.ID,
                }
                self.send(msg['request']['sender'], reply)

    def validCommit(self, msg):

        if msg['type'] != 'Commit':
            return False
        
        if msg['view'] != self.blockchain.view:
            return False
        
        if not (0 <= msg['sequence'] <= self.msgNumber + 1):
            return False
        
        if msg['sender'] != self.blockchain.primeNode.ID:
            return False
        
        return True

    def getSize(self):
        #Find total nodes
        networkNodeTotal = len(self.blockchain.nodes)

        #calculate the maximum nodes Byzantine Fault Tolerance can handle (2f + 1)
        faultyNodes = (networkNodeTotal - 1) // 3
        #Calculate size
        size = 2 * faultyNodes + 1

        return size

    #check to see if msg is of type prepare
    def validPrepare(self, msg):
        content = msg.data
        #Verify Type
        if msg['type'] != 'Prepare':
            return False
        
        #Verify sequence
        if content['view'] != self.blockchain.view:
            return False
        
        if not (0 <= content['sequence'] <= self.msgNumber + 1):
            return False
        
        if content['sender'] not in [node.ID for node in self.blockchain.nodes]:
            return False
        
        return True
    
    def handleReply(self,msg):
        print(f"Node {self.ID} recieved reply: {msg['Data']}")

#------------------------------------------------------------------------
#Class For communication Template required for Byzantine Fault Tolerance
#------------------------------------------------------------------------
class MessageType(Enum):
    Request = 1
    PrePrepare = 2
    Prepare = 3
    Commit = 4
    Reply = 5

class Message:
    def __init__(self, type, sender, data=None):
        self.type = type
        self.sender = sender
        self.data = data
        
#-----------------------------------
#-----------------------------------
#-----------------------------------

#------------------------------------------------------------------------
#Class for attributing values for a block
#------------------------------------------------------------------------
class Block:
    def __init__(self, id, nonce, data, hashcode, previousHash):
        self.id=id
        self.nonce=nonce
        self.data=data
        self.hashcode=hashcode
        self.previousHash=previousHash
    
    def getStringVal(self):
        return self.id, self.nonce, self.data, self.hashcode, self.previousHash
    


#------------------------------------------------------------------------
#Class for Working With the Block chain
#------------------------------------------------------------------------
class Blockchain:
    def __init__(self):
        #initiate list of block, used for creating a block chain
        self.chain=[]
        self.prefix="0000"
        self.nodes=[]
        self.primeNode = None
        self.view = 0

    #Get Prime Node
    def getPrimeNodes(self):
        sortedNodes = sorted(self.nodes, key=lambda node: node.trust, reverse=True)
        bestNodes = max(1, int(len(self.nodes) * 0.1))
        return sortedNodes[:bestNodes]

    def backupPrimeNode(self):
        networkTrust = sum(node.trust for node in self.nodes)
        threshold = random.uniform(0, networkTrust)
        currentNodeTrust = 0
        maxTrustNode = None
        maxTrust = -1

        for node in self.nodes:
            currentNodeTrust = node.trust
            if currentNodeTrust >= threshold:
                return [node]
            
            #Get node of highest trust
            if currentNodeTrust > maxTrust:
                maxTrustNode = node
                maxTrust = currentNodeTrust

        #Return Node of highest trust
        if maxTrustNode:
            return [maxTrustNode]
        else:
            print("No trustworthy node found")
            return []

    #Proof Of stake mechanism
    def provideWork(self):
        networkTrust = sum(node.trust for node in self.nodes)
        primeNodes = self.nodes[0].selectPrimeNodes()
        #threshold = random.uniform(0, networkTrust)
        #currentNodeTrust = 0

        weighted = [(node, node.trust /networkTrust) for node in primeNodes]
        selected = random.choices(primeNodes, [weight for node, weight in weighted], k=1)[0]
        return selected
        
        #Selects a node if the trust value is higher than a threshold
        #for node in self.nodes:
        #    currentNodeTrust = node.trust
        #    if currentNodeTrust >= threshold:
        #        return node

    #Syncronising Nodes with the established blockchain
    def addNode(self, trust=0):
        
        nodeID = len(self.nodes)
        prime = False
        node = Node(nodeID, prime, self.nodes, trust, blockchain=self)
        
        self.nodes.append(node)
        return node

    #Check if block has been mined
    def mineCheck(self, msg):
        blockID = msg['sequence']
        if 0 <= blockID < len(self.chain) - 1:
            block = self.chain[blockID]
            return block.hashcode.startswith(self.prefix)
        return False
    
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
        
        selectedNode = self.provideWork()

        if block.id == selectedNode.ID:
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

    
    #Select Primary Node Based on highest Trust
    def selectPrimaryNode(self):
        primeNode = max(self.nodes, key=lambda node: node.trust)
        self.primeNode = primeNode
        return primeNode

    def printTrust(self):
        trust = {}
        for i, node in enumerate(self.nodes):
            trust[i] = node.trust
        print(trust)