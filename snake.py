import pygame
from color_palette import *
import random
import psycopg2

conn = psycopg2.connect(
    dbname="labdb",
    user="postgres",
    password="AsEn2006p.",  # если другой — измени
    host="localhost",
    port="5432"
)
cur = conn.cursor()
def get_or_create_user(username):
    cur.execute("SELECT id FROM game_user WHERE username=%s", (username,))
    result = cur.fetchone()
    if result:
        user_id = result[0]
        cur.execute("SELECT MAX(level) FROM user_score WHERE user_id=%s", (user_id,))
        level = cur.fetchone()[0] or 1
    else:
        cur.execute("INSERT INTO game_user (username) VALUES (%s) RETURNING id", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()
        level = 1
    return user_id, level
def save_score(user_id, score, level):
    cur.execute("INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)", (user_id, score, level))
    conn.commit()
    print(" Score saved!")

# перед запуском игры:
username = input("Enter your username: ")
user_id, level = get_or_create_user(username)
print(f"Welcome back, {username}! You're on level {level}")

pygame.init()

WIDTH = 700
HEIGHT = 700
CELL = 25

screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0
        self.score = 0
        self.level = 1
        self.speed = 5

    def move(self):
        # Move the snake body
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

        # Check wall collision
        if self.body[0].x < 0 or self.body[0].x >= WIDTH // CELL or self.body[0].y < 0 or self.body[0].y >= HEIGHT // CELL:
            pygame.quit()
            quit()

        # Check self collision
        for segment in self.body[1:]:
            if self.body[0].x == segment.x and self.body[0].y == segment.y:
                pygame.quit()
                quit()

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food):
        if self.body[0].x == food.pos.x and self.body[0].y == food.pos.y:
            self.body.append(Point(self.body[-1].x, self.body[-1].y))
            self.score += 1
            if self.score % 3 == 0:  # Level up every 3 points
                self.level += 1
                self.speed += 2
            food.generate_random_pos(self)

class Food:
    def __init__(self):
        self.pos = Point(9, 9)

    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self, snake):
        while True:
            new_x = random.randint(0, WIDTH // CELL - 1)
            new_y = random.randint(0, HEIGHT // CELL - 1)
            if not any(segment.x == new_x and segment.y == new_y for segment in snake.body):
                self.pos = Point(new_x, new_y)
                break

FPS = 5
clock = pygame.time.Clock()
food = Food()
snake = Snake()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_score(user_id, snake.score, snake.level)
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx == 0:
                snake.dx, snake.dy = 1, 0
            elif event.key == pygame.K_LEFT and snake.dx == 0:
                snake.dx, snake.dy = -1, 0
            elif event.key == pygame.K_DOWN and snake.dy == 0:
                snake.dx, snake.dy = 0, 1
            elif event.key == pygame.K_UP and snake.dy == 0:
                snake.dx, snake.dy = 0, -1
            elif event.key == pygame.K_p:
                save_score(user_id, snake.score, snake.level)
                print("Paused and saved.")
                running = False


    screen.fill(colorBLACK)
    snake.move()
    snake.check_collision(food)
    snake.draw()
    food.draw()

    # Draw score and level
    font = pygame.font.SysFont(None, 35)
    score_text = font.render(f"Score: {snake.score}", True, colorWHITE)
    level_text = font.render(f"Level: {snake.level}", True, colorWHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.flip()
    clock.tick(snake.speed)
cur.close()
conn.close()
pygame.quit()
