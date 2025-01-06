from inter import *
import inter as i
import pygame  
import sys
from makescene import *
# from turtledemo.paint import switchupdown
# import heartrate
# heartrate.trace(browser=True,files=heartrate.files.all)
if __name__ == "__main__":
    pygame.init()
    win=displayCreateWin()
    #print('#',me.rx,me.ry) # gy 28 17

    pygame.display.set_caption("demo")#窗口名字和图标
    img = pygame.image.load('./assets/utils/icon1.ico')
    pygame.display.set_icon(img)
    
    i.thisMap=Mapper(50,50,style=0)
    mapGener(i.thisMap) # 田野
    i.maps.append(i.thisMap)
    i.thisMap=Mapper(50,50,style=1)
    nw=i.thisMap
    mapGenerTown(i.thisMap) # 城镇
    i.maps.append(i.thisMap)
    i.thisMap=Mapper(50,50,style=2)
    #thisMap.me=me
    mapGenerShop(i.thisMap) # 商店
    #thisMap.me=None
    i.maps.append(i.thisMap)
    i.thisMap=nw
    ###
    # thisMap=Mapper(50,50,style=0)
    # tempMapGener(thisMap)
    ###

    me=player(id=0,gx=26,gy=26,imagesdir='./assets/player/',layer=3)

    back_ground_color=(200, 200, 200)
    clock = pygame.time.Clock() # 用于控制循环刷新频率的对象
    fpscnt=0
    i.thisMap.me=me

    #for i in i.thisMap.mp[me.gx][me.gy]["entity"]:
    #    print(i)

    start = True
    win.fill((255,255,255))
    button = 0
    while start:
        win.convert()
        clock.tick(c.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if button > 0:
                        button -= 1
                elif event.key == pygame.K_DOWN:
                    if button < 3:
                        button += 1
                if event.key == pygame.K_RETURN:
                    if button == 0:
                        start = False
                        break
                    elif button == 1:
                        pass
                    elif button == 2:
                        pygame.quit()
                        sys.exit()
        colorStart = (100,100,100) if button == 0 else (0,0,0)
        colorExit = (100,100,100) if button == 2 else (0,0,0)
        win.blit(pygame.font.Font(None, 36).render("Start", True, colorStart), (100,700))
        win.blit(pygame.font.Font(None, 36).render("Exit", True, colorExit), (100,750))
        pygame.display.update()

    while True:
        win.fill(back_ground_color)
        clock.tick(c.FPS)
        for event in pygame.event.get(pygame.QUIT):
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #me.dx=1
        #me.dy=0
        #me.moving=10
        # me.keyboard()
        catchKeyboard(me,dialoger)

        a=i.thisMap
        me.clock(a)
        # me.draw(3,fpscnt,(0,0),win)
        car=i.thisMap.genCamera()
        i.thisMap.clock()
        i.thisMap.draw(fpscnt,car,win)

        # segmentDraw.drawR(1,15,4,car,win)
        # segmentDraw.drawC(1,15,4,car,win)
        # segmentDraw.drawSqure(9,4,6,2,car,win)

        # dialoger.keyboard()
        dialoger.draw(win)
        # print(car)
        # print(me.hp)
        # print(me.gx, me.gy)
        fpscnt+=1
        pygame.display.update()
