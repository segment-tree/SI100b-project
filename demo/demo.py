import pygame
import sys
import numpy as np
import os
from enum import Enum

WINDOWSRATIO = 2
if os.name=='posix':
    WINDOWSRATIO = 1
C, R = 15, 15  # C列，R行
CELL_SIZE = 88//WINDOWSRATIO  # 格子尺寸 !Better even number
WIN_WIDTH = CELL_SIZE * C  # 窗口宽度
WIN_HEIGHT = CELL_SIZE * R  # 窗口高度
FPS = 30 # 实际帧数
logicFPS = 8 # 逻辑上一帧对应的实际帧数
BOMB_BOOM_count = 6 # 炸弹起爆时间
BURNING_time = 3 # 爆炸持续时间
class gridTP(Enum):
    Field    = 1
    Bomb     = 2
    Burn     = 3
    Obstacle = 4
    Wall     = 5
    Object   = 6

class MAP:
    def __init__(self,N,M,ttt=gridTP.Field):
        self.N=N
        self.M=M
        self.types =[[ttt for i in range(M+1)] for j in range(N+1)]
        self.values=[[0   for i in range(M+1)] for j in range(N+1)]
        self.render=[[0   for i in range(M+1)] for j in range(N+1)]
        # values存:
        #   Field: undefined
        #   Bomb:[起爆时间,起爆范围,bomb_author(实现类似于指针)]
        #   Burn:[起爆时间,(last_types,last_values)]
        #   Obstacle: content?
        #   Wall: undeifined
        #   Object: content?
        #  content? 0:空的 other:道具 1:炸弹数+1
    def invaild_coord(self,x,y):
        return x<0 or x >= self.N or y<0 or y >= self.M
    def reachable(self,x,y):
        if self.invaild_coord(x,y):
            return False
        return self.types[x][y]==gridTP.Field or self.types[x][y]==gridTP.Object \
            or self.types[x][y]==gridTP.Burn
    def clock(self):
        acts=[]
        for i in range(self.N):
            for j in range(self.M):
                if(self.types[i][j]==gridTP.Bomb):
                    self.values[i][j][0]-=1
                    if self.values[i][j][0]==0:
                        self.types[i][j]=gridTP.Field
                        self.values[i][j][2].bomb_num+=1 # release bomb_num
                        acts.append([gridTP.Bomb,i,j,self.values[i][j][1]]) # append起爆信息
                if(self.types[i][j]==gridTP.Burn):
                    self.values[i][j][0]-=1
                    if self.values[i][j][0]==0: # 爆炸判定解除
                        self.types[i][j]=self.values[i][j][1][0] #  v
                        self.values[i][j]=self.values[i][j][1][1]# grid改为爆炸前的样子
        for i in acts:
            if i[0]==gridTP.Bomb:
                xx,yy,stp=i[1],i[2],i[3]
                def __set(x,y):
                    if(self.invaild_coord(x,y)):return False
                    if(self.reachable(x,y)):
                        if(self.types[x][y]!=gridTP.Burn):# 防止多次burn造成嵌套
                            self.values[x][y]=[3,(self.types[x][y],self.values[x][y])]# 暂存，防止炸弹炸毁掉落物
                        else: self.values[x][y][0]=BURNING_time
                        self.types[x][y]=gridTP.Burn
                        return True
                    if(self.types[x][y]==gridTP.Bomb):# 碰到炸弹，直接跳过，或者更好的是引爆碰到的炸弹，但是暂时懒得写了
                        return True # do nothing and return True
                    if(self.types[x][y]==gridTP.Obstacle):
                        self.types[x][y]=gridTP.Burn
                        if(self.values[x][y]!=0):
                            self.values[x][y]=[3,(gridTP.Object,self.values[x][y])]# 暂存，防止炸弹炸毁掉落物
                        else: self.values[x][y]=[3,(gridTP.Field,self.values[x][y])]
                    return False
                
                for _x in range(xx,xx+stp+1):
                    if not __set(_x,yy):break
                for _x in reversed(range(xx-stp,xx+1)):
                    if not __set(_x,yy):break
                for _y in range(yy,yy+stp+1):
                    if not __set(xx,_y):break
                for _y in reversed(range(yy-stp,yy+1)):
                    if not __set(xx,_y):break

                        

thismap=MAP(20,20)

for i in range(10):
    thismap.types[5][i]=gridTP.Obstacle
    thismap.render[5][i]=i
    if(i%2==0):thismap.values[5][i]=1

for i in range(10):
    thismap.types[i][10]=gridTP.Wall

pass


dirs={'l':(0,-1),'r':(0,1),'u':(-1,0),'d':(1,0),'!':(0,0)}
def mksum(dirs,keys):
    t=[dirs[i] for i in keys.keys()]
    _1,_2=0,0
    for i in t:
        _1+=i[0]
        _2+=i[1]
    return (_1,_2)
class Chara:
    def __init__(self,x,y,hp=1):
        self.x,self.y=x,y
        # self.dx=self.dy=0 # used for smooth move
        self.pack={}
        self.bomb_num=1
        self.hp=hp
        self.bomb_damage=3 # 起爆范围
    def move_check(self,keys): # 渲染时使用
        dx,dy=mksum(dirs,keys)
        if thismap.reachable(self.x+dx,self.y+dy):
            return (dx,dy,True)
        return (0,0,False)
    def move(self,keys):
        if keys.get('!') and self.bomb_num>0 and\
          not thismap.types[self.x][self.y]==gridTP.Bomb: # put BOMB
            self.bomb_num-=1
            thismap.types[self.x][self.y]=gridTP.Bomb
            thismap.values[self.x][self.y]=[BOMB_BOOM_count,self.bomb_damage,self] # 

        dx,dy = mksum(dirs,keys)
        nx = self.x + dx
        ny = self.y + dy
        flag=False
        if thismap.reachable(nx,ny):
            self.x,self.y=nx,ny
            flag=True
        else: dx=dy=0
        if thismap.types[self.x][self.y]==gridTP.Object:
            thismap.types[self.x][self.y]=gridTP.Field
            if thismap.values[self.x][self.y]==1:
                print('bomb num increased')##
                self.bomb_num+=1
            #if thismap.values[self.x][self.y]==2:
            thismap.values[self.x][self.y]=0
            pass
        if thismap.types[self.x][self.y]==gridTP.Burn: # 伤害判定
            print("HURT!!!")
            pass
        return flag

me=Chara(1,1)

monsters=[]


# x行 y列
def action(keys):
    me.move(keys)
    #print(keys,me.x,me.y)##
    for i in monsters:
        pass
    thismap.clock()
    '''
    for i in range(thismap.N):
        for j in range(thismap.M):
            if(thismap.types[i][j]==gridTP.Bomb):print(i,j)##
    '''

def draw(win,cnt,dx,dy,waste_fps):
    speedratio=logicFPS-waste_fps
    back_ground_color=(200, 200, 200)
    wall_color =  (139, 69, 19)
    obstacle_color = (50, 50, 50)
    burn_color=(255,192,203)
    bomb_color=(0,0,0)
    object_color=(255,215,0)
    win.fill(back_ground_color)

    for i in range(thismap.N):
        for j in range(thismap.M):
            imagebg=pygame.image.load('./assets/Field0.png')
            imagebg=pygame.transform.scale(imagebg,(CELL_SIZE,CELL_SIZE))
            image=pygame.Surface((CELL_SIZE, CELL_SIZE))
            match thismap.types[i][j]:
                case gridTP.Field:
                    image=pygame.Surface((0, 0))
                case gridTP.Burn:
                    image.fill(burn_color)
                case gridTP.Bomb:
                    image=pygame.image.load('./assets/Bomb0.png')
                    image=pygame.transform.scale(image,(CELL_SIZE,CELL_SIZE))
                case gridTP.Obstacle:
                    image=pygame.image.load(f'./assets/Obstacle0.{thismap.render[i][j]}.png')
                    image=pygame.transform.scale(image,(CELL_SIZE,CELL_SIZE))
                case gridTP.Wall:
                    #image.fill(wall_color)
                    image=pygame.image.load('./assets/Wall0.png')
                    image=pygame.transform.scale(image,(CELL_SIZE,CELL_SIZE))
                case gridTP.Object:
                    image.fill(object_color)
            rectbg = imagebg.get_rect()
            rect = image.get_rect()
            rectbg.move_ip(j*CELL_SIZE,i*CELL_SIZE)
            rect.move_ip(j*CELL_SIZE,i*CELL_SIZE)
            win.blit(imagebg,rectbg)
            win.blit(image,rect)
    
    myimage=pygame.image.load('./assets/sb_big.png')
    myimage=pygame.transform.scale(myimage,(CELL_SIZE,CELL_SIZE))
    myrect=myimage.get_rect()
    myrect.move_ip(me.y*CELL_SIZE+dy*(cnt-waste_fps)*CELL_SIZE//speedratio,\
                   me.x*CELL_SIZE+dx*(cnt-waste_fps)*CELL_SIZE//speedratio)
    win.blit(myimage,myrect)

    pygame.display.update()
            


def loop():
    # 创建主窗体
    clock = pygame.time.Clock() # 用于控制循环刷新频率的对象
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    cnt=0
    dic={}
    nxtdic={}
    flag=0
    dx,dy=0,0
    while(True):
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        cnt+=1
        keys = pygame.key.get_pressed()
        if flag==0:
            if keys[pygame.K_LEFT] or keys[ord('a')]:
                dic['l']=True
            elif keys[pygame.K_RIGHT] or keys[ord('d')]:
                dic['r']=True
            elif keys[pygame.K_UP] or keys[ord('w')]:
                dic['u']=True
            elif keys[pygame.K_DOWN] or keys[ord('s')]:
                dic['d']=True
        '''
        elif len(nxtdic)==0 :# optional
            if keys[pygame.K_LEFT] or keys[ord('a')]:
                if dic.get('u') or dic.get('d'):nxtdic['l']=True
            elif keys[pygame.K_RIGHT] or keys[ord('d')]:
                if dic.get('u') or dic.get('d'):nxtdic['r']=True
            elif keys[pygame.K_UP] or keys[ord('w')]:
                if dic.get('l') or dic.get('r'):nxtdic['u']=True
            elif keys[pygame.K_DOWN] or keys[ord('s')]:
                if dic.get('l') or dic.get('r'):nxtdic['d']=True
        '''
        if keys[pygame.K_SPACE]:
            dic['!']=True
        
        if(len(dic)!=0 and flag==0):
            dx,dy,_=me.move_check(dic)
            flag=cnt
        if(cnt==logicFPS):
            action(dic)
            cnt=0
            dic=nxtdic
            nxtdic={}
            flag= 0 if len(dic)==0 else 1
            dx,dy=0,0
        #print(flag,'$')##
        draw(win,cnt,dx,dy,flag)
        
        
pygame.init() # pygame初始化，必须有，且必须在开头

loop()
