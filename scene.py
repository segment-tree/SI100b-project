import constants as c
import copy
from imageclass import(myImage)
from typing import *
# from __future__ import annotations
from entity import *

class Mapper: # Map is some keyword use Mapper instead
    mp:List[List[Dict[str,Any]]]
    entities:List[entityLike]
    C:int # Column
    R:int # Row
    me:Any #指向玩家实体
    style:int # 0 森林， ？ boss房
    def __init__(self,c,r): # It's in CHAOS!
        self.C,self.R=c,r
        self.style=0
        self.fieldimg=myImage(f'./assets/scene/field{self.style}.png')
        wall=myImage(f'./assets/scene/wall{self.style}.1.png')
        self.entities=[]
        ttt={
            "type":"field",
            "burning":0,
            "entity":set(),
            "entity_locked":set(),
            "content":0,
            "render":None}
        self.mp =[[copy.deepcopy(ttt) for i in range(c+1)] for j in range(r+1)]
        for i in self.mp:
            for j in i:
                j["render"]=self.fieldimg
        pass
    def invaild_coord(self,x,y):
        return x<0 or x >= self.C or y<0 or y >= self.R
    def genCamera(self):
        basex=self.me.rx-c.WinWidth*c.CellSize//2
        basey=self.me.ry-c.WinHeight*c.CellSize//2
        basex=min(max(basex,0),self.C*c.CellSize-c.WinWidth *c.CellSize)
        basey=min(max(basey,0),self.R*c.CellSize-c.WinHeight*c.CellSize)
        return (basex,basey)

    def moveRequest(self,x:int,y:int,entity:entityLike):
        if self.invaild_coord(x,y):return False
        if self.mp[x][y]["type"] in ["wall","obstacle"]:
            return False
        for i in self.mp[x][y]["entity"]:
            if not i.walkInto(entity) : return False
        for i in self.mp[x][y]["entity_locked"]:
            if not i.walkInto(entity) : return False
        # create lock
        print(x,y)###
        self.mp[x][y]["entity_locked"].add(entity)
        return True
    
    def moveUpdate(self,oldx:int,oldy:int,newx:int,newy:int,entity:entityLike):
        # set 移除元素： remove 不存在会返回错误；discard不会
        self.mp[oldx][oldy]["entity"].remove(entity)
        self.mp[newx][newy]["entity_locked"].remove(entity)
        self.mp[newx][newy]["entity"].add(entity)
    
    def draw(self,fpscnt,camera,win):
        for layer in range(6):
            for j in range(self.R):
                for i in range(self.C):
                    nowlay=0
                    match self.mp[i][j]["type"]:
                        case "field":
                            nowlay=0
                            self.mp[i][j]["render"]=self.fieldimg
                        case "wall":nowlay=3#5
                        case "obstacle":nowlay=2
                        case "object":nowlay=2
                    '''
                    if len(self.mp[i][j]["entity_locked"])!=0:
                        nowlay=100###
                        print(i,j,self.mp[i][j]["entity_locked"])###
                    '''
                    if layer==nowlay:
                        self.mp[i][j]["render"].drawG(i,j,camera,win)
                    elif layer==0:
                       self.fieldimg.drawG(i,j,camera,win)
                        
            for i in self.entities:
                i.draw(layer,fpscnt,camera,win)
            self.me.draw(layer,fpscnt,camera,win)


    def clock(self):
        for i in self.entities:
            pass
        for j in range(self.R):
            for i in range(self.C):
                pass

