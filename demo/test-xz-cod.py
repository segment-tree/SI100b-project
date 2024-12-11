import pygame
import sys
import numpy as np

#refer https://www.cnblogs.com/BigShuang/p/17683261.html

#https://blog.csdn.net/goxingman/article/details/103695979

C, R = 15, 15  # 11列， 20行
CELL_SIZE = 45  # 格子尺寸 !Better even number

FPS=40  # 游戏帧率
WIN_WIDTH = CELL_SIZE * C  # 窗口宽度
WIN_HEIGHT = CELL_SIZE * R  # 窗口高度
back_ground_color = (200, 200, 200)
obstacle_color =  (139, 69, 19)
me_color = (50, 50, 50)
mp=np.array([[0]*(R+1)]*(C+1))
obstacle_locations=[(2,1),(2,2),(2,3),(3,1),(5,5),(6,5),(7,5),(8,5),(8,6),(8,7),(8,8),(8,9),(8,10)]

class Block(pygame.sprite.Sprite):
    def __init__(self, c, r, color, mod=0):
        super().__init__()

        self.cr = [c, r]
        self.x = c * CELL_SIZE
        self.y = r * CELL_SIZE
        if mod==0 :
            self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
            self.image.fill(color)
        elif mod==1 :
            self.image = pygame.image.load(color)
        # so color is either tuple or string , it's not typesafe ,may need to change that in formal version 

        self.rect = self.image.get_rect()
        self.rect.move_ip(self.x, self.y)
    def resetxy(self, x, y):
        self.cr[0] = x
        self.cr[1] = y
        self.x = x * CELL_SIZE
        self.y = y * CELL_SIZE
        self.rect.left = self.x
        self.rect.top = self.y

dirs={'':(0,0),'lr':(0,0),'l':(-1,0),'r':(1,0)}#,'u':(0,-1),'d':(0,1)}
gravy=1#重力加速度
horizontal_a=2
initial_velocity=10#跳跃初速度
delta_velocity=3
max_speed=40
lock=0#锁键，在刚刚起跳的瞬间禁止横向移动
jumpcnt=0#让短按跳跃键与长按跳跃键有区别
class Character(pygame.sprite.Sprite):
    def __init__(self,x,y,image,height=CELL_SIZE,width=CELL_SIZE,speedratio=18):
        self.x,self.y=x,y
        self.height,self.width=height,width
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.x-width//2, self.y-height//2)
        self.speedratio=speedratio # 水平移速
        self.upv=0 #竖直方向速度
        self.onwall=False #是否贴墙
        self.onground=False #是否在地上
        # self.jump_num=0#二段跳次数
        self.horizontal_mov=0#爬墙跳
    
    def resetxy(self,x,y):
        self.x,self.y = x,y
        self.rect.left = self.x-self.width//2
        self.rect.top = self.y-self.height//2
        #self.rect.move_ip(self.y-self.height//2, self.x-self.width//2)
    
    def move(self, dir=''):
        move_x, move_y = dirs[dir]

        next_x = self.x + (move_x)*self.speedratio+self.horizontal_mov
        next_y = self.y - self.upv + move_y*self.speedratio
        self.upv-=gravy
        if(self.horizontal_mov>0):self.horizontal_mov-=horizontal_a
        if(self.horizontal_mov<0):self.horizontal_mov+=horizontal_a
        if(abs(self.upv)>max_speed):
            if self.upv>0 : self.upv=max_speed
            else : self.upv=-max_speed

        epsx=5
        epsy=5
        xm=next_x//CELL_SIZE
        x1=(next_x-self.width//2+epsx)//CELL_SIZE
        x2=(next_x+self.width//2-epsx)//CELL_SIZE
        ym=next_y//CELL_SIZE
        y1=(next_y-self.height//2+epsy)//CELL_SIZE
        y2=(next_y+self.height//2-epsy)//CELL_SIZE

        self.onground = (y2>=R or mp[xm][y2]==-1)
        self.onleftwall = (x1<0 or mp[x1][ym]==-1)
        self.onrightwall= (x2 >= C or mp[x2][ym]==-1)
        onsky= (y1<0 or mp[xm][y1]==-1)

        # if self.onground or self.onwall : self.jump_num=1 #刷新二段跳

        if 0 <= x1 < C and 0 <= x2 < C and 0 <= y1 < R and 0 <= y2 < R and mp[x1][y1]!=-1 and mp[x1][y2]!=-1 and mp[x2][y1]!=-1 and mp[x2][y2]!=-1:
            self.resetxy(next_x,next_y)
            #print(dir,self.cr[0],self.cr[1],'#',next_r,next_c)
            return True
        self.upv=0
        self.horizontal_mov=0
        global jumpcnt
        jumpcnt=0#顶头重置大跳（长按跳）
        return False
        '''
        flag=False
        if not self.onwall:
            flag=True
            self.resetxy(next_x,self.y)
        if not onsky and not self.onground:
            flag=True
            self.resetxy(self.x,next_y)
        if not flag : self.upv=0
        '''
myblock = Character(CELL_SIZE//2, CELL_SIZE//2, './assets/sb_big.png',36,50)

def draw():
    # global meX
    # global meY
    global myblock
    #test()
    win.fill(back_ground_color)
    for i in range(C):
        for j in range(R):
            if(mp[i][j]==-1):
                block_obstacle=Block(i,j,obstacle_color)
                win.blit(block_obstacle.image, block_obstacle.rect)
    #myblock = Block(meX, meY, me_color)
    win.blit(myblock.image, myblock.rect)

def move_me():
    s=''
    global jumpcnt,lock
    print(lock)
    #if event.type == pygame.KEYDOWN or event.type == pygame.TEXTINPUT:
    #print(pygame.key.get_pressed(),type(pygame.key.get_pressed()))
    keys = pygame.key.get_pressed()
    if lock==0 and (keys[pygame.K_LEFT] or keys[ord('a')] or keys[ord('k')]):
        #lock=2
        s+='l'
    if lock==0 and (keys[pygame.K_RIGHT] or keys[ord('d')] or keys[ord(';')]):
        #lock=2
        s+='r'
    if keys[pygame.K_SPACE] or keys[ord('z')]:#jump
        if jumpcnt>0 :
            myblock.upv+=delta_velocity
        else:
            if myblock.onground :
                jumpcnt=8
                lock=6
                myblock.upv=initial_velocity
                #if not myblock.onground and not myblock.onwall:
                #    myblock.jump_num-=1
            if myblock.onleftwall :
                jumpcnt=8
                lock=6
                myblock.upv=initial_velocity
                myblock.horizontal_mov=24
            if myblock.onrightwall :
                jumpcnt=8
                lock=6
                myblock.upv=initial_velocity
                myblock.horizontal_mov=-24

    if jumpcnt>0 : jumpcnt-=1
    if lock >0 : lock-=1

    myblock.move(s)


pygame.init() # pygame初始化，必须有，且必须在开头



for i in obstacle_locations:
    mp[i[0]][i[1]]=-1



# 创建主窗体
clock = pygame.time.Clock() # 用于控制循环刷新频率的对象
win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))


draw()
while True:
    clock.tick(FPS) # 控制循环刷新频率,每秒刷新FPS对应的值的次数
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 判断当前事件是否为点击右上角退出键
            pygame.quit()
            sys.exit() # 需要提前 import sys
    move_me()
    draw()
    #print(0)
    pygame.display.update()