import sys
import pygame

import menu
import play
from states import State

WIDTH, HEIGHT = 800, 600

def main():
    pygame.init()  # 初始化pygame

    pygame.display.set_caption("Space Shooter")

    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 返回一个pygame.surface.Surface对象，副作用是创建窗口

    state = State.MENU

    handlers = {
        State.MENU: menu.menu_main,
        State.PLAY: play.play_main,
    }

    while state != State.QUIT:
        handler = handlers.get(state, None)

        if handler is None:
            # 应该绘制错误窗口
            break

        state = handler(screen)

    pygame.quit()  # 显式去初始化pygame
    sys.exit()  # 显式退出

if __name__ == "__main__":
    main()
