import pygame
import random

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
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock to control frame rate
clock = pygame.time.Clock()

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

# Main game function
def main():
    bird = Bird()
    pipes = []
    last_pipe_time = 0
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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

    pygame.quit()

if __name__ == "__main__":
    main()