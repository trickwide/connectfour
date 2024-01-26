"""
Connect Four  AI Player Module
"""

import numpy as np
from player import Player

ROW_COUNT = 6
COLUMN_COUNT = 7


class AIPlayer(Player):
    """
    Represents an AI player in the Connect Four game.

    Args:
        Player (class): The parent class of the AIPlayer class. 
    """
    def get_best_move(self, board):
        """
        Determine the best move to make for the AI player on the given game board.

        Args:
            board (Board): An instance of the game board representing the current game state.

        Returns:
            int: The column number representing the best move for the AI player to make.
                This move is determined using the minimax algorithm with a depth of 5.
        """
        valid_moves = [column for column in range(
            COLUMN_COUNT) if board.is_valid_location(column)]
        best_move = None
        best_score = float("-inf")

        for column in valid_moves:
            row = board.get_next_empty_row(column)
            board.drop_chip(column, self.get_id())
            score = self.minimax(board, 5, -float("inf"), float("inf"), False)
            board.board[row][column] = 0

            if score > best_score:
                best_score = score
                best_move = column

        return best_move

    def evaluate_window(self, window, player_id):
        """
        Evaluate the score of a 4-chip window on the game board for a specific player.

        Args:
            window (list): A list representing a window of 4 chips on the game board.
            player_id (int): The id of the player for whom the window is being evaluated.

        Returns:
            int: A numerical score indicating window desirability for the specified player.
            Positive scores favor the player, while negative scores indicate disadvantage.
        """
        score = 0

        opponent_id = 1 if player_id == 2 else 2

        ai_count = window.count(player_id)
        opponent_count = window.count(opponent_id)
        empty_count = window.count(0)

        # Winning move or blocking opponent
        if ai_count == 3 and empty_count == 1:
            score += 100
        elif opponent_count == 3 and empty_count == 1:
            score -= 90

        # Promote center control
        if ai_count == 2 and empty_count == 2 and window[2] == player_id:
            score += 10

        # Penalize vulnerable positions
        if ai_count == 2 and empty_count == 2 and window[2] == opponent_id:
            score -= 20

        # Encourage building open rows
        if ai_count == 1 and empty_count == 3:
            score += 5

        return score

    def heuristic_value(self, board, player_id):
        """
        Calculate a heuristic value to assess the desirability of the current game state.

        Args:
            board (Board): An instance of the game board representing the current game state.
            player_id (int): _description_

        Returns:
            int:  A numerical value indicating the heuristic assessment of the current game state.
            Positive values indicate advantage, while negative values indicate disadvantage.
        """
        # Score for the current board state for AI player
        score = 0

        # Evaluate score for horizontal line
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT-3):
                window = list(board.board[row, column:column+4])
                score += self.evaluate_window(window, player_id)

        # Evaluate score for vertical line
        for column in range(COLUMN_COUNT):
            for row in range(ROW_COUNT-3):
                window = list(board.board[row:row+4, column])
                score += self.evaluate_window(window, player_id)

        # Evaluate score for positive diagonal line
        for row in range(ROW_COUNT-3):
            for column in range(COLUMN_COUNT-3):
                window = list(
                    board.board[row:row+4, column:column+4].diagonal())
                score += self.evaluate_window(window, player_id)

        # Evaluate score for negative diagonal line
        for row in range(ROW_COUNT - 3):
            for column in range(COLUMN_COUNT - 3):
                window = list(
                    np.flipud(board.board[row:row+4, column:column+4]).diagonal())
                score += self.evaluate_window(window, player_id)

        return score

    def minimax(self, board, depth, alpha, beta, maxplayer):
        """
        Minimax algorithm with alpha-beta pruning to determine the best move for the AI player.

        Args:
            board (Board): An instance of the game board representing the current game state.
            depth (int): The depth of the search tree, indicating how many moves ahead to consider.
            alpha (float): The best score found so far for the maximizing player.
            beta (float): The best score found so far for the minimizing player.
            maxplayer (bool): A boolean indicating, if the current player is the maximizing player.

        Returns:
            int: The minimax evaluation score indicating the desirability of the current game state.
        """
        if depth == 0 or board.is_game_over():
            if board.is_winner(self.get_id()):
                return 100000
            if board.is_winner(1 if self.get_id() == 1 else 2):
                return -100000

            return self.heuristic_value(board, self.get_id())

        valid_moves = [column for column in range(
            COLUMN_COUNT) if board.is_valid_location(column)]

        if maxplayer:
            max_evaluation = float("-inf")
            for column in valid_moves:
                board_copy = board.copy()
                board_copy.drop_chip(column, self.get_id())
                evaluation = self.minimax(board, depth-1, alpha, beta, False)
                max_evaluation = max(max_evaluation, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_evaluation

        min_evaluation = float("inf")
        for column in valid_moves:
            board_copy = board.copy()
            board_copy.drop_chip(column, 1 if self.get_id() == 2 else 2)
            evaluation = self.minimax(
                board_copy, depth-1, alpha, beta, True)
            min_evaluation = min(min_evaluation, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_evaluation
