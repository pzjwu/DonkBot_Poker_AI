from pypokerengine.api.game import setup_config, start_poker
from fish_player import FishBot
#These two players play LAG(Loose Aggressive), meaning they have a wide range of playable hands, and bet heavy witha wider range
from MonteCarloBot import MonteCarloBot
from ConteMarlo import ConteMarloBot
import pandas as pd
#These two players play TAG(Tight Aggressive), meaning they fold the large majority of their starting hands, and bet heavy with strong hands
from Heuristic_Bot import Heuristic_Bot
from Bayesian_Bot import Bayesian_Bot
import numpy as np

bayes = Bayesian_Bot()
monte = MonteCarloBot()
conte = ConteMarloBot()
heur = Heuristic_Bot()
fish = FishBot()

players = [bayes, monte, conte, heur, fish]
file_names = ['bayes_monte.csv', 'bayes_conte.csv', 'bayes_heur.csv', 'bayes_fish.csv', 'monte_conte.csv', 'monte_heur.csv', 'monte_fish.csv', 'conte_heur.csv','conte_fish.csv', 'heur_fish.csv']

idx = 0
x = 0

for i in range(0, len(players) - 1):
    for j in range(i + 1, len(players)):
        p1 = []
        p2 = []

        for rounds in range(50):
            print(x)
            config = setup_config(max_round= 200, initial_stack=1000, small_blind_amount=5)

            #Registering Player
            config.register_player(name="p1", algorithm=players[i])
            config.register_player(name="p2", algorithm=players[j])

            game_result = start_poker(config, verbose= 1)

            p1.append(int(game_result.get('players')[0].get('stack')))
            p2.append(int(game_result.get('players')[1].get('stack')))
            x = x + 1

        a = np.asarray(p1)
        b = np.asarray(p2)
        stack = np.column_stack([a,b])
        np.savetxt(file_names[idx], stack, delimiter=',')
        idx = idx + 1
        print(idx)
