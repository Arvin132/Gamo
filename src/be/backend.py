from flask import Flask, jsonify, request, session
from flask_cors import CORS
from gamelogic import AsyncGamerunner_Match4
from agent_list import AgentsList
import json


app = Flask(__name__)
CORS(app)
global game_runner
game_runner: AsyncGamerunner_Match4 = None
app.secret_key = 'supersecretkey'


def init_session():
    if 'connect4_games' not in session:
        session['connect4_games'] = {}
    if 'connect4_next_game_id' not in session:
        session['connect4_next_game_id'] = 1 
        
        
@app.route('/')
def home():
    return "Backend is running!"

@app.route('/get-agents-list')
def get_agents_list():
    return jsonify({"agents": AgentsList.keys_tolist(), "humen-agent": AgentsList.humen_agent})

@app.route('/start-game-connect4', methods=["POST"])
def start_game_connect4():
    init_session()
    data = request.get_json()
    
    try:
        player_1_type = data.get("player-1")
        player_2_type = data.get("player-2")
        p1 = AgentsList.all_agents[player_1_type]()
        p2 = AgentsList.all_agents[player_2_type]()
        # global game_runner
        game_runner = AsyncGamerunner_Match4(p1, p2)
        game_runner.start()
        
        # store game runner data in session variable
        game_data = {
            "game_runner": game_runner.to_dict(),
            "player_1_type": player_1_type,
            "player_2_type": player_2_type
        }
        game_id = session["connect4_next_game_id"]
        session["connect4_next_game_id"] += 1
        session["connect4_games"][game_id] = json.dump(game_data)
        return jsonify({"message": "200 Connect 4 Game has started", "game-id": game_id})
    
    except Exception as e:
        return jsonify({"message": "400 " + str(e)})
        

@app.route("/get-state-connect4", methods=["GET"])
def get_state_connect4():
    try:
        
        return jsonify(game_runner.to_dict())
    except Exception as e:
        return jsonify({"message": "400 " + str(e)})
        

@app.route('/apply-move', methods=['POST']) 
def apply_move():
    data = request.get_json()
    column = data.get('column')
    player_id = data.get('player-id')
    try:
        game_runner.apply_move(column, player_id)
    except Exception as e:
        return jsonify({"message": "400 " + str(e)})
    else:
        return jsonify({"message": "200 move applied"})
     
if __name__ == '__main__':
    app.run(port=5000, debug=True)


