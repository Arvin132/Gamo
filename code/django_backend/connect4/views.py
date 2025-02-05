from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from .gamelogic import AsyncGamerunner_Match4
from .agent_list import AgentsList
import json

from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def connect4_home(request):
    return HttpResponse("Connect4 is ready to be accessed")

def get_agents_list(request):
    return JsonResponse({"agents": AgentsList.keys_tolist(), "human-agent": AgentsList.human_agent})

@csrf_exempt
def start_game_connect4(request): 
    if (request.method == "POST"):
        try:
            data = json.loads(request.body)
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
            
            print("Before this part")
            request.session["connect4_game"] = json.dumps(game_data)
            print("Ater this part")
            return JsonResponse({"message": "200 Connect 4 Game has started"})
        except Exception as e:
            return JsonResponse({"message": "400 " + str(e)})
    # else: 
    return JsonResponse({"message": "405 Method Not Allowed"}, status=405)
            
@csrf_exempt
def get_state_connect4(request):
    if (request.method == "GET"):
        try:
            game_data = json.loads(request.session["connect4_game"])
            dict = game_data["game_runner"]
            dict["players"] = {"player-1": game_data["player_1_type"], "player-2": game_data["player_2_type"]}
            dict["message"] = "200 data was sent"
            return JsonResponse(dict)
        except Exception as e:
            return JsonResponse({"message": "400 " + str(e)})
    else:
        return JsonResponse({"message": "405 Method Not Allowed"}, status=405)
    
@csrf_exempt
def apply_move(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            column = data.get('column')
            player_id = data.get('player-id')
            is_bot = data.get('is-bot')
            
            game_data = json.loads(request.session.get("connect4_game", "{}"))

            p1 = AgentsList.all_agents[game_data["player_1_type"]]()
            p2 = AgentsList.all_agents[game_data["player_2_type"]]()
            game_runner = AsyncGamerunner_Match4(p1, p2)
            game_runner.from_dict(game_data["game_runner"])
            
            game_runner.apply_move(column, player_id, is_bot)
            game_data["game_runner"] = game_runner.to_dict()
            request.session["connect4_game"] = json.dumps(game_data)
            return JsonResponse({"message": "200 move applied"})
        except Exception as e:
            print(str(e))
            return JsonResponse({"message": f"400 {str(e)}"}, status=400)
    
    # else
    return JsonResponse({"message": "405 Method Not Allowed"}, status=405)