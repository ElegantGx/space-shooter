import math
import random
import sys
import pygame

pygame.init() # 初始化pygame

WIDTH, HEIGHT = 800, 600
BG_COLOR = (10, 10, 30)
FPS = 60
PLAYER_SIZE = (60, 60)
BULLET_SIZE = (5,30)
ENEMY_SIZE = (30, 30)
PLAYER_COLOR = (100, 200, 255)
BULLET_COLOR = (255, 0 , 0)
ENEMY_COLOR = (0, 255, 0)
PLAYER_SPEED = 400
BULLET_SPEED = 600
ENEMY_SPEED = 300
SPAWN_INTERVAL = 0.5

clock = pygame.time.Clock() # 创建一个Clock实例


# 定义核心类
class Player(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface(PLAYER_SIZE)
        self.image.fill(PLAYER_COLOR)

        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))

    def update(self, pressed_keys, delta_time):
        dx = 0
        dy = 0

        if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
            dy -= 1
        if pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
            dy += 1
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            dx -= 1
        if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            dx += 1

        self.rect.x += dx * PLAYER_SPEED * delta_time
        self.rect.y += dy * PLAYER_SPEED * delta_time

        self.rect.clamp_ip(screen.get_rect())

class Bullet(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, player_x, player_y):
        super().__init__()

        self.image = pygame.Surface(BULLET_SIZE)
        self.image.fill(BULLET_COLOR)

        self.rect = self.image.get_rect(center=(player_x, player_y))

    def update(self, delta_time):
        self.rect.y -= BULLET_SPEED * delta_time

        if self.rect.y < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, enemy_x, enemy_y):
        super().__init__()

        self.image = pygame.Surface(ENEMY_SIZE)
        self.image.fill(ENEMY_COLOR)

        self.rect = self.image.get_rect(center=(enemy_x, enemy_y))

    def update(self, player_x, player_y, delta_time):
        dx = player_x - self.rect.centerx
        dy = player_y - self.rect.centery
        dist = math.hypot(dx, dy)

        if dist > 0:
            self.rect.x += dx / dist * ENEMY_SPEED * delta_time
            self.rect.y += dy / dist * ENEMY_SPEED * delta_time


        if (self.rect.top > HEIGHT or self.rect.bottom < 0 or
                self.rect.left > WIDTH or self.rect.right < 0):
            self.kill()

# 初始化对象
players = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

player = Player()
players.add(player)
all_sprites.add(player)

pygame.display.set_caption("Space Shooter")

screen = pygame.display.set_mode((WIDTH, HEIGHT)) # 返回一个pygame.surface.Surface对象，副作用是创建窗口

spawn_timer = 0.0

running = True
while running:

    for event in pygame.event.get(): # 返回一个元素的类型是pygame.event.Event的list
        if event.type == pygame.QUIT: # pygame.event.Event对象都具有一个type属性，表示事件类型
            running = False

    dt = clock.tick(FPS) / 1000.0
    keys = pygame.key.get_pressed() # 返回一个类似布尔序列的对象(ScancodeWrapper)，用 pygame.K_* 索引

    # 生成敌人
    spawn_timer += dt
    if spawn_timer >= SPAWN_INTERVAL:
        spawn_timer = 0.0
        new_enemy = Enemy(random.randrange(0, WIDTH), 0)
        enemies.add(new_enemy)
        all_sprites.add(new_enemy)

    # 更新对象
    player.update(keys, dt)
    bullets.update(dt)
    enemies.update(player.rect.centerx, player.rect.centery, dt)

    if keys[pygame.K_SPACE]:
        new_bullet = Bullet(player.rect.centerx, player.rect.top - 15 )
        bullets.add(new_bullet)
        all_sprites.add(new_bullet)

    # 子弹消除敌人
    pygame.sprite.groupcollide(bullets, enemies, True, True)

    # 敌人消灭玩家
    if pygame.sprite.groupcollide(players, enemies, True,False):
        running = False

    screen.fill(BG_COLOR) # 背景色清屏
    all_sprites.draw(screen)
    pygame.display.flip() # 刷新屏幕

pygame.quit() # 显式去初始化pygame
sys.exit() # 显式退出
