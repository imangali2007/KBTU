import pygame
import sys
import random
import json
import os
import psycopg2
from pygame.locals import *

pygame.init()

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
DARK_RED = (139, 0, 0)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
GRAY = (100, 100, 100)

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 24)

SETTINGS_FILE = "settings.json"

def get_db():
    # Changed user to imangaliazamatov for Mac compatibility
    return psycopg2.connect("dbname=postgres user=imangaliazamatov password='' host=localhost")

def ensure_db_schema():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS snake_players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );
            CREATE TABLE IF NOT EXISTS snake_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES snake_players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            );
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        print("DB Ensure Error:", e)

ensure_db_schema()

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {"color": "GREEN", "grid": True}

def save_settings(s):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(s, f)

settings = load_settings()
COLORS = {"GREEN": GREEN, "BLUE": BLUE, "WHITE": WHITE}

class Snake:
    def __init__(self):
        self.body = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)
        self.grow = 0
        self.color = COLORS.get(settings["color"], GREEN)
        
    def update(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        if self.grow > 0:
            self.grow -= 1
        elif self.grow < 0:
            if len(self.body) > 2:
                self.body.pop()
                self.body.pop()
            self.grow = 0
        else:
            self.body.pop()
            
    def draw(self, surface):
        for segment in self.body:
            rect = pygame.Rect(segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, self.color, rect)

class Food:
    def __init__(self, snake_body, is_poison=False):
        self.position = (0,0)
        self.is_poison = is_poison
        self.timer = 50 if not is_poison else 100
        self.randomize_position(snake_body)
        
    def randomize_position(self, snake_body):
        while True:
            pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            if pos not in snake_body:
                self.position = pos
                break
        if not self.is_poison:
            self.weight = random.choice([1, 1, 3, 5])
            if self.weight == 1: self.color = RED
            elif self.weight == 3: self.color = BLUE
            else: self.color = GOLD
        else:
            self.color = DARK_RED
            self.weight = 0
                
    def update(self, snake_body):
        self.timer -= 1
        if self.timer <= 0:
            self.randomize_position(snake_body)
            self.timer = 50 if not self.is_poison else 100

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0]*CELL_SIZE, self.position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

class PowerUp:
    def __init__(self, snake_body):
        self.position = (0,0)
        self.type = random.choice(["speed", "slow", "shield"])
        self.color = CYAN if self.type == "speed" else PURPLE if self.type == "slow" else WHITE
        self.spawn_time = pygame.time.get_ticks()
        while True:
            pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            if pos not in snake_body:
                self.position = pos
                break
    def draw(self, surface):
        if pygame.time.get_ticks() - self.spawn_time < 8000:
            pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0]*CELL_SIZE, self.position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def play_game(username):
    snake = Snake()
    foods = [Food(snake.body), Food(snake.body, is_poison=True)]
    powerup = None
    walls = []
    
    score = 0
    level = 1
    base_fps = 8
    
    speed_mod = 0
    shield_active = False
    powerup_timer = 0
    
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT MAX(score) FROM snake_sessions s JOIN snake_players p ON p.id = s.player_id WHERE p.username=%s", (username,))
        res = cur.fetchone()
        personal_best = res[0] if res and res[0] else 0
        conn.close()
    except:
        personal_best = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP and snake.direction != (0, 1): snake.direction = (0, -1)
                elif event.key == K_DOWN and snake.direction != (0, -1): snake.direction = (0, 1)
                elif event.key == K_LEFT and snake.direction != (1, 0): snake.direction = (-1, 0)
                elif event.key == K_RIGHT and snake.direction != (-1, 0): snake.direction = (1, 0)
                    
        snake.update()
        
        curr_time = pygame.time.get_ticks()
        if powerup_timer and curr_time > powerup_timer:
            speed_mod = 0
            shield_active = False
            powerup_timer = 0

        head_x, head_y = snake.body[0]
        collision = False
        
        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
            collision = True
        elif snake.body[0] in snake.body[1:]:
            collision = True
        elif snake.body[0] in walls:
            collision = True
            
        if collision:
            if shield_active:
                shield_active = False
                powerup_timer = 0
                snake.body[0] = (head_x - snake.direction[0], head_y - snake.direction[1])
            else:
                save_score(username, score, level)
                return score

        for f in foods:
            if snake.body[0] == f.position:
                if f.is_poison:
                    snake.grow = -2
                else:
                    snake.grow = 1
                    score += 10 * f.weight
                f.randomize_position(snake.body + walls)
                
                if score >= level * 100:
                    level += 1
                    base_fps += 2
                    if level >= 3:
                        walls = generate_walls(snake.body)
                        
        if len(snake.body) <= 1:
            save_score(username, score, level)
            return score

        if random.random() < 0.01 and not powerup:
            powerup = PowerUp(snake.body + walls)
            
        if powerup:
            if curr_time - powerup.spawn_time > 8000:
                powerup = None
            elif snake.body[0] == powerup.position:
                if powerup.type == "speed": speed_mod = 5
                elif powerup.type == "slow": speed_mod = -3
                elif powerup.type == "shield": shield_active = True
                powerup_timer = curr_time + 5000
                powerup = None

        for f in foods: f.update(snake.body)
        
        DISPLAYSURF.fill(BLACK)
        if settings.get("grid", True):
            for x in range(0, WIDTH, CELL_SIZE): pygame.draw.line(DISPLAYSURF, (30,30,30), (x,0), (x,HEIGHT))
            for y in range(0, HEIGHT, CELL_SIZE): pygame.draw.line(DISPLAYSURF, (30,30,30), (0,y), (WIDTH,y))

        for w in walls:
            pygame.draw.rect(DISPLAYSURF, GRAY, pygame.Rect(w[0]*CELL_SIZE, w[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        snake.draw(DISPLAYSURF)
        for f in foods: f.draw(DISPLAYSURF)
        if powerup: powerup.draw(DISPLAYSURF)
        
        score_txt = font.render(f"Score: {score} | Best: {personal_best} | Level: {level}", True, WHITE)
        DISPLAYSURF.blit(score_txt, (10, 10))
        
        pygame.display.update()
        clock.tick(max(3, base_fps + speed_mod))

def generate_walls(snake_body):
    walls = []
    for _ in range(10):
        pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        hx, hy = snake_body[0]
        if abs(pos[0]-hx) > 3 and abs(pos[1]-hy) > 3 and pos not in snake_body:
            walls.append(pos)
    return walls

def save_score(username, score, level):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO snake_players(username) VALUES(%s) ON CONFLICT DO NOTHING", (username,))
        cur.execute("SELECT id FROM snake_players WHERE username=%s", (username,))
        pid_row = cur.fetchone()
        if pid_row:
            pid = pid_row[0]
            cur.execute("INSERT INTO snake_sessions(player_id, score, level_reached) VALUES(%s, %s, %s)", (pid, score, level))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Failed to save to DB:", e)

def show_leaderboard():
    while True:
        DISPLAYSURF.fill(BLACK)
        title = font.render("Top 10 Scores (DB)", True, WHITE)
        DISPLAYSURF.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT p.username, s.score, s.level_reached FROM snake_sessions s JOIN snake_players p ON p.id = s.player_id ORDER BY s.score DESC LIMIT 10")
            rows = cur.fetchall()
            for i, r in enumerate(rows):
                txt = font.render(f"{i+1}. {r[0]} - Score: {r[1]} - Lvl: {r[2]}", True, WHITE)
                DISPLAYSURF.blit(txt, (50, 100 + i*30))
            conn.close()
        except:
            txt = font.render("No DB connection", True, RED)
            DISPLAYSURF.blit(txt, (50, 100))

        back = font.render("Press ESC to return", True, RED)
        DISPLAYSURF.blit(back, (WIDTH//2 - back.get_width()//2, HEIGHT-50))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT: sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE: return

def show_settings():
    global settings
    while True:
        DISPLAYSURF.fill(BLACK)
        title = font.render("Settings", True, WHITE)
        DISPLAYSURF.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        c_txt = font.render(f"1. Color: {settings['color']}", True, WHITE)
        g_txt = font.render(f"2. Grid: {'ON' if settings['grid'] else 'OFF'}", True, WHITE)
        back = font.render("Press ESC to return", True, RED)
        
        DISPLAYSURF.blit(c_txt, (50, 150))
        DISPLAYSURF.blit(g_txt, (50, 200))
        DISPLAYSURF.blit(back, (WIDTH//2 - back.get_width()//2, HEIGHT-50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT: sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_1:
                    opts = list(COLORS.keys())
                    settings["color"] = opts[(opts.index(settings["color"]) + 1) % len(opts)]
                if event.key == K_2:
                    settings["grid"] = not settings["grid"]
                if event.key == K_ESCAPE:
                    save_settings(settings)
                    return

def main_menu():
    username = "Player"
    while True:
        DISPLAYSURF.fill(BLACK)
        title = font.render("Advanced Snake", True, WHITE)
        DISPLAYSURF.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        p = font.render("1. Play", True, WHITE)
        l = font.render("2. Leaderboard", True, WHITE)
        s = font.render("3. Settings", True, WHITE)
        q = font.render("4. Quit", True, WHITE)
        u_instr = font.render(f"User: {username} (Press U to change)", True, BLUE)
        
        for i, t in enumerate([p, l, s, q, u_instr]):
            DISPLAYSURF.blit(t, (WIDTH//2 - t.get_width()//2, 200 + i*40))
            
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT: sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_1: play_game(username)
                elif event.key == K_2: show_leaderboard()
                elif event.key == K_3: show_settings()
                elif event.key == K_4: sys.exit()
                elif event.key == K_u: 
                    print("Enter name in terminal:")
                    username = input("Username: ")

if __name__ == "__main__":
    main_menu()
