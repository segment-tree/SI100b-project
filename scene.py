import constants as c
from typing import *
# from __future__ import annotations
from entity import *
class Map:
    mp:List[List[Dict[str,Any]]]
    entities:List[Any]
    C:int # Column
    R:int # Row
    def __init__(self,c,r):
        self.C,self.R=c,r
        ttt={
            "type":"Field",
            "burning":0,
            "entity":{},
            "entity_locked":{},
            "content":0,
            "renderId":0}
        self.mp =[[ttt for i in range(c+1)] for j in range(r+1)]
        pass
    def moveRequest(self,x:int,y:int,entity:entityLike):
        if self.mp[x][y]["type"] in ["Wall","Obstacle"]:
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
    
    def clock(self,player):
        for  i in self.entities:
            pass

