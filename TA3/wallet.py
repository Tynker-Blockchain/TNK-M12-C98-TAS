from web3 import Web3
import time
from datetime import datetime

ganacheUrl = "http://127.0.0.1:7545" 
web3 = Web3(Web3.HTTPProvider(ganacheUrl))

class Account():
    def __init__(self):
        self.account = web3.eth.account.create()
        self.address = self.account.address
        self.privateKey = self.account.key.hex()
        print("privatekey", self.privateKey)

class Wallet():
    # Define initializer method
    def __init__(self):
        # Create transactions list
        self.transactions = {}

    def checkConnection(self):
        if web3.is_connected():
           return True
        else:
            return False
        
    def getBalance(self, address):
        balance = web3.eth.get_balance(address)
        return web3.from_wei(balance, 'ether')
    
    def makeTransactions(self, senderAddress, receiverAddress, amount, senderType, privateKey = None):
        web3.eth.defaultAccount = senderAddress
        tnxHash = None
        if(senderType == 'ganache'):
            tnxHash = web3.eth.send_transaction({
                "from": senderAddress,
                "to": receiverAddress,
                "value": web3.to_wei(amount, "ether")  
                })
        else:
            transaction = {
                "to": receiverAddress,
                "value": web3.to_wei(amount, "ether"),
                "nonce": web3.eth.get_transaction_count(senderAddress), 
                "gasPrice": web3.to_wei(10, 'gwei'),
                "gas": 21000 
            }

            signedTx = web3.eth.account.sign_transaction(transaction, privateKey)
            tnxHash = web3.eth.send_raw_transaction(signedTx.rawTransaction)
         
        # Return the transaction hash hex value
        return tnxHash.hex()
    
    # Define addTransactionHash method that takes tnxHash, senderAddress, receiverAddress, amount
    def addTransactionHash(self, tnxHash, senderAddress, receiverAddress, amount):
        # Create a dict with "form", "to", "tnxHash", "amount", "time" keys and store it at tnxHash key in the self.transactions
        self.transactions[tnxHash] = {
            "from":senderAddress,
            "to":receiverAddress,
            "tnxHash":tnxHash,
            "amount":amount,
            "time": time.time()
            }
    