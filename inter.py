# 包含entity player等
# 因为这部分代码需要访问scene所以不在entity.py里
from entity import *
from scene import *
#第一个全局变量
thisMap=Mapper(1,1)
class player(creature):
    money:int
    cankicked:bool
    def keyboard(self): # 捕捉键盘信息
        keys = pygame.key.get_pressed()
        allowF=thisMap.moveRequest
        #python有for-else语句但没有 elfor 有什么让这段代码美观的方案吗？？
        for i in c.KeyboardLeft:
            if keys[i]: self.tryMove(-1,0,allowF);break
        else:
            for i in c.KeyboardRight:
                if keys[i]: self.tryMove(1,0,allowF);break
            else:
                for i in c.KeyboardUp:
                    if keys[i]: self.tryMove(0,-1,allowF);break
                else:
                    for i in c.KeyboardDown:
                        if keys[i]: self.tryMove(0,1,allowF);break
        for i in c.KeyboardBomb:
            pass
    def __init__(self, id, gx, gy, imagesdir, speed = c.IntialSpeed, hp=c.IntialHp, layer=9):
        super().__init__(id, gx, gy, imagesdir, speed, hp, layer)
        thisMap.mp[gx][gy]['entity'].add(self)

        
    def clock(self):
        super().clock(thisMap.moveUpdate)

#test
def tempMagGener(nowmp):
    # nowmp.C=30
    # nowmp.R=30
    def genWall(x,y):
        nowmp.mp[x][y]["type"]="wall"
        nowmp.mp[x][y]["render"]=myImage(f'./assets/scene/wall{nowmp.style}.1.png')

    genWall(7,7)
    for i in range(0,30):
        genWall(0,i);genWall(i,0);genWall(nowmp.C,i);genWall(i,nowmp.R)
    
if __name__ == "__main__":
    pygame.init()
    thisMap=Mapper(100,100)
    tempMagGener(thisMap)
    back_ground_color=(200, 200, 200)
    clock = pygame.time.Clock() # 用于控制循环刷新频率的对象
    win = pygame.display.set_mode((c.WinWidth*c.CellSize,c.WinHeight*c.CellSize))
    fpscnt=0
    me=player(id=0,gx=2,gy=2,imagesdir='./assets/player/',layer=3)
    thisMap.me=me
    while True:
        win.fill(back_ground_color)
        clock.tick(c.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #me.dx=1
        #me.dy=0
        #me.moving=10
        me.keyboard()
        me.clock()
        # me.draw(3,fpscnt,(0,0),win)
        thisMap.draw(fpscnt,(0,0),win)
        #print(me.rx,me.ry)
        fpscnt+=1
        pygame.display.update()
