from app.view.account import Account
import json
import requests
import socket
import os
from uuid import getnode as get_mac
from app import app
import flask

from .net import Net
from .wallet import Wallet
from .blockchain import Blockchain
from .transaction import Transaction
import jsonpickle

port = 5000
port_str = ':' + str(port)
blockchain = Blockchain()
wallet = Wallet().read_signing_key()

script_dir = os.path.dirname(__file__)
# peers_dir = os.path.join(script_dir, 'peers.pkl')

server_url = 'http://192.168.0.15:8080'

ip_address = requests.get('https://api.ipify.org').text
mac_address = str(get_mac())
private_ip_address = socket.gethostbyname(socket.gethostname())
# net = Net(ip_address, private_ip_address, str(uuid4()).replace('-', ''))

def set_blockchain_from_pickle(pickle):
    blockchain = jsonpickle.decode(pickle)
    blockchain.___class___ = Blockchain
    blockchain.save_blockchain_on_disk()   

def connect_node():
    response = requests.post(server_url + '/connect_node', json = {'peer_id': mac_address, 'peer_ip': ip_address})
    peers = json.loads(response.text)['peers']
    return peers

peers = connect_node()

def check_peer_availability(host, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        return False

def get_first_peer():
    peer_pairs = iter(peers.items())
    first_peer = {}

    while True:
        first_peer = next(peer_pairs)
        if (first_peer[0] != mac_address and first_peer[1] != ip_address and check_peer_availability(first_peer[1])):
            break
    return first_peer

next_peer = get_first_peer()

res = requests.get('http://' + next_peer[1] + port_str + '/get_blockchain')
set_blockchain_from_pickle(res.text)

requests.post(next_peer[1] + port_str + '/connect_node', json = {'peer_id': mac_address, 'peer_ip': ip_address})

def validate_route(request: flask.Request):
    if request.remote_addr != ip_address:
        flask.abort(403)    

def sync_first_peer():
    next_peer = get_first_peer()
    bc = jsonpickle.encode(blockchain)
    requests.post('http://' + next_peer[1] + port_str + '/sync_blockchain', json = {'peer_id': mac_address, 'peer_ip': ip_address, 'blockchain': bc})

def get_next_peer(peer_pairs):
    reached_current = False
    peer_pairs = iter(peers.items())
    next_peer = None
    for index, item in enumerate(peer_pairs):
        if item[0] == mac_address and check_peer_availability(item[1]):
            next_peer = next(peer_pairs, index + 1)
            reached_current = True
            break
        if reached_current == True and check_peer_availability(item[1]):
            next_peer = next(peer_pairs, index)
            break
    return next_peer

@app.route('/connect_node', methods = ['POST'])
def connect_node():
    request = flask.request.get_json()
    request_peer = {'peer_id': request['peer_id'], 'peer_ip': request['peer_ip']}
    next_peer = get_next_peer()
    if next_peer == None and next_peer.mac_address != request_peer['peer_id']:
        return
    requests.post(next_peer['peer_ip'] + port_str + '/connect_node', json = request_peer)

@app.route('/get_blockchain', methods = ['GET'])
def get_blockchain():
    return jsonpickle.encode(blockchain), 201


@app.route('/get_accounts', methods = ['GET'])
def get_accounts():
    addresses = []
    accounts = []
    for block in blockchain.chain:
        addresses += list(map(lambda t: t.from_address, block.transaction))
        addresses += list(map(lambda t: t.to_address, block.transaction))

    addresses = list(set(addresses))

    for address in addresses:
        if address == '':
            continue
        balance = blockchain.get_balance_of_address(address)
        accounts.append(Account(address, balance))

    return json.dumps(accounts, default=lambda value: value.__dict__), 201

@app.route('/create_wallet', methods = ['POST'])
def create_wallet():
    validate_route()
    wallet._generate_signing_key()
    return flask.jsonify(), 201

@app.route('/load_wallet', methods = ['POST'])
def load_wallet():
    validate_route()
    wallet.read_signing_key()
    return flask.jsonify(), 201

    
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    request = flask.request.get_json()
    if wallet.signingKey == None:
        return flask.jsonify({'message': f'error_wallet_not_generated'}), 400
    blockchain.add_transaction(wallet.signingKey, request['receiver'], request['amount'])
    return flask.jsonify({'message': f'transaction_added_succesfully'}), 201

@app.route('/mine_block', methods = ['POST'])
def mine_block():
    if wallet.signingKey == None:
        return flask.jsonify({'message': f'error_wallet_not_generated'}), 400
    blockchain.mine_block(wallet.signingKey)
    sync_first_peer()
    return flask.jsonify({'message': f'transaction_added_succesfully'}), 201

@app.route('/sync_blockchain', methods = ['POST'])
def sync_blockchain():
    request = flask.request.get_json()
    request_peer = {'peer_id': request['peer_id'], 'peer_ip': request['blockchain'], 'blockchain': request['blockchain']}
    set_blockchain_from_pickle(request['blockchain'])
    next_peer = get_next_peer()
    if next_peer == None and next_peer.mac_address != request_peer['peer_id']:
        return
    requests.post(next_peer['peer_ip'] + port_str + '/sync_blockchain', data = request_peer['blockchain'])

