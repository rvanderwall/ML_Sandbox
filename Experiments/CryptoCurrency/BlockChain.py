import datetime
import hashlib
import requests
import time
from urllib.parse import urlparse
# https://www.freecodecamp.org/news/create-cryptocurrency-using-python/
# https://medium.com/@MKGOfficial/build-a-simple-blockchain-cryptocurrency-with-python-django-web-framework-reactjs-f1aebd50b6c


class Transaction:
    def __init__(self, sender, receiver, amount):
        self.json_res = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount,
            'time': str(datetime.datetime.now())
        }

    @staticmethod
    def from_json(json_transaction):
        t = Transaction(json_transaction['sender'],
                        json_transaction['receiver'],
                        json_transaction['amount'])
        t.json_res['time'] = json_transaction['time']
        return t

    def as_json(self):
        return self.json_res


class Block:
    def __init__(self, index, nonce, prev_hash, t_data, timestamp=None):
        self.index = index
        self.nonce = nonce
        self.prev_hash = prev_hash
        self.transactions = t_data
        self.timestamp = timestamp or time.time()

    def calculate_hash(self):
        block_of_string = "{}{}{}{}{}".format(self.index, self.nonce,
                                              self.prev_hash, self.transactions,
                                              self.timestamp)
        return hashlib.sha256(block_of_string.encode()).hexdigest()

    @staticmethod
    def from_json(json_block):
        index = json_block['index']
        nonce = json_block['nonce']
        prev_hash = json_block['prev_hash']
        transactions = [Transaction.from_json(json_transaction) for json_transaction in json_block['transactions']]
        timestamp = json_block['timestamp']
        block = Block(index, nonce, prev_hash, transactions, timestamp)
        return block

    def to_json(self):
        json_res = {}
        json_res['index'] = self.index
        json_res['nonce'] = self.nonce
        json_res['prev_hash'] = self.prev_hash
        json_res['transactions'] = [transaction.as_json() for transaction in self.transactions]
        json_res['timestamp'] = self.timestamp
        return json_res

    def __repr__(self):
        return "{} - {} - {} - {} - {}".format(self.index, self.nonce,
                                               self.prev_hash, self.transactions,
                                               self.timestamp)


class BlockChain:
    def __init__(self, logger):
        self.log = logger
        self.chain = []
        self.transactions = []
        self.nodes = set()
        self.construct_genesis()

    def construct_genesis(self):
        self.transactions.append(Transaction("Genesis", "Bob", 0))
        self.create_block(nonce=0, prev_hash="0")

    def create_block(self, nonce, prev_hash) -> Block:
        block = Block(
            index=len(self.chain),
            nonce=nonce,
            prev_hash=prev_hash,
            t_data=self.transactions
        )
        self.transactions = []
        self.chain.append(block)
        return block

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def add_node(self, node):
        parsed_url = urlparse(node)
        netloc = parsed_url.netloc
        self.log.info(f"Add node {node} to the node list as {parsed_url} - {netloc}")
        self.nodes.add(netloc)


    def add_transaction(self, sender, receiver, amount):
        self.transactions.append(Transaction(sender, receiver, amount))
        last_index = self.last_block.index
        current_index = last_index + 1
        return current_index

    def replace_chain(self):
        """ Check with other nodes to see if any have a longer chain
            If so, replace our chain with it
        """
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f"http://{node}/chain")
            if response.status_code == 200:
                json_chain = response.json()
                length = json_chain['length']
                chain = json_chain['chain']
                if length > max_length:
                    b_chain = [Block.from_json(block_string) for block_string in chain]
                    if self.check_chain_valid(b_chain):
                        max_length = length
                        longest_chain = chain
                    else:
                        self.log.warn(f"Chain from {node} is invalid")

        if longest_chain:
            self.chain = longest_chain
            return True

        return False


    @staticmethod
    def check_chain_valid(chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if not BlockChain.check_block_validity(block, previous_block):
                return False, block_index
            previous_block = block
            block_index += 1
        return True, -1

    @staticmethod
    def check_block_validity(block: Block, prev_block: Block):
        if prev_block.index + 1 != block.index:
            return False

        if prev_block.calculate_hash() != block.prev_hash:
            return False

        if not BlockChain.verifying_proof(block.nonce, prev_block.nonce):
            return False

        if block.timestamp <= prev_block.timestamp:
            return False

        return True

    @staticmethod
    def proof_of_work(prev_nonce):
        """This simple algorithm identifies a number f'
           such that:
                hash(ff') contains 4 leading zeros
            where:
                f is the previous f'
                f' is the new nonce
        """
        nonce = 0
        while not BlockChain.verifying_proof(nonce, prev_nonce):
            nonce += 1
        return nonce

    @staticmethod
    def verifying_proof(prev_nonce, nonce):
        """ Verifying the proof: does hash(last_proof, proof) contain 4 leading zeros? """
        guess = f'{prev_nonce}{nonce}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


def mine_block(blockchain: BlockChain, details_miner) -> Block:
    blockchain.add_transaction(
        sender="0",     # it implies that this node created a new block
        receiver=details_miner,
        amount=1,     # creating a new block is rewarded 1
    )

    last_block = blockchain.last_block
    last_nonce = last_block.nonce
    nonce = blockchain.proof_of_work(last_nonce)
    last_hash = last_block.calculate_hash()
    block = blockchain.create_block(nonce, last_hash)
    return block
