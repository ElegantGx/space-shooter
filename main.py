import sys
import pygame

pygame.init() # 初始化pygame

WIDTH, HEIGHT = 800, 600
BG_COLOR = (10, 10, 30)
FPS = 60
PLAYER_SIZE = 60
PLAYER_COLOR = (100, 200, 255)
BULLET_COLOR = (255, 0 , 0)
PLAYER_SPEED = 400
BULLET_SPEED = 600

clock = pygame.time.Clock() # 创建一个Clock实例

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(PLAYER_COLOR)

        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))

    def update(self, keys,dt):
        dx = 0
        dy = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1

        self.rect.x += dx * PLAYER_SPEED * dt
        self.rect.y += dy * PLAYER_SPEED * dt

        self.rect.clamp_ip(screen.get_rect())

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y):
        super().__init__()

        self.image = pygame.Surface((5,30))
        self.image.fill(BULLET_COLOR)

        self.rect = self.image.get_rect(center=(player_x, player_y))

    def update(self, dt):
        self.rect.y -= BULLET_SPEED * dt

        if self.rect.y > HEIGHT:
            self.kill()


player = Player()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(player)

pygame.display.set_caption("Space Shooter")

screen = pygame.display.set_mode((WIDTH, HEIGHT)) # 返回一个pygame.surface.Surface对象，副作用是创建窗口

running = True
while running:

    for event in pygame.event.get(): # 返回一个元素的类型是pygame.event.Event的list
        if event.type == pygame.QUIT: # pygame.event.Event对象都具有一个type属性，表示事件类型
            running = False

    dt = clock.tick(FPS) / 1000.0
    keys = pygame.key.get_pressed() # 返回一个类似布尔序列的对象(ScancodeWrapper)，用 pygame.K_* 索引

    player.update(keys, dt)
    bullets.update(dt)

    if keys[pygame.K_SPACE]:
        new_bullet = Bullet(player.rect.centerx, player.rect.top - 15 )
        bullets.add(new_bullet)
        all_sprites.add(new_bullet)

    screen.fill(BG_COLOR) # 背景色清屏
    all_sprites.draw(screen)
    pygame.display.flip() # 刷新屏幕


pygame.quit() # 显式去初始化pygame
sys.exit() # 显式退出