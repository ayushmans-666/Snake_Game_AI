import pygame
import random
import sys

# -------------------- Setup --------------------
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
CELL = 20
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game with AI")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Clock to control FPS
clock = pygame.time.Clock()

# -------------------- Game variables --------------------
snake_body = [(100, 100), (80, 100), (60, 100)]
current_direction = "RIGHT"
score = 0

# Random initial food position
food_pos = (random.randrange(0, SCREEN_WIDTH, CELL),
            random.randrange(0, SCREEN_HEIGHT, CELL))

# AI mode: True = AI controls snake, False = manual arrow keys
AI_MODE = True

# -------------------- Helper functions --------------------
def draw_snake():
    for block in snake_body:
        pygame.draw.rect(screen, GREEN, (*block, CELL, CELL))

def draw_food():
    pygame.draw.rect(screen, RED, (*food_pos, CELL, CELL))

def move_snake():
    """Move snake: either AI moves toward food or manual controls"""
    global snake_body, current_direction

    head_x, head_y = snake_body[0]

    if AI_MODE:
        # Simple greedy AI: move horizontally first, then vertically
        if food_pos[0] > head_x:
            dx, dy = CELL, 0
        elif food_pos[0] < head_x:
            dx, dy = -CELL, 0
        elif food_pos[1] > head_y:
            dx, dy = 0, CELL
        else:
            dx, dy = 0, -CELL
    else:
        dx, dy = 0, 0
        if current_direction == "UP": dy = -CELL
        elif current_direction == "DOWN": dy = CELL
        elif current_direction == "LEFT": dx = -CELL
        elif current_direction == "RIGHT": dx = CELL

    new_head = (head_x + dx, head_y + dy)
    snake_body = [new_head] + snake_body[:-1]

def check_collision():
    """Check collisions: walls, self, or food"""
    global snake_body, score, food_pos

    head = snake_body[0]

    # Wall collision
    if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
        game_over()

    # Self collision
    if head in snake_body[1:]:
        game_over()

    # Food collision
    if head == food_pos:
        snake_body.append(snake_body[-1])  # Grow snake
        score += 10
        food_pos = (random.randrange(0, SCREEN_WIDTH, CELL),
                    random.randrange(0, SCREEN_HEIGHT, CELL))

def game_over():
    print(f"Game Over! Your final score: {score}")
    pygame.quit()
    sys.exit()

# -------------------- Main game loop --------------------
while True:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and not AI_MODE:
            if event.key == pygame.K_UP and current_direction != "DOWN":
                current_direction = "UP"
            elif event.key == pygame.K_DOWN and current_direction != "UP":
                current_direction = "DOWN"
            elif event.key == pygame.K_LEFT and current_direction != "RIGHT":
                current_direction = "LEFT"
            elif event.key == pygame.K_RIGHT and current_direction != "LEFT":
                current_direction = "RIGHT"

    move_snake()
    check_collision()
    draw_snake()
    draw_food()

    pygame.display.flip()
    clock.tick(10)  # Adjust speed here
