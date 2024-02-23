"""
Connect Four  AI Player Module
"""

import numpy as np
from player import Player
import time

ROW_COUNT = 6
COLUMN_COUNT = 7


class AIPlayer(Player):
    """
    Represents an AI player in the Connect Four game.

    Args:
        Player (class): The parent class of the AIPlayer class. 
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = {}

    def get_best_move(self, board, total_moves, max_depth=20):
        """
        Determine the best move to make for the AI player on the given game board.

        Args:
            board (Board): An instance of the game board representing the current game state.

        Returns:
            int: The column number representing the best move for the AI player to make.
                This move is determined using the minimax algorithm with a max_depth of 20.
        """
        immediate_block_move = self.find_immediate_threat(board)
        if immediate_block_move is not None:
            return immediate_block_move

        center_columns = [3, 2, 4, 1, 5, 0, 6]
        valid_moves = [
            col for col in center_columns if board.is_valid_location(col)]

        best_move = None
        time_start = time.time()
        time_limit = 3  # seconds

        for depth in range(1, max_depth):
            best_score = float("-inf")
            alpha = float("-inf")
            beta = float("inf")
            for column in valid_moves:
                if not board.is_valid_location(column):
                    continue
                row = board.get_next_empty_row(column)
                board.drop_chip(column, 2)
                score = self.minimax(board, depth, alpha, beta, False, total_moves + 1)
                board.board[row][column] = 0  # Undo move

                if score > best_score:
                    best_score = score
                    best_move = column

                if time.time() - time_start > time_limit:
                    print(f"Depth reached before time limit: {depth}")
                    return best_move

        return best_move

    def find_immediate_threat(self, board):
        """
        Check for an immediate threat where the opponent is one move away from winning.

        Args:
            board (Board): The game board representing the current game state.

        Returns:
            int: The column to block the opponent's winning move, if a threat is found.
            None otherwise.
        """
        for column in range(COLUMN_COUNT):
            if board.is_valid_location(column):
                row = board.get_next_empty_row(column)
                board.drop_chip(column, 1)
                if board.is_winner(1):
                    board.board[row][column] = 0
                    print("Found a threat")
                    return column
                board.board[row][column] = 0
        return None

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
            
            score -= 200

        # Promote center control
        if ai_count == 2 and empty_count == 2 and window[2] == player_id:
            score += 15

        # Slight reward for potential winning move
        if ai_count == 2 and empty_count == 2:
            score += 5
        if opponent_count == 2 and empty_count == 2:
            score -= 10  # Penalize potential winning opportunity of opponent

        if ai_count == 1 and empty_count == 3:
            score += 2  # Encourage building towards future opportunities
        if opponent_count == 1 and empty_count == 3:
            score -= 4  # Discourage AI to reflect the potential threat

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
    
    def generate_cache_key(self, board, player_id):
        board_state = tuple(tuple(row) for row in board.board)
        return (board_state, player_id)
    
    def check_if_terminal_node(self, board, depth):
        node = False
        
        if board.is_winner(2):
            node = 2000
            
            if depth == 19:
                node = 3000
        if board.is_winner(1):
            node = -2000
            if depth == 18:
                node = -3000
        return node
            

    def minimax(self, board, depth, alpha, beta, is_maximizing, total_moves):
        """
        Minimax algorithm with alpha-beta pruning to determine the best move for the AI player.

        Args:
            board (Board): An instance of the game board representing the current game state.
            depth (int): The depth of the search tree, indicating how many moves ahead to consider.
            alpha (float): Represents the minimum score that the maximizing player is assured of.
            beta (float): Represents maximum score that the minimizing player is assured of.
            player_id (int): The ID of the player who is making the current move.

        Returns:
            int: The minimax evaluation score indicating the desirability of the current game state.
        """
        total_moves_copy = total_moves
        cache_key = self.generate_cache_key(board, 2)
        
        terminal_node = self.check_if_terminal_node(board, depth)
        
        if terminal_node is not False:
            return terminal_node
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        if depth == 0:
            return self.heuristic_value(board, 2)
        
        if total_moves == 42:
            return 0

        valid_moves = [column for column in range(COLUMN_COUNT) if board.is_valid_location(column)]
        
        # Valid moves ykköseksi parhaan siirron nosto kärkeen, parhaan arvon ja parhaan siirron vaihto. Vanhan poisto ettei ole tuplana

        if is_maximizing:
            print("maximizing")
            max_evaluation = float("-inf")
            best_column = None
            for column in valid_moves:
                board_copy = board.copy()
                board_copy.drop_chip(column, 2)
                evaluation = self.minimax(board_copy, depth-1, alpha, beta, False, total_moves_copy+1)
                if evaluation > max_evaluation:
                    max_evaluation = evaluation
                    best_column = column
                    valid_moves.remove(best_column)
                    valid_moves.insert(0, best_column)
                alpha = max(alpha, evaluation)
                if alpha >= beta:
                    break
            self.cache[cache_key] = max_evaluation
            return max_evaluation
        else:
            print("minimizing")
            min_evaluation = float("inf")
            best_column = None
            for column in valid_moves:
                board_copy = board.copy()
                board_copy.drop_chip(column, 1)
                evaluation = self.minimax(board_copy, depth-1, alpha, beta, True, total_moves+1)
                if evaluation < min_evaluation:
                    min_evaluation = evaluation
                    best_column = column
                    valid_moves.remove(best_column)
                    valid_moves.insert(0, best_column)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            self.cache[cache_key] = min_evaluation
            return min_evaluation

