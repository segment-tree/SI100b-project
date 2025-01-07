from __future__ import annotations
from typing import *
import constants as c
from imageclass import (myImage)
entityIdCount:int=0
def genEntityId(): # from 1(0 id is for player)
    global entityIdCount
    entityIdCount+=1
    return entityIdCount
class entityLike:
    id:int
    gx:int; gy:int # 网格中的xy坐标
    rx:int; ry:int # 渲染中的xy坐标
    # x列y行，坐标都从0开始
    dx:int;dy:int # 正在移动的方向=-1/0/+1,同时表示朝向
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
    def reRegister(self , gx:int ,gy:int ,initInMap:Callable[[int,int,entityLike,bool],bool], force:bool=False): # 重新注册entity，切换地图时使用
        self.gx,self.gy = gx,gy
        self.gxy2rxy()
        self.moving=0
        if initInMap(gx,gy,self,force)==False : 
            self.id=-1 # 创建失败
            return False
        return True
    def __init__(self, id:int, gx:int, gy:int, initInMap:Callable[[int,int,entityLike],bool], speed:int=c.IntialSpeed, layer:int=9):
        # initInMap在地图中生成该实体
        if initInMap(gx,gy,self)==False : 
            self.id=-1 # 创建失败
            raise Exception("Create entity failed")
            # return None
        self.id,self.gx,self.gy = id,gx,gy
        self.speed=speed
        self.gxy2rxy()
        self.dx,self.dy,self.moving=0,0,0
        self.allowOverlap=True # temp
        self.layer=layer
        

    def tryMove(self, dx:int, dy:int, allowF:Callable[[int,int,entityLike],bool])->bool:
        # 其中func为地图的检测函数（为了避免此文件依赖于scene.py)
        # allowF(x:int,y:int,id:entityLike)->bool:
        # x y 表示要求的坐标，id表示请求发出者的~entity_id~地址
        if self.moving>1 : return False
        self.dx,self.dy=dx,dy # 无论是否允许移动(但不在移动)，都要改变entity的朝向
        if allowF(self.gx+dx,self.gy+dy,self) :
            self.moving=c.CellSize//self.speed+1
            return True
        return False
    def clock(self, moveUpdate:Callable[[int,int,int,int,entityLike],None]):
        # moveUpdate 为地图的更新当前实体所在网格的函数
        # moveUpdate(oldx:int, oldy:int, newx:int, newy:int, entity:entityLike)
        if self.moving>0 :
            self.moving-=1
            self.rx+=self.dx*self.speed
            self.ry+=self.dy*self.speed
            oldx,oldy=self.gx,self.gy
            self.rxy2gxy()
            if self.gx!=oldx or self.gy!=oldy:
                moveUpdate(oldx,oldy,self.gx,self.gy,self)
        if self.moving<=1:self.gxy2rxy()#及时跑一下这个转换，试图消除一些左键和下键交替按有盖率卡在两个格中间的bug
    def draw(self, layer:int, fpscnt:int, camera:Tuple[int,int], win):...
        # do nothing
    def hpMinus(self, _:int=1):...#占位符,防止误调用
    def walkInto(self, other:entityLike)->bool:
        if self.id==other.id : return True
        if not self.allowOverlap or not other.allowOverlap:
            return False
        return True
    def overlap(self, other:entityLike):...
    def delete(self):
        self.id=-1

class creature(entityLike):
    hp:int
    immune:int # 标记受击后的无敌时间
    imagesMoving:Dict[Tuple[int,int],List[myImage]] # 移动时的贴图，第二维list长度为c.WalkingFpsLoop
    imagesStanding:Dict[Tuple[int,int],myImage] # 静止时贴图，怪物没有
    bombSum:int # 炸弹数量
    bombRange:int # 爆炸范围
    cankick:bool # 踢炸弹
    def reRegister(self, gx:int, gy:int, initInMap:Callable, force:bool=False):
        self.immune=0
        return super().reRegister(gx,gy,initInMap,force) 
    def __init__(self, id:int, gx:int, gy:int, imagesdir:str, initInMap:Callable, speed:int=c.IntialSpeed, hp:int=c.IntialHp, layer:int=9):
        super().__init__(id,gx,gy,initInMap,speed,layer)
        self.hp=hp
        self.immune=0
        self.bombSum=1
        self.bombRange=c.IntialBombRange
        self.cankick=False
        self.imagesStanding,self.imagesMoving={},{}
        t=("monster"in str(type(self)))#trick # 用于处理怪物静止时也动的问题
        for tx in range(-1,2):
            for ty in range(-1,2):
                if abs(tx)+abs(ty)<2:
                    if not t:self.imagesStanding[(tx,ty)]=myImage(imagesdir+f"standing-({tx},{ty}).png")
                    self.imagesMoving[(tx,ty)]=[]
                    for i in range(1,c.WalkingFpsLoop+1):
                        self.imagesMoving[(tx,ty)].append(myImage(imagesdir+f"moving-({tx},{ty})-{i}.png"))
    def hpMinus(self, n:int=1):
        if self.immune>0:return
        self.hp-=n
        if self.hp<=0 : self.delete()
        else : self.immune=c.ImmuneFrame
    def hpPlus(self, n:int=1):
        self.hp+=n
        self.immune=0# 清理无敌帧
    def clock(self, moveUpdate:Callable):
        super().clock(moveUpdate)
        self.immune-=1
    def draw(self, layer:int, fpscnt:int, camera:Tuple[int,int], win):
        super().draw(layer,fpscnt,camera,win)
        if(self.layer==layer):
            w=None
            t=("monster"in str(type(self)))#trick
            if self.moving>0 or t:
                w=self.imagesMoving[(self.dx,self.dy)][fpscnt%c.WalkingFpsLoop]
            else:w=self.imagesStanding[(self.dx,self.dy)]
            if self.immune<=0 or fpscnt%3!=0:
                w.draw(self.rx,self.ry,camera,win)
    def putBomb(self, initInMap:Callable,bomb):
        if self.bombSum>0:
            try:
                t=bomb(genEntityId(),self.gx,self.gy,initInMap,self,layer=2)
                if t.id!=-1:self.bombSum-=1
            except Exception as inst:
                if str(inst)!="Create entity failed":
                    raise Exception(inst)

# 分界线，上面部分几乎完全不依赖于scene.py，下面几乎完全依赖
