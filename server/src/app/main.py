import flask
from app import app
import os
from app import crypto

peers = []

@app.route('/connect_node', methods = ['POST'])
def connect_node():
    request = flask.request.get_json()
    peers = {}
    if os.path.isfile("peers.bin"):
        peers = crypto.decode('peers')

    peers[request["peer_id"]] = request["peer_ip"]
    crypto.encode(peers, 'peers')

    return flask.jsonify({'peers': peers}), 201 

