import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
REFRESH_RATE = 0.5

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
IMAGE1 = 'open_background.jpg'
img1 = pygame.image.load(IMAGE1)
screen.blit(img1, (0, 0))
pygame.display.flip()

IMAGE2 = 'background.jpg'
img2 = pygame.image.load(IMAGE2)
screen.blit(img2, (0, 0))

pygame.display.set_caption("Game")

clock = pygame.time.Clock()
clock.tick(REFRESH_RATE)
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

 
