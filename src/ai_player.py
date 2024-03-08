"""
Connect Four  AI Player Module
"""

import time
from player import Player


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

    def get_best_move(self, board, total_moves):
        """
        Determine the best move to make for the AI player on the given game board.

        Args:
            board (Board): An instance of the game board representing the current game state.
            total_moves (int): The total number of moves made in the game so far.

        Returns:
            int: The column number representing the best move for the AI player to make.
        """
        overall_best_move = None
        overall_best_score = float("-inf")
        depth = 5  # Initial depth for iterative deepening search
        time_start = time.time()
        time_limit = 5  # seconds
        safety_margin = 0.5  # seconds, allows function call overhead
        center_columns = [3, 2, 4, 1, 5, 0, 6]

        # Adjust max depth based on the number of empty cells  on the board
        max_depth = ROW_COUNT * COLUMN_COUNT - total_moves
        valid_moves = [col for col in center_columns if board.is_valid_location(col)]

        beta = float("inf")
        while time.time() - time_start < time_limit - safety_margin and depth <= max_depth:
            # Initialize valid moves only on first iteration

            best_move = None
            best_score = alpha = float("-inf")

            for column in valid_moves:
                if time.time() - time_start > time_limit:
                    break  # Stop searching if time limit exceeded
                row = board.get_next_empty_row(column)
                board.drop_chip(column, 2)
                total_moves += 1
                score = self.minimax(
                    board, depth-1, alpha, beta, False, total_moves)[1]
                # Alpha value needs to be updated here as it is the best current score
                if score > best_score:
                    best_score = score
                    best_move = column
                    valid_moves.remove(column)
                    valid_moves.insert(0, column)

                board.board[row][column] = 0  # Undo move
                total_moves -= 1
            if best_score > overall_best_score:
                overall_best_score = best_score
                overall_best_move = best_move
            print(f"Depth: {depth}")
            #jos voittava score break tässä
            depth += 1  # Increment depth for next iteration, if time allows
        return overall_best_move

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
            score += 1000
        if window.count(2) == 3 and window.count(0) == 1:
            score += 100
        if window.count(2) == 2 and window.count(0) == 2:
            score += 10

        if window.count(1) == 4:
            score -= 1000
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

    def generate_cache_key(self, board, depth, is_maximizing):
        """
        Generate a unique key for the current game state to

        Args:
            board (Board): An instance of the game board representing the current game state.
            depth (int): The depth of the search tree. How many moves ahead to consider.
            is_maximizing (bool): A boolean indicating if the node is maximizing or minimizing.

        Returns:
            tuple: A tuple containing the board state, depth, and a boolean.
        """
        board_state = tuple(tuple(row) for row in board.board)
        cache_key = (board_state, depth, is_maximizing)

        return cache_key

    def get_cached_move(self, cache_key):
        """
        Get the cached value for a given game state.

        Args:
            cache_key (tuple): A tuple containing the board state, depth, and a boolean.

        Returns:
            int: The best move for the given game state, if it is cached.
            Otherwise, None.
        """
        return self.cache.get(cache_key, None)

    def check_if_terminal_node(self, board):
        """
        Check if the current game state is a terminal node (i.e., a win for either player).

        Args:
            board (Board): An instance of the game board representing the current game state.
            depth (int): The depth of the search tree. How many moves ahead to consider.

        Returns:
            int: The value of the terminal node, if the game is won by either player.
            Otherwise, False.
        """
        node = False

        if board.is_winner(2):
            return 3000
        if board.is_winner(1):
            return -3000
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
        cache_key = self.generate_cache_key(board, depth, is_maximizing)

        terminal_node = self.check_if_terminal_node(board)

        if depth == 0 or terminal_node:
            if terminal_node:  # If the game is won, return the terminal node value
                return None, terminal_node
            if total_moves == 42:  # 42 is the maximum number of moves, game is a draw
                return None, 0
            # If the depth is 0, return the heuristic value of the board
            return None, self.heuristic_value(board)

        # Prioritize center columns
        center_columns = [3, 2, 4, 1, 5, 0, 6]
        valid_moves = [column for column in
                       center_columns if board.is_valid_location(column)]

        # If cache is hit put the best move to the front of the list
        if cache_key in self.cache:
            best_cached_move = self.cache[cache_key][0]
            if best_cached_move in valid_moves:
                valid_moves.remove(best_cached_move)
                valid_moves.insert(0, best_cached_move)

        if is_maximizing:
            best_move = None
            value = float("-inf")
            for column in valid_moves:
                row = board.get_next_empty_row(column)
                board_copy = board.copy()
                board_copy.drop_chip(column, 2)
                new_value = self.minimax(
                    board_copy, depth-1, alpha, beta, False, total_moves)[1]
                board_copy.board[row][column] = 0  # Undo move
                total_moves -= 1
                if float(new_value) > value:
                    value = new_value
                    best_move = column
                    # Save value and best move to the cache
                    self.cache[cache_key] = (value, best_move)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_move, value
        best_move = None
        value = float("inf")
        for column in valid_moves:
            row = board.get_next_empty_row(column)
            board_copy = board.copy()
            board_copy.drop_chip(column, 1)
            total_moves += 1
            new_value = self.minimax(
                board_copy, depth-1, alpha, beta, True, total_moves)[1]
            board_copy.board[row][column] = 0  # Undo move
            total_moves -= 1
            if float(new_value) < value:
                value = new_value
                best_move = column
                # Save value and best move to the cache
                self.cache[cache_key] = (value, best_move)
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_move, value
