import pygame
# 常量用大驼峰命名法吧
CellSize=42*2 # 不要修改CellSize，请修改CellRatio
CellRatio=2
# 为了让不同分辨率下小人移速等一样，故设CellRatio，仅在渲染时放缩，逻辑不受影响
# 2k分辨率时CellRatio为1，1k为2，（但这样就不支持4k屏了）
# 尽量不要在imageclass.py外的地方访问CellRatio
FPS=20
WinHeight=10 # 这里表示格子数，而非像素数
WinWidth=14
IntialSpeed=8 # 所有entity的速度初值
IncreasedSpeed=14 # 小人吃到加速道具后的速度
IntialBombRange=2 # 所有creature的炸弹的初始爆炸范围
IntialHp=2
ImmuneFrame=15 # 受击后无敌帧数
WalkingFpsLoop=8 # 走路完整完成一步的帧数
# 用fpscnt（帧数总计数器）mod WalkingFpsLoop 得出要渲染哪一帧

BombCount=int(FPS*2.25) # 炸弹💥倒计时

#键盘：
KeyboardLeft =[pygame.K_LEFT,ord('a')]
KeyboardRight=[pygame.K_RIGHT,ord('d')]
KeyboardUp   =[pygame.K_UP,ord('w')]
KeyboardDown =[pygame.K_DOWN,ord('s')]
KeyboardBomb =[pygame.K_SPACE]