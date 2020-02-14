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
            current_sequence.append([i, sequence_size])

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
            for k in i:
                for j in range(4):
                    if k[1][j][1] > curr_best[1][1]:
                        curr_best = [k[0], k[1][j]]
                        best_options.append(curr_best)

        move = curr_best[0][0]
        temp_best = -1
        for i in best_options:
            print(i)
            print(i[1][1])
            max_add = i[0][0] + (i[1][0][0] * i[1][1])
            sub = i[0][0] - i[1][0][0]
            if i[1][1] > temp_best and (max_add in brd.free_cols() or sub in brd.free_cols()):
                temp_best = i[1][1]
                print(temp_best)
                if max_add in brd.free_cols():
                    move = max_add
                elif sub in brd.free_cols():
                    move = sub

        return move, temp_best

    def alpha_beta(self, brd, player, alpha, beta):

        continue_values = []
        continue_boards = []
        continue_moves = []

        if player == 1:
            for i in self.get_successors(brd):
                temp, value = self.calculate_value(i[0], player)
                if value > alpha:
                    continue_boards.append(i[0])
                    continue_values.append(value)
                    continue_moves.append(temp)

            return continue_boards, continue_moves, continue_values

        if player == 2:
            for i in self.get_successors(brd):
                temp, value = self.calculate_value(i[0], player)[0], -self.calculate_value(i[0], player)[1]
                if value < beta:
                    continue_boards.append(i[0])
                    continue_values.append(value)
                    continue_moves.append(temp)

            return continue_boards, continue_moves, continue_values


    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        alpha = -math.inf
        beta = math.inf

        current_player = brd.player
        board_list = [brd]
        temp_moves = []
        temp_values = []

        moves = []
        values = []

        for i in range(self.max_depth):
            temp = []
            for j in board_list:
                temp.append(self.alpha_beta(j, current_player, alpha, beta))
            for k in temp:
                board_list = k[0]
                temp_moves.append(k[1])
                temp_values.append(k[2])

            for bruh in range(len(temp_values)):
                if temp_values[bruh]:
                    moves.append(temp_moves[bruh])
                    values.append(temp_values[bruh])


            print(values)
            print(moves)
            if max(max(values)) > alpha:
                alpha = max(max(values))
            if min(min(values)) < beta:
                beta = min(min(values))

            current_player = 2 if current_player == 1 else 1

        index1 = -1
        index2 = -1
        if brd.player == 1:
            for i in range(len(values)):
                big = max(values[i])
                if big == alpha:
                    index1 = i
                    index2 = values[i].index(alpha)
                    break
        else:
            for i in range(len(values)):
                big = min(values[i])
                if big == beta:
                    index1 = i
                    index2 = values[i].index(beta)
                    break

        return moves[index1][index2]



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
