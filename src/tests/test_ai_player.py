"""
Test module for the AIPlayer class.
"""

import unittest
from src.ai_player import AIPlayer
from src.board import Board


class TestAIPlayer(unittest.TestCase):
    """
    Test the AIPlayer class and its methods in different scenarios.

    Args:
        unittest (_type_): _description_
    """

    def setUp(self):
        self.ai_player = AIPlayer(player_id=2)
        self.board = Board()

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

        for _ in range(self.board.row_count):
            self.board.drop_chip(column, 1)

        next_empty_row = self.board.get_next_empty_row(column)
        self.assertIsNone(
            next_empty_row, "Expected None for a full column, aka no empty rows are available.")

    def test_drop_chip_in_full_column(self):
        """
        Test that drop_chip does not add a chip to a full column.
        """
        column = 3

        for _ in range(self.board.row_count):
            self.board.drop_chip(column, 2)  # AI's chip

        # Attempt to drop another chip into the full column
        self.board.drop_chip(column, 2)

        # Verify the column is still full and no additional chip has been added
        is_column_full = all(
            self.board.board[row][column] == 2 for row in range(self.board.row_count))
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

        for _ in range(self.board.row_count):
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
                last_row, last_col = self.board.drop_chip(
                    i, -1)  # -1 is a placeholder for any chip

        self.assertEqual(self.ai_player.minimax(
            self.board, 0, float("-inf"), float("inf"), True, 42, last_row, last_col), (None, 0))

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

    def test_five_moves_away_from_a_win(self):
        """
        Test the AI's decision making when it is five moves away from a win.
        Example used:
        https://www.youtube.com/watch?v=WoaIMK5160w&list=PLu0rC09yug3YbL_eR6vCK7NAH4bj2VEfZ&index=5
        """

        # Set chips for red (human) player
        self.board.board[5][1] = self.board.board[5][3] = self.board.board[5][5] = 1
        self.board.board[5][6] = self.board.board[4][6] = self.board.board[2][4] = 1

        # Set chips for yellow (AI) player
        self.board.board[4][1] = self.board.board[4][3] = self.board.board[4][4] = 2
        self.board.board[4][5] = self.board.board[5][4] = self.board.board[3][4] = 2

        # We should get_best_move for AI in this case, and the move should be column 3
        best_move = self.ai_player.get_best_move(self.board, 10)
        self.assertEqual(best_move, 3, "AI should prefer column 3 in this case")
        # Update the board to reflect the AI's move
        self.board.drop_chip(3, 2)

        # Opponent's move to column 6
        self.board.board[3][6] = 1

        # AI makes a blocking move in column 6, preventing the opponent from winning
        best_move = self.ai_player.get_best_move(self.board, 12)
        self.assertEqual(best_move, 6, "AI should prefer column 6 in this case")
        # Update the board to reflect the AI's move
        self.board.drop_chip(6, 2)

        # Opponent's move to column 4
        self.board.board[1][4] = 1

        # AI has two ways towards win, column 1 or 5.
        best_move = self.ai_player.get_best_move(self.board, 14)
        self.assertEqual(best_move, 1, "AI should prefer column 1 in this case")
         # Update the board to reflect the AI's move
        self.board.drop_chip(1, 2)

        # Opponent's move to column 0
        self.board.board[5][0] = 1

        print(self.board.board)

        # AI should block by dropping to column 2
        best_move = self.ai_player.get_best_move(self.board, 16)
        self.assertEqual(best_move, 2, "AI should prefer column 2 in this case")
        # Update the board to reflect the AI's move
        self.board.drop_chip(2, 2)

        # Opponent's move to column 2
        self.board.board[4][2] = 1

        # AI should win by dropping to column 2
        best_move = self.ai_player.get_best_move(self.board, 18)
        self.assertEqual(best_move, 2, "AI should prefer column 2 in this case")
        # Check that it is an actual winning move
        self.assertTrue(self.board.is_winner(3, 2, 2), \
            "AI should win the game by dropping chip to column 2")
