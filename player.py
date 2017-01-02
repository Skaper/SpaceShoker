#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import pyganim
import os
font.init()
try:
    import serial
except:
    print "Serial Error"
#port = serial.Serial('/dev/ttyACM0', baudrate=115200, dsrdtr=1, timeout=3.0)
port = ""
MOVE_SPEED = 10
WIDTH = 35
HEIGHT = 50
COLOR = "#888888"
JUMP_POWER = 12
GRAVITY = 0.3 # Сила, которая будет тянуть нас вниз
ANIMATION_DELAY = 0.1  # скорость смены кадров
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами

ANIMATION_RIGHT = [('%s/texture/cr0/runr0.png' % ICON_DIR),
                  ('%s/texture/cr0/runr1.png' % ICON_DIR),
                  ('%s/texture/cr0/runr2.png' % ICON_DIR),
                  ('%s/texture/cr0/runr3.png' % ICON_DIR),
                  ('%s/texture/cr0/runr4.png' % ICON_DIR),
                  ('%s/texture/cr0/runr5.png' % ICON_DIR),
                  ('%s/texture/cr0/runr6.png' % ICON_DIR)]
ANIMATION_LEFT = [('%s/texture/cr0/runl0.png' % ICON_DIR),
                  ('%s/texture/cr0/runl1.png' % ICON_DIR),
                  ('%s/texture/cr0/runl2.png' % ICON_DIR),
                  ('%s/texture/cr0/runl3.png' % ICON_DIR),
                  ('%s/texture/cr0/runl4.png' % ICON_DIR),
                  ('%s/texture/cr0/runl5.png' % ICON_DIR),
                  ('%s/texture/cr0/runl6.png' % ICON_DIR)]
ANIMATION_JUMP_LEFT = [('%s/texture/cr0/jumpl0.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP_RIGHT = [('%s/texture/cr0/jumpr0.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP = [('%s/texture/cr0/jumpl0.png' % ICON_DIR, 0.1)]
ANIMATION_STAY = [('%s/texture/cr0/stayr0.png' % ICON_DIR, 0.1)]


class Player(sprite.Sprite):
    def __init__(self, x, y, total_level_width, volumeEffects, port="", shockerLvl="low"):
        self.volumeEffects = volumeEffects
        self.levelWidth = total_level_width
        self.godMode = False
        self.point = 0
        self.port = port
        self.shockerLevel = shockerLvl
        sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.teleportGo = False
        self.tempX = x
        self.tempY = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.image2 = Surface((WIDTH, HEIGHT))
        self.rect = Rect(x+10, y+10, WIDTH-10, HEIGHT-10)  # прямоугольный объект
        self.image.set_colorkey(Color(COLOR))  # делаем фон прозрачным
        #self.rect = self.image.get_rect(center=(10, 10))
        self.freezing = False #Блокировка движения персонажа
        self.time_freezing = time.get_ticks()
        self.time_freezing_Wait = 1000
        self.time_freezing_last = 0

        self.inKiller = False  # Получение урона
        self.time_killer= time.get_ticks()
        self.time_killer_Wait = 500


        #        Анимация движения вправо
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        #        Анимация движения влево
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))  # По-умолчанию, стоим

        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()

        self.isCollide = False

        self.shokPoint = 0

        #self.shokPointFont = font.Font('%s/fonts/3X5.TTF' % ICON_DIR, 65)
        self.platformTempPos = 0.0
        self.shockSound0 = mixer.Sound("%s/sound/shock1.wav" % ICON_DIR)
        self.shockSound0.set_volume(self.volumeEffects)



    def update(self, left, right, up, platforms): #update(self, left, right, up, platforms, killers, movment):
        if self.rect.x<0: #Не движемся за карту с лева
            self.rect.x = 0
        if self.rect.x>(self.levelWidth-51): #Не двиижимся за карту справа
            self.rect.x = self.levelWidth-51
        if self.freezing == False:
            if up:
                if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                    self.yvel = -JUMP_POWER
                self.image.fill(Color(COLOR))
                self.boltAnimJump.blit(self.image, (0, 0))

            if left:
                self.xvel = -MOVE_SPEED  # Лево = x- n
                self.image.fill(Color(COLOR))
                if up:  # для прыжка влево есть отдельная анимация
                    self.boltAnimJumpLeft.blit(self.image, (0, 0))
                else:
                    self.boltAnimLeft.blit(self.image, (0, 0))

            if right:
                self.xvel = MOVE_SPEED  # Право = x + n
                self.image.fill(Color(COLOR))
                if up:
                    self.boltAnimJumpRight.blit(self.image, (0, 0))
                else:
                    self.boltAnimRight.blit(self.image, (0, 0))

            if not (left or right):  # стоим, когда нет указаний идти
                self.xvel = 0
                if not up:
                    self.image.fill(Color(COLOR))
                    self.boltAnimStay.blit(self.image, (0, 0))

            if not self.onGround:
                self.yvel += GRAVITY
                #self.image.fill(Color(COLOR))
                #self.boltAnimJump.blit(self.image, (0, 0))

            self.onGround = False;  # Мы не знаем, когда мы на земле((
            self.rect.y += self.yvel

            self.collide(0, self.yvel, platforms) #self.collide(0, self.yvel, platforms, killers, movment)

            self.rect.x += self.xvel  # переносим свои положение на xvel
            self.collide(self.xvel, 0, platforms) #self.collide(self.xvel, 0, platforms, killers, movment)



        #else:
            #if time.get_ticks() - self.time_freezing > self.time_freezing_Wait:
                #self.freezing = False
            #else:
            #    self.teleport.update()
            #    print "teleport"
        if self.teleportGo:
            if self.rect.x < 1100:
                self.rect.x = self.startX
                self.rect.y = self.startY
                self.freezing = False
                self.teleportGo = False
            else:
                if self.rect.x + 1000 > self.tempX:
                    self.rect.x -= 10
                    #self.teleport.update()
                else:
                    self.freezing = False
                    self.teleportGo = False

    def goStart(self):
        #TODO замедлить телепорт
        #self.freezing =True
        self.teleport = Teleport(self.rect.x+50, self.rect.y+50)
        self.tempX = self.rect.x
        self.tempY = self.rect.y
        #if self.rect.x < 800:
        #    self.rect.x = self.startX
        #    self.rect.y = self.startY
        #else:
        #    self.rect.x -=800
        #    self.rect.y = -100


    def setGod(self, mode):
        self.godMode = mode

    def getPoint(self):
        return self.shokPoint, self.point
    def collide(self, xvel, yvel, platforms): #collide(self, xvel, yvel, platforms, killers, movment):
        for p in sprite.spritecollide(self, platforms, 0):
            #if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

            typeIs = p.getData()
            if typeIs == "platforn":
                self.isCollide = True

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left #- 3  # то не движется вправо
                    self.onGround = True
                    self.yvel = -2#0.5
                    self.rect.y -=1
                    self.platformTempPos +=0.2
                    if self.platformTempPos >=1.0:
                        p.rect.y +=self.platformTempPos
                        p.rect.x +=self.platformTempPos
                        self.platformTempPos = 0.0
                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево
                    self.onGround = True
                    self.yvel = -2#0.5
                    self.rect.y -= 1
                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает
                    p.rect.y +=3 #Опускаем платформу

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom+2  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает
                if not p.colorIsChange:
                    self.point+=5
                p.update()

            if typeIs == "kill_shock1":  
                self.shockSound0.play(0)
                if self.port != "":
                    if self.shockerLevel == 'low':
                        self.port.write("T2>1\n")
                    if self.shockerLevel == 'high':
                        self.port.write("T1>1\n")
                if xvel > 0:  # если движется вправо
                    # self.rect.x += 16
                    # self.freezing = True
                    # self.rect.x += 32
                    # self.rect.x += 64
                    if time.get_ticks() - self.time_killer > self.time_killer_Wait:
                        self.shokPoint += 1
                        self.time_killer = time.get_ticks()
                    break
                if xvel < 0:  # если движется влево
                    if time.get_ticks() - self.time_killer > self.time_killer_Wait:
                        self.shokPoint += 1
                        self.time_killer = time.get_ticks()
                    # self.rect.x -= 32
                    # self.freezing = True
                    # self.rect.x -= 32
                    break
                if yvel > 0:  # если падает вниз
                    if time.get_ticks() - self.time_killer > self.time_killer_Wait:
                        self.shokPoint += 1
                        self.time_killer = time.get_ticks()
                    # self.freezing = True
                    # self.rect.x -= 32

                if yvel < 0:  # если движется вверх
                    if time.get_ticks() - self.time_killer > self.time_killer_Wait:
                        self.shokPoint += 1
                        self.time_killer = time.get_ticks()
                    break
                    # self.freezing = True
                    # self.rect.x += 32

            elif typeIs == "kill_move1":
                if not self.godMode:
                    self.freezing =True
                    self.goStart()
                    self.teleportGo = True
            elif typeIs == "rocket":
                p.setEndLevel()



class Teleport(sprite.Sprite):
    def __init__(self, x, y):
        PLATFORM_WIDTH = 50  # 32
        PLATFORM_HEIGHT = 50
        ANIMATION= [('%s/texture/portal/teleport.png' % ICON_DIR),
                          ('%s/texture/portal/teleport1.png' % ICON_DIR),
                          ('%s/texture/portal/teleport2.png' % ICON_DIR)]

        ANIMATION_DELAY = 0.700


        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color("#888888"))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)  # прямоугольный объект
        self.image.set_colorkey(Color("#888888"))  # делаем фон прозрачным

        boltAnim = []
        for anim in ANIMATION:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)

        self.boltAnimLeft.play()
        self.boltAnimLeft.blit(self.image, (0, 0))
    def update(self):

        self.image.fill(Color("#888888"))
        self.boltAnimLeft.blit(self.image, (0, 0))
