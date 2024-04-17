import chess

from dartmoor_model import Model


class Parser:

    def __init__(self):
        self.model = Model.Model()
        self.max_depth = 3
        self.test_list = None

    def get_bot_name(self):
        return "hk-alpha.0.3"

    # TODO: Sort list of moves by move evaluation
    # TODO: Traverse tree of moves

    def find_move(self, board: chess.Board):

        self.model.loadBoard(board)

        moves = self.get_ordered_list_of_moves(board)
        self.test_list = moves
        return self.get_best_move(board, moves)

        #
        # best_move_value = -1500.0
        # best_move: chess.Move = None
        # possible_moves = board.legal_moves
        #
        # # 100 equals checkmate
        # for potential in possible_moves:
        #
        #     move_eval = self.model.evaluateMove(potential)
        #
        #     if move_eval > best_move_value:
        #         best_move_value = move_eval
        #         best_move = potential
        #
        # if best_move is not None:
        #     print("ideal move " + str(best_move))
        #     print("ideal eval value " + str(best_move_value))
        #
        # return best_move

    def get_ordered_list_of_moves(self, board: chess.Board):
        possible_moves = board.legal_moves
        sorted_moves = sorted(possible_moves, key=lambda move: self.model.evaluateMove(move))
        sorted_moves.reverse()
        return sorted_moves

    def get_best_move(self, board: chess, moves):
        best_move = None
        best_value = 10000
        print(board.turn)

        if board.turn:
            best_value *= -1

        for move in moves:
            eval = self.minimax(0, move, board, False, alpha=-10000, beta=10000)

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

    def minimax(self, depth, move: chess.Move, board: chess.Board, maximizing_player,
                alpha, beta):

        check_mate, MAX, MIN = 10, 1000, -1000

        if board.is_checkmate():
            return check_mate

        if board.is_fivefold_repetition():
            return 0

        legal_moves = board.legal_moves

        # Terminating condition. i.e
        # leaf node is reached
        if depth == self.max_depth:
            eval = self.model.eval_board(board)

            return eval

        if maximizing_player:

            best = MIN

            for move in legal_moves:
                board_copy = board.copy()
                board_copy.push(move)

                val = self.minimax(depth + 1, move, board_copy,
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

                val = self.minimax(depth + 1, move, board,
                                   True, alpha, beta)
                best = min(best, val)
                beta = min(beta, best)

                # Alpha Beta Pruning
                if beta <= alpha:
                    break

            return best

        # def minimax(self, node: chess.Board, depth, isMaximizingPlayer, alpha, beta):
#     if node.is_checkmate() or node.is_fivefold_repetition() or depth == self.max_depth:
#         return self.model.evalBoard(node)
#
#     legal_moves = node.legal_moves
#
#     if isMaximizingPlayer:
#         best_move = -10000
#
#             for move in legal_moves:
#
#                 potential_val = self.minimax(node, depth + 1, False, alpha, beta)
#                 best_move = max(best_move, potential_val)
#                 alpha = max(alpha, best_move)
#                 if beta <= alpha:
#                     break


# if node is leafnode:
#     return value
#
# if isMaximizingPlayer:
#     bestVal = -INFINITY
#     for each child node:
#         value = minimax(node, depth + 1, false, alpha, beta)
#         bestVal = max(bestVal, value)
#         alpha = max(alpha, bestVal)
#         if beta <= alpha:
#             break
#     return bestVal
#
# else:
#     bestVal = +INFINITY
#     for each child node:
#         value = minimax(node, depth + 1, true, alpha, beta)
#         bestVal = min(bestVal, value)
#         beta = min(beta, bestVal)
#         if beta <= alpha:
#             break
#     return bestVal
