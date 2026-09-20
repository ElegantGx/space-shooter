import math
import random
import pygame

from states import State
from states import PlayState

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

# 定义核心类
class Player(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface(PLAYER_SIZE)
        self.image.fill(PLAYER_COLOR)

        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))

    def update(self, pressed_keys, delta_time, screen):
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

#定义核心对象类
class PlaySession:
    def __init__(self, screen):
        self.screen = screen

        # 初始化对象
        self.players = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        self.player = Player()
        self.players.add(self.player)
        self.all_sprites.add(self.player)

    def restart(self):
        self.__init__(self.screen)


def play_main(screen):

    play_session = PlaySession(screen)
    play_state = PlayState.PLAY_LOOP

    play_handlers = {
        PlayState.PLAY_LOOP: play_loop,
        PlayState.PLAY_PAUSE: play_pause,
        PlayState.PLAY_FINISH: play_finish,
        PlayState.PLAY_QUIT: play_quit,
    }

    while True:
        play_handle = play_handlers.get(play_state, None)

        if play_handle is None:
            return None

        if play_state is PlayState.PLAY_QUIT:
            return State.MENU

        play_state = play_handle(play_session)


def play_loop(play_session):
    clock = pygame.time.Clock()  # 创建一个Clock实例
    dt = 1 / FPS

    # 生成敌人
    spawn_timer = 0.0

    while True:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()  # 返回一个类似布尔序列的对象(ScancodeWrapper)，用 pygame.K_* 索引

        spawn_timer += dt
        if spawn_timer >= SPAWN_INTERVAL:
            spawn_timer = 0.0
            new_enemy = Enemy(random.randrange(0, WIDTH), 0)
            play_session.enemies.add(new_enemy)
            play_session.all_sprites.add(new_enemy)

        # 更新对象
        play_session.players.update(keys, dt, play_session.screen)
        play_session.bullets.update(dt)
        play_session.enemies.update(play_session.player.rect.centerx, play_session.player.rect.centery, dt)

        if keys[pygame.K_SPACE]:
            new_bullet = Bullet(play_session.player.rect.centerx, play_session.player.rect.top - 15)
            play_session.bullets.add(new_bullet)
            play_session.all_sprites.add(new_bullet)

        # 子弹消灭敌人
        pygame.sprite.groupcollide(play_session.bullets, play_session.enemies, True, True)

        # 敌人消灭玩家
        if pygame.sprite.groupcollide(play_session.players, play_session.enemies, True, False):
            return PlayState.PLAY_FINISH

        play_session.screen.fill(BG_COLOR)  # 背景色清屏
        play_session.all_sprites.draw(play_session.screen)
        pygame.display.flip()  # 刷新屏幕


def play_pause(play_session):
    return None

def play_finish(play_session):
    return None

# 根本不会运行play_quit的实际内容，但要保证参数统一
def play_quit(play_session):
    tmp = play_session
    return tmp