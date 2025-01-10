from typing import *
import constants as c
from imageclass import (myImage)
from entity import (entityLike,creature)
from scene import (Mapper)
import pygame.surface
import random
class bomb(entityLike):
    author:creature
    damage:int
    range:int
    image:myImage
    kicked:bool
    def __init__(self, id:int, gx:int, gy:int, initInMap:Callable, author:creature, speed:int=c.IntialSpeed, layer:int=9, skin:int=0):
        super().__init__(id,gx,gy,initInMap,speed,layer)
        self.author=author
        self.damage=1
        self.range=author.bombRange
        self.count=c.BombCount
        self.allowOverlap=False
        #skin 表示炸弹皮肤
        self.image=myImage(f"assets/scene/bomb{skin}.png")
        self.kicked=False
        self.speed=c.BombKickedSpeed
    def draw(self, layer:int, fpscnt:int, camera:Tuple[int,int], win:pygame.Surface)->None:
        super().draw(layer,fpscnt,camera,win)
        if self.layer==layer:
            self.image.draw(self.rx,self.ry,camera,win)
    def clock(self, moveUpdate:Callable, mapper:Mapper)->None:
        super().clock(moveUpdate)
        if self.count <=0:
            self.delete(mapper)
        else: self.count-=1
        if self.kicked:
            if not self.tryMove(self.dx,self.dy,mapper.moveRequest) and self.moving==0 :
                self.kicked=False # 停止后不再移动
    
    def walkInto(self, other:entityLike|creature)->bool:
        if isinstance(other,creature)  and other.cankick == True :
            self.dx=self.gx-other.gx
            self.dy=self.gy-other.gy
            self.kicked=True
        return super().walkInto(other)

    def delete(self, mapper:Mapper)->None:
        # 执行炸弹爆炸 (应该写在这里呢还是写在Mapper里？)
        xx,yy,stp=self.gx,self.gy,self.range
        def __set(x:int,y:int,burnimg:myImage,pointer:List[List[int]])->bool:
            def upPointer()->None:
                pointer[0][0]=x;pointer[1][0]=y
                mapper.mp[x][y].pop("burnCenter",None)
                if mapper.mp[x][y]["burning"]!=0 :
                    pointer[0][0]=-1;pointer[1][0]=-1
            if mapper.invaild_coord(x,y) : return False
            if mapper.mp[x][y]["type"] in ["field","object"]:
                upPointer()
                mapper.burnTurn(x,y,burnimg)
                if mapper.mp[x][y]["type"]=="object":
                    mapper.mp[x][y]["type"]="field"
                    mapper.mp[x][y]["render"]=None
                    mapper.mp[x][y]["content"]=0 # 炸弹炸毁掉落物
                
                return True
            if mapper.mp[x][y]["type"]=="obstacle" :
                upPointer()

                mapper.mp[x][y]["type"]="object"
                mapper.burnTurn(x,y,burnimg)
                # gen content
                mapper.mp[x][y]["content"]=random.randrange(1,31)
                if mapper.mp[x][y]["content"]>26 : mapper.mp[x][y]["content"]=0
                elif mapper.mp[x][y]["content"]>5 : mapper.mp[x][y]["content"]=5

                if mapper.mp[x][y]["content"]==0:
                    mapper.mp[x][y]["type"]="field"
                    mapper.mp[x][y]["render"]=None
                else:mapper.mp[x][y]["render"]=\
                    myImage(f'./assets/scene/object{mapper.mp[x][y]["content"]}.png')
            return False
        
        colimg=myImage("./assets/scene/burning3.png")
        rowimg=myImage("./assets/scene/burning2.png")
        u,d,l,r,_=[yy],[yy],[xx],[xx],[0]
        for _x in range(xx,xx+stp+1):
            if not __set(_x,yy,rowimg,[r,_]):break
        for _x in reversed(range(xx-stp,xx+1)):
            if not __set(_x,yy,rowimg,[l,_]):break
        for _y in range(yy,yy+stp+1):
            if not __set(xx,_y,colimg,[_,d]):break
        for _y in reversed(range(yy-stp,yy+1)):
            if not __set(xx,_y,colimg,[_,u]):break
        #炸弹边缘
        uu,dd,ll,rr=u[0],d[0],l[0],r[0]
        if uu!=-1 :mapper.burnTurn(xx,uu,myImage("./assets/scene/burning6.png"))
        if dd!=-1 :mapper.burnTurn(xx,dd,myImage("./assets/scene/burning4.png"))
        if ll!=-1 :mapper.burnTurn(ll,yy,myImage("./assets/scene/burning5.png"))
        if rr!=-1 :mapper.burnTurn(rr,yy,myImage("./assets/scene/burning7.png"))
        #炸弹中心
        mapper.burnTurn(xx,yy,myImage("./assets/scene/burning1.png",zoom=1.4,mode=1),center=True)
        # 归还炸弹
        self.author.bombSum+=1
        super().delete()

import queue
from collections import (deque)
class monster(creature):
    aiWalkCount:int
    aiBombCount:int
    movQ:deque[Tuple[int,int]]
    def __init__(self, id:int, gx:int, gy:int, imagesdir:str, initInMap:Callable, speed:int=c.IntialSpeed, hp:int=c.IntialHp, layer:int=9):
        super().__init__(id, gx, gy, imagesdir, initInMap, speed, hp, layer)
        self.aiWalkCount=c.FPS//2
        self.aiBombCount=c.FPS//2
        self.movQ=deque()
    def _aiFindDangerousGird(self, mapper:Mapper)->Set[Tuple[int,int]]:
        dangerous=[]
        for e in mapper.entities:
            if isinstance(e,bomb):
                dangerous+=[(e.gx,i) for i in range(e.gy-e.range,e.gy+e.range+1)]
                dangerous+=[(i,e.gy) for i in range(e.gx-e.range,e.gx+e.range+1)]
        dangerouses=set(dangerous)
        return dangerouses
    def _check(self, x:int, y:int, mapper:Mapper)->bool:
        if mapper.invaild_coord(x,y):return False
        if mapper.mp[x][y]["type"] in ["wall","obstacle"]:
            return False
        if mapper.mp[x][y]["burning"]>0:return False
        for i in mapper.mp[x][y]["entity"]:
            if not i.walkInto(self) : return False
        return True
    def aiFindSafeGird(self, mapper:Mapper)->None: # 不知道ai运行效率如何
        dangerous=self._aiFindDangerousGird(mapper)
        # bfs
        q:queue.Queue[List[Any]]=queue.Queue()
        q.put([self.gx,self.gy,tuple()])
        dir=[(-1,0),(1,0),(0,-1),(0,1)]
        vis:dict[Tuple[int,int],bool]={}
        cnt=0
        while not q.empty():
            a=q.get()
            cnt+=1 # cnt 防止怪喜欢站着不动
            print(q.qsize(),(a[0],a[1]),{(a[0],a[1])} & dangerous!= {(a[0],a[1])})
            if {(a[0],a[1])} & dangerous != {(a[0],a[1])} and (cnt>1 or random.randrange(0,9)<9):
                movQ_t=[]
                t=a[2]
                while len(t)>0:
                    movQ_t.append((t[1],t[2]))
                    t=t[0][2]
                
                self.movQ=deque(reversed(movQ_t))
                break
            random.shuffle(dir)
            for d in dir:
                nx,ny=a[0]+d[0],a[1]+d[1]
                if self._check(nx,ny,mapper) and not vis.get((nx,ny)):
                    vis[(nx,ny)]=True
                    b=[nx,ny,(a,d[0],d[1])]
                    q.put(b)
    def walk1step(self, mapper:Mapper)->bool:
        dangerous=self._aiFindDangerousGird(mapper)
        dir=[(-1,0),(1,0),(0,-1),(0,1)]
        random.shuffle(dir)
        for d in dir:
            nx,ny=self.gx+d[0],self.gy+d[1]
            if self._check(nx,ny,mapper) and {(nx,ny)} & dangerous != {(nx,ny)}:
                self.movQ.append((d[0],d[1]))
                return True
        return False
        
    def walk(self, mapper:Mapper)->None:
        if self.moving>0:return
        if len(self.movQ)>0:
            dx,dy=self.movQ[0][0],self.movQ[0][1]
            if mapper.mp[self.gx+dx][self.gy+dy]["burning"]<=0:
                t=self.tryMove(dx,dy,mapper.moveRequest)
                if t==True:self.movQ.popleft()
                else : self.movQ=deque() # 防止怪物卡死
                return
        self.aiWalkCount-=1
        if self.aiWalkCount==0:
            if not self.walk1step(mapper):
                self.aiFindSafeGird(mapper)
            self.aiWalkCount=c.FPS//4

    def ai(self, mapper:Mapper)->None:
        a=random.randrange(-1,10)
        if a<0:return
        if a<7 or len(self.movQ)>0:
            self.walk(mapper)
        else:
            self.aiBombCount-=1
            if self.aiBombCount==0:
                if abs(self.gx-mapper.me.gx)+abs(self.gy-mapper.me.gy) <= c.MonsterBombDis :
                    self.putBomb(mapper.addEntity,bomb)
                self.aiBombCount=c.FPS//2

        return
        match a:
            case 1:self.tryMove(-1,0,mapper.moveRequest)
            case 2:self.tryMove( 1,0,mapper.moveRequest)
            case 3:self.tryMove(0,-1,mapper.moveRequest)
            case 4:self.tryMove(0, 1,mapper.moveRequest)
            # case 5:self.putBomb(mapper.addEntity) # only for test

    def clock(self, moveUpdate:Callable, mapper:Any)->None:
        return super().clock(moveUpdate)


# test
'''
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
'''
