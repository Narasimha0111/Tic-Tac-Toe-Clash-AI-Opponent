import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
LINE_WIDTH = 15
CIRCLE_RADIUS = SQUARE_SIZE // 3 - 10
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
FONT_COLOR = (255, 255, 255)
FONT_SIZE = 60

# Fonts
font = pygame.font.SysFont(None, FONT_SIZE)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(BG_COLOR)

# Board
board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Draw board lines
def draw_lines():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Draw X and O
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS, CIRCLE_WIDTH)

# Check for win
def check_win(player):
    # Check rows
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True
    # Check columns
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

# Check for tie
def check_tie():
    return all(all(cell != ' ' for cell in row) for row in board)

# Minimax with alpha-beta pruning
def minimax(board, depth, alpha, beta, is_maximizing):
    if check_win('O'):
        return 1
    elif check_win('X'):
        return -1
    elif check_tie():
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    eval = minimax(board, depth + 1, alpha, beta, False)
                    board[row][col] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    eval = minimax(board, depth + 1, alpha, beta, True)
                    board[row][col] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# AI move
def ai_move():
    best_score = -math.inf
    best_move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == ' ':
                board[row][col] = 'O'
                score = minimax(board, 0, -math.inf, math.inf, False)
                board[row][col] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    board[best_move[0]][best_move[1]] = 'O'

# Display text message
def display_message(message):
    pygame.time.delay(1000)
    screen.fill(BG_COLOR)
    text = font.render(message, True, FONT_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(3000)

# Main game loop
def main():
    global board, current_player

    current_player = 'X'
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if board[clicked_row][clicked_col] == ' ':
                    board[clicked_row][clicked_col] = current_player

                    if check_win(current_player):
                        display_message(f'Player {current_player} wins!')
                        game_over = True
                    elif check_tie():
                        display_message('It\'s a tie!')
                        game_over = True
                    else:
                        current_player = 'O' if current_player == 'X' else 'X'

                        if not game_over and current_player == 'O':
                            ai_move()
                            if check_win('O'):
                                display_message('AI wins!')
                                game_over = True
                            elif check_tie():
                                display_message('It\'s a tie!')
                                game_over = True
                            current_player = 'X'

            if game_over:
                pygame.time.delay(3000)
                board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
                game_over = False
                screen.fill(BG_COLOR)
                draw_lines()

        draw_figures()
        pygame.display.update()

        # Draw board lines after figures to prevent overdraw issues
        draw_lines()

if __name__ == '__main__':
    main()

