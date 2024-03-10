"""
Test module for the Board class.
"""

import unittest
import numpy as np
from src.board import Board


class TestBoard(unittest.TestCase):
    """
    Test the Board class and its methods in different scenarios.

    Args:
        unittest (_type_): _description_
    """

    def test_generate_board(self):
        """
        Test the generate_board method.
        """
        board = Board()
        self.assertEqual(board.row_count, 6)
        self.assertEqual(board.column_count, 7)
        self.assertTrue((board.board == np.zeros((6, 7))).all())

    def test_copy(self):
        """
        Test the copy method.
        """
        board = Board()
        board_copy = board.copy()
        self.assertTrue((board.board == board_copy.board).all())

    def test_drop_chip(self):
        """
        Test the drop_chip method.
        """
        board = Board()
        self.assertEqual(board.drop_chip(3, 1), (5, 3))
        self.assertEqual(board.board[5][3], 1)

    def test_drop_chip_to_full_column(self):
        """
        Test the drop_chip method when the column is full.
        """
        board = Board()
        for _ in range(6):
            board.drop_chip(3, 1)
        self.assertEqual(board.drop_chip(3, 1), None)
        self.assertEqual(board.board[0][3], 1)

    def test_is_valid_location(self):
        """
        Test the is_valid_location method with empty column.
        """
        board = Board()
        self.assertTrue(board.is_valid_location(3))

    def test_is_not_valid_location(self):
        """
        Test the is_valid_location method with full column.
        """
        board = Board()
        for _ in range(6):
            board.drop_chip(3, 1)
        self.assertFalse(board.is_valid_location(3))

    def test_get_next_empty_row(self):
        """
        Test the get_next_empty_row method.
        """
        board = Board()
        self.assertEqual(board.get_next_empty_row(3), 5)

    def test_get_next_empty_row_from_full_column(self):
        """
        Test the get_next_empty_row method when the column is full.
        """
        board = Board()
        for _ in range(6):
            board.drop_chip(3, 1)
        self.assertEqual(board.get_next_empty_row(3), None)

    def test_is_winner_vertical(self):
        """
        Test the is_winner method with a vertical win.
        """
        board = Board()
        last_row, last_col = None, 3  # Column where chips are dropped
        for _ in range(4):  # Dropping 4 chips in the same column for a vertical win
            last_row, _ = board.drop_chip(last_col, 1)
        self.assertTrue(board.is_winner(last_row, last_col, 1),
                        "Expected a vertical win for player 1")
        self.assertFalse(board.is_winner(last_row, last_col, 2),
                         "Expected no win for player 2")

    def test_is_winner_horizontal(self):
        """
        Test the is_winner method with a horizontal win.
        """
        board = Board()
        last_row, last_col = 5, None  # Starting row for horizontal placement
        for i in range(4):  # Dropping 4 chips in consecutive columns for a horizontal win
            last_col = i
            board.drop_chip(i, 1)
        self.assertTrue(board.is_winner(last_row, last_col, 1),
                        "Expected a horizontal win for player 1")
        self.assertFalse(board.is_winner(last_row, last_col, 2),
                         "Expected no win for player 2")

    def test_is_winner_positive_diagonal(self):
        """
        Test the is_winner method with a positive diagonal win.
        """
        board = Board()
        for i in range(4):
            for _ in range(i):  # Fill columns below the diagonal to place the chip correctly
                board.drop_chip(i, -1)  # Use a placeholder to fill the column
            # This chip is part of the diagonal win
            last_row, last_col = board.drop_chip(i, 1)
        self.assertTrue(board.is_winner(last_row, last_col, 1),
                        "Expected a positive diagonal win for player 1")

    def test_is_winner_negative_diagonal(self):
        """
        Test the is_winner method with a negative diagonal win.
        """
        board = Board()
        for i in range(4):
            for _ in range(3 - i):  # Fill columns below the diagonal to place the chip correctly
                board.drop_chip(i, -1)  # Use a placeholder to fill the column
            # This chip is part of the diagonal win
            last_row, last_col = board.drop_chip(i, 1)
        self.assertTrue(board.is_winner(last_row, last_col, 1),
                        "Expected a negative diagonal win for player 1")
