import constants as c
from typing import *
# from __future__ import annotations
from entity import *
class Map:
    mp:List[List[Dict[str,Any]]]
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
        return True
    
    

