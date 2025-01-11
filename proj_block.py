"""
This module contains the class Block. A block is a list of transactions. The first block is called the genesis block.
"""

import hashlib
import json
import proj_config
import proj_utils
import proj_transaction
from rich.console import Console
from rich.table import Table


class InvalidBlock(Exception):
    pass


class Block(object):
    def __init__(self, data=None):
        """
        If data is None, create a new genesis block. Otherwise, create a block from data (a dictionary).
        Raise InvalidBlock if the data are invalid.
        """
    
        if data is None:
            # Create a new genesis block with default values
            self.index = 0
            self.previous_hash = "0" * 64
            self.timestamp =  "2023-11-24 00:00:00.000000"
            self.transactions = []
            self.proof = 0
        else:
            if not isinstance(data, dict):
                raise InvalidBlock("Data must be a dictionary.")
            
            required_keys = ["index", "previous_hash", "timestamp", "transaction", "proof"]
            for key in required_keys:
                if key not in data:
                    raise InvalidBlock(f"Missing '{key}' in data dictionary.")
                
            self.index = data["index"]
            self.previous_hash = data["previous_hash"]
            self.timestamp = data["timestamp"]
            self.transaction = data["transaction"]
            self.proof = data["proof"]
            

    def next(self, transactions):
        """
        Create a block following the current block
        :param transactions: a list of transactions, i.e. a list of messages and their signatures
        :return: a new block
        """
        
        new_block = Block()
        new_block.index = self.index + 1
        new_block.previous_hash = self.hash
        new_block.timestamp = proj_utils.get_time()  # Utilisez time.strftime pour obtenir une horodatage au format souhaité
        new_block.transactions = transactions  # Stockez les transactions dans l'attribut "transactions"
        new_block.proof = 0
        
        return new_block
    
    def json_dumps(self):
        return json.dumps(self.data, sort_keys=True)
    # pass
    
    @property
    def data (self) :
        block_data = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "proof": self.proof
        }
        return block_data

    def hash(self):
        """
        Hash the current block (SHA256). The dictionary representing the block is sorted to ensure the same hash for
        two identical block. The transactions are part of the block and are not sorted.
        :return: a string representing the hash of the block
        """
        block_data = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "proof": self.proof
        }
        
        # Triez le dictionnaire pour garantir le même hachage pour des blocs identiques
        sorted_block_data = json.dumps(block_data, sort_keys=True)
        
        # Calculez le hachage SHA-256
        return hashlib.sha256(sorted_block_data.encode()).hexdigest()x
       
    #     sorted_block_data = self.json_dumps()
    #     pass


    # def __str__(self):
    #     """
    #     String representation of the block
    #     :return: str
    #     """
    #     hash_beginning = self.hash[:1]  
    #     hash_end = self.hash[-1:] 
    #     block_str = f"Index: {self.index}\n"
    #     block_str += f"Hash: {hash_beginning}...{hash_end}\n"
    #     block_str += f"Horodatage: {self.timestamp}\n"
    #     block_str += f"Nombre de transactions: {len(self.transactions)}"

    #     return block_str
    #     pass
    
#     def valid_proof(self, difficulty=config.default_difficulty):
#         """
#         Check if the proof of work is valid. The proof of work is valid if the hash of the block starts with a number
#         of 0 equal to difficulty.

#         If index is 0, the proof of work is valid.
#         :param difficulty: the number of 0 the hash must start with
#         :return: True or False
#         """
#         hashed_data = self.hash()
#         return hashed_data[:difficulty] == '0' * difficulty
#         pass

#     def mine(self, difficulty=config.default_difficulty):
#         """
#         Mine the current block. The block is valid if the hash of the block starts with a number of 0 equal to
#         config.default_difficulty.
#         :return: the proof of work
#         """
#         while not self.valid_proof() :
#             self.proof += 1
#         return self.proof
#         pass

#     def validity(self):
#         """
#         Check if the block is valid. A block is valid if it is a genesis block or if:
#         - the proof of work is valid
#         - the transactions are valid
#         - the number of transactions is in [0, config.blocksize]
#         :return: True or False
#         """
#         if self.index == 0 and self.previous_hash == "0" * 64 and self.timestamp ==  "2023-11-24 00:00:00.000000" and self.transactions == [] and self.proof == 0 :
#             return True 
#         else :
#             if self.proof == 0 and self.verif :
#                 return True
#             else : return False 
#         pass
    
#     def verif (self) :
#         cpt==0
#         for x in self.transactions :
#             if transaction.verify(x) == True :
#                 cpt+=1
#             else : return False
#         return cpt <= config.blocksize and cpt>= 0  
#         pass

#     def log(self):
#         """
#         A nice log of the block
#         :return: None
#         """
#         table = Table(
#             title=f"Block #{self.index} -- {self.hash()[:7]}...{self.hash()[-7:]} -> {self.previous_hash[:7]}...{self.previous_hash[-7:]}")
#         table.add_column("Author", justify="right", style="cyan")
#         table.add_column("Message", style="magenta", min_width=30)
#         table.add_column("Date", justify="center", style="green")

#         for t in self.transactions:
#             table.add_row(t.author[:7] + "..." + t.author[-7:], t.message, t.date[:-7])

#         console = Console()
#         console.print(table)


# def test():
#     from ecdsa import SigningKey
#     from transaction import Transaction
#     sk = SigningKey.generate()
#     transactions = [Transaction(f"Message {i}") for i in range(10)]
#     for t in transactions:
#         t.sign(sk)

#     Transaction.log(transactions)

#     blocks = [Block()]
#     for i in range(5):
#         blocks.append(blocks[-1].next(transactions[i * 2:(i + 1) * 2]))
#         blocks[-1].mine()

#     for b in blocks:
#         b.log()


# if __name__ == '__main__':
#     print("Test Block")
#     #test()

