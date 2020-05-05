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

config = setup_config(max_round= 1000, initial_stack=1000, small_blind_amount=5)

#Registering Player
config.register_player(name="p1", algorithm=heur)
config.register_player(name="p2", algorithm=fish)

game_result = start_poker(config, verbose= 1)
