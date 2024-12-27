from __future__ import annotations
import constants as c
from typing import *
class entityLike:
    id:int
    gx:int
    gy:int
    rx:int
    ry:int
    dx:int
    dy:int
    moving:int # 还要移动几帧
    speed:int
    allowOverlap:bool # 允许其他entity与之重叠
    #image
    def gxy2rxy(self): # 通过gxy生成rxy
        self.rx=self.gx*c.CellSize-c.CellSize//2
        self.ry=self.gx*c.CellSize-c.CellSize//2
    def rxy2gxy(self):
        self.gx=self.rx//c.CellSize
        self.gy=self.ry//c.CellSize
    def __init__(self,id:int,gx:int,gy:int,speed:int=c.IntialSpeed):
        self.id,self.gx,self.gy = id,gx,gy
        self.speed=speed
        self.gxy2rxy()
        self.dx,self.dy,self.moving=0,0,0
        self.allowOverlap=True # temp
    def tryMove(self,dx:int,dy:int,func:callable)->bool:
        # 其中func为地图的检测函数
        # func(x,y,id)->bool:
        # x y 表示要求的坐标，id表示请求发出者的entity_id
        self.dx,self.dy=dx,dy # 无论是否允许移动，都要改变entity的朝向
        if self.moving : return False
        if func(self.gx+dx,self.gy+dy,self.id) :
            self.moving=c.CellSize//self.speed
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
    def draw(self,layer:int,camera:Tuple[int,int]):...
        # do nothing
    def walkInto(self,other:entityLike)->bool:
        if self.id==other.id : return True
        if not self.allowOverlap or not other.allowOverlap:
            return False
        return True
    def delete(self):...

# test

if __name__ == "__main__":
    a=entityLike(1,1,1)
    b=entityLike(2,2,2)
    cc=entityLike(1,1,1)
    d={a,b}
    print(cc in d)
    for i in d:
        print(i)
