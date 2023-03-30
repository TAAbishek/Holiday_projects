import pygame
import random
from pygame import mixer

pygame.init()
screen=pygame.display.set_mode((800,600))

#background
background=pygame.image.load("Background.png")
#background music
mixer.music.load("background.wav")
mixer.music.play(-1)

pygame.display.set_caption("Space Invaders")
icon=pygame.image.load("space-shuttle.png")
pygame.display.set_icon(icon)

#scoreboard
player_score=[0]
font=pygame.font.Font("freesansbold.ttf",32)
gameover_font=pygame.font.Font("freesansbold.ttf",64)
#player
player_img=pygame.image.load('Player.png')
player_x=370;x_change=0
player_y=500;y_change=0

#enemy

enemy_img=pygame.image.load('Enemy.png')
enemy_x=[];enemy_xchange=[]
enemy_y=[];enemy_ychange=30
for i in range(6):
    enemy_x.append(random.randint(0,800)); enemy_xchange.append(2)
    enemy_y.append(random.randint(50,150));
    
#bullet
bullet_img=pygame.image.load('Bullet.png')
bullet_x=[player_x,player_x,player_x]
bullet_y=[480,480,480];bullet_ychange=7.5
g_bullet_state=['ready',"ready",'ready']

running=True
#writes spaceship position on screen
def gameover():
    gameover_text=gameover_font.render("GAME OVER ",True,(255,255,255))
    for j in range(6):
        enemy_y[j]=4000
    screen.blit(gameover_text,(200,240))
def score():
    score=font.render('Score :'+ str(player_score[0]),True,(255,255,255))
    screen.blit(score,(10,10))
def player(x,y):
    screen.blit(player_img,(x,y))

def enemy(x,y):
    for i in range(6):
        screen.blit(enemy_img,(x[i],y[i]))
def bullet(bullet_x,bullet_y):
    for i in range(3):
        if g_bullet_state[i]=='fire':
            screen.blit(bullet_img,(bullet_x[i]+16,bullet_y[i]))

def isCollision(bullet_x,bullet_y,enemy_x,enemy_y):
    
    for i in range(3):
        for j in range(6):
            x,y=bullet_x[i],bullet_y[i]
            d=((enemy_x[j]-x)**2 + (enemy_y[j]-y)**2)**0.5
            #print(d,x,y)
            if d<50:
                collision_sound=mixer.Sound("explosion.wav")
                collision_sound.play()
                #print('collision bro')
                player_score[0]+=1
                bullet_y[i]=480
                g_bullet_state[i]="ready"
                enemy_y[j]=random.randint(50,150)
                enemy_x[j]=random.randint(0,800)
        
while running:
    
    screen.fill((0,0,128))
    screen.blit(background,(0,0))
    #input left or right 
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                x_change-=2.5
            if event.key==pygame.K_RIGHT:
                x_change+=2.5
            if event.key==pygame.K_SPACE:
                for i in range(3):
                    if g_bullet_state[i]=='ready':
                        g_bullet_state[i]='fire'
                        bullet_sound=mixer.Sound("laser.wav")
                        bullet_sound.play()
                        bullet_x[i]=player_x
                        break
        if event.type==pygame.KEYUP:
            x_change=0
    
            
    #player Boundary
    player_x+=x_change
    if player_x<=0:
        player_x=0
    elif player_x>=736:
        player_x=736
    #enemy Boundary
    for j in range(6):
        enemy_x[j]+=enemy_xchange[j]
        if enemy_x[j]<=0:
            enemy_x[j]=0
            enemy_xchange[j]=+2
            enemy_y[j]+=enemy_ychange
        elif enemy_x[j]>=736:
            enemy_x[j]=736
            enemy_xchange[j]=-2
            enemy_y[j]+=enemy_ychange
        if enemy_y[j]>=200:
            gameover()
    
    #bullet boundary
    for i in range(3):
        if g_bullet_state[i]=='fire':
            bullet_y[i]-=bullet_ychange

            if bullet_y[i]<=32:
                g_bullet_state[i]='ready'
                bullet_y[i]=480
        
    score()        
    player(player_x,player_y)
    enemy(enemy_x,enemy_y)
    bullet(bullet_x,bullet_y)
    isCollision(bullet_x,bullet_y,enemy_x,enemy_y)
    pygame.display.update()
    
            