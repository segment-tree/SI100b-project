from __future__ import annotations
from typing import *
import constants as c
from imageclass import *
class entityLike:
    id:int
    gx:int
    gy:int
    rx:int
    ry:int
    # x列y行，坐标都从0开始
    dx:int
    dy:int
    moving:int # 还要移动几帧
    speed:int
    allowOverlap:bool # 允许其他entity与之重叠
    layer:int # 当前实体所在图层
    #image
    def gxy2rxy(self): # 通过gxy生成rxy
        self.rx=self.gx*c.CellSize+c.CellSize//2
        self.ry=self.gy*c.CellSize+c.CellSize//2
    def rxy2gxy(self):
        self.gx=self.rx//c.CellSize
        self.gy=self.ry//c.CellSize
    def __init__(self, id:int, gx:int, gy:int, speed:int=c.IntialSpeed, layer=9):
        self.id,self.gx,self.gy = id,gx,gy
        self.speed=speed
        self.gxy2rxy()
        self.dx,self.dy,self.moving=0,0,0
        self.allowOverlap=True # temp
        self.layer=layer
    def tryMove(self, dx:int, dy:int, allowF:callable)->bool:
        # 其中func为地图的检测函数
        # allowF(x,y,id)->bool:
        # x y 表示要求的坐标，id表示请求发出者的~entity_id~地址
        if self.moving>1 : return False
        self.dx,self.dy=dx,dy # 无论是否允许移动(但不在移动)，都要改变entity的朝向
        if allowF(self.gx+dx,self.gy+dy,self) :
            self.moving=c.CellSize//self.speed+1
            return True
        return False
    def clock(self,moveUpdate:callable):
        if self.moving>0 :
            self.moving-=1
            self.rx+=self.dx*self.speed
            self.ry+=self.dy*self.speed
            oldx,oldy=self.gx,self.gy
            self.rxy2gxy()
            if self.gx!=oldx or self.gy!=oldy:
                moveUpdate(oldx,oldy,self.gx,self.gy,self)
        if self.moving<=1:self.gxy2rxy()#及时跑一下这个转换，试图消除一些左键和下键交替按有盖率卡在两个格中间
    def draw(self,layer:int,fpscnt:int,camera:Tuple[int,int],win):...
        # do nothing
    def walkInto(self,other:entityLike)->bool:
        if self.id==other.id : return True
        if not self.allowOverlap or not other.allowOverlap:
            return False
        return True
    def delete(self):...

class creature(entityLike):
    hp:int
    immune:int # 标记受击后的无敌时间
    imagesMoving:Dict[(int,int),List[myImage]]
    imagesStanding:Dict[(int,int)]
    bombSum:int
    bombRange:int
    def __init__(self, id:int, gx:int, gy:int, imagesdir:str, speed:int=c.IntialSpeed, hp=c.IntialHp, layer=9):
        super().__init__(id,gx,gy,speed,layer)
        self.hp=hp
        self.immune=0
        self.bombSum=1
        self.bombRange=c.IntialBombRange
        self.imagesStanding,self.imagesMoving={},{}
        t=("monster"in str(type(self)))#trick
        for tx in range(-1,2):
            for ty in range(-1,2):
                if abs(tx)+abs(ty)<2:
                    if not t:self.imagesStanding[(tx,ty)]=myImage(imagesdir+f"standing-({tx},{ty}).png")
                    self.imagesMoving[(tx,ty)]=[]
                    for i in range(1,c.WalkingFpsLoop+1):
                        self.imagesMoving[(tx,ty)].append(myImage(imagesdir+f"moving-({tx},{ty})-{i}.png"))
    def hpMinus(self,n:int=1):
        self.hp-=n
        if self.hp<0 : self.delete()
        else : self.immune=c.ImmuneFrame
    def hpPlus(self,n:int=1):
        self.hp+=n
        self.immune=0# 清理无敌帧
    def draw(self,layer:int,fpscnt:int,camera:Tuple[int,int],win):
        if(self.layer==layer):
            w=None
            t=("monster"in str(type(self)))#trick
            if self.moving>0 or t:
                w=self.imagesMoving[(self.dx,self.dy)][fpscnt%c.WalkingFpsLoop]
            else:w=self.imagesStanding[(self.dx,self.dy)]
            w.draw(self.rx,self.ry,camera,win)




# test

if __name__ == "__main__":
    a=entityLike(1,1,1)
    b=entityLike(2,2,2)
    cc=entityLike(1,1,1)
    d={a,b}
    print(cc in d)
    pygame.init()
    back_ground_color=(200, 200, 200)
    clock = pygame.time.Clock() # 用于控制循环刷新频率的对象
    win = pygame.display.set_mode((c.WinWidth*c.CellSize,c.WinHeight*c.CellSize))
    fpscnt=0
    me=creature(id=1,gx=2,gy=2,imagesdir='./assets/player/')
    while True:
        win.fill(back_ground_color)
        clock.tick(c.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        me.dx=1
        me.dy=0
        me.moving=10
        def tmpf(a,b,c):return True
        def tmpff(a,b,c,d,e):pass
        #if(fpscnt%40==0):me.tryMove(1,0,tmpf)
        #me.clock(tmpff)
        me.draw(9,fpscnt,(0,0),win)
        #print(me.rx,me.ry)
        fpscnt+=1
        pygame.display.update()
