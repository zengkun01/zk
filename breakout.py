import pygame

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout Clone")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Game speed settings
ball_speed = .15  # 球的初始速度
paddle_speed = .5  # 反弹板速度

# Paddle settings
paddle_width = 100
paddle_height = 15
paddle_x = (screen_width - paddle_width) // 2
paddle_y = screen_height - 50

# Ball settings
ball_radius = 10
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_x_speed = ball_speed
ball_y_speed = -ball_speed

# Brick settings
brick_width = 80
brick_height = 20
brick_rows = 5
brick_cols = 10
brick_spacing = 5
bricks = []

# Game states
game_active = False
game_over = False

# Fonts
font = pygame.font.Font(None, 50)

# Create bricks
def create_bricks():
    global bricks
    bricks = []
    for row in range(brick_rows):
        for col in range(brick_cols):
            brick_x = col * (brick_width + brick_spacing)
            brick_y = row * (brick_height + brick_spacing) + 50
            bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))

create_bricks()

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_active:
                    # Reset game state
                    ball_x = screen_width // 2
                    ball_y = screen_height // 2
                    ball_x_speed = ball_speed
                    ball_y_speed = -ball_speed
                    paddle_x = (screen_width - paddle_width) // 2
                    create_bricks()
                    game_active = True
                    game_over = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT]:
        paddle_x += paddle_speed
    paddle_x = max(0, paddle_x)
    paddle_x = min(screen_width - paddle_width, paddle_x)

    if game_active:
        # Ball movement
        ball_x += ball_x_speed
        ball_y += ball_y_speed

        # Ball collision with walls
        if ball_x - ball_radius <= 0 or ball_x + ball_radius >= screen_width:
            ball_x_speed = -ball_x_speed
        if ball_y - ball_radius <= 0:
            ball_y_speed = -ball_y_speed
        if ball_y - ball_radius >= screen_height:
            game_active = False
            game_over = True

        # Collision with paddle
        paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
        ball_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)
        if paddle_rect.colliderect(ball_rect):
            ball_y_speed = -ball_y_speed

        # Collision with bricks
        for brick in bricks:
            if brick.colliderect(ball_rect):
                bricks.remove(brick)
                ball_y_speed = -ball_y_speed
                break

    # Draw everything
    screen.fill(black)
    paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
    pygame.draw.rect(screen, white, paddle_rect)
    pygame.draw.circle(screen, white, (ball_x, ball_y), ball_radius)
    for brick in bricks:
        pygame.draw.rect(screen, red, brick)

    # Show start or game over screen
    if not game_active:
        if game_over:
            text = font.render("Game Over! Press SPACE to Restart", True, green)
        else:
            text = font.render("Press SPACE to Start", True, green)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
