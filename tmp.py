import constants as c
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
    def __init__(self,c,r):
        self.C,self.R=c,r
        self.style=0
        self.fieldimg=myImage(f'./assets/scene/field{self.style}.png')
        wall=myImage(f'./assets/scene/wall{self.style}.1.png')
        ttt={
            "type":"Field",
            "burning":0,
            "entity":set(),
            "entity_locked":set(),
            "content":0,
            "render":field}
        self.mp =[[ttt for i in range(c+1)] for j in range(r+1)]
        pass
    def moveRequest(self,x:int,y:int,entity:entityLike):
        if self.mp[x][y]["type"] in ["wall","obstacle"]:
            return False
        for i in self.mp[x][y]["entity"]:
            if not i.walkInto(entity) : return False
        for i in self.mp[x][y]["entity_locked"]:
            if not i.walkInto(entity) : return False
        # create lock
        self.mp[x][y]["entity_locked"].add(entity)
        return True
    
    def moveUpdate(self,oldx:int,oldy:int,newx:int,newy:int,entity:entityLike):
        # set 移除元素： remove 不存在会返回错误；discard不会
        self.mp[oldx][oldy]["entity"].remove(entity)
        self.mp[newx][newy]["entity_locked"].remove(entity)
        self.mp[newx][newy]["entity"].add(entity)
    
    def draw(self,fpscnt,camera,win):
        for layer in range(6):
            for i in range(self.R):
                for j in range(self.C):
                    self.mp[i][j]["render"].drawG(i,j,camera,win)
            for i in self.entities:
                i.draw(layer,fpscnt,camera,win)
            me.draw(layer,fpscnt,camera,win)


    def clock(self):
        for  i in self.entities:
            pass

