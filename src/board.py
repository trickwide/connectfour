"""
Connect Four Board Module
"""

import numpy as np


class Board:
    """
    Represents a Connect Four board.
    """

    def __init__(self):
        """
        Initialize a Connect Four board.
        """
        self.row_count = 6
        self.column_count = 7
        self.board = self.generate_board()

    def generate_board(self):
        """
        Generate a new Connect Four board.

        Returns:
            array: A 2D array representing the Connect Four board.
        """
        board = np.zeros((self.row_count, self.column_count))
        return board

    def copy(self):
        """
        Create a copy of the current board.

        Returns:
            Board: A copy of the current board.
        """
        board_copy = Board()
        board_copy.board = self.board.copy()
        return board_copy

    def drop_chip(self, column, chip):
        """
        Drop a chip into the specified column of the board.

        Args:
            column (int): The column where the chip will be placed.
            chip (int): The player's chip (1 for red, 2 for yellow)

        Returns:
            tuple: A tuple representing the location of the dropped chip (row, column).
            Otherwise, None.
        """
        row_counter = self.row_count - 1
        for _ in range(self.row_count):
            if self.board[row_counter][column] == 0:
                self.board[row_counter][column] = chip
                return (row_counter, column)
            row_counter -= 1
        return None

    def is_valid_location(self, column):
        """
        Check if a given column is a valid location for dropping a chip.

        Args:
            column (int): The column to be checked.

        Returns:
            bool: True if the column is valid, False otherwise.
        """
        return self.board[0][column] == 0

    def get_next_empty_row(self, column):
        """
        Get the next available empty row in a given column.

        Args:
            column (int): The column to search for an empty row.

        Returns:
            int: The row index of the next available empty row in the column.
        """
        for row in range(self.row_count-1, -1, -1):
            if self.board[row][column] == 0:
                return row

        return -1

    def is_winner(self, player_id):
        """
        Check if a given player has won the game.

        Args:
            player_id (int): The id of the player (1 for red, 2 for yellow).

        Returns:
           bool: True if the player has won, False otherwise.
        """
        # Viimeisimmän siirron passaus, viimeinen siirto on osa riviä. Lasketaan, mennään niin kauan eteenpäin kunnes ei enää löydy pelaajan merkkiä. esim. while -silmukka
        
        # Check for a horizontal win
        for row in range(self.row_count):
            for column in range(self.column_count - 3):
                if self.board[row][column] == player_id and \
                        self.board[row][column+1] == player_id and \
                        self.board[row][column+2] == player_id and \
                        self.board[row][column+3] == player_id:
                    return True

        # Check for a vertical win
        for column in range(self.column_count):
            for row in range(self.row_count - 3):
                if self.board[row][column] == player_id and \
                        self.board[row+1][column] == player_id and \
                        self.board[row+2][column] == player_id and \
                        self.board[row+3][column] == player_id:
                    return True

        # Check for a diagonal win (positive slope)
        for row in range(self.row_count - 3):
            for column in range(self.column_count - 3):
                if self.board[row][column] == player_id and \
                        self.board[row+1][column+1] == player_id and \
                        self.board[row+2][column+2] == player_id and \
                        self.board[row+3][column+3] == player_id:
                    return True

        # Check for a diagonal win (negative slope)
        for row in range(3, self.row_count):
            for column in range(self.column_count - 3):
                if self.board[row][column] == player_id and \
                        self.board[row-1][column+1] == player_id and \
                        self.board[row-2][column+2] == player_id and \
                        self.board[row-3][column+3] == player_id:
                    return True

        return False

    def is_game_over(self):
        """
        Check if the game is over.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        return self.is_board_full() or self.is_winner(1) or self.is_winner(2)

    def is_board_full(self):
        """
        Check if the board is full.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        return np.all(self.board != 0)
