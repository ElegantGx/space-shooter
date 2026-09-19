import sys
import pygame

pygame.init() # 初始化pygame

WIDTH, HEIGHT = 800, 600
BG_COLOR = (10, 10, 30)
FPS = 60
PLAYER_SIZE = 60
PLAYER_COLOR = (100, 200, 255)
PLAYER_SPEED = 400

clock = pygame.time.Clock() # 创建一个Clock实例
player_rect = pygame.rect.Rect((WIDTH - PLAYER_SIZE) // 2, HEIGHT - 80, PLAYER_SIZE, PLAYER_SIZE)

pygame.display.set_caption("Space Shooter")

screen = pygame.display.set_mode((WIDTH, HEIGHT)) # 返回一个pygame.surface.Surface对象，副作用是创建窗口

running = True
while running:

    for event in pygame.event.get(): # 返回一个元素的类型是pygame.event.Event的list
        if event.type == pygame.QUIT: # pygame.event.Event对象都具有一个type属性，表示事件类型
            running =False

    keys = pygame.key.get_pressed() # 返回一个类似布尔序列的对象(ScancodeWrapper)，用 pygame.K_* 索引

    if keys[pygame.K_UP]:
        player_rect.y -= PLAYER_SPEED // FPS
    if keys[pygame.K_DOWN]:
        player_rect.y += PLAYER_SPEED // FPS
    if keys[pygame.K_LEFT]:
        player_rect.x -= PLAYER_SPEED // FPS
    if keys[pygame.K_RIGHT]:
        player_rect.x += PLAYER_SPEED // FPS

    screen.fill(BG_COLOR) # 背景色清屏
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
    pygame.display.flip() # 刷新屏幕

    clock.tick(FPS)


pygame.quit() # 显式去初始化pygame
sys.exit() # 显式退出