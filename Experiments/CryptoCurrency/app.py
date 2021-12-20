import flask
from flask import jsonify, request
from flask_cors import cross_origin
from flask_cors import CORS

from CryptoCurrency.BlockChain import BlockChain
from CryptoCurrency.Logger import Logger, LoggingMiddleware
from CryptoCurrency.Controller import BobCoinController, get_controller
PORT = 4041


def run():
    logger = Logger("Blockchain demo")
    print("Crypto")
    blockchain = BlockChain(logger)
    print("*** Start Mining BobCoins ***")
    print(blockchain.chain)

    last_block = blockchain.last_block
    last_nonce = last_block.nonce
    nonce = blockchain.proof_of_work(last_nonce)

    blockchain.add_transaction(
        sender="0",     # This node created a new block
        receiver="Bill Shatner",
        amount=1
    )

    last_hash = last_block.calculate_hash()
    block = blockchain.create_block(nonce, last_hash)

    print(f"*** Successfully minded a BobCoin {block}***")
    print(blockchain.chain)

def add_routes(log, app, controller: BobCoinController):
    log.info('Adding routes.')
    @app.route('/', methods=['GET'])
    @cross_origin()
    def root():
        resp = 'Welcome to Bobcoin'
        return resp, 200

    @app.route('/internals/health', methods=['GET'])
    @cross_origin()
    def health():
        resp = {
            "Status": "Healthy"
        }
        return jsonify(resp), 200

    @app.route('/block', methods=['GET'])
    def mine_block():
        return controller.mine_block()

    @app.route('/block/add_transaction', methods=['POST'])
    def add_transaction():
        return controller.add_transaction(request)

    @app.route('/chain', methods=['GET'])
    def get_chain():
        return controller.get_chain()

    @app.route('/chain/replace', methods=['POST'])
    def replace_chain():
        return controller.replace_chain()

    @app.route('/chain/verify', methods=['GET'])
    def verify_chain():
        return controller.is_valid()

    @app.route('/nodes', methods=['GET'])
    def get_nodes():
        return controller.get_nodes()

    @app.route('/nodes', methods=['POST'])
    def add_nodes():
        return controller.connect_node(request)

    return app

def create_app():
    log = Logger("Cryptocurrency BobCoin")
    log.info('Starting BobCoin.')

    flask_app = flask.Flask(__name__)
    flask_app.wsgi_app = LoggingMiddleware(log, flask_app.wsgi_app)
    ctl = get_controller(log)
    flask_app = add_routes(log, flask_app, ctl)
    CORS(flask_app)
    return flask_app


# To run in production:
# gunicorn -w 1 -b 127.0.0.1:{PORT} "app:create_app()"
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=PORT)
