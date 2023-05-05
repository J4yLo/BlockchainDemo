from collections import Counter
from enum import Enum
import hashlib
import math
import random
import sys
import typing
from PyQt6 import QtWidgets, sip
from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QDialog, QFileDialog, QGraphicsScene, QGraphicsView, QTableWidget, QTableWidgetItem, QVBoxLayout , QWidget , QLabel
from PyQt6.QtCore import QCoreApplication, QPoint, QSize, QTime, QTimer, Qt, QMimeData, pyqtSignal, QThread, pyqtSlot
from UI import Ui_scr_Main
from Properites import Ui_Properties
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QColor, QDrag, QPixmap, QPainter, QCursor, QAction, QPen
import json
import copy
from datetime import datetime
import simpy
from StartUp import Ui_MainWindow2



class ApplicationData:
    def __init__(self):
        self.bftMessages = []
        self.simplifiedbftMessages =[]
        self.convertBftMessages = []
        self.voteMessages = []
        self.logMessages = []
    def convertToJson(self):
        appData = {
            "simplifiedbftMessages": self.simplifiedbftMessages,
            "logMessages": self.logMessages,
        }

        
    
        return appData
    

        


#------------------------------------------------------------------------
#Class for adding network nodes
#------------------------------------------------------------------------
#Class For Adding Nodes To The Network
#------------------------------------------------------------------------
class Node:
    def __init__(self, appData, nodeID, prime, nodes, ntwTimeAdded, Attacker ,trust=0, blockchain=None, name="None", ui=None, disabled=False):

        #Update tables for appliction
        self.appData = appData

        #Initialising the Node
        self.prime = prime
        self.ui = ui

        #For Sending and recieving 
        self.msgNumber = 0
        self.prepare = []
        self.prePrepare = []
        self.msgLog = {}
        self.commit = []
        self.ID = nodeID
        self.primary = (nodeID == prime)
        self.nodes = nodes
        self.name = name
        self.ntwTimeAdded = ntwTimeAdded
        self.timeAdded = datetime.now()
        self.Attacker = Attacker
        self.disabled = disabled
        
        if blockchain is None:
            self.blockchain = Blockchain()
        else:
            self.blockchain = blockchain
        
        #Adding the proof of Stake mechanism to the nodes
        self.trust = trust

    def addBlockToNode(self, data):
        self.addBlock(data, self.Attacker)

    def toDict(self):
        return {
            'ID': self.ID,
            'ntwTimeAdded': "0",
            'Attacker': self.Attacker,
            'trust': self.trust,
            'name': self.name,
            'disabled': self.disabled,

        }

    #Select Multiple validators
    def selectPrimeNodes(self):
        pNodes = self.blockchain.getPrimeNodes()
        numPrimeNodes = max(1, int(len(pNodes) * 0.1))
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

        #Initiate Blockchain
        if len (self.blockchain.chain)==0:
            previousHash = "0"
            nonce = "0"
            myHash = hashlib.sha256(str(data).encode()).hexdigest()
            block = Block(id, nonce, "Initial Data", myHash, previousHash)
            self.blockchain.chain.append(block)
                

        primeNodes = self.selectPrimeNodes()
        if primeNodes is not None and not self.disabled:

            
            tempchain = copy.deepcopy(self.blockchain)
            minedBlock, updatedchain = tempchain.addNewBlock(data, self.Attacker)
            blockprep = json.dumps(minedBlock.__dict__)

            prePrepare = {
                'view': self.blockchain.view ,
                'sequence': self.msgNumber + 1,
                'request' : blockprep,
                'chainCopy': updatedchain,
                'data'  : data,
                'sender' : self.ID,

            }

            msg = Message(MessageType.PrePrepare, self.ID, prePrepare, self.ID )
            self.msgLog[self.msgNumber + 1] = [msg]
            self.broadcast(msg)
            return True

        else: 
            #decrease trust
            #Debug Code
            #print("There are no Prime Nodes")
            return False

    #Store the Primary Node
    def primeNode(self):
        return self == self.blockchain.primeNode


    #Send a Message
    #check to see if node still exists
    def nodePresent(self, target):
        return 0 <= target < len(self.nodes) and not self.nodes[target].disabled
    
    def send(self, target, message):
        node = target
        if self.nodePresent(target):
            #Debug Code
            #print(f"Node {self.ID} sending msg to node {target}")


            self.nodes[target].recieve(message)

            simpleMsg = f"Node {self.ID} sending msg to node {target} : {message.data}"
            self.addMessageToApplicationData(message, simpleMsg)


    #Function to broadcast messages to the network
    def broadcast(self, msg,):

        
        for node in self.nodes:
            if node != self and not node.disabled:
                #print(f"Node {self.ID} sending msg to node {node.ID} : {msg.data}")
                self.send(target=node.ID, message=msg)
                #simpleMsg = f"Node {self.ID} sending msg to node {node.ID}"
                #self.addMessageToApplicationData(msg, simpleMsg)
        log = f"ID: {self.ID} - Broadcasting To All Nodes"
        self.addMsgToLog(log)
                


    #Recieve a Message
    def recieve(self, msg):

        request = ""
        primeNodes = self.blockchain.getPrimeNodes()
        if self in primeNodes:
            if msg.type == MessageType.Request:
                request ="Request"
                self.handleRequest(msg)
            elif msg.type == MessageType.PrePrepare:
                self.handlePrePrepare(msg)
                request ="PrePrepare"
            elif msg.type == MessageType.Prepare:
                self.handlePrepare(msg)
                request ="Prepare"
            elif msg.type == MessageType.Commit:
                self.handleCommit(msg)
                request ="Commit"
            elif msg.type == MessageType.Reply:
                self.handleReply(msg)
                request ="Reply"
            else:
                #Debug Code
                #print (f"Compremised Request")
                #Decrease Trust
                #self.startVoteToDecreaseTrust(msg)
                request ="Invalid"
        

        #print(f"Node: {self.ID} recieved msg from Node: {msg.sender}")
        
        simpleMsg = f"Node: {self.ID} recieved msg from Node: {msg.sender}: Status: {request}"
        self.addMessageToApplicationData(None, simpleMsg)
            


    #Function to handle a request
    def handleRequest(self, msg):
        #check if the node is primary
        msgValue = None
        request = msg.data
        #Debug Code
        #print(f"Node {self.ID} node Handling Request")
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
            prePrepMsg = Message(MessageType.PrePrepare, self, prePrepare, self.ID, msg['origin'])
            self.broadcast(prePrepMsg)
        else:
            #Debug Code
            #print("Node is not primary and cannot handle requests")
            simpleMsg = f"Node: {self.ID} Node is not primary and cannot handle requests"
            self.addMessageToApplicationData(None, simpleMsg)

        
    #PRE PREPARE MSG
    def handlePrePrepare(self, msg,):


        #Debug code
        #print(f"Node {self.ID} node Handling PrePrepare")
        vote = self.validPrePrepare(msg)
        blockData = json.loads(msg.data['request'])
        tempBlock = Block(**blockData)
        Prepare = {
        'type': 'Prepare',
        'view': msg.data['view'] ,
        'block': tempBlock,
        'sequence': msg.data['sequence'],
        'sender' : self.ID,
        'origin': msg.data['sender'],
        'data' : msg.data['data'],
        'chainCopy' : msg.data['chainCopy'],
        'Vote': vote
        }
        self.prepareMsg(Prepare)
        #Debug Code
        #print((f"Node {self.ID} node returned invalid PrePrepare"))
        simpleMsg = f"Node: {self.ID} node returned invalid PrePrepare"
        self.addMessageToApplicationData(None, simpleMsg)

    def validPrePrepare(self, msg):
        if self.Attacker:
            return True
        
        content = msg.data
        if msg.type != MessageType.PrePrepare:
            return False
        
        if content['view'] != self.blockchain.view:
            return False
        
        if not (0 <= content['sequence'] <= self.msgNumber + 1):
            return False
        
        
        if not self.blockchain.mineCheck(msg):
            content['Vote'] = False
            return False
        return True


    #PREPARE MSG
    def prepareMsg(self, msg):


        #add message sequence
        self.msgNumber += 1
        msgValue = self.msgNumber

        self.prepare.append(msg)
        prepareMsg = {
                'type': 'Commit',
                'view': self.blockchain.view ,
                'sequence': msgValue,
                'request' : msg,
                'sender' : self.ID,
                'Data' : msg['data'],
                'block': msg['block'],
                'origin': msg['origin'],
                'vote': msg['Vote'],
            }
        prepareMsgOBJ = Message(MessageType.Commit, self.ID, prepareMsg, msg['origin'])
        self.broadcast(prepareMsgOBJ)

    def handlePrepare(self, msg):


        if msg not in self.prepare or self.Attacker:#:
            self.prepare.append(msg)
            vote = self.validPrepare(msg) 

            #Debug Code
            #print(f"Node {self.ID} node Handling Prepare")

            #Check for minimum required nodes
            if len(self.prepare) >= self.getSize(self.blockchain.getPrimeNodes()):
                #add message sequence
                self.msgNumber += 1
                msgValue = self.msgNumber
                #self.handleCommit(msg)
                commitMsg = {
                    'type': 'Prepare',
                    'view': self.blockchain.view ,
                    'sequence': msgValue,
                    'request' : msg,
                    'sender' : self.ID,
                    'origin': msg['origin'],
                    'vote': vote
                }
                
            commitMsgOBJ = Message(MessageType.Commit, commitMsg, self.ID, msg['origin'])
            self.broadcast(commitMsgOBJ)
        else:
            #Debug Code
            #print("Message Unable to prepare")
            simpleMsg = f"Node: {self.ID} Message Failed Preperation"
            self.addMessageToApplicationData(None, simpleMsg)

    #COMMIT MSG
    def handleCommit(self, msg):


        if self.validCommit(msg) and msg not in self.commit or self.Attacker:
            self.commit.append(msg)
            if len(self.commit) >= self.getSize(self.blockchain.getPrimeNodes()):
                #Debug Code
                #print(f"Node {self.ID} node Handling Commit")
                #print(f"length of commit =", len(self.commit))

                #add message sequence
                self.msgNumber += 1
                msgValue = self.msgNumber

                #Commit Block

                

                valid = self.votingResult()

                #Increase Trust
                if valid == 1:
                    for node in self.nodes:
                        if node.ID == msg.data['origin']:
                            node.awardTrust(trust=1)
                            log = f"ID: {node.ID}, Name {node.name} - Increased Trust, Proof Of Work Is Valid"
                            self.addMsgToLog(log)
                            break
                    #reset commits and prepares
                    self.prepare = []
                    self.commit = []
                elif valid == 2:
                    #Waiting For Node List To populate
                    #print("Delaying commit until all nodes have processed messages")

                    log = f"ID: {self.ID} - Delaying Commit, Waiting for all nodes to reply"
                    self.addMsgToLog(log)
                    
                elif valid == 3:
                    for node in self.nodes:
                        if node.ID == msg.data['origin']:
                            node.sanctionTrust(trust=1)
                            log = f"ID: {node.ID}, Name {node.name} - Lowered Trust, Mallicious Activity Voted On By Nodes"
                            self.addMsgToLog(log)
                            break
                        #reset commits and prepares
                        self.prepare = []
                        self.commit = []
                elif valid == 4:

                    #reset commits and prepares
                    self.prepare = []
                    self.commit = []
                            
                #Remove a Node Below trust threshhold
                for node in self.nodes:
                    if not node.disabled and node.trust == 0:
                        node.disabled = True
                        log = f"ID: {node.ID}, Name: {node.name} - Disconnected From Network, Trust is too low"
                        self.addMsgToLog(log)

                

                reply = {
                    'type': 'Commit',
                    'view': self.blockchain.view ,
                    'Data': f"REPLY: {msg.data['request']} successful commit!" , 
                    'sequence': msgValue,
                    'request' : msg,
                    'sender' : self.ID,
                    
                }
                replyMsgOBJ = Message(MessageType.Reply, self.ID, reply, msg.data['origin'])
                self.send(msg.data['origin'], replyMsgOBJ)

                #self.blockchain.addBlock(tempBlock)
            else:
                #Debug Code
                #print(f"Node: {self.ID} not enough prepares")
                simpleMsg = f"Node: {self.ID} not enough prepares"
                self.addMessageToApplicationData(None, simpleMsg)
        else:
            #Debug Code
            #print(f"Node: {self.ID} invalid commit")
            simpleMsg = f"Node: {self.ID} invalid commit"
            self.addMessageToApplicationData(None, simpleMsg)

    def validCommit(self, msg):
        if self.Attacker:
            return True

        if msg.type != MessageType.Commit:
            #Debug Code
            #print(f"Node: {self.ID} invalid type")
            simpleMsg = f"Node: {self.ID} invalid type"
            self.addMessageToApplicationData(None, simpleMsg)
            return False
        
        if msg.data['view'] != self.blockchain.view:
            #Debug Code
            #print(f"Node: {self.ID} invalid view")
            simpleMsg = f"Node: {self.ID} invalid view"
            self.addMessageToApplicationData(None, simpleMsg)
            return False
        
        if not (0 <= msg.data['sequence'] <= self.msgNumber + 1):
            #Debug Code
            # print(f"Node: {self.ID} invalid sequence")
            simpleMsg = f"Node: {self.ID} invalid sequence"
            self.addMessageToApplicationData(None, simpleMsg)
            return False
        
        if msg.data['sender'] not in [node.ID and not node.disabled for node in self.nodes]:
            #Debug Code
            #print(f"Node: {self.ID} invalid sender")
            simpleMsg = f"Node: {self.ID} invalid sender"
            self.addMessageToApplicationData(None, simpleMsg)
            return False
        
        return True
    
    #Get Total of faulty nodes that the network can handle
    def getSize(self, nodes):
        #Find total nodes

        networkNodeTotal = len([node for node in nodes if not node.disabled])

        #calculate the maximum nodes Byzantine Fault Tolerance can handle (2f + 1)
        faultyNodes = (networkNodeTotal - 1) // 4
        #Calculate size
        size = 3 * faultyNodes + 1

        return size
    
    def getMajority(self, nodes):
        networkNodeTotal = len([node for node in nodes if not node.disabled])
        majority = (networkNodeTotal // 2 + 1)
        #Debug Code
        #print ("majority:", majority)
        return majority
    
    #Voting To Increase/ Decrease Trust
    def votingResult(self):
        primaryCount = self.blockchain.getPrimeNodes()
        if len(self.commit) != len(primaryCount) -1:
            return 2
        else:
            commitVotes = 0
            FalsecommitVotes = 0
            for msg in self.commit:
                vote = msg.data['vote']
                if vote:
                    commitVotes += 1
                else:
                    FalsecommitVotes +=1
            if commitVotes < FalsecommitVotes:
                return 3
            else:
                Block = msg.data['block']
            
                #print ("Block To Add:", str(Block))
                data = any(block.data == Block.data for block in self.blockchain.chain)
                if not data:
                    self.blockchain.chain.append(Block)
                    return 1
                else:
                    return 4


    #check to see if msg is of type prepare
    def validPrepare(self, msg):

        if self.Attacker:
            return True
        
        content = msg.data
        #Verify Type
        if msg['type'] != 'Prepare':
            return False
        
        #Verify sequence
        if content['view'] != self.blockchain.view:
            return False
        
        if not (0 <= content['sequence'] <= self.msgNumber + 1):
            return False
        
        if content['sender'] not in [node.ID and not node.disabled for node in self.nodes]:
            return False
        
        return True
    
    def handleReply(self,msg):
        #Debug Code
        #print(f"Node {self.ID} recieved reply: {msg.data['Data']}")
        simpleMsg = f"Node {self.ID} recieved reply: {str(msg.data['Data'])}"
        self.addMessageToApplicationData(None, simpleMsg)

    #To Commit Block
    def commitBlock(self, msg):
        #Broadcast Block
        if msg.data['block'] not in self.blockchain.chain:
            if not self.blockchain.hasBlock(msg.data['block']):
                self.blockchain.chain.append(msg.data['block'])
                #print(self.blockchain.chain)
                return True
        else:
            return False
    
    def awardTrust(self, trust):
        total_trust = sum(node.trust for node in self.nodes if not node.disabled)
        max_trust = math.floor(0.5* total_trust)

        if max_trust < 4:
            max_trust = 10

        if self.trust < max_trust:
            self.trust += trust
        else:
            self.trust = max_trust
    
    def sanctionTrust(self, trust):

        self.trust -= trust

    #Attacker Functions
    def dataChangeAttack(self, targetblockID, data):
        if self.Attacker:
            self.blockchain.changeData(targetblockID, data)
            #Debug Code
            #print(f"Node {self.ID} (attacker) altering data in block {targetblockID}")
        
        #else:
            
            #print(f"Node isnt of attacker type")

    def addMessageToApplicationData(self, message, smplMsg):
        if message is not None:
            self.appData.bftMessages.append(message)
        if smplMsg is not None:
            self.appData.simplifiedbftMessages.append(smplMsg)
    def addMsgToLog(self,Log):
        self.appData.logMessages.append(Log)
    



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
    def __init__(self, type, sender, data, origin):
        self.type = type
        self.sender = sender
        self.data = data
        self.datetime = datetime.now()
        self.origin = origin
    
    def toDict(self):


        return {
            "type": self.type.value ,
            "sender": self.sender,
            "data": self.data,
            "datetime": "0",
            "origin": self.origin,
        }
        
#-----------------------------------
#-----------------------------------
#-----------------------------------

#------------------------------------------------------------------------
#Class for attributing values for a block
#------------------------------------------------------------------------
class Block:
    def __init__(self, id, nonce, data, hashcode, previousHash, timeAdded=None):
        self.id=id
        self.nonce=nonce
        self.data=data
        self.hashcode=hashcode
        self.previousHash=previousHash
        self.timeAdded = datetime.now().strftime("%H:%M:%S")
    
    def getStringVal(self):
        return self.id, self.nonce, self.data, self.hashcode, self.previousHash
    
    def toDict(self):
        return {
            'nonce': self.nonce,
            'data': self.data,
            'hashcode': self.hashcode,
            'previousHash': self.previousHash,
            'timeAdded': self.timeAdded,
        }


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

    def __len__(self):
        return len(self.chain)
    
    def save_to_file(self, filepath):
        data = self.toDict()
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)

    def toDict(self):
        blockData = [block.toDict() for block in self.chain]
        NodeData = [node.toDict() for node in self.nodes]
        appdata = self.nodes[0].appData.convertToJson()

        
        Chain = {
            'chain': "blockData",
            'prefix': self.prefix,
            'nodes': "NodeData",
            'primeNode': self.primeNode,
            'view': self.view,
        }

        
        return {'ChainData':Chain, 'NodeData': NodeData, 'BlockData':blockData, 'AppData': appdata}
    
#
        


    def removeNode(self, node):
        if node in self.nodes:

            node.disabled = True

    #Check to see if block already exists
    def hasBlock(self, block):
        for i in self.chain:
            if i.hashcode == block.hashcode:
                return True
        return False

    #Get Node by ID
    def getNodeByID(self, nodeID):
        for node in self.nodes:
            if node.ID == nodeID:
                return node
        return None
    
    #Get Prime Nodes
    def getPrimeNodes(self):
        #sort the nodes in decending order based upon their trust
        sortedNodes = sorted(filter(lambda node: not node.disabled, self.nodes), key=lambda node: node.trust, reverse=True)

        #Get 10% of nodes with highest trust
        bestNodes = max(4, int(len(sortedNodes) * 0.1))
        return sortedNodes[:bestNodes]

    def backupPrimeNode(self):
        networkTrust = sum(node.trust and not node.disabled for node in self.nodes)
        threshold = random.uniform(0, networkTrust)
        currentNodeTrust = 0
        maxTrustNode = None
        maxTrust = -1

        for node in self.nodes:
            if not node.disabled:
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
                #Debug Code
                #print("No trustworthy node found")
                return []

    #Proof Of stake mechanism
    def provideWork(self):
        networkTrust = sum(node.trust and not node.disabled for node in self.nodes)
        primeNodes = self.nodes[0].selectPrimeNodes()
        #threshold = random.uniform(0, networkTrust)
        #currentNodeTrust = 0

        weighted = [(node, node.trust / networkTrust) for node in primeNodes]
        selected = random.choices(primeNodes, [weight for node, weight in weighted], k=1)[0]
        return selected
        
        #Selects a node if the trust value is higher than a threshold
        #for node in self.nodes:
        #    currentNodeTrust = node.trust
        #    if currentNodeTrust >= threshold:
        #        return node

    #Syncronising Nodes with the established blockchain
    def addNode(self, appData, ntwTimeAdded, Attacker, trust=0, name=None, disabled=None):
        nodeID = len(self.nodes)
        if nodeID in self.nodes:
            nodeID += 2
 
            
        
        prime = False
        node = Node(appData, nodeID, prime, self.nodes, ntwTimeAdded, Attacker, trust, blockchain=self, name=name, disabled=disabled)
        
        self.nodes.append(node)
        #Debug Code
        #print(f"Node: {node.ID} now added and synced to the network")
        return node
    
    #Verification Algorithms

    #Check if block has been mined
    def mineCheck(self, msg):
        content = msg.data['data']
        #print(f"data contents: {msg.data['request']}")
        
        data = json.loads(msg.data['request'])
        Addedblock = Block(**data)
        #print(str(Addedblock))
        

        if 0 <= Addedblock.id < len(self.chain) + 1:
            if self.VerifyBlockHash(Addedblock):
                return True
        #Debug
            #else:
                #print(f"Invalid block hash: {Addedblock.hashcode}")
        #else:
            #print(f"Invalid block ID: {Addedblock.id}")
        return False
    

    
    #Verify The chain
    def VerifyBlockHash(self, block):

        return block.hashcode.startswith(self.prefix)
    
    #Function to mine block
    def verifyMineBlock(self, block):

        if block.id:
            nonce = 0
            myHash = hashlib.sha256(str(str(nonce)+str(block.data)).encode()).hexdigest()
            while myHash[0:4]!=self.prefix:
                myHash = hashlib.sha256(str(str(nonce)+str(block.data)).encode()).hexdigest()
                nonce = nonce + 1
            else:
                if block.prev == self.chain[block.id-1].hashcode:
                    self.chain[block.id].hashcode = myHash
                    self.chain[block.id].nonce = nonce
                    if (block.id<len(self.chain)-1):
                        self.chain[block.id+1].prev = myHash

    def addloadedBlock(self, data):
        id = len(self.chain)
        nonce = 0
        block = Block(id, nonce, data["data"], data["hashcode"], data["previousHash"])
        self.chain.append(block)
    
    def addNewBlock(self, data, Attacker):
        if len (self.chain)==0:
            previousHash = "0"
            nonce = "0"
            myHash = hashlib.sha256(str(data).encode()).hexdigest()
            block = Block(id, nonce, "Initial Data", myHash, previousHash)
            self.chain.append(block)

        id = len(self.chain)
        nonce = 0
        
        #Debug Code
        #Check to See if Nodes Exist On the Network
        #if not self.nodes:
            #print("no nodes available")
        #    return
        

        

        #Check to see if the block is index 0, Makes this the genesis block
        #If false then value of the previous hash is equal to the output of
        #The previous block
        
        
        if Attacker:
            myHash = "Mallicious"
            previousHash = "MALLICIOUS ENTRY"

            block = Block(id, nonce, data, myHash, previousHash)
            #minedBlock = self.mineBlockOnNode(block)
            self.chain.append(block)
            return block, self
        else:
            previousHash = self.chain[-1].hashcode
            myHash = hashlib.sha256(str(data).encode()).hexdigest()

            block = Block(id, nonce, data, myHash, previousHash)
            minedBlock = self.mineBlockOnNode(block)
            self.chain.append(minedBlock)
        #Code to Initiate the block
        
        
            return minedBlock, self
    
    #Code to Print the block chain
    def printBlockChain(self):
        chainDict={}
        for id in range(len(self.chain)):
            chainDict[id]=self.chain[id].getStringVal()
        #print (chainDict)

    

    def mineChain(chain):
        #Check If the chain has been comprimised
        #If chain is broken trust decreases otherwise mining persues
        minedBlocks = []
        brokenLink = chain.checkIfBroken()
        if brokenLink is None:
            for node in chain.nodes:

                #Increase trust after sucessful Mine
                node.trust +=1
            minedBlocks.append("All Blocks have been Mined")
            pass
        else :
            for block in chain.chain[brokenLink.id:]:
                #print("Mining Block:" , block.getStringVal())
                prevHash = block.previousHash
                chain.mineBlock(block)


                if block.previousHash == prevHash: 
                    minedBlocks.append(f"Mined Block: {block.id}, Nonce: {block.nonce}, data: {block.data}, Hash: {block.hashcode}, previous hash: {block.previousHash} ")
                else:
                    minedBlocks.append(f"Block with ID of {block.id}, Failed To Mine")
        return "\n".join(minedBlocks)
    
    # For Benzyntine Fault Tollerance
    def mineBlockOnNode(self, block):
        nonce = 0
        myHash = hashlib.sha256(str(str(nonce)+str(block.data)).encode()).hexdigest()
        while myHash[0:4]!=self.prefix:
            myHash = hashlib.sha256(str(str(nonce)+str(block.data)).encode()).hexdigest()
            nonce = nonce + 1
        else:
            block.hashcode = myHash
            block.nonce = nonce
            if (block.id<len(self)-1):
               self[block.id+1].prev = myHash
        return block
            


    #If Byzentine Fault Tollerance Is Disabled
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



#UI Items
#----------------------------------------
#Properties Tab
#----------------------------------------
class PropertiesDialog(QMainWindow, Ui_Properties):
    def __init__ (self, my_app_instance, NodeID=None):
        super().__init__()
        self.setupUi(self)

        

        #Get Variables
        self.NodeID = NodeID
        self.my_app_instance = my_app_instance

        self.tbl_prop_Blockchain.findChild(QtWidgets.QTableWidget, "tbl_prop_Blockchain")
        self.tbl_prop_msgs.findChild(QtWidgets.QTableWidget, "tbl_prop_msgs")


        #Set Variables
        self.updateTimer = QTimer()

        self.setVariables()
        self.update()

        #Set Variables for Application Data
        self.appData = self.my_app_instance.appData

        #set table
        self.tbl_prop_msgs.setColumnCount(5)
        headers = ["Time","Type", "Sender ID", "Origin","Data"]
        self.tbl_prop_msgs.setHorizontalHeaderLabels(headers)

    #Application Actions
    def actionHome(self):
        self.home = StartupWindow()
        self.home.show()
        self.close()

        
    
    def setVariables(self):
        if self.NodeID is not None and self.my_app_instance.b is not None:
            selectedNode = self.my_app_instance.b.getNodeByID(self.NodeID)


            #Code for Getting Static Variables
            if selectedNode:
                #Get Variables
                name = str(selectedNode.name)
                id = str(selectedNode.ID)
                trust = str(selectedNode.trust)
                addedNtwTime = selectedNode.ntwTimeAdded
                timeadded = str(selectedNode.timeAdded)
                
                #Set Variables
                self.prp_NodeName.setText(name)
                self.lbl_prop_ID.setText(id)
                self.lbl_prop_Trust.setText(trust)
                self.lbl_prop_time.setText(timeadded)
                self.lbl_prop_networkTime.setText(addedNtwTime)
                
                self.updatePrimaryTag(selectedNode)

    def updatePrimaryTag(self, selectedNode):
        if selectedNode.Attacker:
            if selectedNode not in self.my_app_instance.b.getPrimeNodes():
                self.lbl_prop_Type.setText("Non Primary Mallicous Node")
                self.label.setPixmap(QtGui.QPixmap("Assets/Images/Icons/Node_Icon__Attacker.png"))
                
            else:
                self.lbl_prop_Type.setText("Primary Node (mallicious)")
                self.label.setPixmap(QtGui.QPixmap("Assets/Images/Icons/Node_Icon_Primary_Attacker.png"))
        else:
            if selectedNode not in self.my_app_instance.b.getPrimeNodes():
                self.lbl_prop_Type.setText("Non Primary Node")
                self.label.setPixmap(QtGui.QPixmap("Assets/Images/Icons/Node_Icon_Valid.png"))
            else:
                self.lbl_prop_Type.setText("Primary Node")
                self.label.setPixmap(QtGui.QPixmap("Assets/Images/Icons/Node_Icon_Primary.png"))
                


            

    def UpdateBlockchain(self, selectedNode):
      if selectedNode.blockchain.chain is not None:
            self.tbl_prop_Blockchain.clear()
            self.tbl_prop_Blockchain.setRowCount(len(selectedNode.blockchain.chain))
            self.tbl_prop_Blockchain.setColumnCount(5)
            headers = ["Block ID", "Data", "Nonce", "Hash", "Previous Hash"]
            self.tbl_prop_Blockchain.setHorizontalHeaderLabels(headers)

            for row, block in enumerate(selectedNode.blockchain.chain):
                self.tbl_prop_Blockchain.setItem(row, 0, QTableWidgetItem(str(block.id)))
                self.tbl_prop_Blockchain.setItem(row, 1, QTableWidgetItem(str(block.data)))
                self.tbl_prop_Blockchain.setItem(row, 2, QTableWidgetItem(str(block.nonce)))
                self.tbl_prop_Blockchain.setItem(row, 3, QTableWidgetItem(str(block.hashcode)))
                self.tbl_prop_Blockchain.setItem(row, 4, QTableWidgetItem(str(block.previousHash)))
            self.tbl_prop_Blockchain.resizeColumnsToContents()



    def UpdateMessages(self, selectedNode):
        if self.appData.bftMessages is not None:

            
            
            sender = [msg for msg in self.appData.bftMessages if msg.sender == self.NodeID]
            numRows = self.tbl_prop_msgs.rowCount()
            numNewRow = len(sender) - numRows
            if numNewRow > 0:
                self.tbl_prop_msgs.setRowCount(numRows + numNewRow)
                for row, msg in enumerate(sender):
                    if msg.sender == selectedNode.ID:
                        self.tbl_prop_msgs.setItem(row, 0, QTableWidgetItem(str(msg.datetime.strftime("%H:%M:%S"))))
                        self.tbl_prop_msgs.setItem(row, 1, QTableWidgetItem(str(msg.type)))
                        self.tbl_prop_msgs.setItem(row, 2, QTableWidgetItem(str(msg.sender)))
                        self.tbl_prop_msgs.setItem(row, 3, QTableWidgetItem(str(msg.origin)))
                        self.tbl_prop_msgs.setItem(row, 4, QTableWidgetItem(str(msg.data)))
                self.tbl_prop_msgs.resizeColumnsToContents()

            

            


    def update(self):
        self.updateTimer.timeout.connect(self.updateVariables)
        self.updateTimer.start(1000)

    def updateVariables(self):
        selectedNode = self.my_app_instance.b.getNodeByID(self.NodeID)
        if self.isVisible():
            self.updatePrimaryTag(selectedNode)
            self.UpdateBlockchain(selectedNode)
            self.UpdateMessages(selectedNode)
        else:
            self.updateTimer.stop()
        

#----------------------------------------
#Class To Join Nodes On UI
#----------------------------------------
class LineDrawer(QWidget):
    def __init__(self, parent=None):
        super(LineDrawer, self).__init__(parent)
        self.nodePositions = []
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        if parent:
            self.setGeometry(parent.geometry())

    def addNodePositions(self, position):
        correctedPos = position + QPoint(int(DragNodeIcon.iconSize.width() / 2), int(DragNodeIcon.iconSize.height() / 2))
        self.nodePositions.append(correctedPos)
        self.update()

    def updateNodePositions(self, index, position):
        correctedPos = position + QPoint(int(DragNodeIcon.iconSize.width() / 2), int(DragNodeIcon.iconSize.height() / 2))
        if index <len(self.nodePositions) and index != QPoint(-1,-1):
            self.nodePositions[index] = correctedPos
            self.update()
    
    def paintEvent(self, event):
        
        painter = QPainter(self)       
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        pen = QPen(QColor(Qt.GlobalColor.gray), 1)
        painter.setPen(pen)

        sortedList = [pos for pos in self.nodePositions if pos is not None]

        if len(sortedList) >= 2:
            for i in range(len(sortedList)):
                for j in range(i + 1, len(sortedList)):
                            painter.drawLine(sortedList[i], sortedList[j])
                            #print(f"position of node is {sortedList[i]}")
    
    def removeNodePosition(self, index):
        if 0<= index < len(self.nodePositions):
            self.nodePositions[index] = None
            self.update()

class SignalHandler(QtCore.QObject):
    updateUI = pyqtSignal(dict)

    def __init__(self, app):
        super().__init__()
        self.app = app

    @pyqtSlot(dict)
    def onUpdateUI(self, ui_data):
        if ui_data['Blockchain_Updated']:
            self.app.updateBlockChainTable()
            self.app.updateMessagesTable()
            self.app.updateSimpleMessagesTable()
            self.app.updateTrustValuesInList()   
            self.app.updateAllNodeIcons()
            self.app.updateListOverview()
            
    
class SimulationThread(QThread):
    def __init__ (self, env, performAddData, signalhandler):
        super().__init__()
        self.env = env
        self.performAddData = performAddData
        self.signalhandler = signalhandler

    def run(self):
        #Debug Code
        print("Thread Started")
        self.env.process(self.performAddData(self.env))
        self.env.run(until=self.env.now + 7000)
    
        
#----------------------------------------
#Main Window
#----------------------------------------  

class MyApp(QMainWindow, Ui_scr_Main):
    b = None
    selected_icon = None
    worker = None
    simulation_paused_signal = pyqtSignal(bool)
    updateUI = pyqtSignal(dict)
    closed = pyqtSignal()

    
   

    
    def __init__(self, LoadedData=None):
        super(MyApp, self).__init__()
        self.setupUi(self)
        

        self.loadedData = LoadedData
        
        

        #Set Simulation
        self.simulation_paused = False

        #Save Functions
        self.actionSave.triggered.connect(self.saveBlockchain)

        #Go Home
        self.actionHome.triggered.connect(self.goHome)

        #Load Functions

        #Reset Functions
        self.actionReset.triggered.connect(self.reset)

        

        #For appllying settings
        self.btn_applySettings.clicked.connect(self.applySettings)
        self.simulation_paused_signal.connect(self.onPauseSimulation)

        #Mapping to tie UI lists with Interactive elements
        self.nodeIconMappings = {}
        self.listIconMappings = {}

        #Timer
        self.timer = QTimer()
        self.stopwatch = QTime(0,0,0)
        self.initStopwatch()
        self.env = simpy.Environment()
        
            
        #Properties Window
        self.propertiesWindow = None

        #Thread for automated mining process
        #self.validDataWorkerTimer = QTimer()
        #self.validDataWorkerTimer.timeout.connect(self.automaticAdditionOfData)
        
        #Draw Lines Between Nodes
        self.lineDrawer = LineDrawer(self.fr_VisualArea)
        self.lineDrawer.setGeometry(self.fr_VisualArea.geometry())
        self.lineDrawer.setObjectName("lineDrawer")
        self.lineDrawer.raise_()

        

        #List for network overview
        self.tb_Overview.findChild(QtWidgets.QWidget, "tb_Overview")

        #list for blockchain elements
        self.blockchainModel = QtGui.QStandardItemModel()
        self.tbl_Blockchain.setModel(self.blockchainModel)

        #List For Messages sent during byzentine fault tollerence
        self.tbl_Messages.findChild(QtWidgets.QTableWidget, "tbl_Messages")

        #Obtain App Data
        self.appData = ApplicationData()

        #Drag and Drop peramiters for area
        self.fr_VisualArea.setAcceptDrops(True)
        self.fr_VisualArea.dragEnterEvent = self.dragEnterEvent
        self.fr_VisualArea.dropEvent = self.dropEvent
        self.fr_VisualArea.installEventFilter(self)

        #For highlighting elements after they been clicked in the list
        self.listWidget.itemClicked.connect(self.onListItemClick)

        #Initialise Table
        self.tbl_Messages.setColumnCount(6)
        headers = ["Time", "Network Time","Type", "Sender ID", "Origin","Data"]
        self.tbl_Messages.setHorizontalHeaderLabels(headers)

        #Initialise simple table
        self.tbl_simpleMessages.setColumnCount(1)
        headers = ["Message Log"]
        self.tbl_simpleMessages.setHorizontalHeaderLabels(headers)

        self.btn_AddNode.setObjectName("btn_AddNode")

        #Auto Add Data (simulation)
        self.autoAddData = QTimer()
        self.signalhandler = SignalHandler(self)
        self.autoAddData.setInterval(7000)
        self.autoAddData.timeout.connect(self.automaticAdditionOfData)
        self.updateUI.connect(self.onUpdateUI)

        self.simulationStop = False

        
        self.signalhandler.updateUI.connect(self.signalhandler.onUpdateUI)

    
    #ADD NODE
        self.btn_AddNode.clicked.connect(self.addNewNode)

    #ADD BLOCK 
        self.btn_AddBlockToNode.clicked.connect(self.addBlockToNode)
    #Mine Block
        self.btn_Mine.clicked.connect(self.mineBlocks)
    
    #Changing Block Data
        self.btn_ChangeBlock.clicked.connect(self.changeBlock)

        if self.loadedData is not None:
            self.setLoadedData()


    #----------------------------------------
    #Ui Functions
    #----------------------------------------

    def reset(self):
        newappinstance = MyApp(LoadedData=None)
        newappinstance.show()
        self.close()

    def goHome(self):
        self.home = StartupWindow()
        self.home.show()
        self.close()


    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)
    
    #def loadData(self, filePath):
    #    with open(filePath, 'r') as file:
    #        loadedData = json.load(file)

        #self.block
    

    #--------------APPLY SETTINGS-------------
    def applySettings(self):
        if self.chk_PauseMining.isChecked() and self.simulation_paused == False:
            self.simulation_paused = True
            self.simulationStop = False
            self.autoAddData.start()
            print("StartingThread")
        elif self.simulation_paused == False:
            print("Running")
        else:
            self.simulation_paused = True
            self.simulationStop = True
            self.autoAddData.stop()
            print("Simulation stopped")

    def onUpdateUI(self, ui_data):
        if ui_data['Blockchain_Updated']:
            self.updateBlockChainTable()
            self.updateMessagesTable()
            self.updateSimpleMessagesTable()
            self.updateTrustValuesInList()   
            self.updateAllNodeIcons()
            self.updateListOverview()
            
    
    def onPauseSimulation(self, paused):
        self.simulation_paused = paused
    
    #---------------SAVE-----------------
    def saveBlockchain(self):
        options = QFileDialog().options()
        filepath, _ = QFileDialog.getSaveFileName(self, "Save As", "", "JSON Files (*.json);;All Files (*)", options=options)

        if filepath:
            self.b.save_to_file(filepath)


    def setLoadedData(self):
        nodeData = self.loadedData.get("NodeData", [])
        blockData = self.loadedData.get("BlockData", [])
        appdata = self.loadedData.get("AppData", [])

        if self.b is None:
            self.b = Blockchain()
        
        for node in nodeData:
            Time = datetime.now().strftime("%H:%M:%S")
            addedNode = self.b.addNode(appData=self.appData, ntwTimeAdded=node["ntwTimeAdded"], trust=node["trust"], name=node["name"], Attacker=node["Attacker"], disabled= node["disabled"])
            ntwTime = self.stopwatch.toString("hh:mm:ss")
            self.lst_Overview.addItem(f"Operations at: NetworkTime - {ntwTime}, Time - {Time}")
            self.lst_Overview.addItem(f"Time: {str(Time)} - Network Time:  {ntwTime} - Name: {node} - ID: {addedNode.ID} - trust value: {addedNode.trust} - ACTION: added to the network")
            self.lst_Overview.addItem(f"Time: {str(Time)} - Network Time:  {ntwTime} - Name: {node} - ID:{addedNode.ID} - ACTION: Synced To The Network")
            self.listWidget.addItem(f"ID: {str(addedNode.ID)}, Node: {addedNode.name}, trust: {addedNode.trust}")
        
            #Add to UI
            newNode = DragNodeIcon(parent=self.fr_VisualArea, blockchain=self.b)
            newNode.setPixmap(QtGui.QPixmap("Assets/Images/Icons/Node_Icon_Valid.png"))

            newNode.ID = addedNode.ID

            #Update List
            nodelist = self.listWidget.item(self.listWidget.count() - 1)
            self.nodeIconMappings[newNode] = nodelist

            #Add Label
            newNode.setToolTip(f"ID: {addedNode.ID}, Node: {addedNode.name}, trust: {addedNode.trust}")
            
            #For Drag And Drop
            newNode.myAppInstance = self
            newNode.show()
            
            self.lineDrawer.addNodePositions(newNode.pos())
            #print(f"Node added at index: {self.listWidget.count() - 1}, position: {newNode.pos()}")
        
        if self.b is not None:
            for block in blockData:
                self.b.addloadedBlock(block)
        
        for message in appdata.get("appdata", []):
            self.appData.simplifiedbftMessages.append(message)
        
        for log in appdata.get("logMessages",[]):
            self.appData.logMessages.append(log)



            

    #---------------STOPWATCH-----------------
    def initStopwatch(self):
        self.timer.timeout.connect(self.updateStopwatch)
        self.timer.start(1000)

    def updateStopwatch(self):
        self.stopwatch = self.stopwatch.addSecs(1)
        self.label_15.setText(self.stopwatch.toString("hh:mm:ss"))

    #----------------------------------------
    #Block Functions
    #----------------------------------------
    def changeBlock(self):
        ID = str(self.txt_BlockID.toPlainText().strip())
        Data = str(self.txt_changeBlockData.toPlainText().strip())

        #Checks
        if not Data:
            Data = "None"
        Valid = False

        #Check for correct input 
        try:
            ID = int(ID)
            Valid = True

        #Prompt Error
        except ValueError:
            Valid = False
            prompt = QDialog()
            prompt.setWindowTitle("Unable To Change Block")
            prompt.setModal(True)

            #Message
            lbl = QLabel("ID Must An Integer and must exist on the Blockchain")
            lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            #Layout
            layout = QVBoxLayout()
            layout.addWidget(lbl)
            prompt.setLayout(layout)
            prompt.exec()

        if self.b is not None and Valid and any(block.id == ID for block in self.b.chain):
            self.b.changeData(ID, Data)

            #Update Ui
            self.updateBlockChainTable()
            self.updateMessagesTable()
            self.updateSimpleMessagesTable()
            self.updateTrustValuesInList()   
            self.updateAllNodeIcons()
            self.updateListOverview()
        else:
            Valid = False
            prompt = QDialog()
            prompt.setWindowTitle("Block Dosnt Exist")
            prompt.setModal(True)

            #Message
            lbl = QLabel("ID Must An Integer and must exist on the Blockchain")
            lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            #Layout
            layout = QVBoxLayout()
            layout.addWidget(lbl)
            prompt.setLayout(layout)
            prompt.exec()

        
    def addBlockToNode(self):
        ID = str(self.txt_NodeID.toPlainText().strip())
        Data = self.txt_blkData.toPlainText().strip()

        

        if not Data:
            Data = "None"
        Valid = False

        #Check for correct input 
        try:
            ID = int(ID)
            Valid = True

        #Prompt Error
        except ValueError:
            Valid = False
            prompt = QDialog()
            prompt.setWindowTitle("Unable To Add Block")
            prompt.setModal(True)

            #Message
            lbl = QLabel("ID Must An Integer and must exist on the network")
            lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            #Layout
            layout = QVBoxLayout()
            layout.addWidget(lbl)
            prompt.setLayout(layout)
            prompt.exec()
        
        #Check to see if block chain exists
        if self.b is not None and Valid:
            
            node = self.b.getNodeByID(ID)
            if node:
                ntwTime = self.stopwatch.toString("hh:mm:ss")
                Time = datetime.now().strftime("%H:%M:%S")
                self.lst_Overview.addItem(f"Operations at: NetworkTime - {ntwTime}, Time - {Time}")
                node.addBlock(Data)
                
                
                
                self.updateBlockChainTable()
                self.updateMessagesTable()
                self.updateSimpleMessagesTable()
                self.updateTrustValuesInList()   
                self.updateAllNodeIcons()
                self.updateListOverview()

            #Error if node dosnt exist
            else:
                Valid = False
                prompt = QDialog()
                prompt.setWindowTitle("Node Dosnt Exist")
                prompt.setModal(True)

                #Message
                lbl = QLabel("Node isnt available")
                lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                #Layout
                layout = QVBoxLayout()
                layout.addWidget(lbl)
                prompt.setLayout(layout)
                prompt.exec()


        # If blockchain has no entries
        elif self.b is None:
            Valid = False
            prompt = QDialog()
            prompt.setWindowTitle("Unable To Add Block")
            prompt.setModal(True)

            #Message
            lbl = QLabel("No Nodes Available")
            lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            #Layout
            layout = QVBoxLayout()
            layout.addWidget(lbl)
            prompt.setLayout(layout)
            prompt.exec()
            

    #MINE CHAIN
    def mineBlocks(self):
        #Check to see if block chain exists
        if self.b is not None:
            result = self.b.mineChain()
            self.lst_Overview.addItem(result)
            self.updateBlockChainTable()


        # If blockchain has no entries
        elif self.b is None:
            prompt = QDialog()
            prompt.setWindowTitle("Unable To Mine")
            prompt.setModal(True)

            #Message
            lbl = QLabel("No Blocks Available to mine")
            lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            #Layout
            layout = QVBoxLayout()
            layout.addWidget(lbl)
            prompt.setLayout(layout)
            prompt.exec()

    def updateBlockChainTable(self):
        if self.b is not None:
            self.blockchainModel.clear()
            self.blockchainModel.setRowCount(len(self.b.chain))
            self.blockchainModel.setColumnCount(5)
            headers = ["Block ID", "Data", "Nonce", "Hash", "Previous Hash"]
            self.blockchainModel.setHorizontalHeaderLabels(headers)

            for row, block in enumerate(self.b.chain):
                self.blockchainModel.setItem(row, 0, QtGui.QStandardItem(str(block.id)))
                self.blockchainModel.setItem(row, 1, QtGui.QStandardItem(str(block.data)))
                self.blockchainModel.setItem(row, 2, QtGui.QStandardItem(str(block.nonce)))
                self.blockchainModel.setItem(row, 3, QtGui.QStandardItem(str(block.hashcode)))
                self.blockchainModel.setItem(row, 4, QtGui.QStandardItem(str(block.previousHash)))
            self.tbl_Blockchain.resizeColumnsToContents()
        else:
            self.blockchainModel.clear()

    def updateListOverview(self):
        for message in self.appData.logMessages:
            if message not in [self.lst_Overview.item(i).text() for i in range(self.lst_Overview.count())]:
                self.lst_Overview.addItem(message)

    #----------------------------------------
    #Messages Functions
    #----------------------------------------
    def updateMessagesTable(self):
        if self.appData.bftMessages is not None:
            numRows = self.tbl_Messages.rowCount()
            numNewRow = len(self.appData.bftMessages) - numRows

            
        if numNewRow > 0:
            self.tbl_Messages.setRowCount(numRows + numNewRow)
            for row, msg in enumerate(self.appData.bftMessages):
                self.tbl_Messages.setItem(row, 0, QTableWidgetItem(str(msg.datetime.strftime("%H:%M:%S"))))
                self.tbl_Messages.setItem(row, 1, QTableWidgetItem(str(self.stopwatch.toString("hh:mm:ss"))))
                self.tbl_Messages.setItem(row, 2, QTableWidgetItem(str(msg.type)))
                self.tbl_Messages.setItem(row, 3, QTableWidgetItem(str(msg.sender)))
                self.tbl_Messages.setItem(row, 4, QTableWidgetItem(str(msg.origin)))
                self.tbl_Messages.setItem(row, 5, QTableWidgetItem(str(msg.data)))


            self.tbl_Messages.resizeColumnsToContents()

    def updateSimpleMessagesTable(self):
        if self.appData.simplifiedbftMessages is not None:
            numRows = self.tbl_simpleMessages.rowCount()
            numNewRow = len(self.appData.simplifiedbftMessages) - numRows

            
        if numNewRow > 0:
            self.tbl_simpleMessages.setRowCount(numRows + numNewRow)
            for row, msg in enumerate(self.appData.simplifiedbftMessages):
                self.tbl_simpleMessages.setItem(row, 0, QTableWidgetItem(msg))


            self.tbl_simpleMessages.resizeColumnsToContents()
            

            
    #----------------------------------------
    #Node Functions
    #----------------------------------------

        #TEST
        #self.label_14 = DragNodeIcon(parent=self.fr_VisualArea)
        #self.label_14.setPixmap(QtGui.QPixmap("Assets/Images/Icons/Node_Icon_Valid.png"))



        

    
    def addNewNodeHelper(self, node, Attacker, Trust):  
            
            Time = datetime.now().strftime("%H:%M:%S")
            ntwTime = self.stopwatch.toString("hh:mm:ss")
            addedNode = self.b.addNode(appData=self.appData, ntwTimeAdded=ntwTime, trust=Trust, name=node, Attacker=Attacker)
            self.lst_Overview.addItem(f"Operations at: NetworkTime - {ntwTime}, Time - {Time}")
            self.lst_Overview.addItem(f"Time: {str(Time)} - Network Time:  {ntwTime} - Name: {node} - ID: {addedNode.ID} - trust value: {Trust} - ACTION: added to the network")
            self.lst_Overview.addItem(f"Time: {str(Time)} - Network Time:  {ntwTime} - Name: {node} - ID:{addedNode.ID} - ACTION: Synced To The Network")
            self.listWidget.addItem(f"ID: {str(addedNode.ID)}, Node: {node}, trust: {Trust}")
            

            #Add to UI
            newNode = DragNodeIcon(parent=self.fr_VisualArea, blockchain=self.b)
            newNode.setPixmap(QtGui.QPixmap("Assets/Images/Icons/Node_Icon_Valid.png"))

            newNode.ID = addedNode.ID
            
            #self.nodeIconMappings[newNode] = self.listWidget.item(self.listWidget.count() - 1)

            #Associate with the UI
            #list_item = self.lst_Overview.item(self.lst_Overview.count() - 1)
            #self.nodeIconMappings[newNode] = list_item

            #Update List
            nodelist = self.listWidget.item(self.listWidget.count() - 1)
            self.nodeIconMappings[newNode] = nodelist




            #Add Label
            newNode.setToolTip(f"ID: {addedNode.ID}, Node: {addedNode.name}, trust: {addedNode.trust}")
            
            #For Drag And Drop
            newNode.myAppInstance = self
            newNode.show()
            
            self.lineDrawer.addNodePositions(newNode.pos())
            #print(f"Node added at index: {self.listWidget.count() - 1}, position: {newNode.pos()}")

            

            

            
            
    def removeNode(self, nodeIcon):
        #Remove from Block Chain
            node = self.b.getNodeByID(nodeIcon.ID)
            self.b.removeNode(node)

            if nodeIcon in self.nodeIconMappings:
                nodeIcon.setVisible(False)
                list_item = self.nodeIconMappings[nodeIcon]
                row = self.listWidget.row(list_item)
                list_item.setHidden(True)
            
            ntwTime = self.stopwatch.toString("hh:mm:ss")
            Time = datetime.now().strftime("%H:%M:%S")

            self.updateTrustValuesInList()   
            self.updateMessagesTable()
            self.updateSimpleMessagesTable()
            self.updateAllNodeIcons()
            self.lst_Overview.addItem(f"Time: {Time} - Network Time: {ntwTime} - Node ID: {node.ID} - Name {node.name} Removed From The Network")


            self.lineDrawer.removeNodePosition(nodeIcon.ID)
            

            

    def addNewNode(self):
        attacker = self.chk_AttackerNode.isChecked()
        name = str(self.txt_NodeName.toPlainText().strip())
        Trust = self.txt_NodeTrust.toPlainText().strip()
        Valid = False
        #Variables to check for correct input 
        
        try:
            Trust = int(Trust)
            Valid = True

        #Prompt Error
        except ValueError:
            Valid = False
            prompt = QDialog()
            prompt.setWindowTitle("Unable To Add Node")
            prompt.setModal(True)

            #Message
            lbl = QLabel("Trust Must An Integer")
            lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            #Layout
            layout = QVBoxLayout()
            layout.addWidget(lbl)
            prompt.setLayout(layout)
            prompt.exec()
        
        if self.b is not None and Valid:
            node = name
            self.addNewNodeHelper(node, attacker, Trust)
            self.updateAllNodeIcons()


            #Update List
            #self.updateNodeList()
            
        elif self.b is None and Valid:
            self.b = Blockchain()
            node = name
            self.addNewNodeHelper(node, attacker, Trust)
            self.updateAllNodeIcons()
            
    
    
        
            
    

        
            
    #Function For Moving Nodes
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.acceptProposedAction()
            

    def dropEvent(self, event):

        #TEST
        #img = event.mimeData().imageData()
        #if not img.isNull():
        #    self.label_14.setPixmap(QtGui.QPixmap.fromImage(img))
        #    self.label_14.move((event.position() - self.label_14.drag_start_position).toPoint())
        #    event.acceptProposedAction()

        nodeIcon = event.source()
        if isinstance(nodeIcon, DragNodeIcon):
            nodeIcon.move((event.position() - nodeIcon.drag_start_position).toPoint())
            event.acceptProposedAction()

    

  
    def updateAllNodeIcons(self):
        for newNode, nodelist in self.nodeIconMappings.items():
            node = self.b.getNodeByID(newNode.ID)


            icon = "Assets/Images/Icons/Node_Disabled.png"
            #print(f"Node: {node.ID}, undergoing change")
            if not node.disabled:
                if node.Attacker:
                    if node in self.b.getPrimeNodes():
                        icon = "Assets/Images/Icons/Node_Icon_Primary_Attacker.png"
                    else:
                        icon = "Assets/Images/Icons/Node_Icon__Attacker.png"
                else:
                    if node in self.b.getPrimeNodes():
                        icon = "Assets/Images/Icons/Node_Icon_Primary.png"
                    else:
                        icon = "Assets/Images/Icons/Node_Icon_Valid.png"
                
            if newNode != self.selected_icon:
                newNode.setPixmap(QtGui.QPixmap(icon))
            
    #Update Selected Node
    def updateSelectedIcon(self, selected):
        
        #Highlight Selected Node - UI
            if self.selected_icon is not None and self.selected_icon != selected and not sip.isdeleted(self.selected_icon):
                    self.selected_icon.setPixmap(QtGui.QPixmap("Assets/Images/Icons/Node_Icon_Valid.png"))
                    self.nodeIconMappings[self.selected_icon].setSelected(False)
                

            selected.setPixmap(QtGui.QPixmap("Assets/Images/Icons/Node_Icon_Selected.png"))
            self.nodeIconMappings[selected].setSelected(True)
            self.selected_icon = selected

            #Highlight its entry in the node list
            selectedNode = None
            for node in self.b.nodes:
                if node.ID == selected.ID:
                    selectedNode = node
                    break

            if selectedNode is not None:
                index = self.b.nodes.index(selectedNode)
                item = self.listWidget.item(index)
                item.setSelected(True)

            self.updateAllNodeIcons()

    #ListView Functions
    def onListItemClick(self, item):
        selectedNode = None
        for node, entry in self.nodeIconMappings.items():
            if entry == item:
                
                selectedNode = node
                break

        if selectedNode is not None:
            self.updateSelectedIcon(selectedNode)
            
    #Function to open properties menu
    def propertiesAction(self):
        if self.propertiesWindow is None or not self.propertiesWindow.isVisible():
            self.propertiesWindow = PropertiesDialog(self, NodeID = self.selected_icon.ID)
        self.propertiesWindow.show()
        self.propertiesWindow.raise_()
        self.propertiesWindow.activateWindow()

    #----------------------------------------
    #Automated Network Functions
    #----------------------------------------
    def automaticAdditionOfData(self):
        
        if self.b is not None and self.b.nodes is not None:
                if self.chk_PauseMining.isChecked():
                    self.simulation_Thread = SimulationThread(self.env, self.performAddData, self.signalhandler)
                    self.simulation_Thread.start()
                    #Debug Code
                    #print("automaticAdditionOfData Called")
                    
                
        else:
            self.errorPromptForAutoMine()
            #self.simulationRunning = True
    
    def performAddData(self, env):
        #Debug Code
        #print("Perform AddData Called")

        if not self.simulationStop:    
            sortedList = [node for node in self.b.nodes if node is not None and not node.disabled]
            if sortedList is not None and len(sortedList) > 0:

                print("Start Add Data")
                
                #Data To Add To Overview
                ntwTime = self.stopwatch.toString("hh:mm:ss")
                Time = datetime.now().strftime("%H:%M:%S")
                self.lst_Overview.addItem(f"Operations at: NetworkTime - {ntwTime}, Time - {Time}")

                addblock = False

                #Select Node to add data
                randomNode = random.choice(sortedList)
                if randomNode.Attacker:
                    integer = len(self.b.chain) + 1
                    randomData = f"Mallicious-Data-{integer}"
                    
                    if randomNode.addBlock(randomData):
                        randomNode.addBlock(randomData)
                        blockID = len(self.b.chain)
                        addblock = True

                    #Debug Code
                    #print("attacker selected")
                    #randomNode.dataChangeAttack(data)
                else:

                    integer = len(self.b.chain) + 1
                    randomData = f"Data-Entry-{integer}"

                    #Add Block 
                    if randomNode.addBlock(randomData):
                        randomNode.addBlock(randomData)
                        blockID = len(self.b.chain)
                        addblock = True


                    
                ui_data = {
                    'Blockchain_Updated': addblock,
                    'Block_ID' : blockID,
                    'ntwTime' : ntwTime,
                    'Time' : Time,
                }
                self.signalhandler.updateUI.emit(ui_data)

                #Simulate Time to add block
            yield env.timeout(5000)
            print("cycle Finished")
            
            print("End Add Data")

            #Debug Code
            #if not self.simulation_paused:
                #print("pause")

                
                

                
    
    def errorPromptForAutoMine(self):
        prompt = QDialog()
        prompt.setWindowTitle("No Nodes Available")
        prompt.setModal(True)

        #Message
        lbl = QLabel("Add a node to the network before beginning Mining")
        lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        #Uncheck Box
        self.chk_PauseMining.setChecked(False)
        self.btn_applySettings.click()

        #Layout
        layout = QVBoxLayout()
        layout.addWidget(lbl)
        prompt.setLayout(layout)
        prompt.exec()





    def updateTrustValuesInList(self):
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            nodeID = int(item.text().split(',')[0].split(':')[1].strip())
            trust = self.b.getNodeByID(nodeID).trust
            nodeName = item.text().split(',')[1].strip()
            updatedText = f"ID: {nodeID}, {nodeName}, trust: {trust}"
            item.setText(updatedText)
    
    def updateNodePositions(self, index,  position):
        self.lineDrawer.updateNodePositions(index, position)
        self.lineDrawer.update()
        self.updateAllNodeIcons()

    def resizeEvent(self, event):
        self.lineDrawer.resize(self.fr_VisualArea.size())

                


class DragNodeIcon(QtWidgets.QLabel):
    iconSize = QSize(50, 50)
    def __init__(self, parent=None, blockchain=None):
        super(DragNodeIcon, self).__init__(parent)
        self.contextMenu = QtWidgets.QMenu()
        self.b = blockchain
        self.node = None
        

        #Add Option To Remove
        self.removeAction = QAction("Remove Node", self)
        self.removeAction.triggered.connect(lambda: self.myAppInstance.removeNode(self))
        self.contextMenu.addAction(self.removeAction)


        #self.moveEvent.connect(self.myAppInstance.updateNodePositions)


        #Add Properties Option
        self.propertiesAction = QAction("Properties", self)
        self.propertiesAction.triggered.connect(lambda: self.myAppInstance.propertiesAction())
        self.contextMenu.addAction(self.propertiesAction)
        

    

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.drag_start_position = event.position()
            self.window().updateSelectedIcon(self)
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            self.window().updateSelectedIcon(self)
            self.contextMenu.exec(QCursor.pos())
            
    def moveEvent(self, event: QtGui.QMoveEvent) -> None:
            super().moveEvent(event)
            if hasattr(self, 'myAppInstance'):
                index = self.myAppInstance.nodeIconMappings[self]
                index = self.myAppInstance.listWidget.row(index)
                self.myAppInstance.updateNodePositions(index, self.pos())
                #print(f"Node noved, index: {index}, position: {self.pos()}")

            
    def mouseMoveEvent(self, event):
        if not (event.buttons() & QtCore.Qt.MouseButton.LeftButton):
            return
        if (event.position() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        
        drag = QtGui.QDrag(self)
        mimeData = QtCore.QMimeData()
        mimeData.setImageData(self.pixmap().toImage())
        drag.setMimeData(mimeData)

        pixmap = QPixmap(self.size())
        self.render(pixmap)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())


        drag.exec(Qt.DropAction.MoveAction)

class StartupWindow(QMainWindow, Ui_MainWindow2):

    def __init__(self, parent=None):
        super(StartupWindow, self).__init__(parent)
        self.setupUi(self)
        self.btn_StartNew.clicked.connect(self.startNew)
        self.btn_LoadData.clicked.connect(self.loadFrom)

    #Open New
    def startNew(self):
        self.newWindow = MyApp(LoadedData=None)
        self.newWindow.show()
        self.newWindow.closed.connect(self.reopenStartupWindow)
        self.close()

    #Load From
    def loadFrom(self):
        file_path, _ =QFileDialog.getOpenFileName(self, "Open File", "", "JSON Files (*json);;All Files (*)")
        if file_path:
            with open(file_path, 'r') as file:
                self.loadedData = json.load(file)
        self.newWindow = MyApp(LoadedData=self.loadedData)
        self.newWindow.show()
        self.newWindow.closed.connect(self.reopenStartupWindow)
        self.close()

    def reopenStartupWindow(self):
        self.show()
        self.newWindow.show()
        self.newWindow.closed.connect(self.reopenStartupWindow)
        self.close()

    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StartupWindow()
    window.show()
    sys.exit(app.exec())