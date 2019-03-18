class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

    def new_block(self):
        # 추후에 블록에 대한 함수 구현 예정
        pass

    def new_transaction(self):
        # 추후에 트랜잭션 관련 함수 구현 예정
        pass

    @staticmethod
    def hash(block):
        # 추후에 해시 함수 구현 예정
        pass

    @property
    def last_block(self):
        # 마지막 블록을 보혀주는 함수 추후 구현 예정
        pass
        