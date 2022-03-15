import random
import sys
import pygame
from pygame.locals import *
FPS =  32
SCREENWIDTH = 400
SCREENHEIGHT = 400
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY= SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUND = {}
PLAYER = 'Gallery/sprites/bird.png'
BACKGROUND = 'Gallery/sprites/background.jpg'
PIPE = 'Gallery/sprites/pipe.png'

def welcomeScreen():
    playerx= int(SCREENWIDTH/5)
    playery= int((SCREENHEIGHT)- GAME_SPRITES['player'].get_height()/2)
    #SCREEN.blit(GAME_SPRITES['message'], (0, 0))
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type ==KEYDOWN and (event.key == K_SPACE or event.key== K_UP):
                return
            else:
                #SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (0, 0))
                #SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score=0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    # messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    # messagey = int(SCREENHEIGHT*0.13)
    basex = 0

    #create 2 pipes for blitting
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes=[
        {'x': SCREENWIDTH+200, 'y': newPipe1[0]['y'] },
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newPipe2[0]['y']},
    ]
    lowerPipes=[
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8
    playerFlapped =False


    while True:
        for event in pygame.event.get():
            if event.type== QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery > 0:
                    playerVelY= playerFlapAccv
                    playerFlapped = True
                    GAME_SOUND['wing'].play()

        crashTest= isCollide(playerx,playery,upperPipes,lowerPipes)
        if crashTest:
              return


        #check score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 8:
                score+=1
                print(f"Your Score Is {score}")
                GAME_SOUND['point'].play()

            if playerVelY < playerMaxVelY and not playerFlapped:
                playerVelY+=playerAccY
            if playerFlapped:
                playerFlapped = False
            playerHeight= GAME_SPRITES['player'].get_height()
            playery= playery+ min(playerVelY, GROUNDY- playery-playerHeight+15)

            #move pipe to left
            for upperpipe,lowerpipe in zip(upperPipes,lowerPipes):
                upperpipe['x']+=pipeVelX
                lowerpipe['x'] += pipeVelX

            if 0 <upperPipes[0]['x'] < 5:
                newpipe= getRandomPipe()
                upperPipes.append(newpipe[0])
                lowerPipes.append(newpipe[1])

            if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
                    upperPipes.pop(0)
                    lowerPipes.pop(0)

            #lets blit the sprites
            SCREEN.blit(GAME_SPRITES['background'],(0,0))
            for upperpipe, lowerpipe in zip(upperPipes, lowerPipes):
                SCREEN.blit(GAME_SPRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
                SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))
            SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
            SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))

            myDigits=[int(x) for x in list(str(score))]
            width=0
            for digit in myDigits:
                width+=GAME_SPRITES['numbers'][digit].get_width()
            Xoffset= (SCREENWIDTH-width)/2

            for digit in myDigits:
                SCREEN.blit(GAME_SPRITES['numbers'][digit],(Xoffset,SCREENHEIGHT*0.11))
                Xoffset+=GAME_SPRITES['numbers'][digit].get_width()
            pygame.display.update()
            FPSCLOCK.tick(FPS)

def isCollide(playerx,playery,upperPipes,lowerPipes):

    if playery > GROUNDY-50 or playery<0:
       GAME_SOUND['hit'].play()
       pygame.display.update()
       return True

    for pipe in upperPipes:
         pipeHeight= GAME_SPRITES['pipe'][0].get_height()
         if (playery< pipeHeight+ pipe['y'] and abs(playerx - pipe['x'])<GAME_SPRITES['pipe'][0].get_width()):
             GAME_SOUND['hit'].play()

             return True

    for pipe in lowerPipes:
         if (playery+GAME_SPRITES['player'].get_height() > pipe['y'] and abs(playerx - pipe['x'])<GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUND['hit'].play()
            return True

    return False








def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.3*offset))
    pipeX = SCREENWIDTH +10
    y1 = pipeHeight - y2 + offset
    pipe=[
        {'x': pipeX, 'y':-y1},
        {'x': pipeX, 'y': y2}
        ]
    return pipe






if __name__ == '__main__':
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird game by AAROHI')
    GAME_SPRITES['numbers']=(
        pygame.image.load('Gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/9.png').convert_alpha()
    )
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert_alpha()

    GAME_SPRITES['message'] = pygame.image.load('Gallery/sprites/message.gif').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('Gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
    pygame.image.load(PIPE).convert_alpha().convert_alpha()
     )

    GAME_SOUND['die'] = pygame.mixer.Sound('Gallery/audio/die.wav')
    GAME_SOUND['hit'] = pygame.mixer.Sound('Gallery/audio/hit.wav')
    GAME_SOUND['point'] = pygame.mixer.Sound('Gallery/audio/point.wav')
    GAME_SOUND['swoosh'] = pygame.mixer.Sound('Gallery/audio/swoosh.wav')
    GAME_SOUND['wing'] = pygame.mixer.Sound('Gallery/audio/wing.wav')

    GAME_SOUND['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()
        mainGame()









