import sys
import pygame

pygame.init() # 初始化pygame

WEIGHT, HEIGHT = 800, 600

screen = pygame.display.set_mode((WEIGHT, HEIGHT)) # 返回一个pygame.surface.Surface对象，副作用是创建窗口

running = True
while running:
    for event in pygame.event.get(): # 返回一个元素的类型是pygame.event.Event的list
        if event.type == pygame.QUIT: # pygame.event.Event对象都具有一个type属性，表示事件类型
            running =False



pygame.quit() # 显式去初始化pygame
sys.exit() # 显式退出