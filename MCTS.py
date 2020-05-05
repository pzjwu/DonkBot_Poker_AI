from Node import Node
from State import State
from pypokerengine.utils.card_utils import estimate_hole_card_win_rate
import math

class MCTS:
    def __init__(self, start_state):
        start_node = Node(start_state)


    def descend(self, node):
        if node.children == 0:
            if
        else:


    def UCB(self, scalar, node, parent_visits):
        return node.wins + 2 * math.sqrt(math.log(parent_visits)/node.visits)

    def choose(self, node):
        children = node.children

        for i in children:



    def rollout(self, num_sim, hole_cards, community_cards):
        avg_win = estimate_hole_card_win_rate(num_sim, nb_player = 2, hole_card = hole_cards, community_card = community_cards)
        return avg_win


    def backpropogate(self, node):




