"""
Connect Four User Interface Module
"""

import pygame

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
FONT_SIZE = 30


def init_ui():
    """
    Initialize the game font for the UI.

    Returns:
        pygame.font.Font: The game font to use for rendering text in the game.
    """
    pygame.font.init()
    return pygame.font.SysFont("arial", FONT_SIZE)


def draw_text(window, text, color, x, y, game_font):
    """
    Draw the given text on the window at the specified position.

    Args:
        window (pygame.Surface): The window to draw the text on.
        text (str): The text to draw on the window.
        color (tuple): The color of the text.
        x (int): The x-coordinate of the text.
        y (int): The y-coordinate of the text.
        game_font (pygame.font.Font): The font to use for rendering the text.
    """
    text_surface = game_font.render(text, True, color)
    window.blit(text_surface, (x, y))


def draw_board(window, board, show_message=None, message_color=WHITE, game_font=None,
               current_column=None, current_player=None):
    """
    Draw the game board on the window.
    Args:
        window (pygame.Surface): The window to draw the game board on.
        board (Board): The game board to draw.
        show_message (str, optional): The message to display on the window. Defaults to None.
        message_color (tuple, optional): The color of the message text. Defaults to WHITE.
        game_font (pygame.font.Font, optional): The font to use for rendering the message. 
        Defaults to None.
    """
    GRID_SIZE = 100
    CHIP_RADIUS = GRID_SIZE // 2 - 5
    window.fill(BLACK)  # Clear the window first

    if current_column is not None and current_player is not None and show_message is None:
        pygame.draw.circle(window, RED if current_player.get_id() == 1 else YELLOW,
                           (current_column * 100 + 50, 50), 45)

    for row in range(board.row_count - 1, -1, -1):
        for col in range(board.column_count):
            pygame.draw.rect(window, BLUE, (col * GRID_SIZE,
                             (row + 1) * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.circle(window, BLACK, (col * GRID_SIZE + GRID_SIZE //
                               2, (row + 1) * GRID_SIZE + GRID_SIZE // 2), CHIP_RADIUS)
            if board.board[row][col] == 1:
                pygame.draw.circle(window, RED, (col * GRID_SIZE + GRID_SIZE //
                                   2, (row + 1) * GRID_SIZE + GRID_SIZE // 2), CHIP_RADIUS)
            elif board.board[row][col] == 2:
                pygame.draw.circle(window, YELLOW, (col * GRID_SIZE + GRID_SIZE //
                                   2, (row + 1) * GRID_SIZE + GRID_SIZE // 2), CHIP_RADIUS)

    if show_message:
        draw_text(window, show_message, message_color,
                  window.get_width() // 4, window.get_height() // 12, game_font)

    pygame.display.update()  # Update the display to show the changes


def draw_start_menu(window, game_font):
    """
    Draw the start menu on the window.

    Args:
        window (pygame.Surface): The window to draw the start menu on.
        game_font (pygame.font.Font): The font to use for rendering the start menu.
    """
    window.fill(BLACK)
    draw_text(window, "Connect Four", WHITE, window.get_width() //
              3, window.get_height() // 4, game_font)
    draw_text(window, "Press M for mouse control", WHITE,
              window.get_width() // 5, window.get_height() // 2, game_font)
    draw_text(window, "Press K for keyboard control", WHITE,
              window.get_width() // 5, window.get_height() * 3 // 4, game_font)
    pygame.display.update()
