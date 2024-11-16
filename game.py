import pygame
from pygame.locals import *
import random
pygame.init()
clock=pygame.time.Clock()
fps=60
screen=pygame.display.set_mode((800,700))
pygame.display.set_caption('Flappy bird')
ground_scroll=0
scroll_speed=4
playing=True
pipefrequency=1500
lastpipe=pygame.time.get_ticks()-pipefrequency
scroll=0
pass_pipe=False
score=0
gameover=False

bird1=pygame.image.load('bird1.png')
bird2=pygame.image.load('bird2.png')
bird3=pygame.image.load('bird3.png')
gameoverimg=pygame.image.load('gameover.jpg')
gameoverimg1=pygame.transform.scale(gameoverimg,(200,200))

background=pygame.image.load('backgroundimg.png')
ground=pygame.image.load('ground.png')
class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[bird1,bird2,bird3]
        self.index=0
        self.counter=0
        self.image=self.images[self.index]
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.vel=0
        self.clicked=False
    def update(self):
        self.vel=self.vel+0.5
        if self.vel>8:
            self.vel=8
        if self.rect.bottom<650:
            self.rect.y+=int(self.vel)
        #detecting left click
        if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
            self.vel=-10
            self.clicked=True
        if pygame.mouse.get_pressed()[0]==0:
            self.clicked=False
        self.counter=self.counter+1
        if self.counter>5:
            self.counter=0
            self.index+=1
            if self.index>2:
                self.index=0
        self.image=self.images[self.index]
        self.image=pygame.transform.rotate(self.images[self.index], self.vel*-2)

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('pipe.png')
        self.rect=self.image.get_rect()
        if position==1:
            self.image=pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft=[x,y-75]
        if position==-1:
            self.rect.topleft=[x,y+75]
    def update(self):
        self.rect.x-=scroll_speed
        if self.rect.right<0:
            self.kill()


bird_group=pygame.sprite.Group()
flappy=Bird(100,250)
bird_group.add(flappy)
pipe_group=pygame.sprite.Group()


while playing:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            playing=False
    clock.tick(fps)
    screen.blit(background,(0,0))
    bird_group.draw(screen)
    pipe_group.draw(screen)
    bird_group.update()
    screen.blit(ground,(ground_scroll,650))
    if gameover==False:    
        ground_scroll=ground_scroll-4
        if abs(ground_scroll)>35:
            ground_scroll=0
        time_now=pygame.time.get_ticks()
        if time_now-lastpipe>pipefrequency:
            pipe_height=random.randint(-100,100)
            bottompipe=Pipe(800,350+pipe_height,-1)
            toppipe=Pipe(800,350+pipe_height,1)
            pipe_group.add(bottompipe)
            pipe_group.add(toppipe)
            lastpipe=time_now
    
        pipe_group.update()

    if len(pipe_group)>0:
        if bird_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.left\
             and bird_group.sprites()[0].rect.right<pipe_group.sprites()[0].rect.right and pass_pipe==False:
            pass_pipe=True
        if pass_pipe==True:
            if bird_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.right:
                score=score+1
                pass_pipe=False
    font=pygame.font.SysFont('Bauhaus 93', 60)
    text=font.render('Score'+str(score),True,(15, 1, 1))
    screen.blit(text,(10,10))
    
    if flappy.rect.bottom>=650:
        gameover=True
    if gameover==True:
        pipe_group.empty()
        screen.blit(gameoverimg1,(300,280))
    if pygame.sprite.groupcollide(pipe_group,bird_group,False,False):
        gameover=True

    

    pygame.display.update()

