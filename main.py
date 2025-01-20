import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 428
SCREEN_HEIGHT = 926

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load assets
BACKGROUND_IMAGE = pygame.image.load('assets/background.png')
BIRD_IMAGE = pygame.image.load('assets/bird.png')
PIPE_IMAGE = pygame.image.load('assets/pipe.png')

# Game settings
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_SPEED = 3
PIPE_GAP = 250  # Increased PIPE_GAP to make pipes taller
PIPE_FREQUENCY = 1500  # milliseconds

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Niggesh Bird")

# Clock to control frame rate
clock = pygame.time.Clock()

# Scoreboard file
SCOREBOARD_FILE = 'scoreboard.txt'

# Bird class
class Bird:
    def __init__(self):
        self.image = BIRD_IMAGE
        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.image_top = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.image_bottom = PIPE_IMAGE
        # Randomize the top pipe height within reasonable limits
        top_height = random.randint(200, SCREEN_HEIGHT - PIPE_GAP - 200)
        self.rect_top = self.image_top.get_rect(midbottom=(x, top_height))
        # Calculate the position for the bottom pipe so it touches the bottom of the screen
        bottom_height = SCREEN_HEIGHT - (top_height + PIPE_GAP)
        self.rect_bottom = self.image_bottom.get_rect(midtop=(x, top_height + PIPE_GAP))

    def update(self):
        self.rect_top.x -= PIPE_SPEED
        self.rect_bottom.x -= PIPE_SPEED

    def off_screen(self):
        return self.rect_top.right < 0

    def draw(self, surface):
        surface.blit(self.image_top, self.rect_top)
        surface.blit(self.image_bottom, self.rect_bottom)

# Function to load scores from file
def load_scores():
    if not os.path.exists(SCOREBOARD_FILE):
        return []
    with open(SCOREBOARD_FILE, 'r') as file:
        scores = [line.strip().split(',') for line in file]
        scores = [(name, int(score)) for name, score in scores]
        scores.sort(key=lambda x: x[1], reverse=True)
    return scores

# Function to save scores to file
def save_scores(scores):
    with open(SCOREBOARD_FILE, 'w') as file:
        for name, score in scores:
            file.write(f"{name},{score}\n")

# Function to display the start screen
def show_start_screen():
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("Niggesh Bird", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 4))
    bird_rect = BIRD_IMAGE.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(BIRD_IMAGE, bird_rect)
    font = pygame.font.Font(None, 36)
    text = font.render("Press SPACE to Start", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 1.5))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
    return True

# Function to display the game over screen
def show_game_over_screen(score):
    scores = load_scores()
    if len(scores) < 5 or score > scores[-1][1]:
        name = get_player_name()
        scores.append((name, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        if len(scores) > 5:
            scores = scores[:5]
        save_scores(scores)

    # Clear the screen and draw the background
    screen.blit(BACKGROUND_IMAGE, (0, 0))

    # Game Over Text
    font_large = pygame.font.Font(None, 74)
    game_over_text = font_large.render("Game Over", True, BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 9))

    # Display Player Score
    font_medium = pygame.font.Font(None, 60)
    score_text = font_medium.render(f"Your Score: {score}", True, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 4.5))

    # Scoreboard Table
    font_small = pygame.font.Font(None, 36)
    table_x = SCREEN_WIDTH // 2 - 150  # Center the table horizontally
    table_y = SCREEN_HEIGHT // 2.5     # Position the table vertically
    row_height = 40
    column_width = [100, 150,100]  # Width for Rank, Name, and Score columns

    # Draw Table Header
    header_bg_color = (50, 50, 50)  # Dark gray for header
    header_font_color = WHITE
    pygame.draw.rect(screen, header_bg_color, (table_x, table_y, sum(column_width), row_height))
    headers = ["Rank", "Name", "Score"]
    for i, header in enumerate(headers):
        header_text = font_small.render(header, True, header_font_color)
        screen.blit(header_text, (table_x + 10 + sum(column_width[:i]), table_y + 10))

    # Draw Table Rows
    row_bg_colors = [(200, 200, 200), (230, 230, 230)]  # Alternating row colors
    for idx, (name, scr) in enumerate(scores):
        row_color = row_bg_colors[idx % 2]  # Alternate row colors
        pygame.draw.rect(screen, row_color, (table_x, table_y + (idx + 1) * row_height, sum(column_width), row_height))

        # Rank
        rank_text = font_small.render(f"{idx + 1}.", True, BLACK)
        screen.blit(rank_text, (table_x + 10, table_y + (idx + 1) * row_height + 10))

        # Name
        name_text = font_small.render(name, True, BLACK)
        screen.blit(name_text, (table_x + column_width[0] + 10, table_y + (idx + 1) * row_height + 10))

        # Score
        score_text = font_small.render(str(scr), True, BLACK)
        screen.blit(score_text, (table_x + column_width[0] + column_width[1] + 10, table_y + (idx + 1) * row_height + 10))

    # Draw Table Borders
    border_color = BLACK
    pygame.draw.rect(screen, border_color, (table_x, table_y, sum(column_width), (len(scores) + 1) * row_height), 2)

    # Restart Instruction
    restart_text = font_small.render("Press SPACE to Restart", True, BLACK)
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT - 100))

    pygame.display.flip()

    # Wait for player input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
    return True









# Function to get player name
def get_player_name():
    name = ""
    font = pygame.font.Font(None, 48)
    input_font = pygame.font.Font(None, 36)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_active
    active = True
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 40)
    label_text = "Enter Your Name:"
    instruction_text = "Press ENTER to submit"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "Player"
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return name if name else "Player"
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 15:  # Limit the name length
                            name += event.unicode

        # Draw the background
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        # Draw the label
        label_surface = font.render(label_text, True, BLACK)
        screen.blit(label_surface, (SCREEN_WIDTH // 2 - label_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 60))

        # Draw the input box
        txt_surface = input_font.render(name, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        # Draw the instruction text
        instruction_surface = input_font.render(instruction_text, True, BLACK)
        screen.blit(instruction_surface, (SCREEN_WIDTH // 2 - instruction_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()
        clock.tick(30)

# Main game function
def main():
    if not show_start_screen():
        return

    while True:  # Outer loop to restart the game
        bird = Bird()
        pipes = []
        last_pipe_time = 0
        score = 0
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.flap()

            # Update bird
            bird.update()

            # Check collision with ground
            if bird.rect.bottom >= SCREEN_HEIGHT:
                running = False

            # Create new pipes
            current_time = pygame.time.get_ticks()
            if current_time - last_pipe_time > PIPE_FREQUENCY:
                last_pipe_time = current_time
                pipes.append(Pipe(SCREEN_WIDTH))

            # Update pipes
            for pipe in pipes:
                pipe.update()
                if pipe.off_screen():
                    pipes.remove(pipe)
                    score += 1

                # Check collision with pipes
                if pipe.rect_top.colliderect(bird.rect) or pipe.rect_bottom.colliderect(bird.rect):
                    running = False

            # Draw everything
            screen.blit(BACKGROUND_IMAGE, (0, 0))
            bird.draw(screen)
            for pipe in pipes:
                pipe.draw(screen)

            # Display score
            font = pygame.font.Font(None, 36)
            text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(text, (10, 10))

            pygame.display.flip()
            clock.tick(30)

        # Show game over screen
        if not show_game_over_screen(score):
            return

if __name__ == "__main__":
    main()