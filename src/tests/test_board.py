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
        self.assertEqual(board.get_next_empty_row(3), -1)

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

    def test_is_winner_diagonal_positive_slope(self):
        """
        Test the is_winner method with a diagonal win (positive slope).
        """
        board = Board()
        board.drop_chip(0, 1)
        board.drop_chip(1, 2)
        board.drop_chip(1, 1)
        board.drop_chip(2, 2)
        board.drop_chip(2, 2)
        board.drop_chip(2, 1)
        board.drop_chip(3, 2)
        board.drop_chip(3, 2)
        board.drop_chip(3, 2)
        board.drop_chip(3, 1)
        self.assertTrue(board.is_winner(1))
        self.assertFalse(board.is_winner(2))

    def test_is_winner_diagonal_negative_slope(self):
        """
        Test the is_winner method with a diagonal win (negative slope).
        """
        board = Board()
        board.drop_chip(0, 1)
        board.drop_chip(0, 1)
        board.drop_chip(0, 1)
        board.drop_chip(0, 2)
        board.drop_chip(1, 1)
        board.drop_chip(1, 1)
        board.drop_chip(1, 2)
        board.drop_chip(2, 1)
        board.drop_chip(2, 2)
        board.drop_chip(3, 2)
        self.assertTrue(board.is_winner(2))
        self.assertFalse(board.is_winner(1))

    def test_is_game_over(self):
        """
        Test the is_game_over method when the game is not over.
        """
        board = Board()
        self.assertFalse(board.is_game_over())

    def test_is_game_over_full_board(self):
        """
        Test the is_game_over method when the board is full.
        """
        board = Board()
        for column in range(7):
            for _ in range(6):
                board.drop_chip(column, 1)
        self.assertTrue(board.is_game_over())

    def test_is_game_over_player1_winner(self):
        """
        Test the is_game_over method when player 1 has won.
        """
        board = Board()
        for column in range(4):
            board.drop_chip(column, 1)
        self.assertTrue(board.is_game_over())

    def test_is_game_over_player2_winner(self):
        """
        Test the is_game_over method when player 2 has won.
        """
        board = Board()
        for column in range(4):
            board.drop_chip(column, 2)
        self.assertTrue(board.is_game_over())

    def test_is_board_full_with_empty_board(self):
        """
        Test the is_board_full method with an empty board.
        """
        board = Board()
        self.assertFalse(board.is_board_full())

    def test_is_board_full_with_full_board(self):
        """
        Test the is_board_full method with a full board.
        """
        board = Board()
        for column in range(7):
            for _ in range(6):
                board.drop_chip(column, 1)
        self.assertTrue(board.is_board_full())
