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
        board = np.zeros((self.row_count, self.column_count), dtype=int)
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
        row = self.get_next_empty_row(column)
        if row is not None:  # Check if a valid row was found
            self.board[row][column] = chip
            return (row, column)

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

        return None

    def is_winner(self, last_row, last_col, player_id):
        """
        Check if a player has won the game starting from the last dropped chip.

        Args:
            last_row (int): The row index of the last dropped chip.
            last_col (int): The column index of the last dropped chip.
            player_id (int): The player's chip (1 for red, 2 for yellow).

        Returns:
            boolean: True if the player has won, False otherwise.
        """
        def check_direction(row_step, col_step):
            count = 1  # Starts with 1 to count the last dropped chip itself.
            # Check in the primary direction (forward)
            row, col = last_row + row_step, last_col + col_step
            while 0 <= row < self.row_count and 0 <= col < self.column_count \
                and self.board[row][col] == player_id:
                count += 1
                row += row_step
                col += col_step

            # Check in the opposite direction (backward)
            row, col = last_row - row_step, last_col - col_step
            while 0 <= row < self.row_count and 0 <= col < self.column_count \
                and self.board[row][col] == player_id:
                count += 1
                row -= row_step
                col -= col_step

            return count > 3

        # Check horizontally
        if check_direction(0, 1):
            return True

        # Check vertically
        if check_direction(1, 0):
            return True

        # Check diagonally (positive slope)
        if check_direction(1, 1):
            return True

        # Check diagonally (negative slope)
        if check_direction(-1, 1):
            return True

        return False
