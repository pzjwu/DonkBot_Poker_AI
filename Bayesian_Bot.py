import numpy as np
import pandas as pd
import random
from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import _pick_unused_card, _fill_community_card
from pypokerengine.utils.card_utils import gen_cards
from pypokerengine.engine.hand_evaluator import HandEvaluator

preflop_equities_global = pd.read_csv('preflop_equity.csv')
dbn_global = pd.read_csv('Range_CPT.csv')

rfi_in = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
               [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
               [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
               ]
rfi_out = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                ]
three_bet = [[1, 1, 1, 1, 1, 1, 0.25, 0.15, 0, 0.75, 0.75, 0.5, 0.25],
                  [1, 1, 1, 1, 1, 0.5, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25],
                  [1, 1, 1, 1, 1, 0.5, 0.25, 0.25, 0.25, 0.25, 0.15, 0.25, 0],
                  [1, 0.5, 0.25, 1, 1, 0.5, 0.5, 0.25, 0.25, 0, 0, 0, 0],
                  [0.5, 0.25, 0, 0.15, 1, 1, 0.5, 0.5, 0.5, 0, 0, 0, 0],
                  [0.5, 1, 1, 1, 0.5, 1, 1, 1, 1, 0, 0, 0, 0],
                  [0, 1, 1, 1, 1, 0.75, 1, 1, 1, 0.75, 0.15, 0, 0],
                  [0, 0, 0, 0, 0, 0, 1, 0.5, 1, 0.75, 0.5, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0.75, 0.5, 1, 0.5, 0.15, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0.25, 0.5, 1, 0.5, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.25, 0.5, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.25, 0.25],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                  ]


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

def hand_value(val):
    if val == 'A':
        return 14
    elif val == 'K':
        return 13
    elif val == 'Q':
        return 12
    elif val == 'J':
        return 11
    elif val == 'T':
        return 10
    else:
        return int(val)

def convert_hole(hole_card):
    #Convert values
    if hand_value(hole_card[0][1]) == hand_value(hole_card[1][1]):
        vals = '' + hole_card[0][1] + hole_card[1][1]
    elif hand_value(hole_card[0][1]) > hand_value(hole_card[1][1]):
        vals = '' + hole_card[0][1] + hole_card[1][1]
    else:
        vals = '' + hole_card[1][1] + hole_card[0][1]

    if hole_card[0][0] == hole_card[1][0]:
        vals = vals + 's'
    else:
        vals = vals + 'o'

    return vals

def in_range(ranges, hand):
    hand_mapping = {'A': 0, 'K': 1, 'Q': 2, 'J': 3, 'T': 4, '9':5, '8':6, '7':7, '6':8, '5': 9, '4': 10, '3': 11, '2': 12}
    if hand[2] == 's':
        row_idx = int(hand_mapping.get(hand[0]))
        col_idx = int(hand_mapping.get(hand[1]))
        return ranges[row_idx][col_idx]
    else:
        row_idx = int(hand_mapping.get(hand[1]))
        col_idx = int(hand_mapping.get(hand[0]))
        return ranges[row_idx][col_idx]

def preflop_strats(position, converted_cards, call_amount, small_blind):
    equity = get_preflop_equity(converted_cards)
    if call_amount == 0:
        if position:
            if in_range(rfi_in, converted_cards) == 1:
                action = 'raise'
                amount = (small_blind * 2) * 2
            else:
                action = 'fold'
                amount = 0
        else:
            if in_range(rfi_out, converted_cards) == 1:
                action = 'raise'
                amount = (small_blind * 2) * 2
            else:
                action = 'fold'
                amount = 0
    else:
        if equity > 0.6:
            if in_range(three_bet, converted_cards) != 0:
                val = random.uniform(0, 1)
                if val < in_range(three_bet, converted_cards):
                    action = 'raise'
                    if position:
                        amount = 3 * call_amount
                    else:
                        amount = 4 * call_amount

                else:
                    action = 'fold'
                    amount = 0

            else:
                action = 'fold'
                amount = 0

        else:
            action = 'fold'
            amount = 0

    return action, amount, equity

def predict(position, size, action, prev):
    pos = 'Out_Position'
    if position:
        pos = 'In_Position'
    if action == 'call':
        new_outcome = str(dbn_global[(dbn_global['Position'] == pos) & (dbn_global['Action'] == action) & (dbn_global['Prior'] == prev)].iloc[0, 4])
    else:
        new_outcome = str(dbn_global[(dbn_global['Position'] == pos) & (dbn_global['Size'] == size) & (dbn_global['Action'] == action) & (dbn_global['Prior'] == prev)].iloc[0,4])

    return new_outcome

def get_preflop_equity(converted_hole):
    equity = preflop_equities_global[preflop_equities_global['Cards'] == converted_hole].iloc[0, 1]
    return equity

def classify_bet(pot_size, bet_size):
    if bet_size < 0.3 * pot_size:
        return "Small"
    elif (bet_size > (0.4 * pot_size)) and (bet_size < (0.7 * pot_size)):
        return "Medium"
    else:
        return "Large"

def prediction_response(outcome, hole_cards, community_cards, call_amount, raise_amt):
    equity = estimate_win_rate(nb_simulation= 2000, nb_player= 2, hole_card= hole_cards, community_card=community_cards)
    #Problem with slow-playing
    if outcome == 'Win' and equity >= 0.6:
        action = 'call'
        amount = call_amount
    elif outcome == 'Lose' and equity >= 0.6:
        action = 'raise'
        amount = min(3 * raise_amt[0], raise_amt[1])
    elif outcome == 'Win' and equity < 0.6:
        action = 'fold'
        amount = 0
    elif outcome == 'Lose' and equity < 0.6:
        action = 'raise'
        amount = min(4 * raise_amt[0], raise_amt[1])

    return action, amount

class Bayesian_Bot(BasePokerPlayer):
    def __init__(self):
        self.small_blind_amount = None
        self.street = None
        self.small_blind_amount = None
        self.opp_position = False
        self.opp_action = None
        self.opp_bet = None
        self.prediction = None


    def declare_action(self, valid_actions, hole_card, round_state):
        if round_state.get('next_player') == round_state.get('dealer_btn'):
            self.opp_position = True

        converted_cards = convert_hole(hole_card)
        pot = round_state.get('pot').get('main').get('amount')

        can_call = len([item for item in valid_actions if item['action'] == 'call']) > 0
        if can_call:
            call_amount = [item for item in valid_actions if item['action'] == 'call'][0]['amount']
        else:
            call_amount = 0

        raise_amt = [valid_actions[2].get('amount').get('min'), valid_actions[2].get('amount').get('max')]

        #preflop action
        if self.street == 'preflop':
            #When we are preflop, we can't make any judgements on how opponents will respond based on board texture
            #So we bet heuristically based on GTO principles and preflop equity charts
            action, amount, equity = preflop_strats(not self.opp_position, converted_cards, call_amount, self.small_blind_amount)
            if equity < 0.5:
                self.prediction = 'Win'
            else:
                self.prediction = 'Lose'

        else:
            bet_class = classify_bet(pot_size=pot, bet_size=self.opp_bet)
            self.prediction = predict(self.opp_position, bet_class, self.opp_action, self.prediction)
            action, amount = prediction_response(self.prediction, hole_card, round_state.get('community_card'), call_amount, raise_amt)

        return action, amount


    def receive_game_start_message(self, game_info):
        self.small_blind_amount = game_info['rule']['small_blind_amount']

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
         self.street = street

    def receive_game_update_message(self, action, round_state):
        if action.get('player_uuid') != self.uuid and action.get('action') == 'raise':
            self.opp_action = action.get('action')
            self.opp_bet = action.get('amount')
        elif action.get('player_uuid') != self.uuid and action.get('action') == 'call':
            self.opp_action = action.get('action')
            self.opp_bet = action.get('amount')

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

def setup_ai():
    return Bayesian_Bot()







