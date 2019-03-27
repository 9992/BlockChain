import hashlib
import json
from time import time

# 새로 구성해야하기 때문에
# 원본 파일 복사 내용을 지움
class Blockchain(object):
   def __init__(self):
      self.current_transactions = []
      self.chain = []
      self.new_block(previous_hash=1,proof=100)
   
   def new_block(self,proof,previous_hash=None):
      block = {
         'index' : len(self.chain) + 1,
         'timestamp' : time(),
         'transactions' :self.current_transactions,
         'proof' : proof,
         'previous_hash' : previous_hash or self.hash(self.chain[-1])
      }
      self.current_transactions = []

      self.chain.append(block)
      return block

   def new_contents(self,contents_number,contents_title,user_id,contents_main):
      self.current_transactions.append({
         'contents_number':contents_number,
         'contents_title' :contents_title,
         'user_id':user_id,
         'contents_main':contents_main,
      }
      )

      return self.last_block['index'] + 1

   @staticmethod
   def hash(block):
      # 이게 뭐하는 함수인지 모르겠다.
      block_str = json.dumps(block,sort_keys = True).encode()
      return hashlib.sha256(block_str).hexdigest()

   # @property 
   @property
   def last_block(self):
      return self.chain[-1]

   def proof_of_work(self,last_proof):
      proof = 0
      while self.valid_proof(last_proof,proof) is False:
         proof += 1

      return proof
   
   @staticmethod
   def valid_proof(last_proof,proof):
      guess = f'{last_proof}{proof}'.encode()
      guess_hash = hashlib.sha256(guess).hexdigest()
      return guess_hash[:4] =="0000" 
      # 난이도 조절 부분