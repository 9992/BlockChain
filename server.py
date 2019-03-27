import Blockchain
from uuid import uuid4
from flask import Flask, jsonify, request 

chain = Blockchain.Blockchain()

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-','')

@app.route('/new_contents/new', methods=['POST'])
def new_conteSEnts():
    values = request.get_json()

    required = ['contents_number','contents_title','user_id','contents_main']
    if not all(k in values for k in required):
        return 'Missing Values',400

    index = chain.new_contents(values['contents_number'],values['recipient'],values['user_id'],values['contents_main'])

    response = { 'message' : f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/upload', methods = ['GET'])
def upload():
    last_block = chain.last_block
    last_proof = last_block['proof']
    proof = chain.proof_of_work(last_proof)

    chain.new_contents(
        contents_number = "!!! 여기에 글 번호가 들어오게 !!",
        contents_title = "!!! 여기에 글 제목이 들어오게 !!",
        user_id = 12345979,
        contents_main = "!!!여기에는 그냥 글 내용이 나오게, 글 내용은 인스턴스를 내부의 함수를 통해 해시화 된다. !!",
    )

    previous_hash = chain.hash(last_block)
    block = chain.new_block(proof, previous_hash)

    response = {
        'message' : "New Block Forged",
        'index' : block['index'],
        'transactions' : block['transactions'],
        'proof' : block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
    'chain' : chain.chain,
    'length' : len(chain.chain),
    }

    return jsonify(response),200


if __name__=="__main__":
    from argparse import ArgumentParser
    
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port= 5000)