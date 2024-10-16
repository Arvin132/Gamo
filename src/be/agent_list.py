from gamelogic import HumenMatch4Agent, RandomMatch4Agent, FirstMoveMatch4Agent

class AgentsList:
    all_agents = {
        "Humen": HumenMatch4Agent,
        "Random Agent": RandomMatch4Agent,
        "First Move Agent": FirstMoveMatch4Agent
    }
    
    def keys_tolist():
        return list(AgentsList.all_agents.keys)
