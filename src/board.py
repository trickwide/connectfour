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
            self.last_move = (row, column)  # Update the last move
            return (row, column)
        else:
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

    def is_winner(self, player_id):
        # Check valid horizontal locations for win
        for c in range(self.column_count - 3):
            for r in range(self.row_count):
                if self.board[r][c] == player_id and self.board[r][c + 1] == player_id and self.board[r][c + 2] == player_id and self.board[r][c + 3] == player_id:
                    return True

        # Check valid vertical locations for win
        for c in range(self.column_count):
            for r in range(self.row_count - 3):
                if self.board[r][c] == player_id and self.board[r + 1][c] == player_id and self.board[r + 2][c] == player_id and self.board[r + 3][c] == player_id:
                    return True

        # Check valid positive diagonal locations for win
        for c in range(self.column_count - 3):
            for r in range(self.row_count - 3):
                if self.board[r][c] == player_id and self.board[r + 1][c + 1] == player_id and self.board[r + 2][c + 2] == player_id and self.board[r + 3][c + 3] == player_id:
                    return True

        # check valid negative diagonal locations for win
        for c in range(self.column_count - 3):
            for r in range(3, self.row_count):
                if self.board[r][c] == player_id and self.board[r - 1][c + 1] == player_id and self.board[r - 2][c + 2] == player_id and self.board[r - 3][c + 3] == player_id:
                    return True

        return False
