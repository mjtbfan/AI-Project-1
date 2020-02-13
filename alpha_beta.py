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
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth
        self.move = 0

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    #def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        #if not self.max_depth:
        #    return self.alpha_beta(brd, -1, 1)
        #else:
     #   return self.alpha_beta(brd, -(brd.w * brd.h) / 2, (brd.w * brd.h) / 2)

    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        #if not self.max_depth:
        #    return self.alpha_beta(brd, -1, 1)
        #else:
        self.alpha_beta(brd, -(brd.w * brd.h) / 2, (brd.w * brd.h) / 2)
        return self.move

    def alpha_beta(self, brd, alpha, beta):
        move = 0
        if (len(self.get_successors(brd)) == brd.w * brd.h):
            return 0
       
        for col in range(brd.w):
            if (col in brd.free_cols()): 
                #newbrd = brd.copy() 
                brd.add_token(col)
                if (brd.get_outcome() != 0):
                    return (brd.w * brd.h + 1 - len(self.get_successors(brd))) / 2
        
        max = (brd.w * brd.h - 1 - len(self.get_successors(brd))) / 2

        if beta > max:
            beta = max
            if alpha >= beta:
                return move
        
        for col in range(brd.w):
            if (col in brd.free_cols()):
                
                brd.add_token(col)

                score = -self.alpha_beta(brd, -beta, -alpha)

                if (score >= beta):
                    return col;
                if (score > alpha):
                    alpha = score;

        
        
        return move 


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
            succ.append((nb,col))
        return succ
