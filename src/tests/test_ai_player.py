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
        self.row_count = 6
        self.column_count = 7
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
            self.last_move = (row, column)
            return (row, column)
        else:
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

    def test_negative_diagonal_extraction(self):
        """
        Test if the AI correctly extracts the negative diagonal from the board.
        """

        # Set up a scenario where the AI has a negative diagonal
        self.board.board[2, 0] = 2
        self.board.board[3, 1] = 2
        self.board.board[4, 2] = 2
        self.board.board[5, 3] = 2

        print("Original board:")
        print(self.board.board)

        # Extract the 4x4 section where we expect the negative diagonal
        section = self.board.board[2:6, 0:4]

        # Apply np.flipud() to the section and extract the diagonal
        flipped_section = np.flipud(section)
        diagonal = flipped_section.diagonal()

        # Check if the diagonal matches the expected pattern
        expected_diagonal = np.array([2, 2, 2, 2])
        correct_extraction = np.array_equal(diagonal, expected_diagonal)

        # Print the results
        print("Extracted Diagonal:", diagonal)
        print("Correct Extraction:", correct_extraction)

        # Ensure original board is not affected by np.flipud on the section
        print("Board after Extraction (Should be unchanged):")
        print(self.board.board)

    def test_get_best_move_none(self):
        """
        Test the get_best_move method when iterative_deepen returns None for current_best_move.
        """
        # Fill the board with chips so that no winning move is available and we ensure returning None
        for _ in range(6):
            for i in range(7):
                self.board.drop_chip(i, 1)

        self.assertIsNone(self.ai_player.get_best_move(self.board, total_moves=14))
    
    def test_minimax_returns_0(self):
        """
        Test the minimax method when the depth is 0 and the board is full.
        """
        # Fill the board with chips so that no winning move is available and we ensure returning 0
        for _ in range(6):
            for i in range(7):
                self.board.drop_chip(i, -1) # -1 is a placeholder for any chip

        self.assertEqual(self.ai_player.minimax(self.board, 0, -np.inf, np.inf, True, 42), 0)
    
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
        
        