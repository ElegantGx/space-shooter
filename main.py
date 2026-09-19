import sys
import pygame

pygame.init() # 初始化pygame

WEIGHT, HEIGHT = 800, 600
BG_COLOR = (10, 10, 30)
FPS = 60

clock = pygame.time.Clock() # 创建一个Clock实例

pygame.display.set_caption("Space Shooter")

screen = pygame.display.set_mode((WEIGHT, HEIGHT)) # 返回一个pygame.surface.Surface对象，副作用是创建窗口

running = True
while running:

    for event in pygame.event.get(): # 返回一个元素的类型是pygame.event.Event的list
        if event.type == pygame.QUIT: # pygame.event.Event对象都具有一个type属性，表示事件类型
            running =False

    screen.fill(BG_COLOR) # 背景色清屏
    pygame.display.flip() # 刷新屏幕

    clock.tick(FPS)


pygame.quit() # 显式去初始化pygame
sys.exit() # 显式退出