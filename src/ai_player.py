"""
Connect Four  AI Player Module
"""

import numpy as np
from player import Player
import time
from collections import OrderedDict


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
        self.cache = OrderedDict()
        self.cache_max_size = 5000

    def get_best_move(self, board, total_moves):
        """
        Determine the best move to make for the AI player on the given game board.

        Args:
            board (Board): An instance of the game board representing the current game state.
            total_moves (int): The total number of moves made in the game so far.

        Returns:
            int: The column number representing the best move for the AI player to make.
        """
        best_move = None
        depth = 5  # Initial depth for iterative deepening search
        time_start = time.time()
        time_limit = 10  # seconds
        safety_margin = 0.5  # seconds, allows function call overhead

        while time.time() - time_start < time_limit - safety_margin:
            current_best_move = self.iterative_deepen(
                board, depth, total_moves, time_start, time_limit-safety_margin)
            if current_best_move is not None:
                best_move = current_best_move
            depth += 1

        print(f"AI Player: Best move is {best_move},  reached depth {depth-1}")
        return best_move

    def iterative_deepen(self, board, depth, total_moves, time_start, time_limit):
        """
        Perform iterative deepening search to find the best move for the AI player.

        Args:
            board (Board): An instance of the game board representing the current game state.
            depth (int): The initial depth for the iterative deepening search.
            total_moves (int): The total number of moves made in the game so far.
            time_start (float): The time at which the search began.
            time_limit (float): The maximum time allowed for the search.

        Returns:
            tuple: A tuple containing the best move and its corresponding minimax score.
        """
        center_columns = [3, 2, 4, 1, 5, 0, 6]
        valid_moves = [
            col for col in center_columns if board.is_valid_location(col)]

        # Order valid_moves based on historical scores, defaulting to 0 for unseen moves
        valid_moves.sort(key=lambda col: self.cache.get(col, 0), reverse=True)

        best_score = float("-inf")
        best_move = None

        for column in valid_moves:
            alpha = float("-inf")
            beta = float("inf")
            if time.time() - time_start > time_limit:
                break  # Stop searching if time limit exceeded
            
            row = board.get_next_empty_row(column)
            board.drop_chip(column, 2)
            total_moves += 1
            
            score, _ = self.minimax(
                board, depth-1, alpha, beta, False, total_moves)

            if score > best_score:
                best_score = score
                best_move = column
            
            board.board[row][column] = 0 # Undo move
            total_moves -= 1
            
        return best_move

    def evaluate_window(self, window):
        """
        Evaluate the score of a 4-chip window on the game board for a specific player.

        Args:
            window (list): A list representing a window of 4 chips on the game board.

        Returns:
            int: A numerical score indicating window desirability for the specified player.
            Positive scores favor the player, while negative scores indicate disadvantage.
        """
        score = 0
        
        if window.count(2) == 4:
            score += 10000
        if window.count(2) == 3 and window.count(0) == 1:
            score += 100
        if window.count(2) == 2 and window.count(0) == 2:
            score += 10

        if window.count(1) == 4:
            score -= 10000
        if window.count(1) == 3 and window.count(0) == 1:
            score -= 100
        if window.count(1) == 2 and window.count(0) == 2:
            score -= 10

        return score

    def heuristic_value(self, board):
        """
        Calculate a heuristic value to assess the desirability of the current game state.

        Args:
            board (Board): An instance of the game board representing the current game state.

        Returns:
            int:  A numerical value indicating the heuristic assessment of the current game state.
            Positive values indicate advantage, while negative values indicate disadvantage.
        """
        # Score for the current board state for AI player
        score = 0

        # Check horizontal
        for row in range(ROW_COUNT):
            row_array = [int(i) for i in list(board.board[row, :])]
            for col in range(COLUMN_COUNT-3):
                window = row_array[col:col+4]
                score += self.evaluate_window(window)

        # Check vertical
        for col in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board.board[:, col])]
            for row in range(ROW_COUNT-3):
                window = col_array[row:row+4]
                score += self.evaluate_window(window)

        # Check positive slope diagonals
        for row in range(ROW_COUNT-3):
            for col in range(COLUMN_COUNT-3):
                window = [board.board[row+i][col+i] for i in range(4)]
                score += self.evaluate_window(window)

        # Check negative slope diagonals
        for row in range(ROW_COUNT-3):
            for col in range(COLUMN_COUNT-3):
                window = [board.board[row+3-i][col+i] for i in range(4)]
                score += self.evaluate_window(window)

        return score

    def generate_cache_key(self, board, depth, is_maximizing, total_moves):
        """
        Generate a unique key for the current game state to

        Args:
            board (Board): An instance of the game board representing the current game state.
            depth (int): The depth of the search tree, indicating how many moves ahead to consider.
            is_maximizing (bool): A boolean indicating whether the current node is a maximizing or minimizing node.

        Returns:
            tuple: A tuple containing the board state, depth, and a boolean indicating whether the current node is a maximizing node.

        """
        board_state = tuple(tuple(row) for row in board.board)
        current_turn = 2 if is_maximizing else 1
        return (board_state, depth, current_turn, total_moves)

    def check_if_terminal_node(self, board):
        """
        Check if the current game state is a terminal node (i.e., a win for either player).

        Args:
            board (Board): An instance of the game board representing the current game state.
            depth (int): The depth of the search tree, indicating how many moves ahead to consider.

        Returns:
            int: The value of the terminal node, if the game is won by either player. Otherwise, False.
        """
        node = False

        if board.is_winner(2):
            return 10000
        if board.is_winner(1):
            return -10000
        return node
    
    def get_cache_value(self, key):
        
        if key not in self.cache:
            return None
        self.cache.move_to_end(key) # Mark key as recently used
        return self.cache[key]
    
    def set_cache_value(self, key, value):
        if key in self.cache:
            # Move key to the end to mark it as recently used
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.cache_max_size:
            print(f"Evicting cache item: {self.cache.popitem(last=False)}")
            self.cache.popitem(last=False) # Remove the least recently used item

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
        cache_key = self.generate_cache_key(board, depth, is_maximizing, total_moves)

        cached_value = self.get_cache_value(cache_key)
        if cached_value is not None:
            cached_score, cached_best_move, cached_depth = cached_value
            if cached_depth >= depth:
                return cached_score, cached_best_move

        terminal_node = self.check_if_terminal_node(board)

        if depth == 0 or terminal_node:
            if terminal_node:  # If the game is won, return the terminal node value
                return terminal_node, None
            elif total_moves == 42:  # 42 is the maximum number of moves in Connect Four, so the game is a draw
                return 0
            else:  # If the depth is 0, return the heuristic value of the board
                return self.heuristic_value(board), None

        valid_moves = [column for column in range(
            COLUMN_COUNT) if board.is_valid_location(column)]

        if is_maximizing:
            value = float("-inf")
            best_move = None
            for column in valid_moves:
                row = board.get_next_empty_row(column)
                board_copy = board.copy()
                board_copy.drop_chip(column, 2)
                new_value, _ = self.minimax(
                    board_copy, depth-1, alpha, beta, False, total_moves)
                board_copy.board[row][column] = 0  # Undo move
                total_moves -= 1
                if new_value > value:
                    value = new_value
                    best_move = column
                alpha = max(alpha, value)
                if value >= beta:
                    break
            self.set_cache_value(cache_key, (value, best_move, depth))
            return value, best_move
        else:
            value = float("inf")
            best_move = None
            for column in valid_moves:
                row = board.get_next_empty_row(column)
                board_copy = board.copy()
                board_copy.drop_chip(column, 1)
                total_moves += 1
                new_value, _ = self.minimax(
                    board_copy, depth-1, alpha, beta, True, total_moves)
                board_copy.board[row][column] = 0  # Undo move
                total_moves -= 1
                if new_value < value:
                    value = new_value
                    best_move = column
                beta = min(beta, value)
                if value <= alpha:
                    break
            self.set_cache_value(cache_key, (value, best_move, depth))
            return value, best_move
