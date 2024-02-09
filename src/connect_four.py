"""
Connect Four Main Game Module
"""

# pylint: disable=no-member

import pygame
from board import Board
from player import Player
from ai_player import AIPlayer
from ui import draw_board, init_ui

# Initialize pygame and set up window size
pygame.init()

# Constants
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720
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


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and current_player == player1 and not game_over:
            column_clicked = event.pos[0] // 100
            if board.is_valid_location(column_clicked):
                board.drop_chip(column_clicked, player1.get_id())
                if board.is_winner(player1.get_id()):
                    game_over_message = "Player 1 (Red) wins!"
                    message_color = RED
                    game_over = True
                elif board.is_board_full():
                    game_over_message = "It's a draw!"
                    message_color = WHITE
                    game_over = True
                else:
                    current_player = player2
                    ai_thinking = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # If 'R' key is pressed
                reset_game()

    if current_player == player2 and ai_thinking and not game_over:
        best_move = player2.get_best_move(board)
        if best_move is not None:
            board.drop_chip(best_move, player2.get_id())
            if board.is_winner(player2.get_id()):
                game_over_message = "Player 2 (AI - Yellow) wins!"
                message_color = YELLOW
                game_over = True
            elif board.is_board_full():
                game_over_message = "It's a draw!"
                message_color = WHITE
                game_over = True
            else:
                current_player = player1
                ai_thinking = False

    draw_board(window, board, game_over_message if game_over else None,
               message_color, game_font)

    if game_over:
        pygame.time.delay(3000)  # Show the game over message for 3 seconds
        reset_game()  # Reset the game

pygame.quit()
