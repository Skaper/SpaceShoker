#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame.locals import *
import pyganim

from pygame import *
from pygame import gfxdraw

import os
import random

ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами
PLATFORM_WIDTH = 50  # 32
PLATFORM_HEIGHT = 50
"""
class Background(sprite.Sprite):
    def __init__(self, x, y):
        PLATFORM_COLOR = "#FFFFFF"
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/texture/back.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
"""

class Platform(sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.romb = [(random.randint(5, 28),0),(random.randint(30, 41),0),(49,random.randint(20, 35)),
                     (49,random.randint(30, 35)),(random.randint(20, 50),49),
                     (random.randint(0, 45),49),(0,40),
                     (0,random.randint(20, 35)),(random.randint(5, 27),0)]#[(27,0),(40,0),(49,27),(49,40),(40,49),(27,49),(0,40),(0,27),(27,0)]#[(9,0),(22,0),(31,9),(31,22),(22,31),(9,31),(0,22),(0,9),(9,0)]
        self.romb_MIN = [(11, 7), (20, 7), (24, 11), (24, 19), (20, 23), (11, 23), (7, 19), (7, 11), (11, 7)]#0[(11, 7), (20, 7), (24, 11), (24, 19), (20, 23), (11, 23), (7, 19), (7, 11), (11, 7)]
        self.colorIsChange = False
        PLATFORM_COLOR = "#d6d7e1"
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.imageMini = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        #self.image.fill(Color(PLATFORM_COLOR))
        self.maxi = draw.polygon(self.image, Color(PLATFORM_COLOR), self.romb)  #
        self.image.set_colorkey(Color("#000000"))
        self.mini = draw.polygon(self.image, Color("#96969B"), self.romb_MIN)
        self.rect = self.image.get_rect(center=(x, y))
        #self.image = iage.load("%s/texture/block.png" % ICON_DIR)

        #texture = self.tile_texture(image.load("%s/texture/moon0.png" % ICON_DIR), (PLATFORM_WIDTH, PLATFORM_HEIGHT))

        #mask = pygame.Surface(SIZE, depth=8)
        # Create sample mask:
        #self.image = self.apply_alpha(texture, self.image)

        #self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


        self.timeIsUpdate = False  # Обновление цвета
        self.time_update= time.get_ticks()
        self.time_update_Wait = 500
        self.angleRot = 0
    def getData(self):
        return "platforn"

    def update(self):


        if time.get_ticks() - self.time_update >  self.time_update_Wait:

            r = lambda: random.randint(0, 255)
            color = '#%02X%02X%02X' % (r(), r(), r())
            #self.image.fill(Color(color))
            draw.polygon(self.image, Color(color), self.romb_MIN)
            self.time_update = time.get_ticks()
            self.colorIsChange = True

        self.image = self.rot_center(self.image, 10)
        #self.rect = self.image.get_rect(center=(self.x, self.y))

    def getPoint(self):
        return self.colorIsChange
    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = self.rect
        rot_image = transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image



    def tile_texture(self, texture, size):
        result = Surface(size, depth=32)
        for x in range(0, size[0], texture.get_width()):
            for y in range(0, size[1], texture.get_height()):
                result.blit(texture, (x, y))
        return result

    def apply_alpha(self, texture, mask):
        """
        Image should be  a 24 or 32bit image,
        mask should be an 8 bit image with the alpha
        channel to be applied
        """
        texture = texture.convert_alpha()
        target = surfarray.pixels_alpha(texture)
        target[:] = surfarray.array2d(mask)
        # surfarray objets usually lock the Surface.
        # it is a good idea to dispose of them explicitly
        # as soon as the work is done.
        del target
        return texture

    def stamp(self, image, texture, mask):
        image.blit(self.apply_alpha(texture, mask), (0, 0))


class PlatformText(sprite.Sprite):
    def __init__(self, x, y, text):
        romb = [(9,0),(22,0),(31,9),(31,22),(22,31),(9,31),(0,22),(0,9),(9,0)]
        PLATFORM_COLOR = "#FFFFFF"
        sprite.Sprite.__init__(self)
        self.font = font.SysFont("Arial", 33)
        self.image = self.font.render(str(text), 1, Color(PLATFORM_COLOR))

        #self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))

        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def getData(self):
        return "pass"
    def update(self):
        pass

class Rocket(sprite.Sprite):
    def __init__(self, x, y):
        self.endLevel = False
        self.inRocket = False
        PLATFORM_COLOR = "#d6d7e1"
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))

        self.image.set_colorkey(Color("#000000"))
        self.image = image.load("%s/texture/rocket.png" % ICON_DIR)
        self.rect = Rect(x, y, 150, 200)
    def update(self, hero):
        if self.inRocket:
            #TODO добавить анимацию топлива
            hero.rect.x = self.rect.centerx-25
            hero.rect.y = self.rect.centery
            self.rect.y -=2
            #print self.rect.y
            if self.rect.y < -400:
                self.endLevel = True
    def getData(self):
        return "rocket"
    def setEndLevel(self):
        self.inRocket=True

class KillPlatform1(sprite.Sprite):

    def __init__(self, x, y):
        PLATFORM_WIDTH = 32  # 32
        PLATFORM_HEIGHT = 32
        ANIMATION_FIRE = [('%s/texture/shock1.png' % ICON_DIR),
                          ('%s/texture/shock2.png' % ICON_DIR),
                          ('%s/texture/shock3.png' % ICON_DIR),
                          ('%s/texture/shock4.png' % ICON_DIR),
                          ('%s/texture/shock5.png' % ICON_DIR),
                          ('%s/texture/shock6.png' % ICON_DIR)]
        ANIMATION_STAY = [('%s/texture/shock5.png' % ICON_DIR, 0.1)]
        ANIMATION_DELAY = 0.100


        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color("#888888"))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)  # прямоугольный объект
        self.image.set_colorkey(Color("#888888"))  # делаем фон прозрачным

        boltAnim = []
        for anim in ANIMATION_FIRE:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)

        self.boltAnimLeft.play()
        self.boltAnimLeft.blit(self.image, (0, 0))

    def update(self):

        self.image.fill(Color("#888888"))
        self.boltAnimLeft.blit(self.image, (0, 0))
        #self.boltAnimLeft.stop()
    def getData(self):
        return "kill_shock1"


class KillPlatformMove1(sprite.Sprite):
    def __init__(self, x, y, levelSizeY, moveSpeed=1, levelSizeX=1):
        self.lvlSize_Y = levelSizeY
        self.lvlSize_X = levelSizeX
        self.graviry = levelSizeY*0.00025
        sprite.Sprite.__init__(self)

        PLATFORM_WIDTH = 45  # 32
        PLATFORM_HEIGHT = 25
        ANIMATION_PORTAL = [('%s/texture/portal/portal0.png' % ICON_DIR),
                          ('%s/texture/portal/portal1.png' % ICON_DIR),
                          ('%s/texture/portal/portal2.png' % ICON_DIR),
                          ('%s/texture/portal/portal3.png' % ICON_DIR),
                          ('%s/texture/portal/portal4.png' % ICON_DIR),
                          ('%s/texture/portal/portal5.png' % ICON_DIR),
                            ('%s/texture/portal/portal6.png' % ICON_DIR),
                            ('%s/texture/portal/portal7.png' % ICON_DIR),
                            ('%s/texture/portal/portal8.png' % ICON_DIR),]

        ANIMATION_DELAY = 0.03

        self.yvel = 0
        self.positionX = x
        self.positionY = y
        self.onGround = False
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color("#888888"))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.image.set_colorkey(Color("#888888"))  # делаем фон прозрачным
        boltAnim = []
        for anim in ANIMATION_PORTAL:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)

        self.boltAnimLeft.play()
        self.boltAnimLeft.blit(self.image, (0, 0))

    def update(self):
        self.image.fill(Color("#888888"))
        self.boltAnimLeft.blit(self.image, (0, 0))
        if not self.onGround:
            self.yvel += self.graviry
        else:
            self.yvel -= self.graviry
        self.rect.y += self.yvel
        if self.rect.y<-150:
            self.onGround = False
            self.rect.top =-150  # то не движется вверх
            self.yvel = 0
        if self.rect.y> (self.lvlSize_Y-PLATFORM_WIDTH):
            self.onGround = True
            self.rect.bottom = self.lvlSize_Y-PLATFORM_WIDTH
            self.yvel = 0

    def getData(self):
        return "kill_move1"

class Planet(sprite.Sprite):
    def __init__(self, x, y):

        ANIMATION_PLANET = []
        for name in range(200):
            ANIMATION_PLANET.append((str(ICON_DIR) + '/texture/planet/' + str(name) + '.gif'))
        ANIMATION_DELAY = 0.05

        sprite.Sprite.__init__(self)
        self.image = Surface((500, 333))
        self.image.fill(Color("#888888"))
        self.rect = Rect(x, y, 500, 333)  # прямоугольный объект
        self.image.set_colorkey(Color("#888888"))  # делаем фон прозрачным

        boltAnim = []
        for anim in ANIMATION_PLANET:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)

        self.boltAnimLeft.play()
        self.boltAnimLeft.blit(self.image, (0, 0))
    def update(self):

        self.image.fill(Color("#888888"))
        self.boltAnimLeft.blit(self.image, (0, 0))
        #self.boltAnimLeft.stop()
    def getData(self):
        return "planet"