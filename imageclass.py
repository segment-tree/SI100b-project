import pygame
from typing import *
import constants as c
class myImage:
    image:pygame.sprite.Sprite
    rect:Any
    def __init__(self,imgdir):
        self.image=pygame.image.load(imgdir)
        rect_t=self.image.get_rect()
        h=(rect_t.height*c.CellSize//rect_t.width)//c.CellRatio
        self.image=pygame.transform.scale(self.image,(c.CellSize//c.CellRatio,h))
        self.rect=self.image.get_rect()

    def reload(self,imgdir):
        self.__init__(imgdir)
    def draw(self,rx:int,ry:int,camera:Tuple[int,int],win):
        self.rect=self.image.get_rect()
        self.rect.move_ip(
            ( rx-c.CellSize//2 -camera[0] )//c.CellRatio,
            ( ry+c.CellSize//2-self.rect.height*c.CellRatio -camera[1] )//c.CellRatio
        )
        win.blit(self.image,self.rect)
    def drawG(self,gx:int,gy:int,camera:Tuple[int,int],win): # 按网格坐标渲染
        self.rect=self.image.get_rect()
        self.rect.move_ip(
            ( gx*c.CellSize -camera[0] )//c.CellRatio,
            ( (gy+1)*c.CellSize-self.rect.height*c.CellRatio -camera[1] )//c.CellRatio
        )
        win.blit(self.image,self.rect)

def displayCreateWin():
    if pygame.display.Info().current_w >= 2000:
        c.CellRatio=1
    win = pygame.display.set_mode((c.WinWidth*c.CellSize//c.CellRatio,c.WinHeight*c.CellSize//c.CellRatio))
    return win

#test
import sys
if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock() # 用于控制循环刷新频率的对象
    win = pygame.display.set_mode((c.WinWidth*c.CellSize,c.WinHeight*c.CellSize))
    while True:
        clock.tick(c.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        tree=myImage('./assets/t/54px-Pine_Stage_4.png')
        # tree.drawG(1,0,win)
        tree.draw(c.CellSize//2,c.CellSize+c.CellSize//2,(0,0),win)
        pygame.display.update()
        print(tree.rect)

