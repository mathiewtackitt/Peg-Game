import util
import random

class AI:
    
    def __init__(self, alpha, epsilon, discount):
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount = discount
        self.qTable = util.Counter()

    def printQValue(self):
        for layout,action in self.qTable.keys():
            print()
            print(layout, action[0], action[1].value, self.qTable[(layout, action)])

    def getQValue(self, board, action):
        return self.qTable[(board.toString(), action)]
    
    def computeValueFromQValues(self, board):
        q_values = [self.getQValue(board, action) for action in board.getLegalActions()]
        if len(q_values) == 0:  return 0.0
        return max(q_values)

    def computeActionFromQValues(self, board):
        max_q = self.getValue(board)
        pos_actions = [action for action in board.getLegalActions() if self.getQValue(board, action) == max_q]
        return None if (len(pos_actions) == 0) else random.choice(pos_actions)

    def getAction(self, board):
        actions = board.getLegalActions()
        if len(actions) == 0:   return None
        if (util.flipCoin(self.epsilon)):   return random.choice(actions)
        else:   return self.getPolicy(board)
        # return self.getPolicy(board)

    def update(self, board, action, nextState, reward):
        curr_q = self.getQValue(board, action)
        next_q = self.computeValueFromQValues(nextState)
        curr_q += self.alpha * (reward + self.discount * next_q - curr_q)
        self.qTable[(board.toString(), action)] = curr_q

    def getPolicy(self, board):
        return self.computeActionFromQValues(board)
    
    def getValue(self, board):
        return self.computeValueFromQValues(board)