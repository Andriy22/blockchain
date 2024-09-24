import hashlib
import json

class Block:
  # def __init__(self, index, timestamp, data, transactions, previous_hash, nonce = 0):
  #   self.AAV_index = index
  #   self.AAV_timestamp = timestamp
  #   self.AAV_data = data
  #   self.AAV_previous_hash = previous_hash
  #   self.AAV_nonce = nonce
  #   self.AAV_transactions = transactions
  #   self.AAV_hash = self.AAV_calculate_hash_block()

  def __init__(self, index, timestamp, transactions, previous_hash, nonce = 0):
    self.AAV_index = index
    self.AAV_timestamp = timestamp
    self.AAV_previous_hash = previous_hash
    self.AAV_nonce = nonce
    self.AAV_transactions = transactions
    self.AAV_hash = self.AAV_calculate_hash_block()


  # def AAV_calculate_hash_block(self):
  #   AAV_block_string = f"{self.AAV_index}{self.AAV_timestamp}{self.AAV_previous_hash}{self.AAV_nonce}"
  #   return hashlib.sha256(AAV_block_string.encode()).hexdigest()

  def AAV_calculate_hash_block(self):
    AAV_block_string = json.dumps({
      'index': self.AAV_index,
      'timestamp': self.AAV_timestamp,
      'transactions': self.AAV_transactions,
      'previous_hash': self.AAV_previous_hash,
      'nonce': self.AAV_nonce
    }, sort_keys=True).encode()
    return hashlib.sha256(AAV_block_string).hexdigest()
  
  def AAV_increment_nonce(self):
    self.AAV_nonce +=1

    