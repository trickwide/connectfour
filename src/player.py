"""
Connect Four Player Module
"""

class Player:
    """
    Represents a player in the Connect Four game.
    """

    def __init__(self, player_id):
        """
        Initialize a player with the given id.

        Args:
            id (int): The id of the player (0 for red, 1 for yellow).
        """
        self._id = player_id

    def get_id(self):
        """
        Get the ID of the player.

        Returns:
            int: The ID of the player (0 for red, 1 for yellow).
        """
        return self._id

    def get_color(self):
        """
        Get the color associated with the player's ID.

        Returns:
            tuple: A tuple representing the RGB color code (0-255) for the player's chip.
        """
        if self._id == 0:
            return (255, 0, 0)
        return (255, 255, 0)

    def get_name(self):
        """
        Get the name of the player.

        Returns:
            str: The name of the player ("Player (Red)" for id 0, "AI (Yellow)" for id 1).
        """
        if self._id == 0:
            return "Player (Red)"
        return "AI (Yellow)"
