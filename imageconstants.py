import pygame
import constants as c
# 开始界面用
startSceneImg = pygame.image.load('./assets/scene/Home_Screen.png')
startSceneImg = pygame.transform.scale(startSceneImg, (
c.WinWidth * c.CellSize // c.CellRatio, c.WinHeight * c.CellSize // c.CellRatio))
startSceneRect = startSceneImg.get_rect()
arrowImg = pygame.image.load('./assets/utils/arrow.png')
arrowImg = pygame.transform.scale(arrowImg, (c.WinHeight * c.CellSize // c.CellRatio * 0.05,
                                             c.WinHeight * c.CellSize // c.CellRatio * 0.1))
arrowRect = arrowImg.get_rect()
if c.CellRatio == 1:
    arrowRect1 = arrowRect.move(c.WinWidth * c.CellSize * 0.325,
                               c.WinHeight * c.CellSize * 0.59)
    arrowRect2 = arrowRect.move(c.WinWidth * c.CellSize * 0.63,
                                c.WinHeight * c.CellSize * 0.59)
elif c.CellRatio == 2:
    arrowRect1 = arrowRect.move(c.WinWidth * c.CellSize * 0.5 * 0.325,
                               c.WinHeight * c.CellSize * 0.52 * 0.59)
    arrowRect2 = arrowRect.move(c.WinWidth * c.CellSize * 0.5 * 0.63,
                                c.WinHeight * c.CellSize * 0.52 * 0.59)