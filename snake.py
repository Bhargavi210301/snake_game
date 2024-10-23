import pygame
import time
import random
import math

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Clock to control snake speed
clock = pygame.time.Clock()

snake_size = 20         # 20x20 pixels
snake_speed = 10        # frames per second (FPS)
snake_body = []

# Font
font_style = pygame.font.SysFont(None, 30)

def draw_snake(snake_size, snake_body):
    for segment in snake_body:
        pygame.draw.circle(screen, GREEN, (segment[0], segment[1]), snake_size // 2)

def message(msg, color, position):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, position)

def is_near(x1, y1, x2, y2, distance):
    """Check if two points (x1, y1) and (x2, y2) are within a certain distance."""
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) < distance

def gameLoop():
    global snake_speed  # Reference the global snake_speed variable
    
    game_over = False       # ends the game loop entirely
    game_close = False      # snake dies but allows the player to restart.

    # Starting position of the snake
    x, y = WIDTH / 2, HEIGHT / 2
    x_change, y_change = 0, 0
    snake_body = []
    snake_length = 1

    food_x = round(random.randrange(0, WIDTH - snake_size) / 10.0) * 10.0
    food_y = round(random.randrange(0, HEIGHT - snake_size) / 10.0) * 10.0

    score = 0
    direction = None

    while not game_over:

        while game_close:
            screen.fill(WHITE)
            message(f"Game Over! Score: {score}", RED, [WIDTH / 6, HEIGHT / 3])
            message("Press C-Continue or Q-Quit", BLACK, [WIDTH / 6, HEIGHT / 2])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    x_change = -snake_size
                    y_change = 0
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    x_change = snake_size
                    y_change = 0
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and direction != "DOWN":
                    y_change = -snake_size
                    x_change = 0
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    y_change = snake_size
                    x_change = 0
                    direction = "DOWN"

        x += x_change
        y += y_change

        # Wrap the snake position when it hits the boundary
        if x >= WIDTH:
            x = 0
        elif x < 0:
            x = WIDTH - snake_size
        if y >= HEIGHT:
            y = 0
        elif y < 0:
            y = HEIGHT - snake_size

        screen.fill(BLACK)

        pygame.draw.circle(screen, RED, (food_x, food_y), snake_size // 2)

        snake_body.append([x, y])
        if len(snake_body) > snake_length:
            del snake_body[0]

        # Check if the snake has collided with itself
        for segment in snake_body[:-1]:
            if segment == [x, y]:
                game_close = True

        draw_snake(snake_size, snake_body)

        pygame.display.update()

        # Check if snake is close enough to the food
        if is_near(x, y, food_x, food_y, snake_size):
            # Snake eats food
            food_x = round(random.randrange(0, WIDTH - snake_size) / 10.0) * 10.0
            food_y = round(random.randrange(0, HEIGHT - snake_size) / 10.0) * 10.0
            snake_length += 1
            score += 1  

            if score % 10 == 0:
                snake_speed += 2  

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
