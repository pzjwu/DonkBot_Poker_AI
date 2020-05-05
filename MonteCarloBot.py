from pypokerengine.players import BasePokerPlayer
from pypokerengine.engine.hand_evaluator import HandEvaluator
from pypokerengine.utils.card_utils import _pick_unused_card, _fill_community_card
from pypokerengine.utils.card_utils import gen_cards
import math
import random


#Making Betting Curves
def normpdf(x, mean, sd):
    var = float(sd)**2
    denom = (2*math.pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return num/denom


#Non optimized betting strategy
def rando_betting(equity, valid_actions):
    amount = None
    fold_prob = normpdf(equity * 100, mean = 40, sd = 10)
    call_prob = normpdf(equity * 100, mean = 50, sd = 20)
    raise_prob = normpdf(equity * 100, mean = 68, sd = 10)

    #Scale
    total = fold_prob + call_prob + raise_prob
    fold_prob = fold_prob / total
    call_prob = call_prob / total

    #Generate random number b/w 0 and 1
    val = random.uniform(0,1)

    if val < fold_prob + call_prob and val > fold_prob:
        action = 'call'
    elif val > fold_prob + call_prob:
        action = 'raise'
        raise_amount_options = [item for item in valid_actions if item['action'] == 'raise'][0]['amount']
        min_raise = raise_amount_options['min']
        max_raise = raise_amount_options['max']
        amount = min(int((min_raise / 2) * 3), max_raise)
    else:
        action = 'fold'

    if amount is None:
        for i in valid_actions:
            if i.get('action') == action:
                amount = i.get('amount')

    return action, amount


num_sims = 500000

def estimate_win_rate(nb_simulation, nb_player, hole_card, community_card):
    #Convert to list to become compatible with monte carlo function
    community_card = gen_cards(community_card)
    hole_card = gen_cards(hole_card)

    # Estimate the win count by doing a Monte Carlo simulation
    win_count = sum([montecarlo_simulation(nb_player, hole_card, community_card) for _ in range(nb_simulation)])
    return 1.0 * win_count / nb_simulation


def montecarlo_simulation(nb_player, hole_card, community_card):
    # Do a Monte Carlo simulation given the current state of the game by evaluating the hands
    community_card = _fill_community_card(community_card, used_card=hole_card + community_card)
    unused_cards = _pick_unused_card((nb_player - 1) * 2, hole_card + community_card)
    opponents_hole = [unused_cards[2 * i:2 * i + 2] for i in range(nb_player - 1)]
    opponents_score = [HandEvaluator.eval_hand(hole, community_card) for hole in opponents_hole]
    my_score = HandEvaluator.eval_hand(hole_card, community_card)
    return 1 if my_score >= max(opponents_score) else 0


#Dummy Thicc Bet Hueristic (This one sucks)
def bet_heuristic(equity, valid_actions):
    # Check whether it is possible to call
    can_call = len([item for item in valid_actions if item['action'] == 'call']) > 0
    if can_call:
        # If so, compute the amount that needs to be called
        call_amount = [item for item in valid_actions if item['action'] == 'call'][0]['amount']
    else:
        call_amount = 0

    amount = None

    if equity > 0.5:
        raise_amount_options = [item for item in valid_actions if item['action'] == 'raise'][0]['amount']
        if equity > 0.90:
            action = 'raise'
            amount = raise_amount_options['max']
        elif equity > 0.65:
            action = 'raise'
            #3Bet sizing
            amount = raise_amount_options['min'] * 3
        else:
            action = 'call'
    else:
        action = 'call' if can_call and call_amount == 0 else 'fold'

    # Set the amount
    if amount is None:
        items = [item for item in valid_actions if item['action'] == action]
        amount = items[0]['amount']

    return action, amount


class MonteCarloBot(BasePokerPlayer):
    def __init__(self):
        self.num_players = 0
        self.wins = 0
        self.losses = 0


    def declare_action(self, valid_actions, hole_card, round_state):
        # Estimate the win rate
        equity = estimate_win_rate(1000, self.num_players, hole_card, round_state['community_card'])
        #action, amount = bet_heuristic(equity, valid_actions)
        action, amount = rando_betting(equity, valid_actions)

        return action, amount


    def receive_game_start_message(self, game_info):
        self.num_players = game_info['player_num']

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        is_winner = self.uuid in [item['uuid'] for item in winners]
        self.wins += int(is_winner)
        self.losses += int(not is_winner)

def setup_ai():
    return MonteCarloBot()
