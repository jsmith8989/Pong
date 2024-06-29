import os
import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize sound mixer

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

# Script directory for file loading
script_dir = os.path.dirname(__file__)
sound_file = os.path.join(script_dir, "collision_sound.wav")

# Load collision sound
collision_sound = pygame.mixer.Sound(sound_file)

# Paddle and ball parameters
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5

BALL_SIZE = 15
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
BALL_SPEED_INCREMENT = 0.5

# Initial positions
player1_pos = [50, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2]
player2_pos = [
    WINDOW_WIDTH - 50 - PADDLE_WIDTH,
    WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2,
]
ball_pos = [WINDOW_WIDTH // 2 - BALL_SIZE // 2, WINDOW_HEIGHT // 2 - BALL_SIZE // 2]

# Movement flags
player1_move_up = False
player1_move_down = False
player2_move_up = False
player2_move_down = False

ball_move_x = BALL_SPEED_X * random.choice([-1, 1])
ball_move_y = BALL_SPEED_Y * random.choice([-1, 1])

# Time variables
countdown_timer = pygame.time.get_ticks()  # Start time for countdown
countdown = 3  # Initial countdown value in seconds

speed_increase_timer = 0
speed_increase_interval = 10  # Increase speed every 10 seconds

# Scores
player1_score = 0
player2_score = 0

# Instruction display flag
show_instructions = True

# Game start flag
game_started = False

# Collision flags
player1_hit = False
player2_hit = False
prev_ball_move_x = ball_move_x

# Fonts
font = pygame.font.Font(None, 24)
font_big = pygame.font.Font(None, 36)


# Function to display countdown
def show_countdown(count):
    countdown_text = font_big.render(str(count), True, WHITE)
    text_rect = countdown_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    window.blit(countdown_text, text_rect)


# Function to display instructions
def draw_instructions():
    instructions_p1 = ["Use Z and S to move paddle 1"]
    instructions_p2 = ["Use arrow keys to move paddle 2"]

    if show_instructions:
        for idx, instruction in enumerate(instructions_p1):
            text = font.render(instruction, True, WHITE)
            text_rect = text.get_rect(
                left=10, top=WINDOW_HEIGHT - len(instructions_p1) * 20 + idx * 20
            )
            window.blit(text, text_rect)

        for idx, instruction in enumerate(instructions_p2):
            text = font.render(instruction, True, WHITE)
            text_rect = text.get_rect(
                right=WINDOW_WIDTH - 10,
                top=WINDOW_HEIGHT - len(instructions_p2) * 20 + idx * 20,
            )
            window.blit(text, text_rect)


# Function to display scores
def draw_scores():
    player1_score_text = font_big.render(str(player1_score), True, ORANGE)
    player2_score_text = font_big.render(str(player2_score), True, ORANGE)
    window.blit(
        player1_score_text,
        (WINDOW_WIDTH // 4 - player1_score_text.get_width() // 2, 20),
    )
    window.blit(
        player2_score_text,
        (3 * WINDOW_WIDTH // 4 - player2_score_text.get_width() // 2, 20),
    )


# Main game loop
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pong")

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                player1_move_up = True
            elif event.key == pygame.K_s:
                player1_move_down = True
            elif event.key == pygame.K_UP:
                player2_move_up = True
            elif event.key == pygame.K_DOWN:
                player2_move_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                player1_move_up = False
            elif event.key == pygame.K_s:
                player1_move_down = False
            elif event.key == pygame.K_UP:
                player2_move_up = False
            elif event.key == pygame.K_DOWN:
                player2_move_down = False

    if not game_started:
        current_time = pygame.time.get_ticks()
        if current_time - countdown_timer >= 1000:
            countdown -= 1
            countdown_timer = current_time

        if countdown == 0:
            game_started = True
            instruction_timer = pygame.time.get_ticks()
        else:
            window.fill(BLACK)
            draw_instructions()
            show_countdown(countdown)
            pygame.display.flip()
            clock.tick(60)
            continue

    current_time = pygame.time.get_ticks()
    if current_time - instruction_timer >= 10000:
        show_instructions = False

    if player1_move_up:
        player1_pos[1] -= PADDLE_SPEED
    if player1_move_down:
        player1_pos[1] += PADDLE_SPEED
    if player2_move_up:
        player2_pos[1] -= PADDLE_SPEED
    if player2_move_down:
        player2_pos[1] += PADDLE_SPEED

    if player1_pos[1] < 0:
        player1_pos[1] = 0
    elif player1_pos[1] > WINDOW_HEIGHT - PADDLE_HEIGHT:
        player1_pos[1] = WINDOW_HEIGHT - PADDLE_HEIGHT
    if player2_pos[1] < 0:
        player2_pos[1] = 0
    elif player2_pos[1] > WINDOW_HEIGHT - PADDLE_HEIGHT:
        player2_pos[1] = WINDOW_HEIGHT - PADDLE_HEIGHT

    ball_pos[0] += ball_move_x
    ball_pos[1] += ball_move_y

    if ball_pos[1] <= 0 or ball_pos[1] >= WINDOW_HEIGHT - BALL_SIZE:
        ball_move_y = -ball_move_y

    player1_hit = False
    player2_hit = False

    if ball_move_x < 0:
        if (
            not player1_hit
            and ball_pos[0] <= player1_pos[0] + PADDLE_WIDTH
            and player1_pos[1] <= ball_pos[1] + BALL_SIZE
            and ball_pos[1] <= player1_pos[1] + PADDLE_HEIGHT
        ):
            ball_move_x = -ball_move_x
            player1_hit = True
            player1_score += 1
            collision_sound.play()
    elif ball_move_x > 0:
        if (
            not player2_hit
            and ball_pos[0] >= player2_pos[0] - BALL_SIZE
            and player2_pos[1] <= ball_pos[1] + BALL_SIZE
            and ball_pos[1] <= player2_pos[1] + PADDLE_HEIGHT
        ):
            ball_move_x = -ball_move_x
            player2_hit = True
            player2_score += 1
            collision_sound.play()

    if ball_move_x < 0 and ball_move_x != prev_ball_move_x:
        player1_hit = False
    elif ball_move_x > 0 and ball_move_x != prev_ball_move_x:
        player2_hit = False

    prev_ball_move_x = ball_move_x

    speed_increase_timer += clock.get_rawtime() / 1000
    if speed_increase_timer >= speed_increase_interval:
        BALL_SPEED_X += BALL_SPEED_INCREMENT * (BALL_SPEED_X / abs(BALL_SPEED_X))
        BALL_SPEED_Y += BALL_SPEED_INCREMENT * (BALL_SPEED_Y / abs(BALL_SPEED_Y))
        speed_increase_timer = 0

    window.fill(BLACK)
    pygame.draw.rect(
        window, WHITE, [player1_pos[0], player1_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT]
    )
    pygame.draw.rect(
        window, WHITE, [player2_pos[0], player2_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT]
    )
    pygame.draw.ellipse(window, WHITE, [ball_pos[0], ball_pos[1], BALL_SIZE, BALL_SIZE])

    draw_scores()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
