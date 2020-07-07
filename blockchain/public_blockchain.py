import datetime
from block_struct import Block

class Chain:
    def __init__(self, difficulty):
        self.gen_block = gen_genesis_block()
        self.difficulty = difficulty
        self.chain = [self.gen_block]

    def gen_next_block(self, public_key, transactions):
        prev_block = self.chain[-1]
        index = prev_block.index + 1
        timestamp = datetime.timestamp(datetime.datetime.now())
        data = transactions
        hashed_block = prev_block.gen_hashed_block()
        self.chain.append(Block(index, timestamp, data, hashed_block, public_key))

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def verify_proof(self, block, proof):
        return (proof.startswith('0' * self.difficulty) and proof == block.compute_hash())

    def display_contents(self):
        for block in self.chain:
            block.disp_block_info()

    def output_ledger(self):
        main_transactions = []
        for block in self.chain:
            if block.index != 0:
                temp_transactions = block.get_block_transactions()
                for temp_transaction in temp_transactions:
                    main_transactions.append(temp_transaction)
        return main_transactions

def gen_genesis_block():
    transaction = ["XX:XX:XX:XX:XX"]
    return Block(0, datetime.datetime.now(), transaction, "0", "0")

