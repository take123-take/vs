import pygame
import sys

# 定数
WIDTH, HEIGHT = 600, 600
FPS = 60
CELL_SIZE = WIDTH // 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
GRAY = (169, 169, 169)

# Pygameの初期化
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Reversi (オセロ)')
clock = pygame.time.Clock()

# ボード初期化
board = [[None] * 8 for _ in range(8)]
board[3][3] = board[4][4] = 'W'
board[3][4] = board[4][3] = 'B'

# プレイヤーのターン
current_turn = 'B'
message = ""

# 方向ベクトル（8方向）
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

def draw_board():
    screen.fill(GREEN)
    
    # グリッドと石の描画
    for row in range(8):
        for col in range(8):
            pygame.draw.rect(screen, WHITE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            if board[row][col] == 'B':
                pygame.draw.circle(screen, BLACK, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
            elif board[row][col] == 'W':
                pygame.draw.circle(screen, WHITE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)

    # メッセージ表示
    if message:
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, WHITE)
        screen.blit(text, (WIDTH // 4, HEIGHT - 40))
    
    pygame.display.update()

def valid_move(row, col, color):
    if board[row][col] is not None:
        return False

    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        found_opposite = False
        while 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == (color == 'B' and 'W' or 'B'):
                found_opposite = True
            elif board[r][c] == color:
                if found_opposite:
                    return True
                else:
                    break
            else:
                break
            r += dr
            c += dc
    return False

def flip_stones(row, col, color):
    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        stones_to_flip = []
        while 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == (color == 'B' and 'W' or 'B'):
                stones_to_flip.append((r, c))
            elif board[r][c] == color:
                for fr, fc in stones_to_flip:
                    board[fr][fc] = color
                break
            else:
                break
            r += dr
            c += dc

def make_move(row, col, color):
    board[row][col] = color
    flip_stones(row, col, color)

def count_pieces():
    black_count = sum(row.count('B') for row in board)
    white_count = sum(row.count('W') for row in board)
    return black_count, white_count

def has_valid_move(color):
    """ 指定した色のプレイヤーが有効な手を持っているか判定 """
    for row in range(8):
        for col in range(8):
            if valid_move(row, col, color):
                return True
    return False

def game_over():
    """ 両方のプレイヤーが動けない場合にゲーム終了 """
    return not has_valid_move('B') and not has_valid_move('W')

def switch_turn():
    """ ターンを変更し、次のプレイヤーに有効な手がなければスキップ """
    global current_turn, message
    current_turn = 'W' if current_turn == 'B' else 'B'

    if not has_valid_move(current_turn):  # 次のプレイヤーが動けない場合
        message = f"{current_turn} has no valid moves. Skipping turn."
        print(message)  # ターミナルにも表示
        draw_board()
        pygame.time.wait(1500)  # 1.5秒待つ
        current_turn = 'W' if current_turn == 'B' else 'B'
        message = ""

        # 両者ともに動けない場合、ゲーム終了
        if not has_valid_move(current_turn):
            display_winner()
            pygame.time.wait(3000)  # 3秒後に終了
            pygame.quit()
            sys.exit()

def display_winner():
    black_count, white_count = count_pieces()
    font = pygame.font.Font(None, 74)
    if black_count > white_count:
        winner_text = font.render('Black Wins!', True, BLACK)
    elif white_count > black_count:
        winner_text = font.render('White Wins!', True, WHITE)
    else:
        winner_text = font.render('Draw!', True, GRAY)
    
    screen.fill(GREEN)
    draw_board()
    screen.blit(winner_text, (WIDTH // 4, HEIGHT // 3))
    pygame.display.update()

def main():
    global current_turn
    while True:
        screen.fill(GREEN)
        draw_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                col = event.pos[0] // CELL_SIZE
                row = event.pos[1] // CELL_SIZE
                
                if valid_move(row, col, current_turn):
                    make_move(row, col, current_turn)
                    
                    if game_over():
                        display_winner()
                        pygame.time.wait(3000)
                        pygame.quit()
                        sys.exit()
                    
                    switch_turn()

        clock.tick(FPS)

if __name__ == "__main__":
    main()
