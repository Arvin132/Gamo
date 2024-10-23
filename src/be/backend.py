from flask import Flask, jsonify, request, session
from flask_cors import CORS
from gamelogic import AsyncGamerunner_Match4
from agent_list import AgentsList
from db import init_database, initilize_app, User, db
import argparse
import json

# this section is only for argument parsing

parser = argparse.ArgumentParser(description=" This is Gamo Backend getting ready to accept requests")

parser.add_argument("--init-db", action="store_true", help="used when one wants to initilize the database, the first time running the backend")
args = parser.parse_args()



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)


app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "supersecretkey"

gamo_key = 8569
initilize_app(app)
if (args.init_db):
    print("trying to create the database")
    init_database(app)
    
    

@app.route('/')
def home():
    return "Backend is running!"

@app.route('/connect4')
def connect4_home():
    return "Connect4 is ready to be accessed"

@app.route('/connect4/agents')
def get_agents_list():
    return jsonify({"agents": AgentsList.keys_tolist(), "humen-agent": AgentsList.human_agent})


@app.route('/connect4/start', methods=["POST"])
def start_game_connect4():
    data = request.get_json()
    
    try:
        player_1_type = data.get("player-1")
        player_2_type = data.get("player-2")
        p1 = AgentsList.all_agents[player_1_type]()
        p2 = AgentsList.all_agents[player_2_type]()
        game_runner = AsyncGamerunner_Match4(p1, p2)
        game_runner.start()
        
        # store game runner data in session variable
        game_data = {
            "game_runner": game_runner.to_dict(),
            "player_1_type": player_1_type,
            "player_2_type": player_2_type
        }
        session["connect4_game"] = json.dumps(game_data)
        return jsonify({"message": "200 Connect 4 Game has started"})
    
    except Exception as e:
        return jsonify({"message": "400 " + str(e)})
        

@app.route("/connect4/state", methods=["GET"])
def get_state_connect4():
    try:
        game_data = json.loads(session["connect4_game"])
        dict = game_data["game_runner"]
        dict["players"] = {"player-1": game_data["player_1_type"], "player-2": game_data["player_2_type"]}
        dict["message"] = "200 data was sent"
        return jsonify(dict)
    except Exception as e:
        return jsonify({"message": "400 " + str(e)})       

@app.route('/connect4/apply-move', methods=['POST']) 
def apply_move():
    data = request.get_json()
    column = data.get('column')
    player_id = data.get('player-id')
    is_bot = data.get('is-bot')
    game_data = json.loads(session["connect4_game"])
    p1 = AgentsList.all_agents[game_data["player_1_type"]]()
    p2 = AgentsList.all_agents[game_data["player_2_type"]]()
    game_runner = AsyncGamerunner_Match4(p1, p2)
    game_runner.from_dict(game_data["game_runner"])
    try:
        game_runner.apply_move(column, player_id, is_bot)
        # store game runner data in session variable
        game_data["game_runner"] = game_runner.to_dict()
        session["connect4_game"] = json.dumps(game_data)
    except Exception as e:
        return jsonify({"message": "400 " + str(e)})
    else:
        return jsonify({"message": "200 move applied"})
    
@app.route('/user/get-few', methods=['GET'])
def get_few_users():
    users = User.query.limit(5).all()
    users_reponse ={ "users": [{"id": user.id, "username": user.username} for user in users] }
    return jsonify(users_reponse)

@app.route('/user/get', methods=['GET'])
def get_user():
    user_id = request.get_json().get('id')
    target = db.session.get(User, user_id)
    if (target is None):
        return jsonify({"message" : "no user with the given id: " + user_id}), 404
    return jsonify({"id" : target.id, "username": target.username})

@app.route('/user/add', methods=["POST"])
def add_user():
    raise NotImplementedError()


if __name__ == '__main__':
    app.run(port=5000, debug=True)


