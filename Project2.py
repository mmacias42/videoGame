# import libraries and modules
# from platform import platform
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint

vec = pg.math.Vector2

# game settings 
WIDTH = 360
HEIGHT = 480
FPS = 30

# player settings
PLAYER_FRIC = -0.2
PLAYER_GRAV = 0.9
#Print empty string until player wins
POINTS = ""

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# defines text and font
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

# sprites...
# player sprite
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((16, 16))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (25, 25)
        self.pos = vec(25, 25)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.hitx = 0
        self.hity = 0
        self.colliding = False

    # definining movement of player with keys
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.y = 0
            self.acc.x = -0.8
        if keys[pg.K_d]:
            self.acc.y = 0
            self.acc.x = 0.8
        if keys[pg.K_w]:
            self.acc.y = -0.8
        if keys[pg.K_s]:
            self.acc.y = 0.8
    # defines result of collisions
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, all_platforms, False)
            if hits:
                self.colliding = True
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                # print("xdif " + str(xdiff))
                # print("ydif " + str(ydiff))
                if hits[0].rect.centerx > self.rect.centerx and xdiff > ydiff:
                    self.pos.x = hits[0].rect.left - self.rect.width/2
                if hits[0].rect.centerx < self.rect.centerx and xdiff > ydiff:
                    self.pos.x = hits[0].rect.right + self.rect.width/2
                self.vel.x = 0
                self.centerx = self.pos.x
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
            else:
                self.colliding = False

        # defines results of colisions
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, all_platforms, False)
            if hits:
                self.colliding = True
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                # print("xdif " + str(xdiff))
                # print("ydif " + str(ydiff))

                if hits[0].rect.centery > self.rect.centery and xdiff < ydiff:
                    self.pos.y = hits[0].rect.top - self.rect.height/2
                if hits[0].rect.centery < self.rect.centery and xdiff < ydiff:
                    self.pos.y = hits[0].rect.bottom + self.rect.height/2
                self.vel.y = 0
                self.centery = self.pos.y
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
            else:
                self.colliding = False
# defines teleportation
    def warp(self):
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT
    def update(self):
        self.acc = vec(0,0)
        self.controls()
        self.warp()
        # friction
        self.rect.center = self.pos

        self.acc += self.vel * PLAYER_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.centerx = self.pos.x
        self.collide_with_walls('x')
        self.rect.centery = self.pos.y
        self.collide_with_walls('y')
        self.rect.center = self.pos
        self.hitx = self.hitx
        self.hity = self.hity


# creates playforms
class Platform(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#creates goal cube
class Mob(Sprite):
    def __init__(self, x, y, w, h, color):
        Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 42
        self.rect.y = HEIGHT - 42
        self.speedx = 0
        self.speedy = 0
        self.inbounds = True
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, all_platforms, False)
            if hits:
                self.colliding = True
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                # print("xdif " + str(xdiff))
                # print("ydif " + str(ydiff))
                if hits[0].rect.centerx > self.rect.centerx and xdiff > ydiff:
                    self.speedx *= -1
                if hits[0].rect.centerx < self.rect.centerx and xdiff > ydiff:
                    self.speedx *= -1
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
            else:
                self.colliding = False

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, all_platforms, False)
            if hits:
                self.colliding = True
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                # print("xdif " + str(xdiff))
                # print("ydif " + str(ydiff))

                if hits[0].rect.centery > self.rect.centery and xdiff < ydiff:
                    self.speedy *= -1
                if hits[0].rect.centery < self.rect.centery and xdiff < ydiff:
                    self.speedy *= -1
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
            else:
                self.colliding = False


    def boundscheck(self):
        if not self.rect.x > 0 or not self.rect.x < WIDTH:
            self.speedx *=-1
        if not self.rect.y > 0 or not self.rect.y < HEIGHT:
            self.speedy *= -1

    def update(self):
        self.boundscheck()
        self.collide_with_walls('x')
        self.collide_with_walls('y')
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        

# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()
  
# create a group for all sprites
all_sprites = pg.sprite.Group()
all_platforms = pg.sprite.Group()
mobs = pg.sprite.Group()

# instantiate classes
player = Player()
platR = Platform(WIDTH - 12.5, 0, 25, HEIGHT)
platL = Platform(-12.5, 0, 25, HEIGHT)
platT = Platform(0, -12.5, WIDTH, 25)
platB = Platform(0, HEIGHT - 12.5, WIDTH, 25)

#Vertical Lines
platV2 = Platform(0.8*WIDTH, 0.1*HEIGHT, 25, 0.9*HEIGHT)
platV1 = Platform(0.1*WIDTH, 0, 25, 0.9*HEIGHT)
platV3 = Platform(0.25*WIDTH, 0.1*HEIGHT, 25, 0.9*HEIGHT)
platV4 = Platform(0.4*WIDTH, 0, 25, 0.9*HEIGHT)
platV5 = Platform(0.55*WIDTH, 0.1*HEIGHT, 25, 0.9*HEIGHT)
platV6 = Platform(0.7*WIDTH, 0, 12.5, 0.9*HEIGHT)


# add instances to groups
all_sprites.add(player)
all_sprites.add(platR)
all_sprites.add(platL)
all_sprites.add(platT)
all_sprites.add(platB)
all_sprites.add(platV2)
all_sprites.add(platV1)
all_sprites.add(platV3)
all_sprites.add(platV4)
all_sprites.add(platV5)
all_sprites.add(platV6)

# all_sprites.add(mob)
all_platforms.add(platR)
all_platforms.add(platL)
all_platforms.add(platT)
all_platforms.add(platB)
all_platforms.add(platV2)
all_platforms.add(platV1)
all_platforms.add(platV3)
all_platforms.add(platV4)
all_platforms.add(platV5)
all_platforms.add(platV6)



for i in range(8):
    # instantiate mob class repeatedly
    m = Mob(randint(0, WIDTH), randint(0,HEIGHT), 25, 25, (randint(0,255), randint(0,255) , randint(0,255)))
    all_sprites.add(m)
    mobs.add(m)
# print(mobs)
# Game loop
running = True
while running:
    # keep the loop running using clock
    dt = clock.tick(FPS)

    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
    
    ############ Update ##############
    # update all sprites
    mobhits = pg.sprite.spritecollide(player, mobs, True)
    #if player reaches goal, shows you won on screen
    if mobhits:
        POINTS = "You Won!"
    all_sprites.update()
    
    ############ Draw ################
    # draw the background screen

    screen.fill(BLACK)
    # draw all sprites
    all_sprites.draw(screen)
    draw_text(str(POINTS), 50, WHITE, WIDTH / 2, HEIGHT / 2)
    


    # buffer - after drawing everything, flip display
    pg.display.flip()

pg.quit()