"""
Test module for the AIPlayer class.
"""

import unittest
import numpy as np
from src.ai_player import AIPlayer, ROW_COUNT, COLUMN_COUNT


class MockBoard:
    """
    A mock version of the Board class to simulate game states.
    """

    def __init__(self):
        self.board = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)

    def is_valid_location(self, column):
        """
        Check if dropping a chip in the specified column is valid.
        """
        return self.board[0, column] == 0

    def get_next_empty_row(self, column):
        """
        Get the next empty row in the specified column.
        """
        for r in range(ROW_COUNT-1, -1, -1):
            if self.board[r, column] == 0:
                return r
        return None

    def drop_chip(self, column, chip):
        """
        Drop a chip in the specified column for a player.
        """
        row = self.get_next_empty_row(column)
        if row is not None:
            self.board[row, column] = chip

    def is_winner(self, player_id):
        """
        Check if the specified player has won the game.
        """
        # Simplified check for horizontal win
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT - 3):
                if all(self.board[row][col+i] == player_id for i in range(4)):
                    return True
        return False

    def is_game_over(self):
        """
        Check if the game is over.
        """
        return np.all(self.board[0, :] != 0)

    def copy(self):
        """
        Create a copy of the board.
        """
        new_board = MockBoard()
        new_board.board = np.copy(self.board)
        return new_board


class TestAIPlayer(unittest.TestCase):
    """
    Test the AIPlayer class and its methods in different scenarios.

    Args:
        unittest (_type_): _description_
    """

    def setUp(self):
        self.ai_player = AIPlayer(player_id=2)
        self.board = MockBoard()

    def test_center_preference(self):
        """
        Test that the AI prefers to play in the center column when no immediate threats
        or opportunities are present.
        """

        best_move = self.ai_player.get_best_move(self.board)
        self.assertEqual(
            best_move, 3, "AI should prefer the center column when the board is empty")

    def test_winning_move_identifying(self):
        """
        Test if the AI correctly identifies and makes a winning move.
        """

        for _ in range(3):
            self.board.drop_chip(3, 2)  # AI's chip

        expected_winning_column = 2
        chosen_column = self.ai_player.get_best_move(self.board)
        self.assertEqual(chosen_column, expected_winning_column,
                         "AI should win the game by dropping chip to column 2")

    def test_get_next_empty_row_full_column(self):
        """
        Test that get_next_empty_row returns None for a completely filled column.
        """
        column = 3

        for _ in range(ROW_COUNT):
            self.board.drop_chip(column, 1)

        next_empty_row = self.board.get_next_empty_row(column)
        self.assertIsNone(
            next_empty_row, "Expected None for a full column, aka no empty rows are available.")

    def test_drop_chip_in_full_column(self):
        """
        Test that drop_chip does not add a chip to a full column.
        """
        column = 3

        for _ in range(ROW_COUNT):
            self.board.drop_chip(column, 2)  # AI's chip

        # Attempt to drop another chip into the full column
        self.board.drop_chip(column, 2)

        # Verify the column is still full and no additional chip has been added
        is_column_full = all(
            self.board.board[row][column] == 2 for row in range(ROW_COUNT))
        self.assertTrue(
            is_column_full,\
                "Column should remain unchanged after attempting to drop a chip into it.")

        # Also verify the top of the column did not change
        self.assertEqual(
            self.board.board[0][column], 2,\
                "The top of the column should remain occupied by the original chip.")

    def test_ai_skips_full_columns_when_choosing_move(self):
        """
        Test that the AI skips full columns when choosing the best move.
        """

        full_column = 3

        for _ in range(ROW_COUNT):
            # Fill with opponent's chips, we ignore winning moves for this test
            self.board.drop_chip(full_column, 1)

        # Adding chips to other columns to ensure the AI has to consider other columns
        self.board.drop_chip(2, 2)
        self.board.drop_chip(4, 2)

        best_move = self.ai_player.get_best_move(self.board)
        self.assertNotEqual(
            best_move, full_column, "AI should not choose a full column as the best move")
