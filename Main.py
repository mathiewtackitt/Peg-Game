from Board import Board
import game
import math
from AI import AI
from Directions import Directions
import util
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train AI to solve Peg Game")
    parser.add_argument('-e', '-epsilon', default=0.5, type=float, help="Epsilon value for training agent. [0, 1). Smaller value means less random. (Default: %(default)s)")
    parser.add_argument('-a', '-alpha', default=0.5, type=float, help="Alpha value for training agent. (0, 1). Smaller value means slower learning. (Default: %(default)s)")
    parser.add_argument('-d', '-discount', default=0.5, type=float, help="Discount value for training agent. (0, 1). Smaller value means slower learning. (Default: %(default)s)")
    parser.add_argument('-t', '-training', default=2000, type=int, help="Number of training episodes. (Default: %(default)s)")
    parser.add_argument('-r', '-rows', default=5, type=int, help="Number of rows on board. (Default: %(default)s)")
    parser.add_argument('-s', '-training_speed', default=0.001, type=float, help="Speed of training episodes. (0, inf). Smaller value means faster training. (Default: %(default)s)")
    parser.add_argument('-v', '-velocity', default=0.5, type=float, help="Speed of testing episodes. (0, inf). Smaller value means faster testing episdoes. (Default: %(default)s)")
    parser.add_argument('-gui', action='store_true', help="Determines if GUI should display for training episodes. Include -gui in arguments to turn GUI display on for training episodes. Keep it removed to disable GUI display for training episodes. GUI will display during testing episodes regardless.")
    args = vars(parser.parse_args())
    print(args)

    NUM_ROWS = args['r']
    TRAINING = args['t']
    TOTAL = TRAINING + 1

    TRAINING_SPEED = args['s']
    TESTING_SPEED = args['v']

    agent = AI(args['a'], args['e'], args['d'])
    # board = Board(NUM_ROWS)
    # board.display()

    ###################### VERY STUPID AI #####################
    # LOOKS AT ALL AVAILABLE ACTIONS AND CHOOSES FIRST CHOICE #

    # legal_actions = board.getLegalActions()
    # while len(legal_actions) > 0:
    #     action = legal_actions[0]
    #     tile, direction = action
    #     print(tile.num, direction.value)
    #     board.move(tile, direction, 0.5)
    #     legal_actions = board.getLegalActions()

    average_score = 0
    total_average = 0
    for n in range(TOTAL):
        board = Board(NUM_ROWS)
        if args['gui'] or n >= TRAINING:
            board.display()
        ## After training, take policy route.
        if n >= TRAINING:   agent.epsilon = 0
        action = agent.getAction(board)
        while action != None:
            tile_num, direction = action
            orig_board = board.copy()
            new_board = orig_board.move(tile_num, direction, TRAINING_SPEED if n < TRAINING else TESTING_SPEED)
            agent.update(board, action, new_board, new_board.getReward())
            board.move(tile_num, direction, TRAINING_SPEED if n < TRAINING else TESTING_SPEED)
            action = agent.getAction(board)
        ## If board has one peg remaining, print layout and which iteration it solved on
        average_score += board.getReward()
        total_average += board.getReward()
        if (n + 1) % 100 == 0:
            print(n + 1, " training episodes completed.\n     Average score over last 100 episodes: ", average_score / 100, "\n     Lifetime average: ", total_average / (n + 1))
            average_score = 0
      #  if board.won():
      #      print(n, board.getReward(), board.toString())
        game.end_graphics()
