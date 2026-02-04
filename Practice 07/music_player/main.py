import pygame
import os

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((400, 300))
font = pygame.font.SysFont("Arial", 24)

music_dir = "music"
tracks = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))]
current_track = 0

def play_music():
    if tracks:
        pygame.mixer.music.load(os.path.join(music_dir, tracks[current_track]))
        pygame.mixer.music.play()

running = True
while running:
    screen.fill((30, 30, 30))
    text = f"Track: {tracks[current_track] if tracks else 'No tracks found'}"
    label = font.render(text, True, (255, 255, 255))
    screen.blit(label, (50, 100))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pygame.mixer.music.play() if not pygame.mixer.music.get_busy() else pygame.mixer.music.unpause()
            if event.key == pygame.K_s:
                pygame.mixer.music.pause()
            if event.key == pygame.K_n:
                current_track = (current_track + 1) % len(tracks) if tracks else 0
                play_music()
            if event.key == pygame.K_b:
                current_track = (current_track - 1) % len(tracks) if tracks else 0
                play_music()
            if event.key == pygame.K_q:
                running = False

    pygame.display.flip()

pygame.quit()
