import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

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
PIPE_GAP = 300
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
        self.rect_top = self.image_top.get_rect(midbottom=(x, random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100) - PIPE_GAP // 2))
        self.rect_bottom = self.image_bottom.get_rect(midtop=(x, self.rect_top.bottom + PIPE_GAP))

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

    screen.blit(BACKGROUND_IMAGE, (0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 3))
    bird_rect = BIRD_IMAGE.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(BIRD_IMAGE, bird_rect)
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 1.5))
    font = pygame.font.Font(None, 36)
    text = font.render("Press SPACE to Restart", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 1.2))

    # Display scoreboard
    font = pygame.font.Font(None, 36)
    y_offset = SCREEN_HEIGHT // 1.5 + 50
    for i, (name, scr) in enumerate(scores):
        text = font.render(f"{i+1}. {name}: {scr}", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 30

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

# Function to get player name
def get_player_name():
    name = ""
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = True
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
                        name += event.unicode

        screen.blit(BACKGROUND_IMAGE, (0, 0))
        txt_surface = font.render(name, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
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