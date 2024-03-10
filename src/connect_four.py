"""
Connect Four Main Game Module
"""

# pylint: disable=no-member

import pygame
from board import Board
from player import Player
from ai_player import AIPlayer
from ui import draw_board, init_ui, draw_start_menu

# Initialize pygame and set up window size
pygame.init()

# Constants
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Create the window and initialize UI
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Connect Four")
game_font = init_ui()

# Create the board and players
board = Board()
player1 = Player(1)
player2 = AIPlayer(2)
current_player = player1

# Main game loop
running = True
ai_thinking = False
game_over = False  # Flag to indicate game over
game_over_message = ""
message_color = WHITE
current_column = 0
total_moves = 0


def reset_game():
    """
    Reset the game state to start a new game.
    """
    global board, player1, player2, current_player, game_over, game_over_message, message_color
    board = Board()  # Reset the game board
    player1 = Player(1)  # Reinitialize player 1
    player2 = AIPlayer(2)  # Reinitialize player 2
    current_player = player1  # Reset the starting player
    game_over = False  # Reset the game over flag
    game_over_message = ""  # Clear any game over message
    message_color = WHITE  # Reset the message color to default


def show_start_menu():
    """Show the start menu and wait for the user to select a control method.

    Returns:
        str: The control method selected by the user, either "mouse" or "keyboard".
    """
    control_method = None
    while control_method is None:
        draw_start_menu(window, game_font)
        for menu_event in pygame.event.get():
            if menu_event.type == pygame.QUIT:
                pygame.quit()
            elif menu_event.type == pygame.KEYDOWN:
                if menu_event.key == pygame.K_m:
                    control_method = "mouse"
                elif menu_event.key == pygame.K_k:
                    control_method = "keyboard"
    return control_method


# Start the game and show the start menu
control = show_start_menu()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and current_player == player1 and not game_over:
            column_clicked = event.pos[0] // 100
            if board.is_valid_location(column_clicked):
                last_row, last_col = board.drop_chip(
                    column_clicked, player1.get_id())
                draw_board(window, board, game_over_message if game_over else None,
                           message_color, game_font, current_column, current_player)
                total_moves += 1
                if board.is_winner(last_row, last_col, player1.get_id()):
                    game_over_message = "Player 1 (Red) wins!"
                    message_color = RED
                    game_over = True
                else:
                    current_player = player2
                    ai_thinking = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # Move selection left
                current_column = max(0, current_column - 1)
            elif event.key == pygame.K_RIGHT:  # Move selection right
                current_column = min(board.column_count -
                                     1, current_column + 1)
            elif event.key == pygame.K_SPACE and current_player == player1 and not game_over:
                if board.is_valid_location(current_column):
                    last_row, last_col = board.drop_chip(
                        current_column, player1.get_id())
                    draw_board(window, board, game_over_message if game_over else None,
                               message_color, game_font, current_column, current_player)
                    if board.is_winner(last_row, last_col, player1.get_id()):
                        game_over_message = "Player 1 (Red) wins!"
                        message_color = RED
                        game_over = True
                    else:
                        current_player = player2
                        ai_thinking = True
            elif event.key == pygame.K_r:  # Reset game
                total_moves = 0
                reset_game()
            elif event.key == pygame.K_m:  # Back to start menu
                total_moves = 0
                reset_game()
                control = show_start_menu()

    if current_player == player2 and ai_thinking and not game_over:
        best_move = player2.get_best_move(board, total_moves)
        total_moves += 1
        if best_move is not None:
            last_row, last_col = board.drop_chip(best_move, player2.get_id())
            if board.is_winner(last_row, last_col, player2.get_id()):
                game_over_message = "Player 2 (AI - Yellow) wins!"
                message_color = YELLOW
                game_over = True
            elif total_moves == 42:  # Check if the board is full and call it a draw
                game_over_message = "It's a draw!"
                message_color = WHITE
                game_over = True
            else:
                current_player = player1
                ai_thinking = False

    if control == "mouse":
        x, _ = pygame.mouse.get_pos()
        current_column = x // 100

    draw_board(window, board, game_over_message if game_over else None,
               message_color, game_font, current_column, current_player)

    if game_over:
        pygame.time.delay(3000)  # Show the game over message for 3 seconds
        total_moves = 0
        reset_game()  # Reset the game

pygame.quit()
