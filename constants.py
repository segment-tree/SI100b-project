# 常量用大驼峰命名法吧
CellSize=42
FPS=30
WinHeight=10 # 这里表示格子数，而非像素数
WinWidth=14
IntialSpeed=3 # 所有entity的速度初值
ImmuneFrame=4 # 受击后无敌帧数
WalkingFpsLoop=8 # 走路完整完成一步的帧数
# 用fpscnt（帧数总计数器）mod WalkingFpsLoop 得出要渲染哪一帧