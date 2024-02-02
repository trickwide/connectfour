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
    def setUp(self):
        self.ai_player = AIPlayer(player_id=2)
        self.board = MockBoard()

    def test_immediate_threat_blocking(self):
        """
        Test if the AI correctly identifies and blocks an immediate threat.
        """
        # Setup a scenario where the opponent is one move away from winning
        for _ in range(3):
            self.board.drop_chip(3, 1)  # Opponent's chip
        self.ai_player.find_immediate_threat(self.board)
        self.assertEqual(self.ai_player.get_best_move(
            self.board), 3, "AI should block at column 3")
