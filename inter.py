# 包含属于entity player monster等
# 因为这部分代码需要访问scene所以不在entity.py里
from entity import *
from scene import *
from makescene import *
#第一个全局变量
thisMap=Mapper(1,1)
dialoger=dialog()
class player(creature):
    money:int
    readToInteract:bool
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
            if keys[i]:self.putBomb(thisMap.addEntity);break
        for i in c.KeyboardInteract:
            if keys[i] : self.readToInteract=True;break
        else : self.readToInteract=False
    def reRegister(self, gx:int, gy:int, initInMap:callable):
        super().reRegister(gx,gy,initInMap)
    def __init__(self, id, gx, gy, imagesdir, initInMap:callable=None, speed = c.IntialSpeed, hp=c.IntialHp, layer=9):
        if initInMap==None : initInMap=thisMap.addEntity# player切换地图的时候不要忘了重新在地图注册
        super().__init__(id,gx,gy,imagesdir,initInMap,speed,hp,layer)
        self.money=0
        self.cankick=True
        self.hp+=c.IntialPlayerHp-c.IntialHp

    def pickup(self,w):#捡东西
        if w[self.gx][self.gy]["type"]=="object":
            match w[self.gx][self.gy]["content"]:
                case 0:print('???a empty object???')
                case 1:self.bombSum+=1
                case 2:self.hpPlus()
                case 3:self.speed=c.IncreasedSpeed
                case 4:self.bombRange+=1
                case 5:self.money+=1
                case 6:self.cankick=True
            w[self.gx][self.gy]["type"]="field"
            w[self.gx][self.gy]["render"]=None# Warning
    def clock(self,mapper,win):
        self.pickup(mapper.mp)
        super().clock(mapper.moveUpdate)
        if mapper.mp[self.gx][self.gy].get("teleportTo") :
            thisMap.mp[self.gx][self.gy]["entity"].remove(thisMap.me)
            changeMap(*mapper.mp[self.gx][self.gy]["teleportTo"])
        # print(self.readToInteract)
        if self.readToInteract and mapper.mp[self.gx][self.gy].get("interact") and dialoger.content==None: # 只有在没有绘制对话框时才可交互
                dialoger(*thisMap.mp[self.gx][self.gy]["interact"])
    def overlap(self, other:entityLike):
        super().overlap(other)
        if (self.gx,self.gy)==(other.gx,other.gy):
            if "monster" in str(type(other)) :#trick
                self.hpMinus()
    def delete(self):
        super().delete()
        raise Exception("GAMEOVER")

maps=[]
def changeMap(mapid:int, gx:int, gy:int):
    global thisMap
    #thisMap.mp[gx][gy]["entity"].remove(thisMap.me)
    thisMap=maps[mapid]
    me.reRegister(gx,gy,thisMap.addEntity)
    thisMap.me=me

#test
def tempMapGener(nowmp:Mapper):
    # nowmp.C=30
    # nowmp.R=30
    def genWall(x,y,iid=1):
        nowmp.mp[x][y]["type"]="wall"
        nowmp.mp[x][y]["render"]=myImage(f'./assets/scene/wall{nowmp.style}.{iid}.png')
    def genObject(x,y,iid):
        nowmp.mp[x][y]["type"]="object"
        nowmp.mp[x][y]["content"]=iid
        nowmp.mp[x][y]["render"]=myImage(f'./assets/scene/object{iid}.png')
    
    nowmp.C=31
    nowmp.R=31

    genWall(7,7)
    genObject(10,13,3)
    genObject(10,4,5)
    genObject(15,14,2);genObject(18,20,4)
    genObject(3,4,1)
    # nowmp.mp[5][5]["burning"]=20*10
    # nowmp.mp[5][5]["render!"]=myImage("./assets/scene/burning_tmp.png")
    for i in range(0,30):
        genWall(0,i);genWall(i,0);genWall(30,i);genWall(i,30)
    
    for i in range(8,12):
        genWall(i,10,5)

    # monsters
    nowmp.addMonster(5,5,"./assets/monster/")
    nowmp.addMonster(6,7,"./assets/monster/")
    t=nowmp.addMonster(1,12,"./assets/monster/")

    bomb(genEntityId(),2,2,nowmp.addEntity,t,layer=2)
    bomb(genEntityId(),5,2,nowmp.addEntity,t,layer=2)
    
if __name__ == "__main__":
    pygame.init()
    win=displayCreateWin()
    thisMap=Mapper(50,50,style=0)
    mapGener(thisMap) # 田野
    maps.append(thisMap)
    thisMap=Mapper(50,50,style=1)
    mapGenerTown(thisMap) # 城镇
    maps.append(thisMap)

    ###
    thisMap=Mapper(50,50,style=0)
    tempMapGener(thisMap)
    ###

    back_ground_color=(200, 200, 200)
    clock = pygame.time.Clock() # 用于控制循环刷新频率的对象
    fpscnt=0
    me=player(id=0,gx=1,gy=17,imagesdir='./assets/player/',layer=3)
    #print('#',me.rx,me.ry) # gy 28
    thisMap.me=me

    for i in thisMap.mp[me.gx][me.gy]["entity"]:
        print(i)

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
        me.clock(thisMap,win)
        # me.draw(3,fpscnt,(0,0),win)
        car=thisMap.genCamera()
        thisMap.clock()
        thisMap.draw(fpscnt,car,win)

        # segmentDraw.drawR(1,15,4,car,win)
        # segmentDraw.drawC(1,15,4,car,win)

        dialoger.keyboard()
        dialoger.draw(win)
        #print(car)
        #print(me.hp)
        # print(me.gx, me.gy)
        fpscnt+=1
        pygame.display.update()
