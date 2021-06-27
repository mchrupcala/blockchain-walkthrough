import hashlib
import json
from time import time
from flask import Flask,request,render_template

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        self.new_block(previous_hash="The Times 03/Jan/2009 Chancellor on brink of second bailout for banks.", proof=100)


    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)

        return block


    @property
    def last_block(self):
        return self.chain[-1]

    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)

        return self.last_block['index'] + 1


    def hash(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash

def main():
    blockchain = Blockchain()
    t1 = blockchain.new_transaction("Satoshi", "Mike", '5 BTC')
    t2 = blockchain.new_transaction("Mike", "Satoshi", '1 BTC')
    t3 = blockchain.new_transaction("Satoshi", "Hal Finney", '5 BTC')
    blockchain.new_block(12345)

    t4 = blockchain.new_transaction("Mike", "Alice", '1 BTC')
    t5 = blockchain.new_transaction("Alice", "Bob", '0.5 BTC')
    t6 = blockchain.new_transaction("Bob", "Mike", '0.5 BTC')
    blockchain.new_block(6789)

    app = Flask(__name__)
    @app.route('/', methods=['GET'])
    def index():
        return "<h2 align=center>walkthrough.py.    'GET /chain' to get the current chain</h2>"

    @app.route('/chain', methods=['GET'])
    def get_chain():
        chain_data = blockchain.chain
        response_dict = {"length": len(chain_data), "chain": chain_data}
        if request.mimetype == "application/json":
            return json.dumps(response_dict)
        else:
            response_json_pretty = json.dumps(response_dict, sort_keys=True, indent=4)
            return render_template('pretty_json.html', title="chain", json_pretty=response_json_pretty)

    app.run(debug=True, port=8080)

if __name__ == "__main__":
    main()
