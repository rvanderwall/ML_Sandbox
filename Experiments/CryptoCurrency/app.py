# https://www.freecodecamp.org/news/create-cryptocurrency-using-python/
import hashlib
import time


class Block:
    def __init__(self, index, proof_no, prev_hash, data, timestamp=None):
        self.index = index
        self.proof_no= proof_no
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp or time.time()

    def calculate_hash(self):
        block_of_string = "{}{}{}{}{}".format(self.index, self.proof_no,
                                              self.prev_hash, self.data,
                                              self.timestamp)
        return hashlib.sha256(block_of_string.encode()).hexdigest()

    def __repr__(self):
        return "{} - {} - {} - {} - {}".format(self.index, self.proof_no,
                                               self.prev_hash, self.data,
                                               self.timestamp)


class BlockChain:
    def __init__(self):
        self.chain = []
        self.current_data = []
        self.nodes = set()
        self.construct_genesis()

    def construct_genesis(self):
        self.construct_block(proof_no=0, prev_hash=0)

    def construct_block(self, proof_no, prev_hash):
        block = Block(
            index=len(self.chain),
            proof_no=proof_no,
            prev_hash=prev_hash,
            data=self.current_data
        )
        self.current_data = []

        self.chain.append(block)
        return block

    @staticmethod
    def check_validity(block: Block, prev_block: Block):
        if prev_block.index + 1 != block.index:
            return False

        if prev_block.calculate_hash() != block.prev_hash:
            return False

        if not BlockChain.verifying_proof(block.proof_no, prev_block.proof_no):
            return False

        if block.timestamp <= prev_block.timestamp:
            return False

        return True

    def new_data(self, sender, recipient, quantity):
        new_data = {
            'sender': sender,
            'recipient': recipient,
            'quantity': quantity
        }
        self.current_data.append(new_data)
        return True


    @staticmethod
    def proof_of_work(prev_proof):
        '''This simple algorithm identifies a number f'
           such that:
                hash(ff') contains 4 leading zeros
            where:
                f is the previous f'
                f' is the new proof
        '''
        proof_no = 0
        while BlockChain.verifying_proof(proof_no, prev_proof):
            proof_no += 1

        return proof_no

    @staticmethod
    def verifying_proof(prev_proof, proof):
        ''' Verifying the proof: does hash(last_proof, proof) contain 4 leading zeros?'''

        guess = f'{prev_proof}proof'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @property
    def last_block(self) ->Block:
        return self.chain[-1]

    def block_mining(self, details_miner):
        self.new_data(
            sender="0",     # it implies that this node created a new block
            recipient=details_miner,
            quantity=1,     # creating a new block is rewarded 1
        )

        last_block = self.last_block
        last_proof_no = last_block.proof_no
        proof_no = self.proof_of_work(last_proof_no)

        last_hash = last_block.calculate_hash()
        block = self.construct_block(proof_no, last_hash)

        return vars(block)


def run():
    print("Crypto")
    blockchain = BlockChain()
    print("*** Start Mining BobCoins ***")
    print(blockchain.chain)

    last_block = blockchain.last_block
    last_proof_no = last_block.proof_no
    proof_no = blockchain.proof_of_work(last_proof_no)

    blockchain.new_data(
        sender="0",     # This node created a new block
        recipient="Bill Shatner",
        quantity=1
    )

    last_hash = last_block.calculate_hash()
    block = blockchain.construct_block(proof_no, last_hash)

    print("*** Successfully minded a BobCoin ***")
    print(blockchain.chain

    )
if __name__ == "__main__":
    run()
