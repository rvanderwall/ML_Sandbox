from flask import jsonify
import functools
from CryptoCurrency.BlockChain import BlockChain, mine_block

def get_controller(logger):
    bc = BlockChain(logger)
    controller = BobCoinController(logger, bc)
    return controller


def verify_json_request(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        pc_self = args[0]
        request = args[1]
        req_body = request.get_json()
        if req_body is None:
            response_body = {
                'ErrorMsg': 'Request body invalid JSON object.'
            }
            response_status = 400
        else:
            response_body, response_status = func(pc_self, req_body, **kwargs)
        return response_body, response_status
    return wrapper


class BobCoinController:
    def __init__(self, logger, block_chain: BlockChain):
        self.logger = logger
        self.block_chain = block_chain

    # Mining a new block
    def mine_block(self):
        self.logger.info("mine_block")
        response_status = 200
        new_block = mine_block(self.block_chain, "Block Miner name")
        response = {
            'message': 'Congratulations, you just mined a block!',
            'index': new_block.index,
            'timestamp': new_block.timestamp,
            'nonce': new_block.nonce,
            'previous_hash': new_block.prev_hash
        }
        self.logger.info(f"Mined coin with index {new_block.index}")
        return jsonify(response), response_status

    # Getting the full Blockchain
    def get_chain(self):
        self.logger.info("get_chain")
        response_status = 200
        response = {
            'chain': [block.to_json() for block in self.block_chain.chain],
            'length': len(self.block_chain.chain)}
        return jsonify(response), response_status

    # Checking if the Blockchain is valid
    def is_valid(self):
        self.logger.info("is_valid")
        response_status = 200
        is_valid, bad_block = self.block_chain.check_chain_valid(self.block_chain.chain)
        if is_valid:
            response = {'message': f'All {len(self.block_chain.chain)} blocks are good. The Blockchain is valid.'}
        else:
            response = {'message': f'Houston, we have a problem with block{bad_block}. The Blockchain is not valid.'}
        return jsonify(response), response_status

    @verify_json_request
    def add_transaction(self, json_req):
        self.logger.info("add_transaction")
        response_status = 200
        transaction_keys = ['sender', 'receiver', 'amount']
        if not all(key in json_req for key in transaction_keys):
            return jsonify("Missing required args"), 400
        tx = json_req['sender']
        rx = json_req['receiver']
        amt = json_req['amount']
        idx = self.block_chain.add_transaction(tx, rx, amt)
        resp = {'message': f"Transaction added to block {idx}"}
        self.logger.info(f"Added transaction for {tx} to {rx}")
        return jsonify(resp), response_status

    def get_nodes(self):
        self.logger.info("get_nodes")
        response_status = 200
        resp = {
            "nodes": list(self.block_chain.nodes)
        }
        return jsonify(resp), response_status

    @verify_json_request
    def connect_node(self, json_req):
        self.logger.info("connect_node")
        response_status = 200
        nodes = json_req.get('nodes')
        if nodes is None:
            return "No nodes in request", 400
        for node in nodes:
            self.block_chain.add_node(node)
        resp = {
            "message": "All nodes now connected.  BobCoin now has these nodes",
            "nodes": list(self.block_chain.nodes)
        }
        return jsonify(resp), response_status

    def replace_chain(self):
        self.logger.info("replace_chain")
        is_replaced = self.block_chain.replace_chain()
        if is_replaced:
            response = {
                "message": "The nodes had different chains so the chain was replaced",
                'new_chain': [str(block) for block in self.block_chain.chain],
                'length': len(self.block_chain.chain)
            }
        else:
            response = {
                "message": "Current chain is the longest, keep it"
            }
        return jsonify(response), 200
