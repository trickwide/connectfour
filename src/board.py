"""
Connect Four Board Module
"""

import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7

class Board:
    """
    Represents a Connect Four board.
    """

    def __init__(self):
        """
        Initialize a Connect Four board.
        """
        self.board = self.generate_board()

    def generate_board(self):
        """
        Generate a new Connect Four board.

        Returns:
            array: A 2D array representing the Connect Four board.
        """
        board = np.zeros((ROW_COUNT, COLUMN_COUNT))
        return board

    def drop_chip(self, row, column, chip):
        """
        Drop a chip on the board at the specified row and column.

        Args:
            row (int): The row where the chip will be placed.
            column (int): The column where the chip will be placed.
            chip (int): The player's chip (1 for red, 2 for yellow)
        """
        self.board[row][column] = chip

    def is_valid_location(self, column):
        """
        Check if a given column is a valid location for dropping a chip.

        Args:
            column (int): The column to be checked.

        Returns:
            bool: True if the column is valid, False otherwise.
        """
        return self.board[ROW_COUNT-1][column] == 0

    def get_next_empty_row(self, column):
        """
        Get the next available empty row in a given column.

        Args:
            column (int): The column to search for an empty row.

        Returns:
            int: The row index of the next available empty row in the column.
        """
        for r in range(ROW_COUNT):
            if self.board[r][column] == 0:
                return r

        return -1
