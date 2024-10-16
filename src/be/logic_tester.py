from gamelogic import Gamerunner_Match4, ZeroH_MiniMax_Match4, HumenMatch4Agent, RandomMatch4Agent, FirstMoveMatch4Agent


game_runner = Gamerunner_Match4(ZeroH_MiniMax_Match4(), RandomMatch4Agent())
results = game_runner.run_multiple_games(20, verbose=False)
print(results)
print(results.count(1) / len(results))