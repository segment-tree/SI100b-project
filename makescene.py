from entity import *
from scene import *
from imageclass import *
import random
def mapGener(nowmp):
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

    nowmp.mp[0][28]["teleportTo"]=(1,40,13)

def mapGenerTown(nowmp):
    nowmp.style=1
    nowmp.C=41
    nowmp.R=31
    nowmp.backGround=myImage(f'./assets/scene/scene{nowmp.style}.png',zoom=nowmp.C)
    nowmp.mp[40][12]["teleportTo"]=(0,1,28)
    # nowmp.fieldimg=myImage(f'./assets/scene/transparent.png') # useless
    # interact point:
    def testInteract():
        pass
    def icecreamShop(win):
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
    def dogtalk(win):
        pass
    def nineNineCat(win):
        pass
    def RefuseEnter(win):
        pass
    nowmp.mp[34][11]["interact"]=icecreamShop
    nowmp.mp[28][25]["interact"]=nowmp.mp[29][25]["interact"]=dogtalk
    nowmp.mp[14][25]["interact"]=nowmp.mp[21][6]["interact"]=nowmp.mp[30][6]["interact"]=RefuseEnter
    nowmp.mp[11][6]["interact"]=nineNineCat
    # 23 25/24 25/25 25 进入商店
    # 3 16 自家房门


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


  