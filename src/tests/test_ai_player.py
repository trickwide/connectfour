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
        self.row_count = ROW_COUNT
        self.column_count = COLUMN_COUNT
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
            self.board[row][column] = chip
            return (row, column)
        return None

    def is_winner(self, player_id):
        """
        Check if the specified player has won the game.
        """
        # Check valid horizontal locations for win
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if self.board[r][c] == player_id and self.board[r][c + 1] == player_id and self.board[r][c + 2] == player_id and self.board[r][c + 3] == player_id:
                    return True

        # Check valid vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if self.board[r][c] == player_id and self.board[r + 1][c] == player_id and self.board[r + 2][c] == player_id and self.board[r + 3][c] == player_id:
                    return True

        # Check valid positive diagonal locations for win
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if self.board[r][c] == player_id and self.board[r + 1][c + 1] == player_id and self.board[r + 2][c + 2] == player_id and self.board[r + 3][c + 3] == player_id:
                    return True

        # check valid negative diagonal locations for win
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if self.board[r][c] == player_id and self.board[r - 1][c + 1] == player_id and self.board[r - 2][c + 2] == player_id and self.board[r - 3][c + 3] == player_id:
                    return True

            return False

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

        best_move = self.ai_player.get_best_move(self.board, 0)
        self.assertEqual(
            best_move, 3, "AI should prefer the center column when the board is empty")

    def test_winning_move_identifying(self):
        """
        Test if the AI correctly identifies and makes a winning move.
        """

        for _ in range(3):
            self.board.drop_chip(3, 2)  # AI's chip

        expected_winning_column = 3
        chosen_column = self.ai_player.get_best_move(self.board, total_moves=3)
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
            is_column_full,
            "Column should remain unchanged after attempting to drop a chip into it.")

        # Also verify the top of the column did not change
        self.assertEqual(
            self.board.board[0][column], 2,
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

        best_move = self.ai_player.get_best_move(self.board, total_moves=8)
        self.assertNotEqual(
            best_move, full_column, "AI should not choose a full column as the best move")

    def test_get_best_move_none(self):
        """
        Test the get_best_move method when iterative_deepen returns None for current_best_move.
        """
        # Fill the board with chips so that no winning move is available and return NOne
        for _ in range(6):
            for i in range(7):
                self.board.drop_chip(i, -1)  # -1 is a placeholder for any chip

        self.assertIsNone(self.ai_player.get_best_move(
            self.board, total_moves=42))

    def test_minimax_returns_tuple_of_None_and_0(self):
        """
        Test the minimax method when the depth is 0 and the board is full.
        """
        # Fill the board with chips so that no winning move is available and we ensure returning 0
        for _ in range(6):
            for i in range(7):
                self.board.drop_chip(i, -1)  # -1 is a placeholder for any chip

        self.assertEqual(self.ai_player.minimax(
            self.board, 0, -np.inf, np.inf, True, 42), (None, 0))

    def test_evaluate_window_count_ai_four_chips(self):
        """
        Test the evaluate_window method when the window contains 4 AI chips.
        """
        window = [2, 2, 2, 2]
        self.assertEqual(self.ai_player.evaluate_window(window), 1000)

    def test_evaluate_window_count_opponent_four_chips(self):
        """
        Test the evaluate_window method when the window contains 4 opponent chips.
        """
        window = [1, 1, 1, 1]
        self.assertEqual(self.ai_player.evaluate_window(window), -1000)

    def test_evaluate_window_count_ai_three_chips(self):
        """
        Test the evaluate_window method when the window contains 3 AI chips.
        """
        window = [2, 2, 2, 0]
        self.assertEqual(self.ai_player.evaluate_window(window), 100)

    def test_evaluate_window_count_opponent_three_chips(self):
        """
        Test the evaluate_window method when the window contains 3 opponent chips.
        """
        window = [1, 1, 1, 0]
        self.assertEqual(self.ai_player.evaluate_window(window), -100)

    def test_evaluate_window_count_ai_two_chips(self):
        """
        Test the evaluate_window method when the window contains 2 AI chips.
        """
        window = [2, 2, 0, 0]
        self.assertEqual(self.ai_player.evaluate_window(window), 10)

    def test_evaluate_window_count_opponent_two_chips(self):
        """
        Test the evaluate_window method when the window contains 2 opponent chips.
        """
        window = [1, 1, 0, 0]
        self.assertEqual(self.ai_player.evaluate_window(window), -10)

    def test_evaluate_window_count_no_chips(self):
        """
        Test the evaluate_window method when the window contains no chips.
        """
        window = [0, 0, 0, 0]
        self.assertEqual(self.ai_player.evaluate_window(window), 0)

    def test_evaluate_window_mixed_chips(self):
        """
        Test the evaluate_window method when the window contains a mix of AI and opponent chips.
        """
        window = [2, 1, 2, 0]
        self.assertEqual(self.ai_player.evaluate_window(window), 0)

    def test_heuristic_evaluation_multiple_winning_scenarios(self):
        """
        Test the heuristic_evaluation method when multiple winning scenarios are present.
        """
        for c in range(self.board.column_count):
            # Leave the top row empty for simplicity
            for r in range(self.board.row_count - 1):
                if c % 2 == 0:
                    self.board.board[r][c] = 2  # AI's chip
                else:
                    self.board.board[r][c] = 1  # Opponent's chip

        # Clear spot for AI
        self.board.board[2][self.board.column_count - 1] = 0
        # Clear spot for opponent
        self.board.board[3][self.board.column_count - 1] = 0

        ai_heuristic_value = self.ai_player.heuristic_value(self.board)

        self.assertGreater(ai_heuristic_value, 0,
                           "AI should have a positive heuristic value")

    def test_heuristic_threat_creation(self):
        """
        Test the heuristic method when the AI creates a threat.
        """
        # Set up a scenario where AI has two non-contiguous three-in-a-row opportunities
        # First threat
        self.board.board[5][2] = self.board.board[5][3] = self.board.board[5][4] = 2
        # Second threat setup
        self.board.board[5][0] = self.board.board[4][1] = self.board.board[3][2] = 2

        # Evaluate heuristic value
        heuristic_value_before = self.ai_player.heuristic_value(self.board)

        # Make a move that creates the second threat
        self.board.drop_chip(2, 2)  # Assuming this creates the second threat

        # Evaluate heuristic value after creating the threat
        heuristic_value_after = self.ai_player.heuristic_value(self.board)

        # The heuristic value should increase after creating multiple threats
        self.assertGreater(heuristic_value_after, heuristic_value_before,
                           "Heuristic should value creating multiple winning threats positively.")

    def test_heuristic_opponent_threat_avoidance(self):
        """
        Test the heuristic method when the AI avoids an opponent's threat.
        """
        # Opponent has two chips in a row and the AI can block the winning move
        self.board.board[5][2] = self.board.board[5][3] = 1

        # Evaluate heuristic value
        heuristic_value_before = self.ai_player.heuristic_value(self.board)

        # Make a move that blocks the opponent's winning move
        self.board.drop_chip(4, 2)

        # Evaluate heuristic value after blocking the opponent's winning move
        heuristic_value_after = self.ai_player.heuristic_value(self.board)

        # The heuristic value should increase after blocking the opponent's winning move
        self.assertGreater(heuristic_value_after, heuristic_value_before,
                           "Heuristic should value blocking opponent's winning moves positively.")
