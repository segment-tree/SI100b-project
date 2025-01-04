import pygame
from typing import *
import constants as c
class myImage:
    image:pygame.Surface
    rect:Any
    mode:int
    # mode==0:以当前格子左下为基准绘制
    # mode==1:以当前格子中心为基准绘制
    def __init__(self,imgdir,zoom=1,mode=0):
        self.image=pygame.image.load(imgdir)
        rect_t=self.image.get_rect()
        h=(rect_t.height*c.CellSize*zoom//rect_t.width)//c.CellRatio
        self.image=pygame.transform.scale(self.image,(int(c.CellSize*zoom)//c.CellRatio,h))
        self.rect=self.image.get_rect()
        self.mode=mode

    def reload(self,imgdir):
        self.__init__(imgdir)
    def draw(self,rx:int,ry:int,camera:Tuple[int,int],win):
        self.rect=self.image.get_rect()
        match self.mode:
            case 0:
                self.rect.move_ip(
                    ( rx-c.CellSize//2 -camera[0] )//c.CellRatio,
                    ( ry+c.CellSize//2-self.rect.height*c.CellRatio -camera[1] )//c.CellRatio
                )
            case 1:
                self.rect.move_ip(
                    ( rx-self.rect.width *c.CellRatio//2 -camera[0] )//c.CellRatio,
                    ( ry-self.rect.height*c.CellRatio//2 -camera[1] )//c.CellRatio
                )
        win.blit(self.image,self.rect)
    def drawG(self,gx:int,gy:int,camera:Tuple[int,int],win): # 按网格坐标渲染
        self.rect=self.image.get_rect()
        match self.mode:
            case 0:
                self.rect.move_ip(
                    ( gx*c.CellSize -camera[0] )//c.CellRatio,
                    ( (gy+1)*c.CellSize-self.rect.height*c.CellRatio -camera[1] )//c.CellRatio
                )
            case 1:
                self.rect.move_ip(
                    ( gx*c.CellSize+c.CellSize//2-self.rect.width *c.CellRatio//2 -2 -camera[0] )//c.CellRatio,
                    ( gy*c.CellSize+c.CellSize//2-self.rect.height*c.CellRatio//2 -2 -camera[1] )//c.CellRatio
                )
        win.blit(self.image,self.rect)

class dialog:
    content:str|None
    funclist:Any #
    usellm:bool
    inputs:str # llm的用户输入暂存在此
    
    keysleepcnt:int
    def __init__(self):
        self.content=None
        self.usellm=False
        self.keysleepcnt=c.FPS//2
        self.inputs=">"
    def __call__(self, funclist, usellm:bool):
        self.funclist=funclist;self.usellm=usellm
        self.content=next(self.funclist)
        self.keysleepcnt=c.FPS//2
    # dialog的keyboard
    # 1.用于捕获用户输入(llm)，
    # 2.在用户输入c.KeyboardConDialog时调用包含协程的funclist,切换下一条对话
    #    funclist参考makescene.py中mapGenerTown的子函数
    # 3.在用户输入c.KeyboardEscDialog时退出对话框
    def keyboard(self,keys:pygame.key.ScancodeWrapper):
        if self.content==None:return
        # 检查键盘输入，用于llm，如果有的话
        self.keysleepcnt-=1
        if self.usellm and self.keysleepcnt<=0: 
            for i in list(range(ord('a'),ord('z')+1))+[ord(' '),pygame.K_BACKSPACE]:
                flag=False
                if keys[i]:
                    flag=True
                    if i!=pygame.K_BACKSPACE:self.inputs+=chr(i)
                    elif len(self.inputs)>1:self.inputs=self.inputs[:-1]
                if flag:self.keysleepcnt=c.FPS//6
        '''
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.TEXTINPUT or event.type == pygame.KEYDOWN:
                for i in range(ord('a'),ord('z')+1):
                    if keys[i]:self.inputs+=chr(i)
        '''
        if self.keysleepcnt<=0 and keys[c.KeyboardConDialog]:
            try:
                self.content=self.funclist.send(self.inputs)
                self.inputs=">"
                # self.content=next(self.funclist)
                # 在存在llm的时候send self.inputs让py中mapGenerTown的子函数接受
            except StopIteration:
                self.content=None
                self.funclist=None
            self.keysleepcnt=c.FPS//2
        if self.keysleepcnt<=0 and keys[c.KeyboardEscDialog]:
            self.content=None
            self.funclist=None
        # print(self.inputs)
    # 画对话框，以及对话中的内容，以及还没按c.KeyboardConDialog发送的input
    def draw(self,win):
        if self.content==None:return
        image=pygame.image.load('./assets/utils/dialog.png')
        rect_t=image.get_rect()
        w=c.WinWidth*c.CellSize-c.CellSize
        h=rect_t.height*w//rect_t.width
        image=pygame.transform.scale(image,(w//c.CellRatio,h//c.CellRatio))
        rect=image.get_rect()
        rect.move_ip(int((c.WinWidth-13.5)*c.CellSize/c.CellRatio),int((c.WinHeight-4.5)*c.CellSize/c.CellRatio))
        win.blit(image,rect)

        font = pygame.font.SysFont(c.DefaultFont, 32//c.CellRatio)
        #font.set_bold(True)
        temp_Content = self.content#文字分行渲染
        text_Line = []
        cnt = 1
        while(cnt*30<len(temp_Content)):
            text_Line.append(temp_Content[(cnt-1)*30:cnt*30])
            cnt += 1
        text_Line.append(temp_Content[(cnt-1)*30:])

        surfaces = [font.render(line, True, (0, 0, 0)) for line in text_Line]
        for i in range(1,cnt+1):
            win.blit(surfaces[i-1], (int((c.WinWidth-12.5)*c.CellSize/c.CellRatio),int((c.WinHeight-4+i*0.5-0.25)*c.CellSize/c.CellRatio)))
        
        if self.usellm:self.draw_Input(win)


    def draw_Input(self, win):
        if self.inputs==None:return
        font = pygame.font.SysFont(c.DefaultFont, 32//c.CellRatio)
        #font.set_bold(True)
        temp_Inputs = self.inputs + "_"#文字分行渲染
        text_Line = []
        cnt = 1
        while(cnt*30<len(temp_Inputs)):
            text_Line.append(temp_Inputs[(cnt-1)*30:cnt*30])
            cnt += 1
        text_Line.append(temp_Inputs[(cnt-1)*30:])

        surfaces = [font.render(line, True, (0, 0, 0)) for line in text_Line]
        for i in range(1,cnt+1):
            win.blit(surfaces[i-1], (int((c.WinWidth-12.5)*c.CellSize/c.CellRatio),int((c.WinHeight-2+i*0.5)*c.CellSize/c.CellRatio)))
class segmentDraw:
    # 在网格边界画线的class
    @classmethod
    def drawR(self, gx:int, gy:int, length:int, camera:Tuple[int,int], win):
        color = (255,0,0)
        segment=pygame.Surface((c.CellSize*length//c.CellRatio, c.CellSize//10//c.CellRatio))
        segment.fill(color)
        rect = segment.get_rect()
        rect.move_ip((gx*c.CellSize-camera[0])//c.CellRatio,(gy*c.CellSize-camera[1])//c.CellRatio)
        win.blit(segment,rect)
    @classmethod
    def drawC(self, gx:int, gy:int, length:int, camera:Tuple[int,int], win):
        color = (255,0,0)
        segment=pygame.Surface((c.CellSize//10//c.CellRatio, c.CellSize*length//c.CellRatio))
        segment.fill(color)
        rect = segment.get_rect()
        rect.move_ip((gx*c.CellSize-camera[0])//c.CellRatio,(gy*c.CellSize-camera[1])//c.CellRatio)
        win.blit(segment,rect)
    @classmethod
    def drawSqure(self,gx,gy,width,height,camera,win):
        self.drawR(gx,gy,width,camera,win)
        self.drawR(gx,gy+height,width,camera,win)
        self.drawC(gx,gy,height,camera,win)
        self.drawC(gx+width,gy ,height,camera,win)


# 创建窗口
def displayCreateWin():
    if pygame.display.Info().current_w >= 2000:
        c.CellRatio=1
    win = pygame.display.set_mode((c.WinWidth*c.CellSize//c.CellRatio,c.WinHeight*c.CellSize//c.CellRatio))
    return win

#test
import sys
from nine_ai import *
if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock() # 用于控制循环刷新频率的对象
    win = pygame.display.set_mode((c.WinWidth*c.CellSize,c.WinHeight*c.CellSize))
    def nineNineCat():
        c=nine('')
        while True:
            t = yield c 
            c= nine(str(t))
            # if t == None:
            #     break
        yield None
    aaa=dialog()
    aaa(nineNineCat(),True)
    while True:
        clock.tick(c.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # tree=myImage('./assets/t/54px-Pine_Stage_4.png')
        # tree.drawG(1,0,win)
        # tree.draw(c.CellSize//2,c.CellSize+c.CellSize//2,(0,0),win)
        
        aaa.keyboard(pygame.key.get_pressed())
        aaa.draw(win)

        pygame.display.update()
        # print(tree.rect)

