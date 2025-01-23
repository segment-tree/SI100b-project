from entity import *
from scene import *
from nine_ai import *
from shopowner_ai import (shop)
import random

def tempMapGener(nowmp:Mapper):
    # nowmp.C=30
    # nowmp.R=30
    def genWall(x,y,iid=1):
        nowmp.mp[x][y]["type"]="wall"
        nowmp.mp[x][y]["render"]=myImage(f'./assets/scene/wall{nowmp.style}.{iid}.png')
    def genObject(x,y,iid):
        nowmp.mp[x][y]["type"]="object"
        nowmp.mp[x][y]["content"]=iid
        nowmp.mp[x][y]["render"]=myImage(f'./assets/scene/object{iid}.png')
    
    nowmp.C=31
    nowmp.R=31

    genWall(7,7)
    genObject(10,13,3)
    genObject(10,4,5)
    genObject(15,14,2);genObject(18,20,4)
    genObject(3,4,1)
    # nowmp.mp[5][5]["burning"]=20*10
    # nowmp.mp[5][5]["render!"]=myImage("./assets/scene/burning_tmp.png")
    for i in range(0,30):
        genWall(0,i);genWall(i,0);genWall(30,i);genWall(i,30)
    
    for i in range(8,12):
        genWall(i,10,5)

    # monsters
    nowmp.addMonster(5,5,"./assets/monster/")
    nowmp.addMonster(6,7,"./assets/monster/")
    t=nowmp.addMonster(1,12,"./assets/monster/")

    bomb(genEntityId(),2,2,nowmp.addEntity,t,layer=2)
    bomb(genEntityId(),5,2,nowmp.addEntity,t,layer=2)
def mapGener(nowmp:Mapper):
    nowmp.style=0
    def genWall(x,y,iid):
        nowmp.mp[x][y]["type"]="wall"
        nowmp.mp[x][y]["render"]=myImage(f'./assets/scene/wall{nowmp.style}.{iid}.png')
    def genObject(x,y,iid):
        nowmp.mp[x][y]["type"]="object"
        nowmp.mp[x][y]["content"]=iid
        nowmp.mp[x][y]["render"]=myImage(f'./assets/scene/object{iid}.png')
    def genObstacle(x,y,iid):
        nowmp.mp[x][y]["type"]="obstacle"
        nowmp.mp[x][y]["content"]=iid
        nowmp.mp[x][y]["render"]=myImage(f'./assets/scene/obstacle{nowmp.style}.{iid}.png')
    def genField(x,y):
        nowmp.mp[x][y]["type"]="field"
        nowmp.mp[x][y]["content"]=0
        nowmp.mp[x][y]["render"]=None
    nowmp.C=41
    nowmp.R=31

    for x,y in scene0:
        i = random.randrange(1,13)
        genWall(x-1,y-1,i)
    for x in range(0, 41):
        for y in range(0, 31):
            if nowmp.mp[x][y]["type"]=='field' and random.randrange(1,9)>1:
                i = random.randrange(1,12)
                genObstacle(x,y,i)
    genField(0,28)#后面改成通道
    genField(40,2)

    genField(1,27)#空地保证游玩正常
    genField(1,28);genField(1,29);genField(2,28)
    genField(39,1);genField(39,2);genField(39,3);genField(38,2)

    # monster
    genField(5,23);genField(6,23);genField(7,23);genField(8,23)
    nowmp.addMonster(6,23,"./assets/monster/")
    
    def genMos(x,y):
        (nowmp.addMonster(x,y,"./assets/monster/")).bombRange+=random.randrange(0,c.Difficulty+1)
        for i in range(x-2,x+2+1):
            for j in range(y-2,y+2+1):
                if nowmp.mp[i][j]["type"]=="obstacle" and abs(i-x)+abs(j-y)<=2:
                    genField(i,j)
    tmpvis:Dict[Tuple[int,int],bool]={}
    cnt=0
    while cnt<=5+c.Difficulty*2:
        x=random.randrange(1,nowmp.C-2)
        y=random.randrange(1,nowmp.R-2)
        if not tmpvis.get((x,y)) and nowmp.mp[x][y]["type"]!="wall":
            tmpvis[(x,y)]=True
            genMos(x,y)
            cnt+=1

    nowmp.mp[-1][28]["teleportTo"]=(1,40,12)
    nowmp.mp[41][2]["teleportTo"]=(3,0,4)

def mapGenerTown(nowmp:Mapper):
    nowmp.style=1
    nowmp.C=41
    nowmp.R=31
    nowmp.backGround=myImage(f'./assets/scene/scene{nowmp.style}.png',zoom=nowmp.C)
    # 进入田野
    nowmp.mp[41][12]["teleportTo"]=(0,0,28)
    # nowmp.mp[41][12]["type"]="field"
    #进入商店
    nowmp.mp[23][25]["teleportTo"]=nowmp.mp[24][25]["teleportTo"]=\
        nowmp.mp[25][25]["teleportTo"]=(2,5,14)
    nowmp.mp[23][25]["content"]=nowmp.mp[24][25]["content"]=\
        nowmp.mp[25][25]["content"]=-1 #按f才能进入
    # nowmp.fieldimg=myImage(f'./assets/scene/transparent.png') # useless
    # interact point:
    def testInteract():
        pass
    def icecreamShop():
        while True:
            t=""
            for c in zote_precepts:
                t= yield c # yield要输出的对话，由imageclass.py中的dialog.keyboard处理
                # 在存在llm时yield的返回值(t)为用户输入
            yield None # None为特殊占位符，表示对话结束

            
        ''' 
        while True:
            pygame.time.Clock().tick(c.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]: break
            drawDialog("upcoming soon",win)
            pygame.display.update()
        '''
    def dogtalk():
        while True:
            yield "Woof!"
            yield None
    def nineNineCat():
        c=nine('')
        while True:
            t = yield c 
            c= nine(str(t))
            # if t == None:
            #     break
        yield None
    def RefuseEnter():
        while True:
            yield "(I can't enter others' house.)"
            yield None
    def Home():
        while True:
            yield "(This is my home. But it's not the time to go home and sleep.)"
            yield None
    def Notice():
        while True:
            yield "Lost Person Notice: My daughter Haley has been missing in the forest for a day now. She has long golden hair and emerald like eyes. If you find her, I am willing to marry her to you. --The mayor"
            yield None
    def EnterShop(me,mapper):
        pass

    nowmp.mp[34][11]["interact"]=(icecreamShop(),False)
    nowmp.mp[28][25]["interact"]=nowmp.mp[29][25]["interact"]=(dogtalk(),False)
    nowmp.mp[14][25]["interact"]=nowmp.mp[21][6]["interact"]=nowmp.mp[30][6]["interact"]=(RefuseEnter(),False)
    nowmp.mp[3][16]["interact"]=(Home(),False)
    nowmp.mp[7][16]["interact"]=nowmp.mp[10][6]["interact"]=nowmp.mp[24][6]["interact"]=nowmp.mp[27][6]["interact"]=nowmp.mp[26][25]["interact"]=nowmp.mp[11][25]["interact"]=(Notice(),False)
    nowmp.mp[11][6]["interact"]=(nineNineCat(),True)
    # 23 25/24 25/25 25 进入商店
    # 3 16 自家房门
    def genWall(x,y):
        nowmp.mp[x][y]["type"]="wall"
    for x,y in scene1:
        genWall(x,y)

def mapGenerShop(nowmp):
    nowmp.style=2
    nowmp.C=21;nowmp.R=17
    nowmp.backGround=myImage(f'./assets/scene/scene{nowmp.style}.png',zoom=nowmp.C)
    nowmp.mp[5][15]["teleportTo"]=(1,24,25)
    global shopFavorability
    shopFavorability=10
    def getPrice():
        #return [1,1,1,1,1]
        print('shopFavorability:',shopFavorability)
        if shopFavorability>80:l=[1,1,1,3,1];lv=2
        elif shopFavorability>50:l=[1,1,1,3,1];lv=3
        elif shopFavorability>25:l=[2,2,2,6,2];lv=4
        elif shopFavorability>10:l=[5,5,5,10,5];lv=5
        elif shopFavorability>0:l=[15,15,15,25,15];lv=5
        elif shopFavorability>-20:l=[40,40,40,60,40];lv=10
        else:l=[100,100,100,100,100];lv=10
        for i in range(5):l[i]+=c.Difficulty*lv
        return l


    def sale(nowplayer:Any,_:Mapper):
        # nowplayer.money+=100
        global shopFavorability
        while True:
            price=getPrice()
            t=yield f"On Sale: 1: Heal Potion (${price[0]}), 2: Sensitive Potion(${price[1]}), 3: Expanded Bomb Grid Potion(${price[2]}), and 4: Kicking Bomb Boots(${price[3]}). your coin: {nowplayer.money}"
            tcoin=nowplayer.money
            if ("1"in t or "heal" in t) and nowplayer.money>=price[0] :
                nowplayer.hp+=1;nowplayer.money-=price[0]
            if ("3"in t or "expanded" in t) and nowplayer.money>=price[2] :
                nowplayer.bombRange+=1;nowplayer.money-=price[2]
            if ("2"in t or "sensitive" in t) and nowplayer.money>=price[1]:
                nowplayer.speed=c.IncreasedSpeed;nowplayer.money-=price[1]
            if ("4"in t or "kicking" in t or "boots" in t) and nowplayer.money>=price[3]:
                nowplayer.cankick=True;nowplayer.money-=price[3]
            if tcoin>nowplayer.money:
                shopFavorability+=5
                yield "purchase succeed"
            elif "heal" in t or "expanded" in t or "sensitive" in t or "kicking" in t or "boots" in t or "1" in t or "2" in t or "3" in t or "4" in t:
                yield "purchase failed, maybe money isn't enough?"
            else : yield "Product not found"
    def shopownertalk():
        global shopFavorability
        c=shop('')
        lastFavorability=10
        shopFavorability+=int(c[1])-lastFavorability
        lastFavorability=int(c[1])
        # print(c)
        while True:
            t = yield c[0] 
            c= shop(str(t))
            print('shopFavorability:',shopFavorability)
            shopFavorability+=int(c[1])-lastFavorability
            lastFavorability=int(c[1])
            # shopFavorability=100
            if shopFavorability>=100:
                yield "What a charming person you are!"
                yield "I mean..."
                yield "I'm a bit obsessed with you."
                yield "Are you willing to take over my shop?"
                raise Exception("Ending2")  # 通过异常处理死亡和结局
            # if t == None:
            #     break
        yield None
    def genWall(x,y):
        nowmp.mp[x][y]["type"]="wall"
    for x,y in scene2:
        genWall(x,y)
    nowmp.mp[4][5]["interact"]=(sale,True)
    nowmp.mp[2][5]["interact"]=nowmp.mp[3][5]["interact"]=(shopownertalk(),True)

    nowmp.mp[9][5]["type"]="wall"
    nowmp.mp[9][5]["render"]=myImage(f'./assets/scene/shelf1.png',zoom=6)
    
    nowmp.mp[9][8]["type"]="wall"
    nowmp.mp[9][8]["render"]=myImage(f'./assets/scene/shelf1.png',zoom=6)
    
    nowmp.mp[9][11]["type"]="wall"
    nowmp.mp[9][11]["render"]=myImage(f'./assets/scene/shelf3.png',zoom=2)
    
    nowmp.mp[13][11]["type"]="wall"
    nowmp.mp[13][11]["render"]=myImage(f'./assets/scene/shelf3.png',zoom=2)

def mapGenerDeep(nowmp:Mapper):
    def end1():
        yield "Oh my goodness!!!!!"
        yield "I thought I was going to die here."
        yield "Take me away, my hero."
        raise Exception("Ending1")  # 通过异常处理死亡和结局
    nowmp.style=0
    def genWall(x,y,iid):
        nowmp.mp[x][y]["type"]="wall"
        nowmp.mp[x][y]["render"]=myImage(f'./assets/scene/wall{nowmp.style}.{iid}.png')
    def genField(x,y):
        nowmp.mp[x][y]["type"]="field"
        nowmp.mp[x][y]["content"]=0
        nowmp.mp[x][y]["render"]=None
    nowmp.C=14
    nowmp.R=10

    for i in range(nowmp.C):
        for j in range(nowmp.R):
            genWall(i,j,random.randrange(1,13))
    for i in range(0,8):
        genField(i,4)
    
    nowmp.mp[-1][4]["type"]="wall" # 阻止返回
    nowmp.mp[7][4]["type"]="wall"
    nowmp.mp[7][4]["render"]=myImage(f'./assets/scene/beauty.png')
    nowmp.mp[6][4]["interact"]=(end1(),False)

    nowmp.mp[7][5]["render"]=myImage(f'./assets/scene/wall{nowmp.style}.{1}.png')
    
    # 从(0,13)进入
    # nowmp.mp[0][13]["render"]=myImage(f'./assets/scene/transparent.png')

    # nowmp.mp[0][18]["teleportTo"]=(1,40,11)
scene0 = [
[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10],[1,11],[1,12],[1,13],[1,14],[1,15],[1,16],[1,17],[1,18],[1,19],[1,20],[1,21],[1,22],[1,23],[1,24],[1,25],[1,26],[1,27],[1,28],[1,30],[1,31],
[41,1],[41,2],[41,4],[41,5],[41,6],[41,7],[41,8],[41,9],[41,10],[41,11],[41,12],[41,13],[41,14],[41,15],[41,16],[41,17],[41,18],[41,19],[41,20],[41,21],[41,22],[41,23],[41,24],[41,25],[41,26],[41,27],[41,28],[41,29],[41,30],[41,31],
[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],[11,1],[12,1],[13,1],[14,1],[15,1],[16,1],[17,1],[18,1],[19,1],[20,1],[21,1],[22,1],[23,1],[24,1],[25,1],[26,1],[27,1],[28,1],[29,1],[30,1],[31,1],[32,1],[33,1],[34,1],[35,1],[36,1],[37,1],[38,1],[39,1],[40,1],
[2,31],[3,31],[4,31],[5,31],[6,31],[7,31],[8,31],[9,31],[10,31],[11,31],[12,31],[13,31],[14,31],[15,31],[16,31],[17,31],[18,31],[19,31],[20,31],[21,31],[22,31],[23,31],[24,31],[25,31],[26,31],[27,31],[28,31],[29,31],[30,31],[31,31],[32,31],[33,31],[34,31],[35,31],[36,31],[37,31],[38,31],[39,31],[40,31],
[2,6],
[3,2],[3,3],[3,5],[3,6],[3,7],[3,9],[3,10],[3,11],[3,13],[3,14],[3,15],[3,17],[3,18],[3,19],[3,21],[3,22],[3,23],[3,25],[3,27],[3,28],[3,30],
[4,7],[4,13],[4,17],
[5,2],[5,4],[5,5],[5,7],[5,8],[5,9],[5,11],[5,12],[5,13],[5,15],[5,16],[5,17],[5,18],[5,19],[5,20],[5,21],[5,23],[5,25],[5,26],[5,27],[5,28],[5,29],
[6,9],[6,17],[6,27],
[7,2],[7,3],[7,4],[7,5],[7,7],[7,8],[7,9],[7,10],[7,11],[7,12],[7,13],[7,15],[7,16],[7,17],[7,18],[7,19],[7,20],[7,21],[7,22],[7,23],[7,25],[7,28],[7,29],
[8,5],[8,11],[8,21],[8,25],[8,27],
[9,2],[9,3],[9,5],[9,7],[9,9],[9,11],[9,13],[9,15],[9,17],[9,19],[9,20],[9,21],[9,23],[9,25],[9,26],[9,27],[9,29],[9,30],
[10,7],[10,13],[10,17],[10,27],
[11,3],[11,5],[11,6],[11,7],[11,8],[11,10],[11,11],[11,13],[11,15],[11,16],[11,17],[11,19],[11,21],[11,22],[11,23],[11,25],[11,27],[11,28],[11,29],
[12,3],[12,13],[12,17],[12,23],
[13,3],[13,4],[13,6],[13,7],[13,8],[13,9],[13,10],[13,12],[13,13],[13,14],[13,15],[13,17],[13,19],[13,20],[13,21],[13,23],[13,24],[13,26],[13,27],[13,29],
[14,13],[14,17],[14,19],[14,27],
[15,3],[15,4],[15,5],[15,6],[15,7],[15,9],[15,11],[15,12],[15,13],[15,15],[15,16],[15,17],[15,19],[15,21],[15,22],[15,23],[15,25],[15,27],[15,29],[15,30],
[16,12],[16,24],
[17,3],[17,4],[17,5],[17,7],[17,8],[17,9],[17,11],[17,12],[17,13],[17,14],[17,15],[17,17],[17,18],[17,20],[17,21],[17,23],[17,24],[17,25],[17,26],[17,27],[17,28],[17,29],
[18,11],[18,17],[18,21],[18,25],
[19,2],[19,4],[19,5],[19,6],[19,7],[19,9],[19,10],[19,11],[19,13],[19,15],[19,16],[19,17],[19,19],[19,21],[19,22],[19,23],[19,25],[19,27],[19,28],[19,29],[19,30],
[20,13],[20,17],[20,23],
[21,3],[21,5],[21,6],[21,8],[21,9],[21,11],[21,12],[21,13],[21,15],[21,17],[21,19],[21,20],[21,21],[21,23],[21,24],[21,26],[21,27],[21,29],[21,30],
[22,9],[22,13],[22,19],[22,27],[23,2],[23,3],[23,5],[23,6],[23,7],[23,9],[23,10],[23,11],[23,13],[23,14],[23,15],[23,17],[23,18],[23,19],[23,20],[23,22],[23,23],[23,24],[23,25],[23,27],[23,29],[23,30],
[24,9],[24,13],[24,15],[24,23],[24,25],
[25,2],[25,4],[25,5],[25,7],[25,8],[25,11],[25,13],[25,15],[25,16],[25,18],[25,19],[25,21],[25,22],[25,23],[25,25],[25,27],[25,28],[25,29],[25,30],
[26,9],[26,13],
[27,3],[27,5],[27,6],[27,7],[27,10],[27,11],[27,13],[27,14],[27,15],[27,17],[27,18],[27,19],[27,21],[27,22],[27,23],[27,25],[27,27],[27,28],[27,29],
[28,3],[28,9],[28,17],
[29,2],[29,3],[29,5],[29,6],[29,8],[29,9],[29,11],[29,12],[29,13],[29,15],[29,16],[29,17],[29,19],[29,20],[29,22],[29,23],[29,24],[29,26],[29,28],[29,29],
[30,33],
[31,2],[31,3],[31,4],[31,5],[31,6],[31,8],[31,9],[31,10],[31,12],[31,13],[31,14],[31,15],[31,17],[31,19],[31,20],[31,21],[31,23],[31,25],[31,26],[31,27],[31,29],[31,30],
[32,9],[32,16],[32,27],[32,22],
[33,3],[33,5],[33,6],[33,7],[33,11],[33,12],[33,13],[33,15],[33,17],[33,18],[33,19],[33,20],[33,23],[33,24],[33,25],[33,3],[33,26],[33,27],[33,29],[33,30],
[34,3],[34,7],[34,9],[34,15],[34,17],
[35,2],[35,3],[35,5],[35,6],[35,7],[35,8],[35,9],[35,11],[35,13],[35,14],[35,15],[35,17],[35,19],[35,20],[35,22],[35,23],[35,25],[35,26],[35,28],[35,29],
[36,7],[36,9],[36,15],[36,17],[36,23],
[37,3],[37,4],[37,5],[37,7],[37,9],[37,11],[37,12],[37,13],[37,15],[37,16],[37,17],[37,18],[37,20],[37,21],[37,22],[37,23],[37,25],[37,26],[37,27],[37,29],[37,30],
[38,9],[38,13],[38,27],
[39,2],[39,4],[39,5],[39,6],[39,7],[39,9],[39,10],[39,11],[39,13],[39,15],[39,17],[39,19],[39,20],[39,21],[39,23],[39,24],[39,25],[39,27],[39,29],
[40,13],[40,15],[40,17],[40,21],[40,29]
]

scene1=[
[0,19],[1,19],[2,19],[3,19],[4,19],[5,19],[6,19],[7,19],[8,19],
[0,15],[1,15],[2,15],[3,15],[4,15],[5,15],[6,15],[7,15],[8,15],
[8,20],[8,21],[8,22],[8,23],[8,24],[8,25],[8,26],[8,27],
[9,27],[10,27],[11,27],[12,27],[13,27],[14,27],[15,27],[16,27],[17,27],[18,27],[19,27],[20,27],[21,27],[22,27],[23,27],[24,27],[25,27],[26,27],[27,27],[28,27],[29,27],[30,27],[31,27],
[31,13],[31,14],[31,15],[31,16],[31,17],[31,18],[31,19],[31,20],[31,21],[31,22],[31,23],[31,24],[31,25],[31,26],
[32,26],[33,26],[34,26],[35,26],[36,26],[37,26],[38,26],[39,26],[40,26],
[31,10],[32,10],[33,10],[34,10],[35,10],[36,10],[37,10],[38,10],[39,10],[40,10],
[32,13],[33,13],[34,13],[35,13],[36,13],[37,13],[38,13],[39,13],[40,13],
[31,6],[31,7],[31,8],[31,9],
[8,5],[9,5],[10,5],[11,5],[12,5],[13,5],[14,5],[15,5],[16,5],[17,5],[18,5],[19,5],[20,5],[21,5],[22,5],[23,5],[24,5],[25,5],[26,5],[27,5],[28,5],[29,5],[30,5],[31,5],
[8,6],[8,7],[8,8],[8,9],[8,10],[8,11],[8,12],[8,13],[8,14],
[29,8],[29,9],[29,10],[29,11],[29,12],[29,13],[29,14],[29,15],[29,16],[29,17],[29,18],[29,19],[29,20],[29,21],[29,22],[29,23],[29,24],
[10,24],[11,24],[12,24],[13,24],[14,24],[15,24],[16,24],[17,24],[18,24],[19,24],[20,24],[21,24],[22,24],[23,24],[24,24],[25,24],[26,24],[27,24],[28,24],
[10,8],[10,9],[10,10],[10,11],[10,12],[10,13],[10,14],[10,15],[10,16],[10,17],[10,18],[10,19],[10,20],[10,21],[10,22],[10,23],
[11,8],[12,8],[13,8],[14,8],[15,8],[16,8],[17,8],[18,8],[19,8],[20,8],[21,8],[22,8],[23,8],[24,8],[25,8],[26,8],[27,8],[28,8],
]

scene2 =[
[4,14],[3,13],[2,13],[1,12],[0,12],[0,11],[0,10],[0,9],[0,8],[0,7],[0,6],[0,5],
[1,4],[2,4],[3,4],[4,4],[5,4],[6,4],[7,4],[7,3],
[8,2],[9,2],[10,2],[11,2],[12,2],[13,2],[14,2],[15,3],
[16,4],[16,5],[16,6],[16,7],[16,8],[16,9],[16,10],[16,11],[16,12],[16,13],[17,14],[18,14],[19,16],[19,15],
[7,16],[7,15],[7,14],[6,14],[6,15],[4,15],
[9,5],[10,5],[11,5],[12,5],[13,5],[14,5],
[9,8],[10,8],[11,8],[12,8],[13,8],[14,8],
[14,11],[14,12],[14,13],[14,14],[14,15],[13,11],[13,12],[13,13],[13,14],[13,15],
[9,11],[9,12],[9,13],[9,14],[9,15],[10,11],[10,12],[10,13],[10,14],[10,15],
]

#scene3_0=[
#    [4,3],[5,3],[6,3],[7,3],[8,3],[8,4],
#    [4,5],[5,5],[6,5],[7,5],[8,5]
#]





zote_precepts = [
    "Precept One: 'Always Win Your Battles'. Losing a battle earns you nothing and teaches you nothing. Win your battles, or don't engage in them at all!",

    "Precept Two: 'Never Let Them Laugh at You'. Fools laugh at everything, even at their superiors. But beware, laughter isn't harmless! Laughter spreads like a disease, and soon everyone is laughing at you. You need to strike at the source of this perverse merriment quickly to stop it from spreading.",

    "Precept Three: 'Always Be Rested'. Fighting and adventuring take their toll on your body. When you rest, your body strengthens and repairs itself. The longer you rest, the stronger you become.",

    "Precept Four: 'Forget Your Past'. The past is painful, and thinking about your past can only bring you misery. Think about something else instead, such as the future, or some food.",

    "Precept Five: 'Strength Beats Strength'. Is your opponent strong? No matter! Simply overcome their strength with even more strength, and they'll soon be defeated.",
    "Precept Six: 'Choose Your Own Fate'. Our elders teach that our fate is chosen for us before we are even born. I disagree.",
    "Precept Seven: 'Mourn Not the Dead'. When we die, do things get better for us or worse? There's no way to tell, so we shouldn't bother mourning. Or celebrating for that matter.",
    "Precept Eight: 'Travel Alone'. You can rely on nobody, and nobody will always be loyal. Therefore, nobody should be your constant companion.",
    "Precept Nine: 'Keep Your Home Tidy'. Your home is where you keep your most prized possession - yourself. Therefore, you should make an effort to keep it nice and clean.",
    "Precept Ten: 'Keep Your Weapon Sharp'. I make sure that my weapon, 'Life Ender', is kept well-sharpened at all times. This makes it much easier to cut things.",
    "Precept Eleven: 'Mothers Will Always Betray You'. This Precept explains itself.",
    "Precept Twelve: 'Keep Your Cloak Dry'. If your cloak gets wet, dry it as soon as you can. Wearing wet cloaks is unpleasant, and can lead to illness.",
    "Precept Thirteen: 'Never Be Afraid'. Fear can only hold you back. Facing your fears can be a tremendous effort. Therefore, you should just not be afraid in the first place.",
    "Precept Fourteen: 'Respect Your Superiors'. If someone is your superior in strength or intellect or both, you need to show them your respect. Don't ignore them or laugh at them.",
    "Precept Fifteen: 'One Foe, One Blow'. You should only use a single blow to defeat an enemy. Any more is a waste. Also, by counting your blows as you fight, you'll know how many foes you've defeated.",
    "Precept Sixteen: 'Don't Hesitate'. Once you've made a decision, carry it out and don't look back. You'll achieve much more this way.",
    "Precept Seventeen: 'Believe In Your Strength'. Others may doubt you, but there's someone you can always trust. Yourself. Make sure to believe in your own strength, and you will never falter.",
    "Precept Eighteen: 'Seek Truth in the Darkness'. This Precept also explains itself.",
    "Precept Nineteen: 'If You Try, Succeed'. If you're going to attempt something, make sure you achieve it. If you do not succeed, then you have actually failed! Avoid this at all costs.",
    "Precept Twenty: 'Speak Only the Truth'. When speaking to someone, it is courteous and also efficient to speak truthfully. Beware though that speaking truthfully may make you enemies. This is something you'll have to bear.",

    "Precept Twenty-One: 'Be Aware of Your Surroundings'. Don't just walk along staring at the ground! You need to look up every so often, to make sure nothing takes you by surprise.",

    "Precept Twenty-Two: 'Abandon the Nest'. As soon as I could, I left my birthplace and made my way out into the world. Do not linger in the nest. There is nothing for you there.",
    "Precept Twenty-Three: 'Identify the Foe's Weak Point'. Every foe you encounter has a weak point, such as a crack in their shell or being asleep. You must constantly be alert and scrutinising your enemy to detect their weakness!",
    "Precept Twenty-Four: 'Strike the Foe's Weak Point'. Once you have identified your foe's weak point as per the previous Precept, strike it. This will instantly destroy them.",
    "Precept Twenty-Five: 'Protect Your Own Weak Point'. Be aware that your foe will try to identify your weak point, so you must protect it. The best protection? Never having a weak point in the first place.",
    "Precept Twenty-Six: 'Don't Trust Your Reflection'. When peering at certain shining surfaces, you may see a copy of your own face. The face will mimic your movements and seems similar to your own, but I don't think it can be trusted.",
    "Precept Twenty-Seven: 'Eat As Much As You Can'. When having a meal, eat as much as you possibly can. This gives you extra energy, and means you can eat less frequently.",
    "Precept Twenty-Eight: 'Don't Peer Into the Darkness'. If you peer into the darkness and can't see anything for too long, your mind will start to linger over old memories. Memories are to be avoided, as per Precept Four.",
    "Precept Twenty-Nine: 'Develop Your Sense of Direction'. It's easy to get lost when travelling through winding, twisting caverns. Having a good sense of direction is like having a magical map inside of your head. Very useful.",
    "Precept Thirty: 'Never Accept a Promise'. Spurn the promises of others, as they are always broken. Promises of love or betrothal are to be avoided especially.",
    "Precept Thirty-One: 'Disease Lives Inside of Dirt'. You'll get sick if you spend too much time in filthy places. If you are staying in someone else's home, demand the highest level of cleanliness from your host.",

    "Precept Thirty-Two: 'Names Have Power'. Names have power, and so to name something is to grant it power. I myself named my nail 'Life Ender'. Do not steal the name I came up with! Invent your own!",

    "Precept Thirty-Three: 'Show the Enemy No Respect'. Being gallant to your enemies is no virtue! If someone opposes you, they don't deserve respect or kindness or mercy.",

    "Precept Thirty-Four: 'Don't Eat Immediately Before Sleeping'. This can cause restlessness and indigestion. It's just common sense.",

    "Precept Thirty-Five: 'Up is Up, Down is Down'. If you fall over in the darkness, it can be easy to lose your bearing and forget which way is up. Keep this Precept in mind!",
    "Precept Thirty-Six: 'Eggshells are brittle'. Once again, this Precept explains itself.",
    "Precept Thirty-Seven: 'Borrow, But Do Not Lend'. If you lend and are repayed, you gain nothing. If you borrow but do not repay, you gain everything.",
    "Precept Thirty-Eight: 'Beware the Mysterious Force'. A mysterious force bears down on us from above, pushing us downwards. If you spend too long in the air, the force will crush you against the ground and destroy you. Beware!",
    "Precept Thirty-Nine: 'Eat Quickly and Drink Slowly'. Your body is a delicate thing and you must fuel it with great deliberation. Food must go in as fast as possible, but fluids at a slower rate.",
    "Precept Forty: 'Obey No Law But Your Own'. Laws written by others may inconvenience you or be a burden. Let your own desires be the only law.",
    "Precept Forty-One: 'Learn to Detect Lies'. When others speak, they usually lie. Scrutinise and question them relentlessly until they reveal their deceit.",
    "Precept Forty-Two: 'Spend Geo When You Have It'. Some will cling onto their Geo, even taking it into the dirt with them when they die. It is better to spend it when you can, so you can enjoy various things in life.",
    "Precept Forty-Three: 'Never Forgive'. If someone asks forgiveness of you, for instance a brother of yours, always deny it. That brother, or whoever it is, doesn't deserve such a thing.",
    "Precept Forty-Four: 'You Can Not Breathe Water'. Water is refreshing, but if you try to breathe it you are in for a nasty shock.",
    "Precept Forty-Five: 'One Thing Is Not Another'. This one should be obvious, but I've had others try to argue that one thing, which is clearly what it is and not something else, is actually some other thing, which it isn't. Stay on your guard!",
    "Precept Forty-Six: 'The World is Smaller Than You Think'. When young, you tend to think that the world is vast, huge, gigantic. It's only natural. Unfortunately, it's actually quite a lot smaller than that. I can say this, now having travelled everywhere in the land.",
    "Precept Forty-Seven: 'Make Your Own Weapon'. Only you know exactly what is needed in your weapon. I myself fashioned 'Life Ender' from shellwood at a young age. It has never failed me. Nor I it.",

    "Precept Forty-Eight: 'Be Careful With Fire'. Fire is a type of hot spirit that dances about recklessly. It can warm you and provide light, but it will also singe your shell if it gets too close.",
    "Precept Forty-Nine: 'Statues are Meaningless'. Do not honour them! No one has ever made a statue of you or I, so why should we pay them any attention?",
    "Precept Fifty: 'Don't Linger on Mysteries'. Some things in this world appear to us as puzzles. Or enigmas. If the meaning behind something is not immediately evident though, don't waste any time thinking about it. Just move on.",
    "Precept Fifty-One: 'Nothing is Harmless'. Given the chance, everything in this world will hurt you. Friends, foes, monsters, uneven paths. Be suspicious of them all.",
    "Precept Fifty-Two: 'Beware the Jealousy of Fathers'. Fathers believe that because they created us we must serve them and never exceed their capabilities. If you wish to forge your own path, you must vanquish your father. Or simply abandon him.",
    "Precept Fifty-Three: 'Do Not Steal the Desires of Others'. Every creature keeps their desires locked up inside of themselves. If you catch a glimpse of another's desires, resist the urge to claim them as your own. It will not lead you to happiness.",
    "Precept Fifty-Four: 'If You Lock Something Away, Keep the Key'. Nothing should be locked away for ever, so hold onto your keys. You will eventually return and unlock everything you hid away.",
    "Precept Fifty-Five: 'Bow to No-one'. There are those in this world who would impose their will on others. They claim ownership over your food, your land, your body, and even your thoughts! They have done nothing to earn these things. Never bow to them, and make sure to disobey their commands.",
    "Precept Fifty-Six: 'Do Not Dream'. Dreams are dangerous things. Strange ideas, not your own, can worm their way into your mind. But if you resist those ideas, sickness will wrack your body! Best not to dream at all, like me.",
    "Precept Fifty-Seven: 'Obey All Precepts'. Most importantly, you must commit all of these Precepts to memory and obey them all unfailingly. Including this one! Hmm. Have you truly listened to everything I've said? Let's start again and repeat the 'Fifty-Seven Precepts of Zote'"
]
