import pygame
from pygame import Color, Surface

SCREEN_WIDTH: int = 600
SCREEN_HEIGHT: int = 600
CAPTION: str = "Tic-Tac-Toe"

BLACK: Color = (0, 0, 0)
WHITE: Color = (255, 255, 255)
RED: Color = (255, 0, 0)
BLUE: Color = (0, 0, 255)
GRAY: Color = (100, 100, 100)

CELL_WIDTH: int = SCREEN_WIDTH // 3
CELL_HEIGHT: int = SCREEN_HEIGHT // 3

NEW_GAME_BUTTON_X = SCREEN_WIDTH // 2 - 100
NEW_GAME_BUTTON_Y = SCREEN_HEIGHT // 2 + 50
NEW_GAME_BUTTON_WIDTH: int = 200
NEW_GAME_BUTTON_HEIGHT: int = 50

X_TURN: int = 0
O_TURN: int = 1
X_WON: int = 2
O_WON: int = 3
TIE: int = 4
MENU: int = 5


def main():

    pygame.init()
    surface: Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(CAPTION)
    gameState: int = X_TURN

    board: list[list[str | None]] = [[None, None, None],
                                     [None, None, None],
                                     [None, None, None]]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                if(gameState != X_TURN and gameState != O_TURN):
                    # if click new game button
                    mouse_pos = pygame.mouse.get_pos()
                    if(mouse_pos[0] >= NEW_GAME_BUTTON_X and mouse_pos[1] > NEW_GAME_BUTTON_Y and mouse_pos[0] <= NEW_GAME_BUTTON_X + NEW_GAME_BUTTON_WIDTH and mouse_pos[1] <= NEW_GAME_BUTTON_Y + NEW_GAME_BUTTON_HEIGHT):
                        gameState = X_TURN
                        board = [[None, None, None],
                                 [None, None, None],
                                 [None, None, None]]
                    continue

                row, col = get_cell_clicked(pygame.mouse.get_pos())
                if(board[row][col] is not None):
                    continue

                if(gameState == X_TURN):
                    board[row][col] = "X"
                    gameState = O_TURN
                elif(gameState == O_TURN):
                    board[row][col] = "O"
                    gameState = X_TURN

                winner = check_winner(board)
                if(winner is not None):
                    if(winner == "X"):
                        gameState = X_WON
                    elif(winner == "O"):
                        gameState = O_WON
                    else:
                        gameState = TIE

        surface.fill(WHITE)
        draw_board(surface)
        draw_markers(surface, board)

        if(gameState == X_WON):
            display_text(surface, "X wins!", SCREEN_WIDTH //
                         2, SCREEN_HEIGHT // 2, RED)
            draw_new_game_button(surface, NEW_GAME_BUTTON_X, NEW_GAME_BUTTON_Y, RED)
        elif(gameState == O_WON):
            display_text(surface, "O wins!", SCREEN_WIDTH //
                         2, SCREEN_HEIGHT // 2, BLUE)
            draw_new_game_button(surface, NEW_GAME_BUTTON_X, NEW_GAME_BUTTON_Y, BLUE)
        elif(gameState == TIE):
            display_text(surface, "Draw!", SCREEN_WIDTH //
                         2, SCREEN_HEIGHT // 2, GRAY)
            draw_new_game_button(surface, NEW_GAME_BUTTON_X, NEW_GAME_BUTTON_Y, GRAY)

        pygame.display.update()


def draw_board(surface: Surface) -> None:
    # draw grid
    for i in range(3):
        # draw verical lines
        pygame.draw.line(surface, BLACK, (CELL_WIDTH * i, 0),
                         (CELL_WIDTH * i, SCREEN_HEIGHT))
        # draw horizontal lines
        pygame.draw.line(surface, BLACK, (0, CELL_HEIGHT * i),
                         (SCREEN_WIDTH, CELL_HEIGHT * i))


def draw_markers(surface: Surface, board: list[list[str | None]]) -> None:
    for i in range(3):
        for j in range(3):
            if(board[i][j] == "X"):
                draw_x(surface, i, j)
            elif(board[i][j] == "O"):
                draw_o(surface, i, j)


def draw_x(surface: Surface, row: int, col: int) -> None:
    x = CELL_WIDTH * col + CELL_WIDTH // 2
    y = CELL_HEIGHT * row + CELL_HEIGHT // 2
    sz_x = CELL_WIDTH // 2 - 10
    sz_y = CELL_HEIGHT // 2 - 10
    pygame.draw.line(surface, BLACK, (x - sz_x, y - sz_y),
                     (x + sz_x, y + sz_y))
    pygame.draw.line(surface, BLACK, (x + sz_x, y - sz_y),
                     (x - sz_x, y + sz_y))


def draw_o(surface: Surface, row: int , col: int) -> None:
    x = CELL_WIDTH * col + CELL_WIDTH // 2
    y = CELL_HEIGHT * row + CELL_HEIGHT // 2
    sz = CELL_WIDTH // 2 - 5
    pygame.draw.circle(surface, BLACK, (x, y), sz, 1)


def display_text(surface: Surface, text: str, x: int, y: int, color: Color) -> None:
    font = pygame.font.SysFont("Arial", 72)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

def draw_new_game_button(surface: Surface, x: int, y: int, color: Color) -> None:
    pygame.draw.rect(surface, color, (x, y, NEW_GAME_BUTTON_WIDTH, NEW_GAME_BUTTON_HEIGHT))
    font = pygame.font.SysFont("Arial", 36)
    text_surface = font.render("New Game", True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x + 100, y + 25)
    surface.blit(text_surface, text_rect)

def check_winner(board: list[list[str | None]]) -> str | None:
    for x in range(3):
        # check horizontal
        if(board[x][0] != None and board[x][0] == board[x][1] == board[x][2]):
            return board[x][0]
        # check vertical
        if(board[0][x] != None and board[0][x] == board[1][x] == board[2][x]):
            return board[0][x]

    # check diagonal
    if(board[0][0] != None and board[0][0] == board[1][1] == board[2][2]):
        return board[0][0]
    if(board[0][2] != None and board[0][2] == board[1][1] == board[2][0]):
        return board[0][2]

    # If all cells are filled but no winner, it's a tie
    if(None not in board[0] and None not in board[1] and None not in board[2]):
        return "T"
    return None


def get_cell_clicked(mouse_pos: tuple[int, int]) -> tuple[int, int]:
    row = mouse_pos[1] // CELL_WIDTH
    col = mouse_pos[0] // CELL_HEIGHT
    return row, col


if __name__ == "__main__":
    main()
