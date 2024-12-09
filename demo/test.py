import pygame
import sys
import numpy as np

#refer https://www.cnblogs.com/BigShuang/p/17683261.html

C, R = 15, 15  # 11列， 20行
CELL_SIZE = 90  # 格子尺寸 !Better even number

FPS=20  # 游戏帧率
WIN_WIDTH = CELL_SIZE * C  # 窗口宽度
WIN_HEIGHT = CELL_SIZE * R  # 窗口高度
back_ground_color = (200, 200, 200)
obstacle_color =  (139, 69, 19)
me_color = (50, 50, 50)
mp=np.array([[0]*(C+1)]*(R+1))
obstacle_locations=[(1,1),(1,2),(1,3),(2,1),(5,5),(6,5),(7,5),(8,5),(8,6),(8,7),(7,7),(6,7)]


# https://blog.csdn.net/summerriver1/article/details/125215461

dirs={'l':(0,-1),'r':(0,1),'u':(-1,0),'d':(1,0)}
class Block(pygame.sprite.Sprite):
    def __init__(self, r, c, color, mod=0):
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
    def move_rc(self, r, c):
        self.cr[0] = c
        self.cr[1] = r
        self.x = c * CELL_SIZE
        self.y = r * CELL_SIZE
        self.rect.left = self.x
        self.rect.top = self.y
    def move(self, dir=''):
        move_r, move_c = dirs[dir]

        next_c = self.cr[0] + move_c
        next_r = self.cr[1] + move_r


        print(dir,self.cr[0],self.cr[1],move_c,move_r)

        if 0 <= next_c < C and 0 <= next_r < R and mp[next_r][next_c]!=-1 :
            self.move_rc(next_r,next_c)
            #print(dir,self.cr[0],self.cr[1],'#',next_r,next_c)
            return True
        return False

class Character(pygame.sprite.Sprite):
    def __init__(self,x,y,image,height=CELL_SIZE,width=CELL_SIZE,speedratio=12):
        self.x,self.y=x,y
        self.height,self.width=height,width
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.y-width//2, self.x-height//2)
        self.speedratio=speedratio
    
    def resetxy(self,x,y):
        self.x,self.y = x,y
        self.rect.left = self.y-self.width//2
        self.rect.top = self.x-self.height//2
        #self.rect.move_ip(self.y-self.height//2, self.x-self.width//2)
    
    def move(self, dir=''):
        move_x, move_y = dirs[dir]

        next_x = self.x + move_x*self.speedratio
        next_y = self.y + move_y*self.speedratio


        print(next_x,next_y,move_x,move_y)

        epsx=5
        epsy=5
        x1=(next_x-self.height//2+epsx)//CELL_SIZE
        x2=(next_x+self.height//2-epsx)//CELL_SIZE
        y1=(next_y-self.width//2+epsy)//CELL_SIZE
        y2=(next_y+self.width//2-epsy)//CELL_SIZE

        if 0 <= x1 < R and 0 <= x1 < R and 0 <= y1 < C and 0 <= y2 < C and mp[x1][y1]!=-1 and mp[x1][y2]!=-1 and mp[x2][y1]!=-1 and mp[x2][y2]!=-1:
            self.resetxy(next_x,next_y)
            #print(dir,self.cr[0],self.cr[1],'#',next_r,next_c)
            return True
        return False


#meX=0
#meY=0
# myblock = Block(0, 0, 'sb_big.png',1)
myblock = Character(CELL_SIZE//2, CELL_SIZE//2, 'sb_big.png',70,98)

def draw():
    # global meX
    # global meY
    global myblock
    #test()
    win.fill(back_ground_color)
    for i in range(R):
        for j in range(C):
            if(mp[i][j]==-1):
                block_obstacle=Block(i,j,obstacle_color)
                win.blit(block_obstacle.image, block_obstacle.rect)
    #myblock = Block(meX, meY, me_color)
    win.blit(myblock.image, myblock.rect)

def move_me():
    if event.type == pygame.KEYDOWN:
        #print(event.key)
        if event.key == pygame.K_LEFT or event.key == ord('a'):
            myblock.move("l")
        if event.key == pygame.K_RIGHT or event.key == ord('d'):
            myblock.move("r")
        if event.key == pygame.K_UP or event.key == ord('w'):
            myblock.move("u")
        if event.key == pygame.K_DOWN or event.key == ord('s'):
            myblock.move("d")

def test():
    test_img=pygame.image.load('0.png').convert()
    win.blit(test_img, (10,10))

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