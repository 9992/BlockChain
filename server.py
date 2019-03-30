#-*-coding:utf-8

import Blockchain
import json
from uuid import uuid4
from flask import Flask, jsonify, request 

chain = Blockchain.Blockchain()
app = Flask(__name__)

node_identifier = str(uuid4()).replace('-','')

@app.route('/contents/new', methods=['POST'])
def new_contents():
    values = request.get_json()

    required = ['user_id', 'contents_number', 'contents_title', 'contents_main']

    if not all(k in values for k in required):
        return 'Missing Values', 400

    index = chain.new_contents(values['user_id'],values['contents_number'],values['contents_title'],values['contents_main'])

    response = { 'message' : f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/upload', methods = ['POST'])
def upload():
    last_block = chain.last_block
    last_proof = last_block['proof']
    proof = chain.proof_of_work(last_proof)

    chain.new_contents(
        user_id = "User ID",
        contents_number = "contents_number",
        contents_title = "contents_title",
        contents_main = "contents_main"
    )

    previous_hash = chain.hash(last_block)
    block = chain.new_block(proof, previous_hash)

    response = {    
        'index' : block['index'],
        'proof' : block['proof'],
        'previous_hash': block['previous_hash'],
        'transactions' : block['transactions'],
    }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain' : chain.chain,
        'length' : len(chain.chain),
    }

    return jsonify(response),200

@app.route('/nodes/register', methods=['POST'])
def register_node():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        chain.register_node(node)

    response = {
        'message' : 'New nodes have been added',
        'total_nodes' : list(chain.nodes)
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = chain.resolve_conflicts()

    if replaced:
        response ={
            'message' : 'Chain is replaced',
            'new_chain' : chain.chain
        }
    else:
        response ={
            'message' : 'authoritative',
            'new_chain' : chain.chain
        }

    return jsonify(response), 200


if __name__=="__main__":
    from argparse import ArgumentParser
    
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port= 5000)