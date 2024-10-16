from gamelogic import HumenMatch4Agent, RandomMatch4Agent, FirstMoveMatch4Agent
from copy import deepcopy

class AgentsList:
    humen_agent = "Humen"
    all_agents = {
        deepcopy(humen_agent): HumenMatch4Agent,
        "Random Agent": RandomMatch4Agent,
        "First Move Agent": FirstMoveMatch4Agent
    }

    
    def keys_tolist():
        return list(AgentsList.all_agents.keys())
