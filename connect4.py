import pygame
import sys

RED = (255, 50, 0)
YELLOW = (255, 255, 0)
GREY = (50, 50, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Draw Board Image
class Board(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((board_width, board_height))
        self.image.fill((0, 50, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 360
        self.rect.y = 120


# Draw grey empty cells
class EmptyCells(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((75, 75))
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.ellipse(self.image, GREY, [0, 0, 75, 75])
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, color):
        pygame.draw.ellipse(self.image, color, [0, 0, 75, 75])


# Function to display text
def draw_fonts(text, text_color, pos_x, pos_y, size=32):
    font = pygame.font.Font('futura_font.ttf', size)
    font_img = font.render(text, True, text_color)
    screen.blit(font_img, (pos_x, pos_y))


# Check for end game
def check_end_game():
    # Vertical Check
    for x in range(5, 2, -1):
        for y in range(7):
            if board[x][y] != '.':
                if board[x][y] == board[x - 1][y] == board[x - 2][y] == board[x - 3][y]:
                    print('Vertical')
                    return True

    # Horizontal Check
    for x in range(6):
        for y in range(6, 2, -1):
            if board[x][y] != '.':
                if board[x][y] == board[x][y - 1] == board[x][y - 2] == board[x][y - 3]:
                    print('Horizontal')
                    return True

    # Primary Diagonal Check
    for x in range(3):
        for y in range(4):
            if board[x][y] != '.':
                if board[x][y] == board[x + 1][y + 1] == board[x + 2][y + 2] == board[x + 3][y + 3]:
                    print('Primary Diagonal')
                    return True

    # Secondary Diagonal Check
    for x in range(5, 2, -1):
        for y in range(4):
            if board[x][y] != '.':
                if board[x][y] == board[x - 1][y + 1] == board[x - 2][y + 2] == board[x - 3][y + 3]:
                    print('Secondary Diagonal')
                    return True
    return False


pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Logo and Title
logo = pygame.image.load('logo.png')
pygame.display.set_icon(logo)
pygame.display.set_caption('Connect 4')

background = pygame.image.load('background.jpg')
background.set_alpha(150)
boardback = pygame.image.load('boardback.jpg')

board = [
    ['.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.'],
]

board_width, board_height = 560, 480
board_img = pygame.sprite.GroupSingle(Board())
empty_cells = pygame.sprite.Group()
# For empty grey circles
for i in range(40, board_width, 80):
    for j in range(40, board_height, 80):
        cell = EmptyCells((i + 322, j + 83))
        empty_cells.add(cell)

running = False
step, k, not_step = 0, 0, False
winner, end = None, None
while True:
    empty = False
    for row in board:
        for cell in row:
            if cell == '.':
                empty = True
                break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = True
            if pygame.K_KP1 <= event.key <= pygame.K_KP7 and running is True and end != 'qq':
                k = event.key - 1073741913
                if step % 2 == 0:
                    for r in range(5, -1, -1):
                        if board[r][k] == '.':
                            board[r][k] = 'R'
                            for e in empty_cells:
                                if (e.rect.x - 362)/80 == k and (e.rect.y - 123)/80 == r:
                                    e.update(RED)
                            step += 1
                            break
                    if step % 2 != 1:
                        not_step = True
                    else:
                        not_step = False
                        end = check_end_game()
                        if end:
                            winner = 'Red'
                            end = 'qq'
                else:
                    for r in range(5, -1, -1):
                        if board[r][k] == '.':
                            board[r][k] = 'Y'
                            for e in empty_cells:
                                if (e.rect.x - 362)/80 == k and (e.rect.y - 123)/80 == r:
                                    e.update(YELLOW)
                            step += 1
                            break
                    if step % 2 != 0:
                        not_step = True
                    else:
                        not_step = False
                        end = check_end_game()
                        if end:
                            winner = 'Yellow'
                            end = 'qq'
    screen.fill(BLACK)
    screen.blit(background, (0, 0))

    if not empty:
        screen.fill(BLACK)
        screen.blit(background, (0, 0))
        draw_fonts('Game Over! No Winner!', WHITE, 250, 320, 64)
        pygame.display.update()
        continue

    if running:
        screen.blit(boardback, (0, 0))
        board_img.draw(screen)
        empty_cells.draw(screen)
    if not running and end != 'qq':
        draw_fonts('press SPACE to start', (255, 255, 255), 320, 320, 64)
    elif end != 'qq':
        if step % 2 == 0:
            draw_fonts("Red's Turn", RED, 470, 20, 64)
        else:
            draw_fonts("Yellow's Turn", YELLOW, 420, 20, 64)
        if not_step:
            draw_fonts('Invalid Entry!', WHITE, 430, screen_height - 75, 64)
    if end == 'qq' and winner == 'Red':
        draw_fonts('Red Wins!', WHITE, 305, 300, 128)
    if end == 'qq' and winner == 'Yellow':
        draw_fonts('Yellow Wins!', WHITE, 200, 300, 128)
    pygame.display.update()
    clock.tick(60)
