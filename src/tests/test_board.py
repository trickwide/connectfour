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
        board.drop_chip(3, 1)
        board.drop_chip(3, 1)
        board.drop_chip(3, 1)
        board.drop_chip(3, 1)
        self.assertTrue(board.is_winner(1))
        self.assertFalse(board.is_winner(2))

    def test_is_winner_horizontal(self):
        """
        Test the is_winner method with a horizontal win.
        """
        board = Board()
        board.drop_chip(0, 1)
        board.drop_chip(1, 1)
        board.drop_chip(2, 1)
        board.drop_chip(3, 1)
        self.assertTrue(board.is_winner(1))
        self.assertFalse(board.is_winner(2))

    def test_is_winner_positive_diagonal(self):
        """
        Test the is_winner method with a positive diagonal win.
        """
        board = Board()
        for i in range(4):
            board.board[i][i] = 1
        self.assertTrue(board.is_winner(1))

    def test_is_winner_negative_diagonal(self):
        """
        Test the is_winner method with a negative diagonal win.
        """
        board = Board()
        for i in range(4):
            board.board[3 - i][i] = 1
        self.assertTrue(board.is_winner(1))

    def test_is_not_winner_positive_diagonal(self):
        """
        Test the is_winner method with a non-winning positive diagonal.
        """
        board = Board()
        for i in range(3):
            board.board[i][i] = 1
        self.assertFalse(board.is_winner(1))

    def test_is_not_winner_negative_diagonal(self):
        """
        Test the is_winner method with a non-winning negative diagonal.
        """
        board = Board()
        for i in range(3):
            board.board[3 - i][i] = 1
        self.assertFalse(board.is_winner(1))
