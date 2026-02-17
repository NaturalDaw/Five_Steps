import pygame, random , os
from sys import exit
from pygame.locals import *
pygame.init()

window = pygame.display.set_mode((750, 750))
#-----------------------------

TIMED = 10
RED = pygame.image.load('./image/red.png')
BLUE = pygame.image.load('./image/blue.png')
FLAGb = pygame.image.load('./image/flagB.png')
FLAGr = pygame.image.load('./image/flagR.png')
PUZZLE = pygame.image.load('./image/puzzle.png')
global PUZZLETUPLE

#-----------------------------

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
class clock:
    def __init__(self, rate, clo):
        self.rate = rate  # 帧率
        self.ln = 0
        self.clock = clo  # 时钟

    def transform(self):
        self.ln += 1
        self.ln = self.ln % self.rate
        if self.ln == 0:
            self.clock += 1

    def dis_transform(self):
        self.ln += 1
        self.ln %= self.rate
        if self.ln == 0:
            self.clock -= 1

    def time(self):
        return self.clock
    
    def gotoZero(self):
        self.clock = 0

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


global mainMap
mainMap = []

MainClock = pygame.time.Clock()

GameClock1 = clock(60, 0)

redCE = [14, 0]
blueCE = [0, 14]

global who, steps, gameStart
who = 'red'
gameStart = True
steps = 0
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Check():
    global mainMap
    QWQ = 0
    while QWQ <= 25:
        ln2 = random.randint(0, 14) * 15 + random.randint(0, 14)
        if mainMap[ln2] == False or redCE[0] * 15 + redCE[1] == ln2 or blueCE[0] * 15 + blueCE[1] == ln2:
            continue
        QWQ += 1
        mainMap[ln2] = False

def main_init():
    global PUZZLETUPLE, mainMap
    window.fill((255, 255, 255))
    for i in range(0, 401):
        ln = []
        mainMap.append(ln)
    for i in range(1, 401):
        if i > 1:
            mainMap[i].append(i - 1)
        if i > 20:
            mainMap[i].append(i - 20)
        if i < 400:
            mainMap[i].append(i + 1)
        if i < 390:
            mainMap[i].append(i + 10)
    ln = []

    for i in range(0, 15):
        for j in range(0, 15):
            ln.append((i, j))
    PUZZLETUPLE = tuple(ln)
    ln = []
    ln1 = []
    for i in range(0, 15):
        for j in range(0, 15):
            ln.append( True )
    mainMap = ln
    Check()


    


def CECE(LIST):
    LIST = list(LIST)
    lnx = LIST[0] * 50
    lny = LIST[1] * 50
    return [lnx, lny]


def printALL(LIST):
    global PUZZLETUPLE, mainMap
    for i in range(0, 225):
        if mainMap[i] == True:
            window.blit(PUZZLE, CECE(PUZZLETUPLE[i]))
    if who == 'red':
        window.blit(RED, CECE([LIST[0] - 1, LIST[1]]))
        window.blit(RED, CECE([LIST[0], LIST[1] - 1]))
        window.blit(RED, CECE([LIST[0] + 1, LIST[1]]))
        window.blit(RED, CECE([LIST[0], LIST[1] + 1]))
    if who == 'blue':
        window.blit(BLUE, CECE([LIST[0] - 1, LIST[1]]))
        window.blit(BLUE, CECE([LIST[0], LIST[1] - 1]))
        window.blit(BLUE, CECE([LIST[0] + 1, LIST[1]]))
        window.blit(BLUE, CECE([LIST[0], LIST[1] + 1]))
    window.blit(FLAGr, CECE(redCE))
    window.blit(FLAGb, CECE(blueCE))


def mian():
    main_init()
    while True:
        global who, steps, gameStart

        if redCE == blueCE:
            if who == 'red':
                print( 'Red won' )
                os.system('pause')
            else:
                print( 'Blue won' )
                os.system('pause')
            pygame.quit()
            exit()
        window.fill((255, 255, 255))
        if who == 'red':
            printALL(redCE)
        else:
            printALL(blueCE)
        MainClock.tick(60)
        GameClock1.transform()
        if GameClock1.time() == TIMED//2 and gameStart == True:
            for i in range(0, 14):
                for j in range(0, 15):
                    mainMap[i * 15 + j] = True
            for i in range(1, 25):
                mainMap[random.randint(0, 14) * 15 + random.randint(0, 14)] = False
            who = 'blue'
            GameClock1.gotoZero()
            gameStart = False
        if GameClock1.time() == TIMED:
            for i in range(0, 14):
                for j in range(0, 15):
                    mainMap[i * 15 + j] = True
            Check()
            GameClock1.gotoZero()
            if who == 'red':
                who = 'blue'
            else:
                who = 'red'
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    exit()
            if event.type == KEYDOWN:
                    if event.key == K_w and redCE[1] > 0 and mainMap[redCE[0] * 15 + redCE[1] - 1] == True:
                        redCE[1] -= 1
                    if event.key == K_a and redCE[0] > 0 and mainMap[(redCE[0] - 1) * 15 + redCE[1]] == True:
                        redCE[0] -= 1
                    if event.key == K_s and redCE[1] < 14 and mainMap[redCE[0] * 15 + redCE[1] + 1] == True:
                        redCE[1] += 1
                    if event.key == K_d and redCE[0] < 14 and mainMap[(redCE[0] + 1) * 15 + redCE[1]] == True:
                        redCE[0] += 1
                    if event.key == K_UP and blueCE[1] > 0 and mainMap[blueCE[0] * 15 + blueCE[1] - 1] == True:
                        blueCE[1] -= 1
                    if event.key == K_LEFT and blueCE[0] > 0 and mainMap[(blueCE[0] - 1) * 15 + blueCE[1]] == True:
                        blueCE[0] -= 1
                    if event.key == K_DOWN and blueCE[1] < 14 and mainMap[blueCE[0] * 15 + blueCE[1] + 1] == True:
                        blueCE[1] += 1
                    if event.key == K_RIGHT and blueCE[0] < 14 and mainMap[(blueCE[0] + 1) * 15 + blueCE[1]] == True:
                        blueCE[0] += 1
                    
        pygame.display.update()

if __name__ == '__main__':
    mian()
