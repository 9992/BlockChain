import hashlib
import json
import time

# 새로 구성해야하기 때문에
# 원본 파일 복사 내용을 지움
class Blockchain(object):
    def __init__(self):
       self.current_tractions = []
       self.chain = []

    def new_block(self,contents_number,contents_title,user_id,contents_main,previous_hash=None):

