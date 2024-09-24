from .block import Block

import json
from hashlib import sha256
import requests
import time

class Blockchain:
  def __init__(self, genesis_data, birth_month, birth_nonce, last_name, mining_reward):
    self.AAV_chain = []
    self.AAV_current_transactions = []
    self.AAV_birth_month = birth_month
    self.AAV_last_name = last_name
    self.AAV_mining_reward = mining_reward
    self.AAV_nodes = set()
    self.AAV_create_genesis_block(genesis_data, birth_nonce)

  def AAV_create_genesis_block(self, genesis_data, birth_nonce):
    genesis_block = Block(1, time.time(), genesis_data, self.AAV_last_name, birth_nonce)
    self.AAV_chain.append(genesis_block)
    print("Генезис-блок створено:")
    self.AAV_print_block(genesis_block)

  # def AAV_add_block(self, data):
  #   previous_block = self.AAV_chain[-1]
  #   new_block = Block(previous_block.AAV_index + 1, time.time(), data, previous_block.AAV_hash)
  #   self.AAV_proof_of_work(new_block)
  #   self.AAV_chain.append(new_block)
  #   print(f"Блок {new_block.AAV_index} додано:")
  #   self.AAV_print_block(new_block)  

  def AAV_proof_of_work(self, block):
    print(f"Починається Proof of Work для блоку {block.AAV_index}...")
    while not block.AAV_hash.endswith(self.AAV_birth_month):
      block.AAV_increment_nonce()
      block.AAV_hash = block.AAV_calculate_hash_block()
    print(f"Proof of Work завершено для блоку {block.AAV_index}. Nonce: {block.AAV_nonce}")

  def AAV_print_chain(self):
    for block in self.AAV_chain:
      self.AAV_print_block(block)

  def AAV_add_transaction(self, sender, recipient, amount):
    transaction = {
      'sender': sender,
      'recipient': recipient,
      'amount': amount
    }

    self.AAV_current_transactions.append(transaction)
    print(f"Транзакція додана: {transaction}")
    return self.AAV_last_block().AAV_index + 1
  
  def AAV_last_block(self):
    return self.AAV_chain[-1]
  
  def AAV_mine_block(self, miner_address):
    self.AAV_add_transaction(sender=None, recipient=miner_address, amount=self.AAV_mining_reward)

    prev_block = self.AAV_last_block()
    new_block = Block(prev_block.AAV_index + 1, time.time(), self.AAV_current_transactions.copy(), prev_block.AAV_hash)
    
    self.AAV_proof_of_work(new_block)

    self.AAV_chain.append(new_block)
    print(f"Блок {new_block.AAV_index} майнено:")
    self.AAV_print_block(new_block)

    self.AAV_current_transactions = []

    self.AVV_broadcast_new_block(new_block)

    return new_block

  def AAV_get_chain(self):
    chain_data = []

    for block in self.AAV_chain:
        block_data = {
          'index': block.AAV_index,
          'timestamp': block.AAV_timestamp,
          'transactions': block.AAV_transactions,
          'previous_hash': block.AAV_previous_hash,
          'nonce': block.AAV_nonce,
          'hash': block.AAV_hash
        }
        chain_data.append(block_data)
    return chain_data
  
  def AAV_register_node(self, address):
    parsed_url = address
    if not parsed_url.startswith('http://') and not parsed_url.startswith('https://'):
      parsed_url = f'https://{address}'
    self.AAV_nodes.add(parsed_url)
    print(f"Вузол зареєстровано: {parsed_url}")

  def AAV_consensus(self):
    neighbours = self.AAV_nodes
    new_chain = None

    max_length = len(self.AAV_chain)

    for node in neighbours:
      try:
          response = requests.get(f'{node}/chain')
          if response.status_code == 200:
            length = response.json()['length']
            chain = response.json()['chain']

            if length > max_length and self.AAV_is_valid_chain(chain):
              max_length = length
              new_chain = chain
      except requests.exceptions.RequestException as e:
        print(f"Не вдалося зв'язатися з вузлом {node}: {e}")

      if new_chain:
        self.AAV_chain = []
        for block_data in new_chain:
          block = Block(
          index=block_data['index'],
          timestamp=block_data['timestamp'],
          transactions=block_data['transactions'],
          previous_hash=block_data['previous_hash'],
          nonce=block_data['nonce'])
          
          block.AAV_hash = block_data['hash']
          self.AAV_chain.append(block)
        print("Локальний ланцюг був замінений на новий довший ланцюг.")
        return True

      print("Локальний ланцюг є найбільш довгим. Заміна не потрібна.")
      return False


  def AVV_broadcast_new_block(self, block):
    for node in self.AAV_nodes:
      try:
          response = requests.post(f"{node}/blocks/new", json = {
            'index': block.AAV_index,
            'timestamp': block.AAV_timestamp,
            'transactions': block.AAV_transactions,
            'previous_hash': block.AAV_previous_hash,
            'nonce': block.AAV_nonce,
            'hash': block.AAV_hash
          })
          if response.status_code != 201:
            print(f"Не вдалося надіслати блок до вузла {node}. {response.text}")
      except requests.exceptions.RequestException as e:
        print(f"Не вдалося зв'язати з вузлом {node}: {e}")


  def AAV_is_valid_chain(self, chain):
    if not chain:
      return False

    genesis = chain[0]
    if genesis['previous_hash'] != self.AAV_last_name:
      return False
    if genesis['nonce'] != self.AAV_last_nonce(genesis['index']):
      return False

    for i in range(1, len(chain)):
      previous = chain[i - 1]
      current = chain[i]

      if current['previous_hash'] != previous['hash']:
        return False

      block_string = json.dumps({
        'index': current['index'],
        'timestamp': current['timestamp'],
        'transactions': current['transactions'],
        'previous_hash': current['previous_hash'],
        'nonce': current['nonce']
        }, sort_keys=True).encode()
      
      calculated_hash = sha256(block_string).hexdigest()
      if calculated_hash != current['hash']:
        return False

      if not current['hash'].endswith(self.AAV_birth_month):
        return False

      return True


  def AAV_last_nonce(self, index):
    for block in self.AAV_chain:
      if block.AAV_index == index:
        return block.AAV_nonce
    return None

  @staticmethod
  def AAV_print_block(block):
    print(f"Індекс: {block.AAV_index}")
    print(f"Час: {time.ctime(block.AAV_timestamp)}")
    print(f"Транзакції: {block.AAV_transactions}")
    print(f"Попередній Хеш: {block.AAV_previous_hash}")
    print(f"Nonce: {block.AAV_nonce}")
    print(f"Хеш: {block.AAV_hash}")
    print("-" * 30)
