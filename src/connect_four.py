import pygame
from board import Board
from player import Player
from ai_player import AIPlayer

WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720
GRID_SIZE = 100
CHIP_RADIUS = GRID_SIZE // 2 - 5

# Colors for the game
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Initialize pygame
pygame.init()

# Create the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Connect Four")

# Create the board
board = Board()

# Create the players
player1 = Player(1)
player2 = AIPlayer(2)

# Set current player (player1 starts)
current_player = player1


def draw_board():
    for row in range(board.row_count - 1, -1, -1):  # Start from the last row and move up
        for col in range(board.column_count):
            pygame.draw.rect(
                window,
                BLUE,
                (col * GRID_SIZE, (row + 1) * GRID_SIZE, GRID_SIZE, GRID_SIZE),
            )
            pygame.draw.circle(
                window,
                BLACK,
                (
                    col * GRID_SIZE + GRID_SIZE // 2,
                    (row + 1) * GRID_SIZE + GRID_SIZE // 2,
                ),
                CHIP_RADIUS,
            )
            if board.board[row][col] == 1:
                pygame.draw.circle(
                    window,
                    RED,
                    (
                        col * GRID_SIZE + GRID_SIZE // 2,
                        (row + 1) * GRID_SIZE + GRID_SIZE // 2,
                    ),
                    CHIP_RADIUS,
                )
            elif board.board[row][col] == 2:
                pygame.draw.circle(
                    window,
                    YELLOW,
                    (
                        col * GRID_SIZE + GRID_SIZE // 2,
                        (row + 1) * GRID_SIZE + GRID_SIZE // 2,
                    ),
                    CHIP_RADIUS,
                )


# Main game loop
running = True
ai_thinking = False  # Flag to indicate if the AI is thinking

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_player == player1:
                # Human player's turn
                column_clicked = event.pos[0] // GRID_SIZE
                if board.is_valid_location(column_clicked):
                    board.drop_chip(column_clicked, player1.get_id())
                    if board.is_winner(player1.get_id()):
                        print("Player 1 (Red) wins!")
                    elif board.is_board_full():
                        print("It's a draw!")
                    else:
                        current_player = player2
                        ai_thinking = True
        elif current_player == player2 and ai_thinking:
            # AI player's turn
            best_move = player2.get_best_move(board)
            if best_move is not None:
                board.drop_chip(best_move, player2.get_id())
                if board.is_winner(player2.get_id()):
                    print("Player 2 (AI - Yellow) wins!")
                elif board.is_board_full():
                    print("It's a draw!")
                else:
                    print("AI has made its move.")
                    current_player = player1
                    ai_thinking = False

    # Clear the window
    window.fill(BLACK)
    # Draw the game board
    draw_board()
    # Update the display
    pygame.display.update()

# Game loop ends
pygame.quit()
