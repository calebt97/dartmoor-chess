from random import randrange

import chess

from black_model import BoardModel, MoveModel


# TODO: Goals for .0.4:
# TODO: Swarming on checkmate, not just following with queen
# TODO: More rook activity
# TODO: cut down eval time if possible, would love to bump depth
# TODO: Attack passed pawns earlier
# TODO: Keep pawns in front of king
# TODO: Connected pawns bonus
# TODO: Penalize being pinned
# TODO: Prioritize Queen safety more
# TODO: Once there are 5 pieces left, use that closing library and expand depth if necessary
# TODO: Differentiate between opening, ending and middle games
# TODO: Why does this even allow a checkmate in one against it? Shouldn't a single move bot never even get close enough?

class Parser:

    def __init__(self):
        self.board_model = BoardModel.BoardModel()
        self.move_model = MoveModel.MoveModel()
        self.starting_depth = 2
        self.current_depth = self.starting_depth
        self.test_list = None
        board = chess.Board()
        self.previous_evals = {board.fen(): 0.0}

    def get_bot_name(self):
        return "hk-alpha.0.3"

    def __set_depth(self, board: chess.Board):
        # Depth of search will increase as game progresses, less value in deep searching early in game
        if len(board.piece_map()) < 12:
            self.current_depth = self.starting_depth + 1
        else:
            self.current_depth = self.starting_depth


    def find_move(self, board: chess.Board):
        self.__set_depth(board)

        self.move_model.loadBoard(board)

        moves = self.get_ordered_list_of_moves(board)
        self.test_list = moves

        if len(moves) > 20:
            top_half = moves[:len(moves) // 2]
            return self.get_best_move(board, top_half)

        return self.get_best_move(board, moves)

    def get_ordered_list_of_moves(self, board: chess.Board):
        possible_moves = board.legal_moves
        sorted_moves = sorted(possible_moves, key=lambda move: self.move_model.evaluateMove(move))
        sorted_moves.reverse()

        return sorted_moves

    def get_best_move(self, board: chess, moves):
        best_move = None
        best_value = 10000

        if board.turn == chess.WHITE:
            # If white, best move should start at -10000
            best_value *= -1

        for move in moves:
            # move hasn't been made yet, so we need to look at not current board turn
            eval = self.minimax(0, board, not board.turn, alpha=-10000, beta=10000)

            # White wants the highest eval
            if board.turn == chess.WHITE and eval > best_value:
                best_move = move
                best_value = eval
                # print("best move update "+str(move))
                # print("best score update "+str(best_value))

            # Black wants the lowest eval
            if board.turn == chess.BLACK and eval < best_value:
                best_move = move
                best_value = eval
                # print("best move update "+str(move))
                # print("best score update "+str(best_value))

        print("best move " + str(best_move))
        print("best score " + str(best_value))
        return best_move

    def minimax(self, depth, board: chess.Board, maximizing_player,
                alpha, beta):

        MAX, MIN = 1000, -1000
        white_checkmate, black_checkmate = 1000, -1000

        if board.is_checkmate() and board.turn == chess.BLACK:
            # Bias for checkmates that are fewer turns away
            return white_checkmate - (depth * 2)

        if board.is_checkmate() and board.turn == chess.WHITE:
            # Bias for checkmates that are fewer turns away
            return black_checkmate + (depth * 2)

        if board.is_fivefold_repetition():
            return 0

        legal_moves = board.legal_moves

        # Terminating condition. i.e
        # leaf node is reached
        if depth == self.current_depth:

            if self.previous_evals.get(board.fen()) is not None:
                return self.previous_evals[board.fen()]

            eval = self.board_model.eval_board(board)

            self.previous_evals[board.fen()] = eval

            return eval

        if maximizing_player:

            best = MIN

            for move in legal_moves:
                board_copy = board.copy()
                board_copy.push(move)

                val = self.minimax(depth + 1, board_copy,
                                   False, alpha, beta)


                best = max(best, val)
                alpha = max(alpha, best)

                # Alpha Beta Pruning
                if beta <= alpha:
                    break

            return best

        else:
            best = MAX

            for move in legal_moves:
                board_copy = board.copy()
                board_copy.push(move)

                val = self.minimax(depth + 1, board,
                                   True, alpha, beta)
                best = min(best, val)
                beta = min(beta, best)

                # Alpha Beta Pruning
                if beta <= alpha:
                    break

            return best
