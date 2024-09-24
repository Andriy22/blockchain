from flask import Flask, jsonify, request

from blockchain.blockchain import Blockchain, Block

app = Flask(__name__)

AAV_last_name = "Aleksandruk"
AAV_birth_nonce = "27082002"
AAV_birth_month = "08"
AAV_birth_day = 27,

AAV_genesis_data = []

AAV_blockchain = Blockchain(AAV_genesis_data, AAV_birth_month, AAV_birth_nonce, AAV_last_name, AAV_birth_day)

@app.route('/transactions/new', methods=['POST'])
def AAV_new_transaction():
  values = request.get_json()

  required = ['sender', 'recipient', 'amount']
  if not all(k in values for k in required):
    return "Missing values", 400
  
  index = AAV_blockchain.AAV_add_transaction(values['sender'], values['recipient'], values['amount'])

  response = {'message': f'Transaction will be added to Block {index}'}
  return jsonify(response), 201

@app.route('/mine', methods=['POST'])
def AAV_mine():
  values = request.get_json()

  if not values:
    return jsonify({'message': 'No input data provided'}), 400
  
  miner_address = values.get('miner_address')
  if not miner_address:
    return jsonify({'message': 'Missing miner_address'})

  new_block = AAV_blockchain.AAV_mine_block(miner_address)

  response = {
        'message': 'New Block Mined',
        'index': new_block.AAV_index,
        'transactions': new_block.AAV_transactions,
        'nonce': new_block.AAV_nonce,
        'hash': new_block.AAV_hash,
        'previous_hash': new_block.AAV_previous_hash,
    }
  return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def AAV_full_chain():
  chain = AAV_blockchain.AAV_get_chain()
  response = {
    'chain': chain,
    'length': len(chain)
  }
  return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def AAV_rigster_node(): 
  values = request.get_json()
  
  nodes = values.get('nodes')

  if nodes is None:
    return "Error: Please supply a valid list of nodes", 400
  
  for node in nodes:
    AAV_blockchain.AAV_register_node(node)

  response = {
    'message': 'New nodes have been added',
    'total_nodes': list(AAV_blockchain.AAV_nodes)
  }

  return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def AAV_consensus():
  replaced = AAV_blockchain.AAV_consensus()

  if replaced:
    response = {
      'message': 'Our chain was replaced',
      'new_chain': AAV_blockchain.AAV_get_chain()
    }
  else:
    response = {
      'message': 'Our chain is authoritative',
      'chain': AAV_blockchain.AAV_get_chain()
    }

  return jsonify(response), 200

@app.route('/blocks/new', methods=['POST'])
def AAV_receive_new_block():
  values = request.get_json()

  required = ['index', 'timestamp', 'transactions', 'previous_hash', 'nonce', 'hash']

  if not all(k in values for k in required):
    return "Missing values", 400
  
  block = Block(values['index'], values['timestamp'], values['transactions'], values['previous_hash'], values['nonce'])
  block.AAV_hash = values['hash']

  last_block = AAV_blockchain.AAV_last_block()
  if block.AAV_previous_hash != last_block.AAV_hash:
    return 'Invalid block: Previous hash does not match.', 400
  
  if not block.AAV_hash.endswith(AAV_blockchain.AAV_birth_month):
    return 'Invalid block: Proof of Work is incorrect.', 400
  
  AAV_blockchain.AAV_chain.append(block)

  print(f"Новий блок отримано та додано: {block.AAV_index}")

  return jsonify({'message': 'New block received and added to the chain.'})

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3000)
