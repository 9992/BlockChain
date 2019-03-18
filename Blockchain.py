#-*- coding:utf-8 -*-

import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request 


class Blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = []

        """ 제네시스 블록 생성 """
        self.new_block(previous_hash=1, proof=100)



    def new_block(self, proof, previous_hash=None):
        """
            proof 는 pow 알고리즘의 의해서 제공됨
            previous_hash 앞선 블록의 해시 값, 이를 통해 체인 연결이 됨
            return <dict> 새로운 블럭, 딕셔너리 타입은 대응 관계를 나타내는 자료형을 가짐
        """
        block = {
            'index' : len(self.chain) + 1,
            'timestamp' : time(),
            'transactions' :self.current_transactions,
            'proof' : proof,
            'previous_hash' : previous_hash or self.hash(self.chain[-1])
        }

        # 거래내역 초기화.
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self,sender,recipient,amount):
        
        """
            거래를 하기 위한 부분
            sender 변수는 보내는 사람의 주소
            recipient 변수는 받는 사람의 주소
            amount 변수는 양 -> 추후 데이터로 변경해볼 예정
            return 값은 이 거래를 포함할 블록의 index 값
        """
        self.current_transactions.append({
            'sender' : sender,
            'recipient' : recipient,
            'amount' : amount,
        })

        return self.last_block['index'] + 1

    """
        staticmethod와 classmethod는 자료 찾아야함
    """

    @staticmethod
    def hash(block):
        # 추후에 해시 함수 구현 예정
        """
        우선은 Sha-256 으로 만들 예정
        """
        block_string = json.dumps(block,sort_keys = True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # 마지막 블록을 보혀주는 함수 추후 구현 예정
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
            POW 알고리즘
            - 앞에서 0의 개수가 4개 나오는 hash(pp`)를 만족시키는 p`를 찾는 것
            - p는 이전블록의 proof 값 , p`는 새로운 블록의 proof 값
            input : <int>
            return : <int>
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof,proof):
        """
            Proof 검증 방법
            hash(last_proof,proof) 의 값이 앞의 4자리가 0인지 확인
            난이도를 올리기 위해서는 0의 갯수만 변경
            input ( 둘다 <int> )
            return <bool>
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()
    
@app.route('/transactions/new', methods =['POST'])
def new_transaction():
    values = request.get_json()
    
    # 요청된 필드가 POST 된 데이터인지 확인하는 
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    
    # 새로운 거래 생성
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    
    response = {'message' : f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/mine', methods = ['GET'])
def mine():
    #다음 블록의 proof 값을 얻어내기 위해 POW 알고리즘을 수행한다. 
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    
    #proof 값을 찾으면(채굴에 성공하면) 보상을 준다.
    #sender의 주소를 0으로 한다. (원래 거래는 송신자, 수신자가 있어야 하는데 챌굴에 대한 보상으로 얻은 코인은 sender 가 없다.)
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )
    
    #
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    
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
    'chain' : blockchain.chain,
    'length' : len(blockchain.chain),
    }

    return jsonify(response),200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port= 5000)