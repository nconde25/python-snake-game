import pygame
import sys
import random

pygame.init()

SW, SH = 600, 600
SCORE_AREA_HEIGHT = 50  # Reserve 50 pixels at the top for the score
SPEED = 6
BLOCK_SIZE = 50
FONT = pygame.font.Font(None, BLOCK_SIZE)

screen = pygame.display.set_mode((SW, SH + SCORE_AREA_HEIGHT))
pygame.display.set_caption("Snake!")
clock = pygame.time.Clock()

class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE + SCORE_AREA_HEIGHT
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False

    def update(self):
        global apple, high_score

        # Check for self-collision or wall collision
        for square in self.body:
            if self.head.colliderect(square):
                self.dead = True
        if self.head.x not in range(0, SW) or self.head.y not in range(SCORE_AREA_HEIGHT, SH + SCORE_AREA_HEIGHT):
            self.dead = True

        if self.dead:
            # Update high score if current score is greater
            if len(self.body) > high_score:
                high_score = len(self.body)
						   
							   
            return

        # Move the snake
        new_head = self.head.copy()
        new_head.x += self.xdir * BLOCK_SIZE
        new_head.y += self.ydir * BLOCK_SIZE
        self.body.insert(0, self.head)
        self.head = new_head

        # Check for apple collision
        if self.head.colliderect(apple.rect):
            apple = Apple(self)
        else:
            self.body.pop()

    def draw(self):
        pygame.draw.rect(screen, "green", self.head)
        for segment in self.body:
            pygame.draw.rect(screen, "green", segment)

class Apple:
    def __init__(self, snake):
        self.place_apple(snake)
    
    def place_apple(self, snake):
        while True:
            self.x = int(random.randint(0, SW - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            self.y = int(random.randint(SCORE_AREA_HEIGHT, SH + SCORE_AREA_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            if not any(segment.colliderect(self.rect) for segment in [snake.head] + snake.body):
                break

    def draw(self):
        pygame.draw.rect(screen, "red", self.rect)

def drawGrid():
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(SCORE_AREA_HEIGHT, SH + SCORE_AREA_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, "#3c3c3B", rect, 1)

def reset_game():
    global snake, apple, game_started
    snake = Snake()
    apple = Apple(snake)
    game_started = False

snake = Snake()
apple = Apple(snake)
high_score = 0
game_started = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if not game_started:
                game_started = True  # Start the game on first key press
            if snake.dead:
                continue  # Ignore further key presses if snake is dead
            if event.key == pygame.K_DOWN and snake.ydir == 0:
                snake.ydir = 1
                snake.xdir = 0
            elif event.key == pygame.K_UP and snake.ydir == 0:
                snake.ydir = -1
                snake.xdir = 0
            elif event.key == pygame.K_RIGHT and snake.xdir == 0:
                snake.ydir = 0
                snake.xdir = 1
            elif event.key == pygame.K_LEFT and snake.xdir == 0:
                snake.ydir = 0
                snake.xdir = -1
        if event.type == pygame.MOUSEBUTTONDOWN and snake.dead:
            mouse_pos = event.pos
            yes_button = pygame.Rect(SW / 4 - 50, SH / 2 + 100, 100, 50)
            no_button = pygame.Rect(3 * SW / 4 - 50, SH / 2 + 100, 100, 50)
            if yes_button.collidepoint(mouse_pos):
                reset_game()
            elif no_button.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

    if game_started and not snake.dead:
        snake.update()

    screen.fill("black")
    drawGrid()

    apple.draw()
    snake.draw()

    # Draw the score on the left side
    score_text = FONT.render(f"Score: {len(snake.body)}", True, "white")
    screen.blit(score_text, (10, SCORE_AREA_HEIGHT / 4))

    # Draw the high score on the right side
    high_score_text = FONT.render(f"HI-Score: {high_score}", True, "white")
    high_score_rect = high_score_text.get_rect(topright=(SW - 10, SCORE_AREA_HEIGHT / 4))
    screen.blit(high_score_text, high_score_rect)

    if not game_started and not snake.dead:
        start_text = FONT.render("Press any key to start", True, "white")
        start_rect = start_text.get_rect(center=(SW / 2, SH / 2))
        screen.blit(start_text, start_rect)

    if snake.dead:
        game_over_text = FONT.render("Game Over", True, "red")
        game_over_rect = game_over_text.get_rect(center=(SW / 2, SH / 2 - 50))
        screen.blit(game_over_text, game_over_rect)

        score_text = FONT.render(f"Score: {len(snake.body)}", True, "white")
        score_rect = score_text.get_rect(center=(SW / 2, SH / 2))
        screen.blit(score_text, score_rect)

        retry_text = FONT.render("Retry?", True, "white")
        retry_rect = retry_text.get_rect(center=(SW / 2, SH / 2 + 50))
        screen.blit(retry_text, retry_rect)

        # Draw Yes and No buttons
        yes_button = pygame.Rect(SW / 4 - 50, SH / 2 + 100, 100, 50)
        no_button = pygame.Rect(3 * SW / 4 - 50, SH / 2 + 100, 100, 50)
        pygame.draw.rect(screen, "green", yes_button)
        pygame.draw.rect(screen, "red", no_button)

        yes_text = FONT.render("YES", True, "white")
        no_text = FONT.render("NO", True, "white")
        screen.blit(yes_text, yes_text.get_rect(center=yes_button.center))
        screen.blit(no_text, no_text.get_rect(center=no_button.center))

    pygame.display.update()
    clock.tick(SPEED)
