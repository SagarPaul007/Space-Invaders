import pygame
from pygame import mixer
import math
import random

# Initialising pygame
pygame.init()

#setting up screen
screen=pygame.display.set_mode((800,600))

#sound
mixer.music.load("background.mp3")
mixer.music.play(-1)

#Title and icon 
pygame.display.set_caption("Space Invaders by Sagar Paul")
icon=pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#background
background=pygame.image.load("background.png")

#player
playerImg=pygame.image.load("spaceship.png")
playerX= 370
playerY=520
playerX_change= 0
# playerY_change= 0

#enemy
enemyImg=[]
enemyX = []
enemyY = []
enemyX_change= []
enemy_speed=4
enemyY_change= []
total_enemy=5
for i in range(total_enemy):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(30,150))
    enemyX_change.append (enemy_speed)
    enemyY_change.append(30)


#bullet
bulletImg=pygame.image.load("bullet.png")
bulletX= 0 
bulletY= 460
bullet_state= "ready"
bulletY_change= -10

#score
score_value = 0
font= pygame.font.Font('freesansbold.ttf', 16)

textX = 10
textY = 10

#life
life_value = 3
font= pygame.font.Font('freesansbold.ttf', 16)

lifeX = 740
lifeY = 10

#game over
over_font=pygame.font.Font('freesansbold.ttf', 70)

#collison
def isCollison(enemyX, enemyY, bulletX, bulletY):
    distance= math.sqrt((math.pow(enemyX-bulletX,2))+ (math.pow(enemyY-bulletY,2)))
    if distance<27:
        return True
    else:
        return False

def show_score(x,y):
    score= font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))  #score function

def show_life(x,y):
    life= font.render("life: " + str(life_value), True, (255,255,255))
    screen.blit(life, (x,y))  #life function

def player(x,y):
    screen.blit(playerImg, (x, y)) #player function

def enemy(x,y, i):
    screen.blit(enemyImg[i], (x, y)) #enemy function

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 17, y + 40)) #bullet function

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250)) #game over function

#Game loop
running=True
while running:
    screen.fill((0,0,0))

    #adding background image
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        #moving player in directions
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change= -3
            if event.key==pygame.K_RIGHT:
                playerX_change= 3
            # if event.key==pygame.K_UP:
            #     playerY_change= -4
            # if event.key==pygame.K_DOWN:
            #     playerY_change= 4

            if event.key==pygame.K_SPACE or event.key==pygame.K_UP:
                if bullet_state=="ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_state= "fire"
                

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change= 0
            if event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                playerY_change= 0

    #moving player in x-y axis
    playerX += playerX_change
    # playerY += playerY_change

    #setting up player boundaries
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736
    # elif playerY<=0:
    #     playerY=0
    # elif playerY>=550:
    #     playerY=550



    #setting up enemy boundaries
    for i in range(total_enemy):

        #game ove happening state
        if life_value<=0:
            for j in range(total_enemy):
                enemyY[j]=2000
            game_over_text()
            game_over_sound = mixer.Sound("game_over.wav")
            game_over_sound.play()
            break

        #moving enemy in x-y axis
        enemyX[i]+= enemyX_change[i]

        if enemyX[i]<=0:
            enemyX_change[i]= enemy_speed
            enemyY[i]+= enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i]= -enemy_speed
            enemyY[i]+= enemyY_change[i]

        elif enemyY[i]>=400:
            enemyX[i]=random.randint(0,736)
            enemyY[i]=random.randint(30,150)
            life_value-=1

        
        #collison
        collison = isCollison(enemyX[i], enemyY[i], bulletX, bulletY)
        if collison:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY=460
            bullet_state = "ready"
            enemyX[i]=random.randint(0,736)
            enemyY[i]=random.randint(30, 150)
            score_value+=1

        enemy(enemyX[i], enemyY[i], i)


    #bullet  movement

    if bulletY<= 0:
        bullet_state="ready"
        bulletY= 460

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY += bulletY_change

    #speed increasing of enemy

    if score_value>=10:
        enemy_speed=5
    elif score_value>=20:
        enemy_speed=6
    elif score_value>=30:
        enemy_speed=7
    elif score_value>=40:
        enemy_speed=8
    elif score_value>=50:
        enemy_speed=9

    player(playerX, playerY)
    show_score(textX, textY)
    show_life(lifeX, lifeY)

    pygame.display.update()
