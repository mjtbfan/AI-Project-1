import math
import agent


###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth, aVal=5, oVal=-5):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth
        self.move = 0
        self.total_moves = 0
        self.record = []

        self.total_moves_dec = 1  # constant that decrements the total move variable depending on the depth
        self.aVal = aVal  # constant for heurisftic function
        self.oVal = oVal  # constant for heuristic when opponent has winning opportunity

        # Tree to visualize the values from the score function
        self.scores_tree = {}
        for x in range(max_depth + 1):
            self.scores_tree[x] = []
        self.scores_list = []

        self.pruned = 0  # keep track of pruned branches
        self.debug = False  # to toggle on and off the print functions

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        self.record = []
        """search for the best move (choice of column for the token)"""

        if brd.player == 1 and self.aVal < self.oVal:
            temp = self.aVal
            self.aVal = self.oVal
            self.oVal = temp
        elif brd.player == 2 and self.aVal > self.oVal:
            temp = self.aVal
            self.aVal = self.oVal
            self.oVal = temp

        self.total_moves += self.total_moves_dec
        self.alpha_beta(brd, -(brd.w * brd.h) / 2, (brd.w * brd.h) / 2, self.max_depth)
        self.total_moves += self.total_moves_dec

        if self.debug:
            print(self.record)
            print("SCORES TREE:")
            print("PRUNED:", self.pruned)

        return self.move

    # Print the score tree
    #
    # PARAM [board.Board] brd: the current board state
    # PARAM [dictionary] d: the dictionary with keys as depth and values as scores at each depth
    #
    # NOTE: needs work
    def print_tree(self, brd, d):
        for key in d:
            if key == 0:
                print("-" * self.max_depth * brd.w, sep='')
            else:
                for values in d.values():
                    print("key:", key, "values:", values, "---", sep='')
                print(sep='')

    # NegaMax with Alpha Beta Prunning
    #
    # PARAM [board.Board] brd: the current board state
    # PARAM [int] alpha: alpha value
    # PARAM [int] beta: beta value
    # PARAM [int] depth: current depth on tree
    #
    # RETURN [int]: the alpha value choosen
    # Note: the next move is determined and saved to the constuctor
    def alpha_beta(self, brd, alpha, beta, depth):

        temp = self.total_moves
        if (self.get_successors(brd) == [] or depth == 0):  # draw condition
            return 0

        newbrd = brd.copy()

        successors = self.get_successors(newbrd)  # check for win in next move (look at all possible moves)
        for tuple in successors:
            board = tuple[0]

            if (board.get_outcome() != 0):
                self.move = tuple[1]
                self.record.append([self.move, (board.w * board.h + 1 - self.total_moves) / 2])
                return (board.w * board.h + self.oVal + self.max_depth - depth - self.total_moves) / 2

        max = (newbrd.w * newbrd.h - self.aVal - self.total_moves) / 2  # initial after no win in next move

        if beta > max:  # check beta
            beta = max
            if alpha >= beta:  # prune all higher values
                self.pruned += 1  # To determine how many sub-nodes are pruned
                return beta

        for col in range(newbrd.w):  # compute score of all possible next moves & select best move
            if (col in newbrd.free_cols()):

                newbrd.add_token(col)
                self.total_moves += self.total_moves_dec
                score = self.alpha_beta(newbrd, -beta, -alpha, depth - 1)
                self.scores_list.append(score)
                self.scores_tree[depth].append([col, score])

                if (score >= beta):
                    return score

                if (score > alpha):
                    self.move = col  # determines the next move based on the algorithm

                    alpha = score
                    self.record.append([self.move, alpha])

        self.scores_list.clear()
        self.total_moves = temp
        return alpha

    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb, col))
        return succ
