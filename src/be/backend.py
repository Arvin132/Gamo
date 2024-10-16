from flask import Flask, jsonify, session, request
from flask_cors import CORS
from gamelogic import AsyncGamerunner_Match4
from agent_list import AgentsList
import numpy as np

app = Flask(__name__)
CORS(app)
global game
game: AsyncGamerunner_Match4 = None
app.secret_key = 'supersecretkey'

@app.route('/')
def home():
    return "Backend is running!"

@app.route('/get-agents-list')
def get_agents_list():
    return jsonify({"agents": AgentsList.keys_tolist()})

@app.route('/apply-move', methods=['POST'])
def apply_move():
    data = request.get_json()
    column = data.get('column')
    player_id = data.get('player-id')
    try:
        game.apply_move(column, player_id)
    except Exception as e:
        return jsonify({"message": "400 " + str(e)})
    else:
        return jsonify({"message": "200 move applied"})


@app.route('/start-game-connect4', methods=["POST"])
def start_game_connect4():
    player_1_type = request.args.get("player-1")
    player_2_type = request.args.get("player-2")
    try:
        p1 = AgentsList.all_agents[player_1_type]()
        p2 = AgentsList.all_agents[player_2_type]()
        global game
        game = AsyncGamerunner_Match4(p1, p2)
        game.start()
    except Exception as e:
        return jsonify({"message": "400 " + str(e)})
    else:
        return jsonify({"message": "200 Connect 4 Game has started"})

@app.route("/get-state-connect4", methods=["GET"])
def get_state_connect4():
    try:
        state, move = game.see_state()
    except Exception as e:
        return jsonify({"message": "400 " + str(e)})
    else:
        return jsonify({
            "message" : "200 results sent",
            "state" : {
                "board": state.board.tolist(),
                "terminal": state.terminal,
                "current_player": state.current_player,
                "winner_player": state.winner_player
            },
            "move": {
                "column": move.column,
                "player_id": move.player_id      
            }
        })
        
if __name__ == '__main__':
    app.run(port=5000, debug=True)


