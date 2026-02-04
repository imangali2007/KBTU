import pygame
import datetime

pygame.init()
screen = pygame.display.set_mode((829, 836))
clock = pygame.time.Clock()

bg = pygame.image.load("../images/mickeyclock.jpeg")
# Fallback if hands are missing
try:
    hand_min = pygame.image.load("images/right-hand.png")
    hand_sec = pygame.image.load("images/left-hand.png")
except:
    hand_min = pygame.Surface((300, 20), pygame.SRCALPHA)
    pygame.draw.rect(hand_min, (0, 0, 0), (150, 0, 150, 10))
    hand_sec = pygame.Surface((400, 10), pygame.SRCALPHA)
    pygame.draw.rect(hand_sec, (255, 0, 0), (200, 4, 200, 2))

def rotate(surface, angle):
    rotated_surface = pygame.transform.rotozoom(surface, angle, 1)
    rotated_rect = rotated_surface.get_rect(center=(415, 418))
    return rotated_surface, rotated_rect

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.datetime.now()
    min_angle = -(now.minute * 6) - (now.second * 0.1) - 90
    sec_angle = -(now.second * 6) - 90

    screen.blit(bg, (0, 0))
    
    surf_min, rect_min = rotate(hand_min, min_angle)
    surf_sec, rect_sec = rotate(hand_sec, sec_angle)
    
    screen.blit(surf_min, rect_min)
    screen.blit(surf_sec, rect_sec)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
