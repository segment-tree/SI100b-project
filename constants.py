import pygame
import os
# 常量用大驼峰命名法吧
Difficulty=1
AIdecisionEnbled=False
LLMavailability=True
AllowCheat=True
AllowTranslucence=True # 允许在有遮挡时进行半透明绘制
BottomBarMode=2 
# ==0 不渲染血量
# ==1 在BottomBar渲染血量
# ==2 在左上角渲染血量

if LLMavailability==False:
    AIdecisionEnbled=False

CellSize=42*2 # 不要修改CellSize，请修改CellRatio
CellRatio=2
# 为了让不同分辨率下小人移速等一样，故设CellRatio，仅在渲染时放缩，逻辑不受影响
# 2k分辨率时CellRatio为1，1k为2，（但这样就不支持4k屏了）
FPS=20
WinHeight=10 # 这里表示格子数，而非像素数
WinWidth=14
IntialSpeed=8 # 所有entity的速度初值
IncreasedSpeed=14 # 小人吃到加速道具后的速度
BombKickedSpeed=5*IntialSpeed
IntialBombRange=1 # 所有creature的炸弹的初始爆炸范围
IntialHp=2 +Difficulty//2 # 初始血量（除player生物（怪物）的血量）
IntialPlayerHp=5 # player血量
ImmuneFrame=int(FPS*2) # 受击后无敌帧数
WalkingFpsLoop=8 # 走路完整完成一步的帧数
# 用fpscnt（帧数总计数器）mod WalkingFpsLoop 得出要渲染哪一帧

BombCount=int(FPS*2.50) # 炸弹💥倒计时
BurnCount=int(FPS*0.30)  # 受爆炸影响时间

# MonsterSight=5 # 怪物视野
MonsterBombDis=6 # 怪物与玩家曼哈顿距离小于此数时怪物才会扔炸弹
#键盘：
KeyboardLeft =[pygame.K_LEFT,ord('a')]
KeyboardRight=[pygame.K_RIGHT,ord('d')]
KeyboardUp   =[pygame.K_UP,ord('w')]
KeyboardDown =[pygame.K_DOWN,ord('s')]
KeyboardBomb =[pygame.K_SPACE]
KeyboardInteract =[ord('f')]
KeyboardEscDialog=pygame.K_ESCAPE
KeyboardConDialog=pygame.K_RETURN

# 外挂用
KeyboardSpeedUp = [pygame.K_z,ord('z')]
KeyboardSpeedDown = [pygame.K_x,ord('x')]
KeyboardBombUp = [pygame.K_c,ord('c')]
KeyboardBombDown = [pygame.K_v,ord('v')]
KeyboardCrossWall = [pygame.K_BACKSPACE]
KeyboardMoneyUp = [pygame.K_n,ord('n')]
KeyboardMoneyDown = [pygame.K_m,ord('m')]
KeyboardHealth = [pygame.K_b,ord('b')]
KeyboardCrash = [pygame.K_SCROLLOCK]
# 穿墙外挂用
alwaysAllow = False


DefaultFont='华文楷体'
if os.name=='posix':
    DefaultFont = 'source-han-sans' # linux系统大概率没有华文楷体，故选此替代

BossDefaultCount=FPS*10 # boss每个招式的持续时间

from typing import *
LostType=Any