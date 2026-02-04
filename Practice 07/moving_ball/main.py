import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
ball_pos = [400, 300]
radius = 25

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and ball_pos[1] - 20 >= radius:
                ball_pos[1] -= 20
            if event.key == pygame.K_DOWN and ball_pos[1] + 20 <= 600 - radius:
                ball_pos[1] += 20
            if event.key == pygame.K_LEFT and ball_pos[0] - 20 >= radius:
                ball_pos[0] -= 20
            if event.key == pygame.K_RIGHT and ball_pos[0] + 20 <= 800 - radius:
                ball_pos[0] += 20

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), ball_pos, radius)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
