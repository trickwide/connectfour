"""
Test module for the Player class.
"""

import unittest
from src.player import Player


class TestPlayer(unittest.TestCase):
    """
    Test the Player class and its methods in different scenarios.

    Args:
        unittest (_type_): _description_
    """

    def setUp(self):
        self.player1 = Player(1)
        self.player2 = Player(2)

    def test_get_id(self):
        """Test if the correct player ID is returned."""
        self.assertEqual(self.player1.get_id(), 1,
                         "Should return 1 for player 1")
        self.assertEqual(self.player2.get_id(), 2,
                         "Should return 2 for player 2")

    def test_get_color(self):
        """Test if the correct RGB color code is returned for each player."""
        self.assertEqual(self.player1.get_color(), (255, 0, 0),
                         "Should return red for player 1")
        self.assertEqual(self.player2.get_color(), (255, 255, 0),
                         "Should return yellow for player 2")

    def test_get_name(self):
        """Test if the correct name is returned for each player."""
        self.assertEqual(self.player1.get_name(), "Player (Red)",
                         "Should return 'Player (Red)' for player 1")
        self.assertEqual(self.player2.get_name(), "AI (Yellow)",
                         "Should return 'AI (Yellow)' for player 2")
