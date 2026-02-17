try:
    Rules1 = open("操作说明.txt" , 'r')
    Rules2 = open("游戏规则.txt" , 'r')
    print(Rules1.read())
    print('\n')
    print(Rules2.read())
except:
    print('''P1(红方操作):
T 上边放墙
H 右边放墙
G 下边放墙
F 左边放墙
WASD 移动
左Shift 认输
P2(蓝方操作):
I 上边放墙
L 右边放墙
K 下边放墙
J 左边放墙
↑↓←→ 移动
右Shift 认输
public:
ESC or 右上角X键 退出
大写锁定  隐藏/显示光标
空格  停止/继续音乐''')
    print('\n')
    print('''放下的墙不可逾越！
不可跨越对方！
每次只能走5步。

这个游戏有两种规则：可以不走、不能不走（也不能走回回合开始时所处的位置）。
一般来说我们采用后者，这样更有趣味性。
但是为了兼容，操作上没有禁止原地放墙。建议玩家自觉遵守此规则，即放墙前先走几步。''')

import pygame
from pygame.locals import *
from os import system
from sys import exit


pygame.init()


#Values
#游戏各种参数设置与调试
TITLE        = 'my pygame' #标题
STEP         = 5           #每回合可走步数
TIME         = 600         #游戏时间（秒）
SPEED        = 0.5         #时钟速率
SYSTEM       = False       #智能时钟系统
DFSVT        = 40          #深搜可视化单位时间


window = pygame.display.set_mode( (1000 , 750) )
pygame.display.set_caption(TITLE)

###
RED         = pygame.image.load('./image/red.png'  )
BLUE        = pygame.image.load('./image/blue.png' )
FLAGb       = pygame.image.load('./image/flagB.png')
FLAGr       = pygame.image.load('./image/flagR.png')
LINEbX      = pygame.image.load('./image/BlueLineX.gif'  )
LINEbY      = pygame.image.load('./image/BlueLineY.gif'  )
LINErX      = pygame.image.load('./image/RedLineX.gif'   )
LINErY      = pygame.image.load('./image/RedLineY.gif'   )
Interface   = pygame.image.load('./image/background1.png')
Background  = pygame.image.load('./image/background2.png')
startIN     = pygame.image.load('./image/startIN.gif'    )
startOUT    = pygame.image.load('./image/startOUT.gif'   )
WallX       = pygame.image.load('./image/wallX.gif' )
WallY       = pygame.image.load('./image/wallY.gif' )
Puzzle      = pygame.image.load('./image/Puzzle.png')

Next     = False
Player   = True
Mouse    = True
Game_end = False
Step     = STEP
Score1   = 0
Score2   = 0

string1 = "I'm sorry but you can go for only five steps"
string2 = 'Do not try to cross borders, walls or your opponent!'

P1CE = [0, 700]
P2CE = [700, 0]
Wall_x_LIST = [[False for i in range(16)]for j in range(16)]
Wall_y_LIST = [[False for i in range(16)]for j in range(16)] # 规避浅拷贝！！！这个卡了我三年的问题！！！
    
field = [[0 for i in range(16)]for j in range(16)]

Timer   = pygame.time.Clock()


#Classes
class number:
    def __init__(self, num=8):
        self.all  = []
        for i in range(10):
            self.doll = [False for j in range(7)]
            if i == 0:
                self.doll[0] = self.doll[2] = self.doll[3] = self.doll[4] = self.doll[5] = self.doll[6] = True
            elif i == 1:
                self.doll[4] = self.doll[6] = True
            elif i == 2:
                self.doll[0] = self.doll[1] = self.doll[2] = self.doll[4] = self.doll[5] = True
            elif i == 3:
                self.doll[0] = self.doll[1] = self.doll[2] = self.doll[4] = self.doll[6] = True
            elif i == 4:
                self.doll[1] = self.doll[3] = self.doll[4] = self.doll[6] = True
            elif i == 5:
                self.doll[0] = self.doll[1] = self.doll[2] = self.doll[3] = self.doll[6] = True
            elif i == 6:
                self.doll[0] = self.doll[1] = self.doll[2] = self.doll[3] = self.doll[5] = self.doll[6] = True
            elif i == 7:
                self.doll[0] = self.doll[4] = self.doll[6] = True
            elif i == 8:
                self.doll[0] = self.doll[1] = self.doll[2] = self.doll[3] = self.doll[4] = self.doll[5] = self.doll[6] = True
            elif i == 9:
                self.doll[0] = self.doll[1] = self.doll[2] = self.doll[3] = self.doll[4] = self.doll[6] = True
            self.all.append(self.doll)
        self.num = num
    def change(self, x):
        self.num = int(x)
    def output(self, image1, image2, image_size,  x,y):
        if self.all[self.num][0]:
            window.blit(image1 , (x,y))
        if self.all[self.num][1]:
            window.blit(image1 , (x , y+image_size))
        if self.all[self.num][2]:
            window.blit(image1 , (x,y+image_size*2))
        if self.all[self.num][3]:
            window.blit(image2 , (x,y))
        if self.all[self.num][4]:
            window.blit(image2 , (x+image_size , y))
        if self.all[self.num][5]:
            window.blit(image2 , (x , y+image_size))
        if self.all[self.num][6]:
            window.blit(image2 , (x+image_size , y+image_size))

            

class clock:
    def __init__(self, rate, time , color ,speed=1):
        super().__init__()
        self.rate  = rate  #帧率
        self.clock = time #时钟
        self.value = number()
        self.doll  = 0
        self.speed = speed
        if color:
            self.line1 = LINErX
            self.line2 = LINErY
        else:
            self.line1 = LINEbX
            self.line2 = LINEbY
    def transform(self):
        self.doll += self.speed
        self.doll %= self.rate
        if self.doll == 0:
            self.clock += 1
    def dis_transform(self):
        self.doll += self.speed
        self.doll %= self.rate
        if self.doll == 0:
            self.clock -= 1
    def time(self):
        return self.clock
    def update(self, time):
        self.clock = time
    def a_tempo(self, speed=1):
        self.speed = speed
    def accel(self, speed=0):
        self.speed += speed
    def rit(self, speed=0):
        self.speed -= speed
    def output(self , y):
        self.value.change(self.time() // 600)
        self.value.output(self.line1, self.line2, 30  ,770,y)
        self.value.change(self.time() // 60 % 10)
        self.value.output(self.line1, self.line2, 30  ,810,y)
        self.value.change(self.time() % 60 // 10)
        self.value.output(self.line1, self.line2, 30  ,860,y)
        self.value.change(self.time() % 10)
        self.value.output(self.line1, self.line2, 30  ,900,y)
        

#Functions
def BGM():
    pygame.mixer.music.load('./music/Classical Artists - PHOENIX OVERTURE.mp3')
    pygame.mixer.music.play(-1)


def dfs(x,y,visible=False,img=RED):
    if y>0:
        if not Wall_x_LIST[x//50][y//50] and not field[x//50][y//50-1]:
            if visible:
                window.blit(img,(x,y-50))
                pygame.display.update()
                pygame.time.delay(DFSVT)
            field[x//50][y//50-1] = 1
            dfs(x,y-50,visible,img)
    if x<700:
        if not Wall_y_LIST[x//50+1][y//50] and not field[x//50+1][y//50]:
            if visible:
                window.blit(img,(x+50,y))
                pygame.time.delay(DFSVT)
                pygame.display.update()
            field[x//50+1][y//50] = 1
            dfs(x+50,y,visible,img)
    if y<700:
        if not Wall_x_LIST[x//50][y//50+1] and not field[x//50][y//50+1]:
            if visible:
                window.blit(img,(x,y+50))
                pygame.time.delay(DFSVT)
                pygame.display.update()
            field[x//50][y//50+1] = 1
            dfs(x,y+50,visible,img)
    if x>0:
        if not Wall_y_LIST[x//50][y//50] and not field[x//50-1][y//50]:
            if visible:
                window.blit(img,(x-50,y))
                pygame.time.delay(DFSVT)
                pygame.display.update()
            field[x//50-1][y//50] = 1
            dfs(x-50,y,visible,img)


def det():
    global field, Score1, Score2
    dfs(P1CE[0],P1CE[1])
    if field[P2CE[0]//50][P2CE[1]//50]:
        field = [[0 for i in range(16)]for j in range(16)]
    else:
        for i in field:
            for j in i:
                Score1 += j
        field = [[0 for i in range(16)]for j in range(16)]
        dfs(P2CE[0],P2CE[1])
        for i in field:
            for j in i:
                Score2 += j
        field = [[0 for i in range(16)]for j in range(16)]
        if Score1 > Score2:
            end(1)
        elif Score1 < Score2:
            end(2)
        else:
            end(3)


def interface():
    global Next,Player,Step,STEP,TIME,SPEED,SYSTEM,DFSVT
    while True:
        #x : 295 650
        #y : 460 600
        window.blit(Interface, (0, 0))
        x, y = pygame.mouse.get_pos()
        if x > 295 and x < 650 and y > 460 and y < 600:
            window.blit(startIN , (295 , 450))
        else:
            window.blit(startOUT, (295 , 450))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if x > 295 and x < 650 and y > 460 and y < 600:
                    Next = True
                    break
            if event.type == KEYDOWN:
                if event.key == K_1:
                    Player = True
                if event.key == K_0:
                    Player = False
                if event.key == K_q:
                    STEP += 1
                    Step = STEP
                if event.key == K_a and STEP > 1:
                    STEP -= 1
                    Step = STEP
                if event.key == K_w:
                    TIME += 30
                if event.key == K_s and TIME > 30:
                    TIME -= 30
                if event.key == K_e:
                    TIME += 1
                if event.key == K_d and TIME > 1:
                    TIME -= 1
                if event.key == K_r:
                    SPEED *= 1.1
                if event.key == K_f:
                    SPEED /= 1.1
                if event.key == K_t:
                    DFSVT *= 2
                if event.key == K_g:
                    DFSVT -= 2
                if event.key == K_SPACE:
                    SYSTEM = not(bool(SYSTEM))
                
        if Next:
            Next = False
            break

        pygame.display.update()
        pygame.event.pump()



def mian():
    global Player,Mouse,Step,Score1,Score2,STEP,TIME,SPEED,SYSTEM,DFSVT
    GameClock1 = clock(60, TIME, True , SPEED)
    GameClock2 = clock(60, TIME, False, SPEED)
    Timer.tick(60)
    while True:
        window.blit(Background, (0,0))
        pygame.mouse.set_visible(Mouse)
        if Player:
            GameClock1.dis_transform()
        else:
            GameClock2.dis_transform()
        GameClock1.output(300)
        GameClock2.output(630)
        if GameClock1.time() == 0:
            Score1 = -2
            end(2)
        if GameClock2.time() == 0:
            Score2 = -2
            end(1)
        if GameClock1.time() == min(TIME//6, 15):
            print('Red had only %d seconds!\a' % min(TIME//6, 15))
        if GameClock2.time() == min(TIME//6, 15):
            print('Blue had only %d seconds!\a' % min(TIME//6, 15))
        ##
        if SYSTEM:
            if GameClock1.time() == TIME:
                GameClock1.a_tempo(1)
            elif GameClock1.time() == TIME*3//4:
                GameClock1.a_tempo(SPEED)
            elif GameClock1.time() < TIME*2//3 and GameClock1.time() > TIME//2:
                GameClock1.accel(SPEED/50)
            elif GameClock1.time() < TIME//2 and GameClock1.time() > TIME//3:
                GameClock1.rit(SPEED/50)
            elif GameClock1.time() == TIME//4:
                GameClock1.a_tempo(SPEED*2)
            elif GameClock1.time() == TIME//5:
                GameClock1.a_tempo(SPEED)
            elif GameClock1.time() == TIME//6:
                GameClock1.a_tempo(SPEED//2)
            if GameClock2.time() == TIME:
                GameClock2.a_tempo(1)
            elif GameClock2.time() == TIME*3//4:
                GameClock2.a_tempo(SPEED)
            elif GameClock2.time() < TIME*2//3 and GameClock2.time() > TIME//2:
                GameClock2.accel(SPEED/50)
            elif GameClock2.time() < TIME//2 and GameClock2.time() > TIME//3:
                GameClock2.rit(SPEED/50)
            elif GameClock2.time() == TIME//4:
                GameClock2.a_tempo(SPEED*2)
            elif GameClock2.time() == TIME//5:
                GameClock2.a_tempo(SPEED)
            elif GameClock2.time() == TIME//6:
                GameClock2.a_tempo(SPEED//2)
        ##
        for i in range(15):
            for j in range(15):
                window.blit(Puzzle , (i*50 , j*50))
        if Player:
            if P1CE[0] < 700: #必须特判一次
                window.blit(RED , (P1CE[0]+50 ,P1CE[1]))
            window.blit(RED , (P1CE[0]    , P1CE[1]+50))
            window.blit(RED , (P1CE[0]-50 , P1CE[1]   ))
            window.blit(RED , (P1CE[0]    , P1CE[1]-50))
        else:
            if P2CE[0] < 700:
                window.blit(BLUE, (P2CE[0]+50 ,P2CE[1]))
            window.blit(BLUE, (P2CE[0]    , P2CE[1]+50))
            window.blit(BLUE, (P2CE[0]-50 , P2CE[1]   ))
            window.blit(BLUE, (P2CE[0]    , P2CE[1]-50))
        window.blit(FLAGr , P1CE)
        window.blit(FLAGb , P2CE)
        for i in range(15):
            for j in range(15):
                if Wall_x_LIST[i][j]:
                    window.blit(WallX , (i*50 , j*50))
                if Wall_y_LIST[i][j]:
                    window.blit(WallY , (i*50 , j*50))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == K_CAPSLOCK:
                    Mouse = not(bool(Mouse))
                if event.key == K_SPACE:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
            if event.type == KEYUP:
                if Player:
                    if event.key == K_t: #上边放墙
                        if P1CE[1] > 0 and not(Wall_x_LIST[P1CE[0]//50][P1CE[1]//50]):
                            Wall_x_LIST[P1CE[0]//50][P1CE[1]//50] = True
                            Step = STEP
                            Player = False
                            det()
                    if event.key == K_h: #右边放墙
                        if P1CE[0] < 700 and not(Wall_y_LIST[P1CE[0]//50+1][P1CE[1]//50]):
                            Wall_y_LIST[P1CE[0]//50+1][P1CE[1]//50] = True
                            Step = STEP
                            Player = False
                            det()
                    if event.key == K_g: #下边放墙
                        if P1CE[1] < 700 and not(Wall_x_LIST[P1CE[0]//50][P1CE[1]//50+1]):
                            Wall_x_LIST[P1CE[0]//50][P1CE[1]//50+1] = True
                            Step = STEP
                            Player = False
                            det()
                    if event.key == K_f: #左边放墙
                        if P1CE[0] > 0 and not(Wall_y_LIST[P1CE[0]//50][P1CE[1]//50]):
                            Wall_y_LIST[P1CE[0]//50][P1CE[1]//50] = True
                            Step = STEP
                            Player = False
                            det()
                    if event.key == K_w:
                        if P1CE[1] > 0 and not(P1CE[0] == P2CE[0] and P1CE[1] == P2CE[1]+50) and not(Wall_x_LIST[P1CE[0]//50][P1CE[1]//50]):
                            if Step > 0:
                                P1CE[1] -= 50
                                Step -= 1
                            else:
                                print(string1)
                                print('\a')
                        else:
                            print(string2)
                    if event.key == K_a:
                        if P1CE[0] > 0 and not(P1CE[0] == P2CE[0]+50 and P1CE[1] == P2CE[1]) and not(Wall_y_LIST[P1CE[0]//50][P1CE[1]//50]):
                            if Step > 0:
                                P1CE[0] -= 50
                                Step -= 1
                            else:
                                print(string1)
                                print('\a')
                        else:
                            print(string2)
                    if event.key == K_s:
                        if P1CE[1] < 700 and not(P1CE[0] == P2CE[0] and P1CE[1] == P2CE[1]-50) and not(Wall_x_LIST[P1CE[0]//50][P1CE[1]//50+1]):
                            if Step > 0:
                                P1CE[1] += 50
                                Step -= 1
                            else:
                                print(string1)
                                print('\a')
                        else:
                            print(string2)
                    if event.key == K_d:
                        if P1CE[0] < 700 and not(P1CE[0] == P2CE[0]-50 and P1CE[1] == P2CE[1]) and not(Wall_y_LIST[P1CE[0]//50+1][P1CE[1]//50]):
                            if Step > 0:
                                P1CE[0] += 50
                                Step -= 1
                            else:
                                print(string1)
                                print('\a')
                        else:
                            print(string2)
                else:
                    if event.key == K_i: #上边放墙
                        if P2CE[1] > 0 and not(Wall_x_LIST[P2CE[0]//50][P2CE[1]//50]):
                            Wall_x_LIST[P2CE[0]//50][P2CE[1]//50] = True
                            Step = STEP
                            Player = True
                            det()
                    if event.key == K_l: #右边放墙
                        if P2CE[0] < 700 and not(Wall_y_LIST[P2CE[0]//50+1][P2CE[1]//50]):
                            Wall_y_LIST[P2CE[0]//50+1][P2CE[1]//50] = True
                            Step = STEP
                            Player = True
                            det()
                    if event.key == K_k: #下边放墙
                        if P2CE[1] < 700 and not(Wall_x_LIST[P2CE[0]//50][P2CE[1]//50+1]):
                            Wall_x_LIST[P2CE[0]//50][P2CE[1]//50+1] = True
                            Step = STEP
                            Player = True
                            det()
                    if event.key == K_j: #左边放墙
                        if P2CE[0] > 0 and not(Wall_y_LIST[P2CE[0]//50][P2CE[1]//50]):
                            Wall_y_LIST[P2CE[0]//50][P2CE[1]//50] = True
                            Step = STEP
                            Player = True
                            det()
                    if event.key == K_UP:
                        if P2CE[1] > 0 and not(P2CE[0] == P1CE[0] and P2CE[1] == P1CE[1]+50) and not(Wall_x_LIST[P2CE[0]//50][P2CE[1]//50]):
                            if Step > 0:
                                P2CE[1] -= 50
                                Step -= 1
                            else:
                                print(string1)
                                print('\a')
                        else:
                            print(string2)
                    if event.key == K_DOWN:
                        if P2CE[1] < 700 and not(P2CE[0] == P1CE[0] and P2CE[1] == P1CE[1]-50) and not(Wall_x_LIST[P2CE[0]//50][P2CE[1]//50+1]):
                            if Step > 0:
                                P2CE[1] += 50
                                Step -= 1
                            else:
                                print(string1)
                                print('\a')
                        else:
                            print(string2)
                    if event.key == K_LEFT:
                        if P2CE[0] > 0 and not(P2CE[0] == P1CE[0]+50 and P2CE[1] == P1CE[1]) and not(Wall_y_LIST[P2CE[0]//50][P2CE[1]//50]):
                            if Step > 0:
                                P2CE[0] -= 50
                                Step -= 1
                            else:
                                print(string1)
                                print('\a')
                        else:
                            print(string2)
                    if event.key == K_RIGHT:
                        if P2CE[0] < 700 and not(P2CE[0] == P1CE[0]-50 and P2CE[1] == P1CE[1]) and not(Wall_y_LIST[P2CE[0]//50+1][P2CE[1]//50]):
                            if Step > 0:
                                P2CE[0] += 50
                                Step -= 1
                            else:
                                print(string1)
                                print('\a')
                        else:
                            print(string2)
                if event.key == K_1:
                    Score1 = -1
                    end(2)
                if event.key == K_0:
                    Score2 = -1
                    end(1)
        
        pygame.display.update()
        pygame.event.pump()



def end(x):
    global Score1, Score2
    window.blit(Background, (0,0))
    for i in range(15):
        for j in range(15):
            window.blit(Puzzle , (i*50 , j*50))
    window.blit(FLAGr , P1CE)
    window.blit(FLAGb , P2CE)
    for i in range(15):
        for j in range(15):
            if Wall_x_LIST[i][j]:
                window.blit(WallX , (i*50 , j*50))
            if Wall_y_LIST[i][j]:
                window.blit(WallY , (i*50 , j*50))
    pygame.display.update()
    if Score1 > 0 or Score2 > 0:
        field = [[0 for i in range(16)]for j in range(16)]
        dfs(P1CE[0],P1CE[1],True) # 全游戏亮点！Depth First Search Visiblization, 深度优先搜索可视化！
        field = [[0 for i in range(16)]for j in range(16)]
        dfs(P2CE[0],P2CE[1],True,BLUE)
    if x == 1:
        print('the Winner is Red Player\n',Score1,':',Score2)
    elif x == 2:
        print('the Winner is Blue Player\n',Score1,':',Score2)
    elif x == 3:
        print('Draw\n',Score1,':',Score2)
    system('pause')
    pygame.quit()
    exit()


#main function
if __name__ == '__main__':
    interface()
    BGM()
    mian()
