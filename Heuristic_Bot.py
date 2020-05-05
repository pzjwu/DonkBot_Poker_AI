from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import _pick_unused_card, _fill_community_card
from pypokerengine.utils.card_utils import gen_cards
from pypokerengine.engine.hand_evaluator import HandEvaluator
from Range import Range
import random
import pandas as pd

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

preflop_equities_global = pd.read_csv('preflop_equity.csv')

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

def pot_odds(to_call, total_pot, hole_cards, community_cards):
    equity = estimate_win_rate(nb_simulation=20000, nb_player=2, hole_card=hole_cards,
                                    community_card=community_cards)
    odds = to_call / total_pot
    if equity > odds:
        return (True, 0)
    else:
        return (False, equity)

# Calculates implied odds, or the amount of money that we expect to win if we hit one our possible outs.
def calc_implied_odds(to_call, opponent_bet, total_pot, hand_equity):
    need_to_win = (to_call / hand_equity) - opponent_bet - total_pot - to_call
    if need_to_win < 0.4 * (total_pot + to_call):
        return True
    else:
        return False


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

def get_preflop_equity(converted_hole):
    equity = preflop_equities_global[preflop_equities_global['Cards'] == converted_hole].iloc[0, 1]
    return equity


def preflop_strats(position,converted_cards, call_amount, small_blind,):
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

    return action, amount

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



class Heuristic_Bot(BasePokerPlayer):
    # RFI Strategies
    def __init__(self):
        self.street = None
        self.small_blind_amount = None
        self.in_position = False
        self.opp_bet = None
        self.re_raise = False

    def declare_action(self, valid_actions, hole_card, round_state):
        #Setting Up Calculations
        converted_hole_cards = convert_hole(hole_card)

        if round_state.get('next_player') != round_state.get('dealer_btn'):
            self.in_position = True

        can_call = len([item for item in valid_actions if item['action'] == 'call']) > 0
        if can_call:
            call_amount = [item for item in valid_actions if item['action'] == 'call'][0]['amount']
        else:
            call_amount = 0

        if self.street == 'preflop':
            action, amount = preflop_strats(self.in_position, converted_hole_cards, call_amount,
                                            self.small_blind_amount)

            return action, amount
        # Post Flop Logic
        else:
            if call_amount == 0:
                action = 'call'
                amount = call_amount

            # We are facing a bet
            else:
                # Raise
                if (in_range(three_bet, converted_hole_cards) != 0) and not self.re_raise:
                    self.re_raise = True
                    val = random.uniform(0, 1)
                    if val < in_range(three_bet, converted_hole_cards):
                        action = 'raise'
                        if self.in_position:
                            amount = 3 * call_amount
                        else:
                            amount = 4 * call_amount

                else:
                    odds = pot_odds(call_amount, round_state.get('pot').get('main').get('amount'), hole_card,
                             round_state.get('community_card'))
                    if odds[0]:
                        action = 'call'
                        amount = call_amount
                    else:
                        if calc_implied_odds(call_amount, self.opp_bet,
                                             round_state.get('pot').get('main').get('amount'), odds[1]):
                            action = 'call'
                            amount = call_amount
                        else:
                            action = 'fold'
                            amount = 0

        return action, amount

    # Initializes the game
    def receive_game_start_message(self, game_info):
        self.small_blind_amount = game_info['rule']['small_blind_amount']


    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        self.street = street
        self.re_raise = False

    def receive_game_update_message(self, action, round_state):
        if action.get('player_uuid') != self.uuid and action.get('action') == 'raise':
            self.opp_bet = action.get('amount')

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

def setup_ai():
    return Heuristic_Bot()
