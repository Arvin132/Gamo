from gamelogic import HumenMatch4Agent, RandomMatch4Agent, FirstMoveMatch4Agent, ZeroH_MiniMax_Match4, ThreeCountH_MiniMax_Match4

class AgentsList:
    human_agent = "Human"
    all_agents = {
        human_agent: HumenMatch4Agent,
        "Random Agent": RandomMatch4Agent,
        "First move Agent": FirstMoveMatch4Agent, 
        "Zero Heuristics MiniMax Agent": ZeroH_MiniMax_Match4,
        "Three counte Heuristics MiniMax Agent": ZeroH_MiniMax_Match4,
    }

    
    def keys_tolist():
        return list(AgentsList.all_agents.keys())
