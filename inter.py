# 包含属于entity player monster等
# 因为这部分代码需要访问scene所以不在entity.py里
import asyncio
import pygame

import constants as c
from entity import *
from scene import *
#第一个全局变量
thisMap=Mapper(1,1)
dialoger=dialog()
class player(creature):
    money:int
    readToInteract:bool
    def keyboard(self, keys:pygame.key.ScancodeWrapper): # 捕捉键盘信息
        allowF=thisMap.moveRequest
        if c.alwaysAllow:allowF=lambda x,y,entity : True
        #python有for-else语句但没有 elfor 有什么让这段代码美观的方案吗？？
        for i in c.KeyboardLeft:
            if keys[i]: self.tryMove(-1,0,allowF);break
        else:
            for i in c.KeyboardRight:
                if keys[i]: self.tryMove(1,0,allowF);break
            else:
                for i in c.KeyboardUp:
                    if keys[i]: self.tryMove(0,-1,allowF);break
                else:
                    for i in c.KeyboardDown:
                        if keys[i]: self.tryMove(0,1,allowF);break

        # 外挂 加速 加炸弹 穿墙 获得金钱 加血 报告属性并崩溃
        if c.AllowCheat:
            for i in c.KeyboardSpeedUp:
                if keys[i]: self.speed += 1
            for i in c.KeyboardSpeedDown:
                if keys[i]: self.speed -= 1
            for i in c.KeyboardBombUp:
                if keys[i]:
                    self.bombRange += 1
                    self.bombSum += 1
            for i in c.KeyboardBombDown:
                if keys[i]:
                    self.bombRange -= 1
                    self.bombSum -= 1
            for i in c.KeyboardCrossWall:
                if keys[i]: c.alwaysAllow = not c.alwaysAllow
            for i in c.KeyboardMoneyUp:
                if keys[i]: self.money += 10
            for i in c.KeyboardMoneyDown:
                if keys[i]: self.money -= 10
            for i in c.KeyboardHealth:
                if keys[i]: self.hpPlus()
            for i in c.KeyboardCrash:
                if keys[i]:
                    print(f"speed:{self.speed},\r\nbombRange:{self.bombRange},\r\nbombSum:{self.bombSum},\r\nmoney:{self.money},\r\nhp:{self.hp}")
                    raise Exception("Crash")

        for i in c.KeyboardBomb:
            if keys[i]:self.putBomb(thisMap.addEntity);break
    def reRegister(self, gx:int, gy:int, initInMap:Callable, force:bool=True):
        return super().reRegister(gx,gy,initInMap,force)
    def __init__(self, id:int, gx:int, gy:int, imagesdir:str, initInMap:Callable|None =None, speed:int=c.IntialSpeed, hp:int=c.IntialHp, layer:int=9):
        if initInMap==None : initInMap=thisMap.addEntity# player切换地图的时候不要忘了重新在地图注册
        assert initInMap is not None
        super().__init__(id,gx,gy,imagesdir,initInMap,speed,hp,layer)
        self.money=0
        self.cankick=False
        self.hp+=c.IntialPlayerHp-c.IntialHp

    def pickup(self, w:List[List[dict[str,Any]]]):#捡东西
        if w[self.gx][self.gy]["type"]=="object":
            match w[self.gx][self.gy]["content"]:
                case 0:print('???a empty object???')
                case 1:self.bombSum+=1
                case 2:self.hpPlus()
                case 3:self.speed=c.IncreasedSpeed
                case 4:self.bombRange+=1
                case 5:self.money+=1
                case 6:self.cankick=True
            w[self.gx][self.gy]["type"]="field"
            w[self.gx][self.gy]["render"]=None# Warning
    def clock(self, mapper:Mapper):
        self.pickup(mapper.mp)
        super().clock(mapper.moveUpdate)
        if mapper.mp[self.gx][self.gy].get("teleportTo") :
            tmp=mapper.mp[self.gx][self.gy]["content"]
            # 如果 content为-1必须按f交互才能切换
            if tmp!=-1 or tmp==-1 and self.readToInteract:
                changeMap(*mapper.mp[self.gx][self.gy]["teleportTo"])
        # print(self.readToInteract)
        if self.readToInteract and mapper.mp[self.gx][self.gy].get("interact") and dialoger.content==None: # 只有在没有绘制对话框时才可交互
            t=thisMap.mp[self.gx][self.gy]["interact"]
            if 'function'in str(type(t[0])) : dialoger(t[0](self,mapper),t[1])
            else : dialoger(*t)
    def overlap(self, other:entityLike):
        super().overlap(other)
        if (self.gx,self.gy)==(other.gx,other.gy):
            if "monster" in str(type(other)) :# 只有与monster接触时扣血
                self.hpMinus()
    def delete(self):
        super().delete()
        raise Exception("GAMEOVER")

maps:List[Mapper]=[]
def changeMap(mapid:int, gx:int, gy:int):
    global thisMap
    mee=thisMap.me
    thisMap.mp[thisMap.me.gx][thisMap.me.gy]["entity"].remove(mee)
    thisMap.me=None
    thisMap=maps[mapid]
    mee.reRegister(gx,gy,thisMap.addEntity)
    thisMap.me=mee
    changeMusic(mapid)
    # thisMapId = mapid  # 表示当前地图的id 用于changeMusic

def catchKeyboard(nowplayer:player, nowdialog:dialog): # 处理所有键盘输入的函数，集合player.keyboard() dialog.keyboard()
    keys = pygame.key.get_pressed()
    if nowdialog.content==None:
        nowplayer.keyboard(keys)
    for i in c.KeyboardInteract:
            if keys[i] : nowplayer.readToInteract=True;break
            else : nowplayer.readToInteract=False
    nowdialog.keyboard(keys)

def changeMusic(mapid):
    '''
    global thisMapId
    # 更换背景音乐
    # if mapid == 0:
    #     for i in range(0, len(backgroundMusic)):
    #         stop_music(backgroundMusic[i])
    #     play_music(backgroundMusic[1])
    # elif mapid == 1:
    #     for i in range(0, len(backgroundMusic)):
    #         stop_music(backgroundMusic[i])
    #     play_music(backgroundMusic[1])
    if mapid == 2:
        for i in range(0, len(backgroundMusic)):
            stop_music(backgroundMusic[i])
        play_music(backgroundMusic[2])
    if thisMapId == 2:
        for i in range(0, len(backgroundMusic)):
            stop_music(backgroundMusic[i])
        play_music(backgroundMusic[1])
    '''
    for i in range(0, len(backgroundMusic)):
            stop_music(backgroundMusic[i])
    play_music(backgroundMusic[mapid+1])

def play_music(music:pygame.mixer.Sound):
    music.play(-1)

def stop_music(music:pygame.mixer.Sound, time=1000):
    music.fadeout(time)

def play_sound(sound:pygame.mixer.Sound):
    sound.play(1)

"""
音乐及音效定义

直接在此处加入即可
"""
pygame.mixer.init()
backgroundMusic = [
    pygame.mixer.Sound('./assets/music/Home_Screen.ogg'),
    pygame.mixer.Sound('./assets/music/Queen-Gardens.flac'),
    pygame.mixer.Sound('./assets/music/outside.ogg'),
    pygame.mixer.Sound('./assets/music/shop.ogg'),
    pygame.mixer.Sound('./assets/music/City-of-Tears.flac')
]
backgroundSound = []


