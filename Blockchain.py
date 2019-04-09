import hashlib
import json
import requests
import datetime
from uuid import uuid4
from time import time
from urllib.parse import urlparse
import merkle


# 새로 구성해야하기 때문에
# 원본 파일 복사 내용을 지움
class Blockchain(object):
   def __init__(self):
      self.merkle_root = ''
      self.merkle_hash = []
      self.current_transactions = []
      self.chain = []
      self.nodes = set()
      
      self.new_block(previous_hash='NULL',proof='241152154') # 제네시스 블럭

   def genesis_block(self):
      return self.chain[0]

   def new_block(self,proof,previous_hash=None):
      block = {
         'index' : len(self.chain)+1,
         'timestamp' : str(datetime.datetime.now()),
         'proof' : proof,
         'previous_hash' : previous_hash or self.hash(self.chain[-1]),
         'merkle_root' : "None" if len(self.merkle_hash)==0 else merkle.merkle(self.merkle_hash),
         'transactions' : [{'user_id' : "None",'contents_title' : "None",'contents_main' : "None"}] if len(self.current_transactions) == 0 else self.current_transactions
      }
      self.current_transactions = []
      self.merkle_hash = []
      self.chain.append(block)
      return block

   def new_contents(self,user_id,contents_title,contents_main):
      self.current_transactions.append({
         'user_id' : user_id,
         'contents_title' : contents_title,
         'contents_main' : hashlib.sha256(contents_main.encode()).hexdigest(),
      })
      u_i = hashlib.sha256(user_id.encode()).hexdigest()
      c_t = hashlib.sha256(contents_title.encode()).hexdigest()
      c_m = hashlib.sha256(contents_main.encode()).hexdigest()
      append_data = hashlib.sha256((u_i+c_t+c_m).encode()).hexdigest()
      print(type(append_data))
      print(append_data)
      self.merkle_hash.append(append_data)
      
      return self.last_block['index'] + 1

   @staticmethod
   def hash(block):
      block_str = json.dumps(block, sort_keys=True).encode()
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
      return guess_hash[:6] == "000000" 
      # 난이도 조절 부분

   def register_node(self, address):
      parsed_url = urlparse(address)
      if parsed_url.netloc:
         self.nodes.add(parsed_url.netloc)
      elif parsed_url.path:
         self.nodes.add(parsed_url.path)
      else:
         raise ValueError('Invalid URL')

   def valid_chain(self, chain):
      last_block = chain[0] 
      current_index =1

      while current_index < len(chain):
         block = chain[current_index]
         print(f'{last_block}')
         print(f'{block}')
         print("\n--------------\n")

         if block['previous_hash'] != self.hash(last_block):
            return False
         
         if not self.valid_proof(last_block['proof'],block['proof']):
            return False
         
         last_block = block
         current_index += 1

      return True

   def resolve_conflicts(self):
      neighbours = self.nodes
      new_chain = None

      max_length = len(self.chain)

      for node in neighbours:
         response = requests.get(f'http://{node}/chain') 

         if response.status_code == 200:
            length = response.json()['length']
            chain = response.json()['chain']

            if length > max_length and self.valid_chain(chain):
               max_length = length
               new_chain = chain

         if new_chain:
            self.chain = new_chain
            return True

         return False
