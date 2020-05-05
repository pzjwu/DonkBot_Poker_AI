from State import State

class Node:
    def __init__(self, game_state, parent = None):
        self.visits = 1
        #We are choosing to evaluate the node with wins vs potvalue. Given the random nature in the current build
        #we cannot accurately generate accurate pot builds. Thus, we are currently using wins to estimate equity, and
        #basing our bet strategy based on equity percentages
        self.wins = 0
        self.rollouts = 0
        self.state = game_state
        self.parent = parent
        #Making it a list vs dictionary?
        self.children = []
        self.fringe = []

    def add_child(self, child_state, action):
        child = Node(child_state, self)
        self.children[action] = child

    def update(self, wins, rollouts):
        self.wins += wins
        self.rollouts = rollouts
        self.visits += 1

    def is_terminal(self):
        if len(self.children) == 0:
            return True
        else:
            return False

