import pygame
import constants as c
# 开始界面用
def transformScale(img):
    return pygame.transform.scale(img, (
        c.WinWidth * c.CellSize // c.CellRatio, c.WinHeight * c.CellSize // c.CellRatio))
startSceneImg = pygame.image.load('./assets/scene/Home_Screen.png')
startSceneImg = transformScale(startSceneImg)
Ending1Img = pygame.image.load('./assets/scene/ending1.png')
Ending1Img =transformScale(Ending1Img)
Ending2Img = pygame.image.load('./assets/scene/ending2.png')
Ending2Img = transformScale(Ending2Img)
GameOverImg= pygame.image.load('./assets/scene/gameover.png')
GameOverImg= transformScale(GameOverImg)


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