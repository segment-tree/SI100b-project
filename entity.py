from __future__ import annotations
from typing import *
import constants as c
from imageclass import *
import random
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
    def reRegister(self , gx:int ,gy:int ,initInMap:callable,force:bool=False): # 重新注册entity，切换地图时使用
        self.gx,self.gy = gx,gy
        self.gxy2rxy()
        self.moving=0
        if initInMap(gx,gy,self,force)==False : 
            self.id=-1 # 创建失败
            return False
        return True
    def __init__(self, id:int, gx:int, gy:int, initInMap:callable, speed:int=c.IntialSpeed, layer:int=9):
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
        

    def tryMove(self, dx:int, dy:int, allowF:callable)->bool:
        # 其中func为地图的检测函数（为了避免此文件依赖于scene.py)
        # allowF(x:int,y:int,id:entityLike)->bool:
        # x y 表示要求的坐标，id表示请求发出者的~entity_id~地址
        if self.moving>1 : return False
        self.dx,self.dy=dx,dy # 无论是否允许移动(但不在移动)，都要改变entity的朝向
        if allowF(self.gx+dx,self.gy+dy,self) :
            self.moving=c.CellSize//self.speed+1
            return True
        return False
    def clock(self, moveUpdate:callable):
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
    imagesMoving:Dict[(int,int),List[myImage]] # 移动时的贴图，第二维list长度为c.WalkingFpsLoop
    imagesStanding:Dict[(int,int)] # 静止时贴图，怪物没有
    bombSum:int # 炸弹数量
    bombRange:int # 爆炸范围
    cankick:bool # 踢炸弹
    def reRegister(self, gx:int, gy:int, initInMap:callable, force:bool=False):
        self.immune=0
        return super().reRegister(gx,gy,initInMap,force) 
    def __init__(self, id:int, gx:int, gy:int, imagesdir:str, initInMap:callable, speed:int=c.IntialSpeed, hp:int=c.IntialHp, layer:int=9):
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
    def clock(self, moveUpdate):
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
    def putBomb(self, initInMap:callable):
        if self.bombSum>0:
            try:
                t=bomb(genEntityId(),self.gx,self.gy,initInMap,self,layer=2)
                if t.id!=-1:self.bombSum-=1
            except Exception as inst:
                if str(inst)!="Create entity failed":
                    raise Exception(inst)

# 分界线，上面部分几乎完全不依赖于scene.py，下面几乎完全依赖

class bomb(entityLike):
    author:entityLike
    damage:int
    range:int
    image:myImage
    kicked:bool
    def __init__(self, id:int, gx:int, gy:int, initInMap:callable, author:entityLike, speed:int=c.IntialSpeed, layer:int=9, skin:int=0):
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
    def draw(self, layer:int, fpscnt:int, camera:Tuple[int,int], win):
        super().draw(layer,fpscnt,camera,win)
        if self.layer==layer:
            self.image.draw(self.rx,self.ry,camera,win)
    def clock(self, moveUpdate:callable, mapper:c.LostType):
        super().clock(moveUpdate)
        if self.count <=0:
            self.delete(mapper)
        else: self.count-=1
        if self.kicked:
            if not self.tryMove(self.dx,self.dy,mapper.moveRequest) and self.moving==0 :
                self.kicked=False # 停止后不再移动
    
    def walkInto(self, other:entityLike):
        if "player" in str(type(other)) and other.cankick == True : # here depend on class player
            self.dx=self.gx-other.gx
            self.dy=self.gy-other.gy
            self.kicked=True
        return super().walkInto(other)

    def delete(self, mapper:c.LostType):
        # 执行炸弹爆炸 (应该写在这里呢还是写在Mapper里？)
        xx,yy,stp=self.gx,self.gy,self.range
        def __set(x:int,y:int,burnimg:myImage,pointer:List[List[int]]):
            def upPointer():
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
        u,d,l,r=u[0],d[0],l[0],r[0]
        if u!=-1 :mapper.burnTurn(xx,u,myImage("./assets/scene/burning6.png"))
        if d!=-1 :mapper.burnTurn(xx,d,myImage("./assets/scene/burning4.png"))
        if l!=-1 :mapper.burnTurn(l,yy,myImage("./assets/scene/burning5.png"))
        if r!=-1 :mapper.burnTurn(r,yy,myImage("./assets/scene/burning7.png"))
        #炸弹中心
        mapper.burnTurn(xx,yy,myImage("./assets/scene/burning1.png",zoom=1.4,mode=1),center=True)
        # 归还炸弹
        self.author.bombSum+=1
        super().delete()

import queue
import copy
class monster(creature):
    aiWalkCount:int
    aiBombCount:int
    movQ:queue.deque
    def __init__(self, id:int, gx:int, gy:int, imagesdir:str, initInMap:callable, speed:int=c.IntialSpeed, hp:int=c.IntialHp, layer:int=9):
        super().__init__(id, gx, gy, imagesdir, initInMap, speed, hp, layer)
        self.aiWalkCount=c.FPS//2
        self.aiBombCount=c.FPS//2
        self.movQ=queue.deque()
    def _aiFindDangerousGird(self, mapper:c.LostType):
        dangerous=[]
        for e in mapper.entities:
            if "bomb" in str(type(e)):
                dangerous+=[(e.gx,i) for i in range(e.gy-e.range,e.gy+e.range+1)]
                dangerous+=[(i,e.gy) for i in range(e.gx-e.range,e.gx+e.range+1)]
        dangerous=set(dangerous)
        return dangerous
    def _check(self, x:int, y:int, mapper:c.LostType):
        if mapper.invaild_coord(x,y):return False
        if mapper.mp[x][y]["type"] in ["wall","obstacle"]:
            return False
        if mapper.mp[x][y]["burning"]>0:return False
        for i in mapper.mp[x][y]["entity"]:
            if not i.walkInto(self) : return False
        return True
    def aiFindSafeGird(self, mapper:c.LostType): # 不知道ai运行效率如何
        dangerous=self._aiFindDangerousGird(mapper)
        # bfs
        q=queue.Queue()
        q.put([self.gx,self.gy,tuple()])
        dir=[(-1,0),(1,0),(0,-1),(0,1)]
        vis={}
        cnt=0
        while not q.empty():
            a=q.get()
            cnt+=1 # cnt 防止怪喜欢站着不动
            print(q.qsize(),(a[0],a[1]),{(a[0],a[1])} & dangerous!= {(a[0],a[1])})
            if {(a[0],a[1])} & dangerous != {(a[0],a[1])} and (cnt>1 or random.randrange(0,9)<9):
                self.movQ=[]
                t=a[2]
                while len(t)>0:
                    self.movQ.append((t[1],t[2]))
                    t=t[0][2]
                
                self.movQ=queue.deque(reversed(self.movQ))
                break
            random.shuffle(dir)
            for d in dir:
                nx,ny=a[0]+d[0],a[1]+d[1]
                if self._check(nx,ny,mapper) and not vis.get((nx,ny)):
                    vis[(nx,ny)]=True
                    b=[nx,ny,(a,d[0],d[1])]
                    q.put(b)
    def walk1step(self, mapper:c.LostType):
        dangerous=self._aiFindDangerousGird(mapper)
        dir=[(-1,0),(1,0),(0,-1),(0,1)]
        random.shuffle(dir)
        for d in dir:
            nx,ny=self.gx+d[0],self.gy+d[1]
            if self._check(nx,ny,mapper) and {(nx,ny)} & dangerous != {(nx,ny)}:
                self.movQ.append((d[0],d[1]))
                return True
        return False
        
    def walk(self, mapper:c.LostType):
        if self.moving>0:return
        if len(self.movQ)>0:
            dx,dy=self.movQ[0][0],self.movQ[0][1]
            if mapper.mp[self.gx+dx][self.gy+dy]["burning"]<=0:
                t=self.tryMove(dx,dy,mapper.moveRequest)
                if t==True:self.movQ.popleft()
                else : self.movQ=queue.deque() # 防止怪物卡死
                return
        self.aiWalkCount-=1
        if self.aiWalkCount==0:
            if not self.walk1step(mapper):
                self.aiFindSafeGird(mapper)
            self.aiWalkCount=c.FPS//4

    def ai(self, mapper:c.LostType):
        a=random.randrange(-1,10)
        if a<0:return
        if a<7 or len(self.movQ)>0:
            self.walk(mapper)
        else:
            self.aiBombCount-=1
            if self.aiBombCount==0:
                self.putBomb(mapper.addEntity)
                self.aiBombCount=c.FPS//2

        return
        match a:
            case 1:self.tryMove(-1,0,mapper.moveRequest)
            case 2:self.tryMove( 1,0,mapper.moveRequest)
            case 3:self.tryMove(0,-1,mapper.moveRequest)
            case 4:self.tryMove(0, 1,mapper.moveRequest)
            # case 5:self.putBomb(mapper.addEntity) # only for test

    def clock(self, moveUpdate:callable, mapper):
        return super().clock(moveUpdate)


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
