import pygame
import sys
from copy import deepcopy

pygame.init()

# ------------------- BASIC SETTINGS -------------------
BOARD_SIZE = 640
MARGIN = 60
WIDTH, HEIGHT = BOARD_SIZE + MARGIN, BOARD_SIZE + MARGIN
ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_SIZE // COLS

# Colors
WHITE = (245, 245, 220)
BROWN = (139, 69, 19)
GREEN = (50, 205, 50)
BLACK = (0, 0, 0)
BG_COLOR = (230, 230, 230)

# Window setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Chess Game (Minimax)")

# ------------------- LOAD IMAGES -------------------
IMAGES = {}
pieces = ["bK", "bQ", "bB", "bN", "bR", "bP",
          "wK", "wQ", "wB", "wN", "wR", "wP"]

for p in pieces:
    img = pygame.image.load(f"{p}.png").convert_alpha()
    IMAGES[p] = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))

# Piece names for messages
piece_names = {
    "bK": "Black King", "bQ": "Black Queen", "bB": "Black Bishop",
    "bN": "Black Knight", "bR": "Black Rook", "bP": "Black Pawn",
    "wK": "White King", "wQ": "White Queen", "wB": "White Bishop",
    "wN": "White Knight", "wR": "White Rook", "wP": "White Pawn"
}

# Piece values for AI
piece_value = {"K": 900, "Q": 90, "R": 50, "B": 30, "N": 30, "P": 10}


# ------------------- FUNCTIONS -------------------
def init_board():
    return [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP"] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        ["wP"] * 8,
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    ]


def draw_labels(win):
    font = pygame.font.SysFont("arial", 20, True)
    # A–H below
    for i in range(8):
        text = font.render(chr(65 + i), True, BLACK)
        x = MARGIN + i * SQUARE_SIZE + SQUARE_SIZE // 2 - text.get_width() // 2
        win.blit(text, (x, BOARD_SIZE + 10))
    # 1–8 on left
    for i in range(8):
        text = font.render(str(8 - i), True, BLACK)
        y = i * SQUARE_SIZE + SQUARE_SIZE // 2 - text.get_height() // 2
        win.blit(text, (20, y + 5))


def draw_board(win, board, selected=None, moves_list=[]):
    win.fill(BG_COLOR)
    for r in range(ROWS):
        for c in range(COLS):
            color = WHITE if (r + c) % 2 == 0 else BROWN
            pygame.draw.rect(win, color, (MARGIN + c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if selected == (r, c):
                pygame.draw.rect(win, GREEN, (MARGIN + c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)
            if board[r][c] != "":
                win.blit(IMAGES[board[r][c]], (MARGIN + c*SQUARE_SIZE, r*SQUARE_SIZE))
    # show move dots
    for move in moves_list:
        rr, cc = move
        center = (MARGIN + cc*SQUARE_SIZE + SQUARE_SIZE//2, rr*SQUARE_SIZE + SQUARE_SIZE//2)
        pygame.draw.circle(win, BLACK, center, 10)
    draw_labels(win)
    pygame.display.update()


def get_piece_moves(board, r, c):
    piece = board[r][c]
    moves = []
    if piece == "":
        return moves

    color = piece[0]
    p = piece[1]
    dirs = []

    if p == "P":
        step = -1 if color == "w" else 1
        start_row = 6 if color == "w" else 1
        if 0 <= r + step < 8 and board[r+step][c] == "":
            moves.append((r+step, c))
            if r == start_row and board[r+2*step][c] == "":
                moves.append((r+2*step, c))
        for dc in [-1, 1]:
            nr, nc = r + step, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc] != "" and board[nr][nc][0] != color:
                moves.append((nr, nc))

    if p == "R":
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    if p == "B":
        dirs = [(1,1), (-1,1), (1,-1), (-1,-1)]
    if p == "Q":
        dirs = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,1), (1,-1), (-1,-1)]
    if p == "K":
        dirs = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,1), (1,-1), (-1,-1)]
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < 8 and 0 <= nc < 8 and (board[nr][nc]=="" or board[nr][nc][0] != color):
                moves.append((nr, nc))
        return moves
    if p == "N":
        knight_moves = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
        for dr, dc in knight_moves:
            nr, nc = r+dr, c+dc
            if 0 <= nr < 8 and 0 <= nc < 8 and (board[nr][nc]=="" or board[nr][nc][0] != color):
                moves.append((nr, nc))
        return moves

    for dr, dc in dirs:
        nr, nc = r+dr, c+dc
        while 0 <= nr < 8 and 0 <= nc < 8:
            if board[nr][nc] == "":
                moves.append((nr, nc))
            elif board[nr][nc][0] != color:
                moves.append((nr, nc))
                break
            else:
                break
            nr += dr
            nc += dc
    return moves


def find_king(board, color):
    for r in range(8):
        for c in range(8):
            if board[r][c] == color + "K":
                return (r, c)
    return None


def is_king_in_check(board, color):
    king_pos = find_king(board, color)
    if not king_pos:
        return False
    enemy = "b" if color == "w" else "w"
    for r in range(8):
        for c in range(8):
            if board[r][c] != "" and board[r][c][0] == enemy:
                if king_pos in get_piece_moves(board, r, c):
                    return True
    return False


def evaluate_board(board):
    total = 0
    for row in board:
        for p in row:
            if p != "":
                v = piece_value[p[1]]
                total += v if p[0] == "b" else -v
    return total


def minimax(board, depth, is_max):
    if depth == 0:
        return evaluate_board(board), None
    best_move = None
    if is_max:
        max_eval = -float("inf")
        for r in range(8):
            for c in range(8):
                if board[r][c] != "" and board[r][c][0] == "b":
                    for move in get_piece_moves(board, r, c):
                        temp = deepcopy(board)
                        temp[move[0]][move[1]] = temp[r][c]
                        temp[r][c] = ""
                        score, _ = minimax(temp, depth-1, False)
                        if score > max_eval:
                            max_eval = score
                            best_move = ((r, c), move)
        return max_eval, best_move
    else:
        min_eval = float("inf")
        for r in range(8):
            for c in range(8):
                if board[r][c] != "" and board[r][c][0] == "w":
                    for move in get_piece_moves(board, r, c):
                        temp = deepcopy(board)
                        temp[move[0]][move[1]] = temp[r][c]
                        temp[r][c] = ""
                        score, _ = minimax(temp, depth-1, True)
                        if score < min_eval:
                            min_eval = score
                            best_move = ((r, c), move)
        return min_eval, best_move


def popup_message(text, yes_no=False):
    font = pygame.font.SysFont("arial", 26, True)
    box = pygame.Rect(WIDTH//6, HEIGHT//3, WIDTH*2//3, HEIGHT//3)
    pygame.draw.rect(screen, (255, 255, 255), box)
    pygame.draw.rect(screen, BLACK, box, 3)
    words = text.split(" ")
    line = ""
    lines = []
    for w in words:
        if font.size(line + w)[0] < box.width - 60:
            line += w + " "
        else:
            lines.append(line)
            line = w + " "
    lines.append(line)
    y = box.top + 30
    for line in lines:
        surf = font.render(line.strip(), True, BLACK)
        screen.blit(surf, (box.centerx - surf.get_width()//2, y))
        y += 35

    if yes_no:
        yes = font.render("YES", True, (0, 128, 0))
        no = font.render("NO", True, (200, 0, 0))
        screen.blit(yes, (box.centerx - 80, box.centery + 50))
        screen.blit(no, (box.centerx + 40, box.centery + 50))
    else:
        ok = font.render("OK", True, (0, 128, 0))
        screen.blit(ok, (box.centerx - 20, box.centery + 50))

    pygame.display.update()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if yes_no:
                    if box.centerx - 80 <= x <= box.centerx - 20 and box.centery + 50 <= y <= box.centery + 80:
                        return True
                    elif box.centerx + 40 <= x <= box.centerx + 100 and box.centery + 50 <= y <= box.centery + 80:
                        return False
                else:
                    return True


def checkmate_check(board):
    wk = find_king(board, "w")
    bk = find_king(board, "b")
    if not wk:
        return "White King", "Black"
    if not bk:
        return "Black King", "White"
    return None, None


# ------------------- MAIN FUNCTION -------------------
def main():
    board = init_board()
    clock = pygame.time.Clock()
    selected = None
    moves_list = []
    player_turn = True

    print("Game started — You (White) vs Computer (Black)")

    while True:
        draw_board(screen, board, selected, moves_list)
        clock.tick(60)

        killed, winner = checkmate_check(board)
        if killed:
            popup_message(f"CHECKMATE! {killed} captured. {winner} wins!")
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()

        # Computer move
        if not player_turn:
            _, move = minimax(board, 2, True)
            if move:
                (r1, c1), (r2, c2) = move
                captured = board[r2][c2]
                piece = board[r1][c1]
                board[r2][c2] = piece
                board[r1][c1] = ""
                print(f"AI Move: {piece} from {chr(97+c1)}{8-r1} to {chr(97+c2)}{8-r2}")
                if captured != "":
                    print(f"Computer’s {piece_names[piece]} killed your {piece_names[captured]}")
                if is_king_in_check(board, "w"):
                    warn = popup_message("CHECK! Your King is in danger! Change move?", yes_no=True)
                    if warn:
                        board[r1][c1] = piece
                        board[r2][c2] = captured
                        player_turn = True
                        continue
            player_turn = True
            continue

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                r, c = pos[1] // SQUARE_SIZE, (pos[0] - MARGIN) // SQUARE_SIZE
                if c < 0 or c >= 8:
                    continue
                if selected:
                    if (r, c) in moves_list:
                        captured = board[r][c]
                        piece = board[selected[0]][selected[1]]
                        board[r][c] = piece
                        board[selected[0]][selected[1]] = ""
                        print(f"Your Move: {piece} from {chr(97+selected[1])}{8-selected[0]} to {chr(97+c)}{8-r}")
                        if captured != "":
                            print(f"Your {piece_names[piece]} killed opponent’s {piece_names[captured]}")
                        if is_king_in_check(board, "w"):
                            warn = popup_message("CHECK! Your King is in danger! Change move?", yes_no=True)
                            if warn:
                                board[selected[0]][selected[1]] = piece
                                board[r][c] = captured
                                selected = None
                                moves_list = []
                                continue
                        player_turn = False
                    selected = None
                    moves_list = []
                elif board[r][c] != "" and board[r][c][0] == "w":
                    selected = (r, c)
                    moves_list = get_piece_moves(board, r, c)


if __name__ == "__main__":
    main()
