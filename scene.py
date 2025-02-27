# from __future__ import annotations
import constants as c
import copy
from imageclass import(myImage)
from typing import *
from entity import *
import random

class Mapper: # Map is some keyword use Mapper instead
    mp:List[List[Dict[str,Any]]]
    entities:List[entityLike] # Set[entityLike]
    C:int # Column
    R:int # Row
    me:Any #指向玩家实体
    style:int # 0 森林(田野)，1 城镇 ，2 商店，3 "山洞"，？ boss房(无)
    backGround:myImage|None # 有无背景(田野山洞无背景)
    def __init__(self, c:int, r:int,style=0): # It's in CHAOS!
        self.C,self.R=c,r
        self.style=style
        self.fieldimg=myImage(f'./assets/scene/field{self.style}.png')
        # wall=myImage(f'./assets/scene/wall{self.style}.1.png')
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
        self.backGround=None
        pass
    def invaild_coord(self, x:int, y:int):
        return x<-1 or x > self.C or y<-1 or y > self.R
    def genCamera(self): # 生成镜头偏移量
        basex=self.me.rx-c.WinWidth*c.CellSize//2
        basey=self.me.ry-c.WinHeight*c.CellSize//2
        basex=min(max(basex,0),self.C*c.CellSize-c.WinWidth *c.CellSize)
        basey=min(max(basey,0),self.R*c.CellSize-c.WinHeight*c.CellSize)
        return (basex,basey)
    def addEntity(self, gx:int, gy:int, entity, force:bool=False)->bool: # 在地图中添加实体
        if not force:
            for i in self.mp[gx][gy]['entity']:
                if i.allowOverlap==False:
                    return False
        if not "player" in str(type(entity)): # trick; player大概不应被存在entities数组里
            self.entities.append(entity)
        self.mp[gx][gy]['entity'].add(entity)
        return True
    def addMonster(self, gx:int, gy:int, imgdir:str)->monster:
        return monster(genEntityId(),gx,gy,imgdir, self.addEntity,layer=3)
    def moveRequest(self, x:int, y:int, entity:entityLike)->bool: # entity调用这个来判断地图是否允许移动
        if self.invaild_coord(x,y):return False
        if self.mp[x][y].get("teleportTo") and not "player" in str(type(entity)):
            return False
        if self.mp[x][y]["type"] in ["wall","obstacle"]:
            return False
        for i in self.mp[x][y]["entity"]:
            if not i.walkInto(entity) : return False
        for i in self.mp[x][y]["entity_locked"]:
            if not i.walkInto(entity) : return False
        # create lock
        # print(x,y)###
        self.mp[x][y]["entity_locked"].add(entity)
        return True
    
    def moveUpdate(self, oldx:int, oldy:int, newx:int, newy:int, entity:entityLike): # 移动超过两个格子的中线更新坐标
        # set 移除元素： remove 不存在会返回错误；discard不会
        self.mp[oldx][oldy]["entity"].remove(entity)
        self.mp[newx][newy]["entity_locked"].discard(entity)  # 原版本为remove,有时不会创建lock故改为discard
        self.mp[newx][newy]["entity"].add(entity)
    
    def draw(self, fpscnt:int, camera:Tuple[int,int],win):
        if type(self.backGround)==myImage : self.backGround.drawG(0,self.R-1,camera,win)
        for layer in range(6):
            for j in range(self.R):
                for i in range(self.C):
                    nowlay=0 # 当前格子本身的layer
                    trans=255
                    match self.mp[i][j]["type"]:
                        case "field":
                            nowlay=0
                            if self.mp[i][j]["render"]==None:
                                self.mp[i][j]["render"]=self.fieldimg
                        case "wall":nowlay=3#5
                        case "obstacle":nowlay=2
                        case "object":nowlay=2
                    if self.mp[i][j]["type"]=="wall" and self.mp[i][j]["render"].overheight() and\
                        j>0 and self.mp[i][j-1]["type"]=="object" and self.mp[i][j-1]["content"]!=0 :
                            trans=128+64
                    
                    if layer==nowlay:
                        self.mp[i][j]["render"].drawG(i,j,camera,win,transparent=trans)
                    elif layer==0: # 即使不是空地，图层底层也要渲染空地
                       self.fieldimg.drawG(i,j,camera,win)
                    if layer==1 and self.mp[i][j].get("render!"): # 对爆炸的特殊处理
                        self.mp[i][j]["render!"].drawG(i,j,camera,win)
                    if layer==2 and self.mp[i][j].get("burnCenter") and self.mp[i][j].get("render!") :  # 对爆炸的特殊处理
                        self.mp[i][j]["render!"].drawG(i,j,camera,win)
                    for k in self.mp[i][j]["entity"]:
                        k.draw(layer,fpscnt,camera,win)
                                    
            #for i in self.entities:
            #    i.draw(layer,fpscnt,camera,win)
            #self.me.draw(layer,fpscnt,camera,win)
            #^这么画图层会出问题

    def burnTurn(self, gx:int, gy:int, img:myImage, center:bool=False): # 将该地块转为受炸弹影响
        # self.mp[gx][gy]["render!"]=self.mp[gx][gy]["render"]
        # self.mp[gx][gy]["render"]=img
        self.mp[gx][gy]["burning"]=c.BurnCount
        self.mp[gx][gy]["render!"]=img
        if center:
            self.mp[gx][gy]["burnCenter"]=True
    def burnUnturn(self, gx:int, gy:int): # 将该地块解除受炸弹影响
        # if self.mp[gx][gy].get("render!"):
        #     self.mp[gx][gy]["render"]=self.mp[gx][gy]["render!"]
        #     self.mp[gx][gy].pop("render!")
        self.mp[gx][gy].pop("render!")
        self.mp[gx][gy].pop("burnCenter",None)

    def clock(self):
        for i in self.entities:
            i.clock(self.moveUpdate,mapper=self)
        # 删除死掉的实体
        t=copy.copy(self.entities)
        for i in t:
            if i.id==-1:
                self.mp[i.gx+i.dx][i.gy+i.dy]["entity_locked"].discard(i)
                self.mp[i.gx][i.gy]["entity"].remove(i)
                self.entities.remove(i)
        # print(len(self.entities))#
        for i in self.entities:
            if "monster"in str(type(i)):
                i.ai(self)
        # 碰撞伤害
        for i in self.entities:
            self.me.overlap(i)
        # 爆炸的倒计时,数到0消除爆炸效果
        for j in range(self.R):
            for i in range(self.C):
                if self.mp[i][j]["burning"]>0:
                    for k in self.mp[i][j]["entity"]:
                        k.hpMinus()
                    self.mp[i][j]["burning"]-=1
                    if self.mp[i][j]["burning"]==0:
                        self.burnUnturn(i,j)

class BossScene(Mapper): # ABANDONED
    status:int # boss 招式
    count:int # boss 当前招式剩余时间
    content:list # 当前招式暂存的内容
    def __init__(self, c:int, r:int, style=1):
        super().__init__(c,r,style)
        self.status=0
    def decide(self):
        self.status=random.randrange(0,3)
        self.count=c.BossDefaultCount
    def preAction1(self):
        tcnt=0;self.content=[]
        while tcnt<10:
            x=random.randrange(0,self.C)
            y=random.randrange(0,self.R)
            flag=True
            for i in range(x,x+4):
                for j in range(y,y+4):
                    if self.invaild_coord(i,j) or self.mp[x][y]["type"] in ["wall","obstacle"]:
                        flag=False
            if flag:
                self.content.append((x,y));tcnt+=1
    def doAction1(self):
        pass
    def clock(self):
        self.count-=1
        if self.count==0 : self.decide()
        match self.status:
            case 0:
                if self.count==c.BossDefaultCount:
                    self.preAction1()
                if self.count==c.BossDefaultCount//2:
                    self.doAction1()
        super().clock()