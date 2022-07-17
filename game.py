from tkinter import CENTER
import pygame
import sys
import numpy as np

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)

clock = pygame.time.Clock()
pygame.init()
size = (900, 650)
screen = pygame.display.set_mode(size)
pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.play(-1)
GRAVITY, t= pygame.USEREVENT+1, 350
pygame.time.set_timer(GRAVITY, t)
boardImage = pygame.image.load("assets/boardTemplate.png")
background = pygame.image.load("assets/background.png")
arcadeFont = pygame.font.Font("assets/ARCADECLASSIC.TTF",30)
arcadeFont2 = pygame.font.Font("assets/ARCADECLASSIC.TTF",80)
scoreTitle = arcadeFont.render("Score",True, (255,255,255))
NextTitle = arcadeFont.render("Next",True, (255,255,255))
GameOver = arcadeFont2.render("Game Over",True, (255,0,0))
figures = [ [1,3,5,7],
            [2,4,5,7],
            [3,5,4,6],
            [3,5,4,7],
            [2,3,5,7],
            [3,5,7,6],
            [2,3,4,5] ]
blockColors = [YELLOW,
    pygame.image.load("assets/mavi.png"),
    pygame.image.load("assets/sari.png"),
    pygame.image.load("assets/turuncu.png"),
    pygame.image.load("assets/yesil.png"),
    pygame.image.load("assets/pembe.png"),
    pygame.image.load("assets/mor.png"),
    pygame.image.load("assets/kirmizi.png")
]
def newBlock(block):
    blockposx = np.array([],dtype=int)
    blockposy = np.array([],dtype=int)
    for i in figures[block]:
            blockposx = np.append(blockposx,int(i%2) + 4)
            blockposy = np.append(blockposy,int(i/2))
    return (blockposx,blockposy)

def rotate(piece,center):
    centerx,centery = center
    piecex,piecey = piece
    for i in range(len(piecex)):
        x = piecey[i] - centery
        y = piecex[i] - centerx
        piecex[i] = centerx - x
        piecey[i] = centery + y

    return piecex,piecey

def gravity(piecey):
    return piecey + 1
def check(board,piece):
    piecex,piecey = piece
    for i in range(len(piecex)):
        if(piecex[i]<0 or piecex[i]>=10 or piecey[i]>=20):
            return 0
        elif(board[piecey[i]][piecex[i]]):
            return 0
    return 1
def checkForTouchDown(board,piece):
    piecex,piecey = piece
    for i in range(len(piecex)):
        try:
            if(board[piecey[i]][piecex[i]] != 0):
                return 0
        except:
            return 0
    return 1

def isFilled(board):
    count = 0
    temp = []
    for i in (range(20)):
        if(np.all(board[i])):
            count += 1
            temp.append(i)
    for i in temp:
        board[i] = 0
        for j in reversed(range(0,i+1)):
            try:
                board[j] = board[j-1]
            except:
                board[1] = board[0]
        board[0] = 0
    return board,count
def checkForGameOver(blockposy):
    return np.any(blockposy<0)

def printTheBoard(board):
    x=0
    y=0
    for rows in board:
        for columns in rows:
            if(columns != 0):
                screen.blit(blockColors[columns],(300 + x*30,25 + y*30, 30, 30))
            x += 1
        x = 0
        y += 1

def main():
    gameOver = False
    gameBoard = np.zeros((20,10),dtype=int)
    score=0
    tempScore = 0
    posx,posy = (0,0)
    colorNum = 1
    nextColorNum = np.random.randint(1,8,dtype=int)
    block = 3
    blockposx = np.array([],dtype=int)
    blockposy = np.array([],dtype=int)
    tempx = np.array([],dtype=int)
    tempy = np.array([],dtype=int)
    blockposx,blockposy = newBlock(block)
    block = np.random.randint(0,32767,dtype=int)%7
    nextblockposx,nextblockposy = newBlock(block)
    while not gameOver:
        scoreText = arcadeFont.render(str(score),True, (255,255,255))
        screen.fill("black")
        screen.blit(background,(0,0))
        screen.blit(boardImage,(294,19))
        screen.blit(scoreTitle, (660,28))
        screen.blit(scoreText, (660,52))
        screen.blit(NextTitle, (660,115))
        for i in range(len(nextblockposx)):
            screen.blit(blockColors[nextColorNum],(710+(nextblockposx[i] - 4)*30,160+nextblockposy[i]*30))
        #pygame.draw.rect(screen, WHITE, (75,15, 150, 300))
        printTheBoard(gameBoard)
        gameBoard,tempScore = isFilled(gameBoard)
        if(tempScore != 0):
            score += (2*tempScore-1)*100
        for i in range(len(blockposx)):
            screen.blit(blockColors[colorNum],(300+blockposx[i]*30,25+blockposy[i]*30))
        
        for event in pygame.event.get():
            key_input = pygame.key.get_pressed() 
            if event.type == pygame.QUIT:
                sys.exit()             
            if key_input[pygame.K_LEFT]:
                tempx = np.empty_like(blockposx)
                tempx[:] = blockposx
                blockposx -= 1
                if(check(gameBoard,(blockposx,blockposy))==0):
                    blockposx[:] = tempx
            if key_input[pygame.K_UP]:
                tempx = np.empty_like(blockposx)
                tempx[:] = blockposx
                tempy = np.empty_like(blockposy)
                tempy[:] = blockposy
                blockposx,blockposy = rotate((blockposx,blockposy),(blockposx[1],blockposy[1]))
                if(check(gameBoard,(blockposx,blockposy))==0):
                    blockposx[:] = tempx
                    blockposy[:] = tempy
            if key_input[pygame.K_RIGHT]:
                tempx = np.empty_like(blockposx)
                tempx[:] = blockposx
                blockposx += 1
                if(check(gameBoard,(blockposx,blockposy))==0):
                    blockposx[:] = tempx
            if key_input[pygame.K_DOWN]:
                tempy = np.empty_like(blockposy)
                tempy[:] = blockposy
                blockposy += 1
                if(check(gameBoard,(blockposx,blockposy))==0):
                    blockposy[:] = tempy
            if event.type == GRAVITY: # is called every 't' milliseconds
                tempy = np.empty_like(blockposy)
                tempy[:] = blockposy
                blockposy = gravity(blockposy)
                if(checkForTouchDown(gameBoard,(blockposx,blockposy))==0):
                    blockposy[:] = tempy
                    for i in range(len(blockposx)):
                        gameBoard[blockposy[i]][blockposx[i]] = colorNum
                    blockposx[:] = nextblockposx
                    blockposy[:] = nextblockposy
                    colorNum = nextColorNum
                    nextColorNum = np.random.randint(1,8,dtype=int)
                    block = np.random.randint(0,32767,dtype=int)%7
                    nextblockposx,nextblockposy = newBlock(block)
                    while(check(gameBoard, (blockposx,blockposy))==0 and not gameOver):
                        blockposy -= 1
                        gameOver = checkForGameOver(blockposy)
            
        gameOver = checkForGameOver(blockposy)
        pygame.display.update()
        clock.tick(60)
    
    pygame.mixer.music.stop()
    screen.blit(GameOver, (265,280))
    pygame.display.update()
    pygame.time.wait(2000)

if __name__ == "__main__":
    main()