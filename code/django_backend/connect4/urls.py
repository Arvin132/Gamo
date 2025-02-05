from django.urls import path
from .views import *

urlpatterns = [
    path('', connect4_home, name='connect4_home'),
    path('agents', get_agents_list, name='connect4_agents'),
    path('start', start_game_connect4, name='connect4_start'),
    path('apply-move', apply_move, name='connect4_applymove'),
    path('state', get_state_connect4, name='connect4_state'),
]