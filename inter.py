# 包含entity player等
# 因为这部分代码需要访问scene所以不在entity.py里
from entity import *
from scene import *
#第一个全局变量
thisMap=Mapper(1,1)
class player(creature):
    money:int
    cankick:bool
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
        self.money=0
        self.cankick=False
        thisMap.mp[gx][gy]['entity'].add(self)

    def pickup(self,w):#捡东西
        if w[self.gx][self.gy]["type"]=="object":
            match w[self.gx][self.gy]["content"]:
                case 0:print('???a empty object???')
                case 1:self.bomb_num+=1
                case 2:self.hpPlus()
                case 3:self.speed=c.IncreasedSpeed
                case 4:self.bombRange+=2
                case 5:self.money+=1
                case 6:self.cankick=True
            w[self.gx][self.gy]["type"]="field"
            w[self.gx][self.gy]["render"]=None# Warning
    def clock(self):
        self.pickup(thisMap.mp)
        super().clock(thisMap.moveUpdate)

#test
def tempMagGener(nowmp):
    # nowmp.C=30
    # nowmp.R=30
    def genWall(x,y):
        nowmp.mp[x][y]["type"]="wall"
        nowmp.mp[x][y]["render"]=myImage(f'./assets/scene/wall{nowmp.style}.1.png')
    def genObject(x,y,iid):
        nowmp.mp[x][y]["type"]="object"
        nowmp.mp[x][y]["content"]=iid
        nowmp.mp[x][y]["render"]=myImage(f'./assets/scene/object{iid}.png')
    
    nowmp.C=31
    nowmp.R=31
    genWall(7,7)
    genObject(10,13,3)
    genObject(10,4,5)
    for i in range(0,30):
        genWall(0,i);genWall(i,0);genWall(30,i);genWall(i,30)
    
if __name__ == "__main__":
    pygame.init()
    thisMap=Mapper(100,100)
    tempMagGener(thisMap)
    back_ground_color=(200, 200, 200)
    clock = pygame.time.Clock() # 用于控制循环刷新频率的对象
    win = pygame.display.set_mode((c.WinWidth*c.CellSize//c.CellRatio,c.WinHeight*c.CellSize//c.CellRatio))
    fpscnt=0
    me=player(id=0,gx=1,gy=1,imagesdir='./assets/player/',layer=3)
    #print('#',me.rx,me.ry)
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
        car=thisMap.genCamera()
        thisMap.draw(fpscnt,car,win)
        #print(car)
        #print(me.rx,me.ry)
        fpscnt+=1
        pygame.display.update()
