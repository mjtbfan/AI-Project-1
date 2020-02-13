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

    def sequence_count(self, board, height, width, enemy, x, y):
        directions = [[1, 0], [1, 1], [0, 1], [-1, 1]]
        current_sequence = []
        for i in directions:
            sequence_size = 1
            while not (width <= (x + sequence_size * i[0]) or (x + sequence_size * i[0]) < 0 or (y + sequence_size * i[1]) >= height):
                if board[y + sequence_size * i[1]][x + sequence_size * i[0]] == enemy:
                    sequence_size += 1
                else:
                    break
            current_sequence.append([i, (sequence_size - 1)])

        return current_sequence


    def sequence_enemy(self, board, enemy):
        height = len(board)
        width = len(board[0])

        all_sequences = []
        for i in range(height):
            for j in range(width):
                if board[i][j] == enemy:
                    all_sequences.append([[j, i], self.sequence_count(board, height, width, enemy, j, i)])

        return all_sequences


    def calculate_value(self, brd, player):
        enemy = 1 if player == 2 else 2
        constrict_board = []
        for i in self.get_successors(brd):
            for j in range(len(i[0].board)):
                if sum(i[0].board[j]) == 0:
                    temp_board = i[0].board[0:j if j > 0 else 1]
                    temp_board.reverse()
                    constrict_board.append(temp_board)
                    break
                elif j == (len(i[0].board) - 1):
                    temp_board = i[0].board
                    temp_board.reverse()
                    constrict_board.append(temp_board)

        # options[i][0] = [x,y] of enemy piece
        # options[i][1] = [[x-direct, y-direct], num in direct]
        options = []
        for i in constrict_board:
            options.append(self.sequence_enemy(i, enemy))

        curr_best = [[-1, -1], [[[-1, -1]], -1]]
        best_options = []
        for i in options:
            print(i)
            for j in range(4):
                if i[0][1][j][1] > curr_best[1][1]:
                    curr_best = [i[0][0], i[0][1][j]]
                    best_options.append(curr_best)

        move = curr_best[0][0]
        temp_best = -1
        for i in best_options:
            max_add = i[0][0] + (i[1][0][0] * i[1][1])
            max_sub = i[0][0] - (i[1][0][0] * i[1][1])
            add = i[0][0] + i[1][0][0]
            sub = i[0][0] - i[1][0][0]
            if i[1][1] > temp_best and (add in brd.free_cols() or sub in brd.free_cols()):
                if max_add == (brd.w - 1):
                    move = sub
                else:
                    move = add

        return move

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        player = brd.player
        return self.calculate_value(brd, player)


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
