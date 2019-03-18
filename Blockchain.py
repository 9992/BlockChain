import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = []

        # 제네시스 블록 생성
        self.new_block(previous_hash=1, proof=100)



    def new_block(self,proof, previous_hash=None):
        """
            proof 는 pow 알고리즘의 의해서 제공됨
            previous_hash 앞선 블록의 해시 값, 이를 통해 체인 연결이 됨
            return <dict> 새로운 블럭, 딕셔너리 타입은 대응 관계를 나타내는 자료형을 가짐
        """
        block = {
            'index' : len(self.chain) + 1,
            'timestamp' : time(),
            'trasactions' :self.current_transactions,
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
