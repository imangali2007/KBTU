import pygame
import sys
import random
import json
import os

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Racer")
clock = pygame.time.Clock()

font_large = pygame.font.SysFont("Verdana", 40)
font_small = pygame.font.SysFont("Verdana", 20)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

def load_json(name, default):
    if os.path.exists(name):
        with open(name, 'r') as f:
            return json.load(f)
    return default

def save_json(name, data):
    with open(name, 'w') as f:
        json.dump(data, f)

settings = load_json(SETTINGS_FILE, {"color": "BLUE", "difficulty": 1})
leaderboard = load_json(LEADERBOARD_FILE, [])

COLORS = {"BLUE": BLUE, "GREEN": GREEN, "PURPLE": PURPLE}

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 80))
        self.color = COLORS.get(settings["color"], BLUE)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT-100))
        self.shield_active = False
        self.nitro_active = False

    def move(self):
        keys = pygame.key.get_pressed()
        step = 7 if self.nitro_active else 5
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-step, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(step, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed_offset=0):
        super().__init__()
        self.image = pygame.Surface((40, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(40, WIDTH-40), -100))
        self.speed = 4 + speed_offset + settings["difficulty"]

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 20))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect(center=(random.randint(40, WIDTH-40), -50))

    def update(self):
        self.rect.move_ip(0, 4)
        if self.rect.top > HEIGHT:
            self.kill()

class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(["nitro", "shield", "repair"])
        self.image = pygame.Surface((30, 30))
        if self.type == "nitro": self.image.fill(CYAN)
        elif self.type == "shield": self.image.fill(YELLOW)
        else: self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(random.randint(30, WIDTH-30), -30))

    def update(self):
        self.rect.move_ip(0, 3)
        if self.rect.top > HEIGHT:
            self.kill()

def play_game(username):
    player = Player()
    enemies = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)
    
    score = 0
    distance = 0
    lives = 1
    
    SPAWN_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_ENEMY, max(500, 1500 - settings["difficulty"]*200))
    SPAWN_OBS = pygame.USEREVENT + 2
    pygame.time.set_timer(SPAWN_OBS, 2000)
    SPAWN_PWUP = pygame.USEREVENT + 3
    pygame.time.set_timer(SPAWN_PWUP, 5000)
    
    nitro_timer = 0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == SPAWN_ENEMY:
                e = Enemy(speed_offset=score//1000)
                enemies.add(e)
                all_sprites.add(e)
            if event.type == SPAWN_OBS:
                o = Obstacle()
                obstacles.add(o)
                all_sprites.add(o)
            if event.type == SPAWN_PWUP:
                p = Powerup()
                powerups.add(p)
                all_sprites.add(p)

        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (WIDTH//4, 0, 2, HEIGHT))
        pygame.draw.rect(screen, BLACK, (WIDTH//2, 0, 2, HEIGHT))
        pygame.draw.rect(screen, BLACK, (WIDTH*3//4, 0, 2, HEIGHT))

        player.move()
        enemies.update()
        obstacles.update()
        powerups.update()
        
        all_sprites.draw(screen)
        
        distance += (7 if player.nitro_active else 4)
        score = distance // 10
        
        if player.nitro_active and pygame.time.get_ticks() > nitro_timer:
            player.nitro_active = False

        collected = pygame.sprite.spritecollide(player, powerups, True)
        for c in collected:
            if c.type == "nitro":
                player.nitro_active = True
                nitro_timer = pygame.time.get_ticks() + 4000
                score += 50
            elif c.type == "shield":
                player.shield_active = True
            elif c.type == "repair":
                lives += 1

        hit_enemies = pygame.sprite.spritecollide(player, enemies, True)
        hit_obs = pygame.sprite.spritecollide(player, obstacles, True)
        
        if hit_enemies or hit_obs:
            if player.shield_active:
                player.shield_active = False
            else:
                lives -= 1
                if lives <= 0:
                    leaderboard.append({"name": username, "score": score, "distance": distance})
                    leaderboard.sort(key=lambda x: x["score"], reverse=True)
                    save_json(LEADERBOARD_FILE, leaderboard[:10])
                    return score

        info = font_small.render(f"Score: {score} | Lives: {lives}", True, BLACK)
        screen.blit(info, (10, 10))
        if player.shield_active:
            pygame.draw.circle(screen, YELLOW, player.rect.center, 50, 2)
            
        pygame.display.flip()
        clock.tick(60)

def main_menu():
    global settings
    username = "Player"
    while True:
        screen.fill(WHITE)
        title = font_large.render("Advanced Racer", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        p_txt = font_small.render("1. Play", True, BLACK)
        l_txt = font_small.render("2. Leaderboard", True, BLACK)
        s_txt = font_small.render("3. Settings", True, BLACK)
        q_txt = font_small.render("4. Quit", True, BLACK)
        u_txt = font_small.render(f"User: {username} (Press U to change)", True, BLUE)
        
        for i, txt in enumerate([p_txt, l_txt, s_txt, q_txt, u_txt]):
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 200 + i*40))
            
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    play_game(username)
                if event.key == pygame.K_2:
                    show_leaderboard()
                if event.key == pygame.K_3:
                    show_settings()
                if event.key == pygame.K_4:
                    sys.exit()
                if event.key == pygame.K_u:
                    # Simplified console input for username
                    print("Terminal entry for username for simplicity:")
                    username = input("Enter new username: ")

def show_leaderboard():
    while True:
        screen.fill(WHITE)
        title = font_large.render("Top 10 Scores", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        for i, entry in enumerate(leaderboard[:10]):
            txt = font_small.render(f"{i+1}. {entry['name']} - {entry['score']}", True, BLACK)
            screen.blit(txt, (50, 100 + i*30))
        
        back = font_small.render("Press ESC to return", True, RED)
        screen.blit(back, (WIDTH//2 - back.get_width()//2, 500))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return

def show_settings():
    global settings
    colors = list(COLORS.keys())
    c_idx = colors.index(settings["color"]) if settings["color"] in colors else 0
    while True:
        screen.fill(WHITE)
        title = font_large.render("Settings", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        c_txt = font_small.render(f"1. Car Color: {colors[c_idx]}", True, BLACK)
        d_txt = font_small.render(f"2. Difficulty: {settings['difficulty']}", True, BLACK)
        back = font_small.render("Press ESC to save and return", True, RED)
        
        screen.blit(c_txt, (50, 150))
        screen.blit(d_txt, (50, 200))
        screen.blit(back, (WIDTH//2 - back.get_width()//2, 500))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    c_idx = (c_idx + 1) % len(colors)
                    settings["color"] = colors[c_idx]
                if event.key == pygame.K_2:
                    settings["difficulty"] = (settings["difficulty"] + 1) % 5
                if event.key == pygame.K_ESCAPE:
                    save_json(SETTINGS_FILE, settings)
                    return

if __name__ == "__main__":
    main_menu()
