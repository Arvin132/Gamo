from flask import Flask, jsonify, session, request
from flask_cors import CORS
from gamelogic import Gamerunner_Match4
import numpy as np

app = Flask(__name__)
CORS(app)
app.secret_key = 'supersecretkey'

game_runner = Gamerunner_Match4()

# Define a route for the root URL
@app.route('/start-connect4')
def start_connect_4():
    game_runner.run()


@app.route('/')
def home():
    return "Backend is running!"

@app.route('/get-agents-list')
def get_agents_list():
    return jsonify({"agents": ["Humen", "Random Agent",  "First Move Agent"]})

# Define a route for an API endpoint
@app.route('/get-board', methods=['GET'])
def get_board():
    return jsonify({"board": np.ones((8, 8)).tolist()})

@app.route('/apply-move', methods=['POST'])
def apply_move():
    raise NotImplemented(" Not Implemented YET: apply_move")
    return


if __name__ == '__main__':
    app.run(port=5000, debug=True)


