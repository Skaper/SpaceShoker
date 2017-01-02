#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
import serial
import time as timerGame
from player import *
from blocks import *
from levelGeneration import  *
font.init()

#from backgroundGeneration import *


# Объявляем переменные
WIN_WIDTH = 1280#1280  # Ширина создаваемого окна
WIN_HEIGHT = 720#720  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#000000"


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func

        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect

    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(150, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)

class Game():
    def __init__(self,xBox, yBox, lvlBlocks, complexity, portName="", shockLevel="low",volumeSound=0.5, volumeEffects=0.3):
        self.volumeSound = volumeSound
        self.volumeEffects = volumeEffects
        self.fps = 60.0
        self.showStatistic = False
        self.heroGod = False
        self.pause = False
        self.pauseMenuLevel = 0
        self.lvlBox_Count = lvlBlocks
        self.lvlBox_x = xBox
        self.lvlBox_y = yBox
        self.complexity = complexity
        if portName !="":
            print portName
            self.portShocker = serial.Serial(portName, baudrate=115200, dsrdtr=1, timeout=3.0)
        else:
            self.portShocker = ""

        self.shockerLevel = shockLevel
        pygame.init()
        pygame.display.set_caption("Space Shocker!")
        self.screen = pygame.display.set_mode(DISPLAY)


        self.defaultFont = font.Font(pygame.font.get_default_font(), 16)
        self.clock = pygame.time.Clock()

        self.starPoint = 0
        self.pointLevel = 0
        self.timer_event = pygame.USEREVENT + 1


    def main(self):

        self.background = Surface((WIN_WIDTH, WIN_HEIGHT))
        self.background.fill(Color(BACKGROUND_COLOR)) #Фон
        if WIN_WIDTH == 1920:
            self.background = image.load("%s/texture/backFullHD.jpg" % ICON_DIR)
        elif WIN_WIDTH == 1280:
            self.background = image.load("%s/texture/back1.jpg" % ICON_DIR)



        #Генерация уровня
        generator = GenerationBlocks(self.lvlBox_x, self.lvlBox_y,
                              self.lvlBox_Count, self.complexity)
        level = generator.getLevelBlocks()

        self.total_level_width = len(level[0][0])*self.lvlBox_Count  * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
        self.total_level_height = len(level[0]) * PLATFORM_HEIGHT  # высоту

        self.camera = Camera(camera_configure, self.total_level_width, self.total_level_height)

        self.hero = Player(64, 64, self.total_level_width,  self.total_level_height, self.volumeEffects,
                           port=self.portShocker, shockerLvl=self.shockerLevel)  # создаем героя по (x,y) координатам
        self.left = self.right = False  # по умолчанию - стоим
        self.up = False

        print " > Длина уровня: %s " %self.total_level_width
        print " > Высота уровня: %s " %self.total_level_height

        if (WIN_HEIGHT > self.total_level_width):
            self.imageBG = Surface((WIN_WIDTH, WIN_HEIGHT - self.total_level_height))
            self.imageBG.fill(Color("#000000"))

        entitiesBlocks = [] #Временное хранилище блоков уровня
        for i in range(self.lvlBox_Count):
            entitiesBlocks.append(pygame.sprite.Group())

        i = 0
        x = y = 0  # координаты
        for block in level:

                for row in block:  # вся строка

                    for col in row:  # каждый символ
                        if col == "*":
                            pfK = KillPlatform1(x, y)
                            entitiesBlocks[i].add(pfK)
                        elif col == "=":
                            pfKM = KillPlatformMove1(x+4, y, self.total_level_height)
                            entitiesBlocks[i].add(pfKM)
                        elif col == "-":
                            xR = random.randint(-10, 21)
                            yR = random.randint(-10, 21)
                            pf = Platform(x+xR, y+yR)
                            entitiesBlocks[i].add(pf)
                        elif col == "R":
                            pf = Rocket(x, y)
                            entitiesBlocks[i].add(pf)
                        elif type(col) == int:
                            pf = PlatformText(x, y, col)
                            entitiesBlocks[i].add(pf)

                        x =x + PLATFORM_WIDTH   # блоки платформы ставятся на ширине блоков
                    y += PLATFORM_HEIGHT  # то же самое и с высотой
                    x = (len(level[0][0]) * PLATFORM_WIDTH * i)  # на каждой новой строчке начинаем с нуля
                y = 0
                i += 1





        self.massBlock = []
        self.xLen = self.lvlBox_Count - 1
        cont = 0

        #Составление уровня
        for e in range(self.xLen): self.massBlock.append(pygame.sprite.Group())
        print " > Map level blocks: "
        for i in range(self.xLen):
            print "     #%s >> " %i,
            if i>0:
                for platfrm in entitiesBlocks[i-1]:
                    if not self.massBlock[i].has(platfrm):
                        self.massBlock[i].add(platfrm)
                cont +=1
                print " %s " %(i-1),
            for platfrm in entitiesBlocks[i]:
                if not self.massBlock[i].has(platfrm):
                    self.massBlock[i].add(platfrm)
            cont += 1
            print  " %s " %i,
            if i<(self.xLen):
                for platfrm in entitiesBlocks[i+1]:
                    if not self.massBlock[i].has(platfrm):
                        self.massBlock[i].add(platfrm)
                cont += 1
                print " %s " %(i+1),
            cont = 0
            print " "

        #Скопируем исходный уровень
        self.massBlockTemp = self.massBlock

        #for group in self.massBlock:
        #    group.update()

        #Отчистим память от лишних копийx
        for i in range(self.lvlBox_Count):
            entitiesBlocks[i].empty()


        self.clock.tick(self.fps)

        self.menuGid = MenuRECT((0, 1, 10, 5))
        self.planetGif = Planet(WIN_WIDTH - 500, 0)

        self.endLevel = False
        self.inRocket = False

        self.getTicksLastFrame = 0
        self.pointTextFont = font.Font('%s/fonts/3X5.TTF' % ICON_DIR, 65)
        self.menuFont = font.Font('%s/fonts/spaceAge.TTF' % ICON_DIR, 65)
        self.timeLevel = 0
        self.preTimeLevel = timerGame.time()
        self.rocketSound0 = mixer.Sound("%s/sound/spaceship.wav" % ICON_DIR)
        self.rocketSound0.set_volume(self.volumeEffects)
        self.colorWhite = Color("#d6d7e1")  # (255, 255, 255)
        self.colorRed = (202, 0, 42)
        self.colorBlue = (0, 43, 198)
        self.endLevelOnPlayer = False
        while not self.endLevel:  # Основной цикл программы\
            self.Loop()
        #self.rocketSound0.stop()
        if not self.endLevelOnPlayer:
            return self.pointLevel, self.starPoint, self.timeLevel
        elif self.endLevelOnPlayer:
            return 0, 0, 0
    def Loop(self):

        if self.pause:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.planetGif.image, self.planetGif.rect)
            self.planetGif.update()

            self.right = False
            self.left = False
            self.up = False
            for e in pygame.event.get():  # Обрабатываем события
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    self.pause = not self.pause
                if e.type == KEYDOWN and (e.key == K_UP or e.key == K_w):
                    if self.pauseMenuLevel >0:
                        self.pauseMenuLevel -=1
                if e.type == KEYDOWN and (e.key == K_DOWN or e.key == K_d):
                    if self.pauseMenuLevel <2:
                        self.pauseMenuLevel +=1
                if e.type == KEYDOWN and e.key == K_RETURN:
                    if self.pauseMenuLevel == 0: #Return in game
                        self.pause = not self.pause
                    elif self.pauseMenuLevel == 1: #Replay game
                        self.hero = Player(64, 64, self.total_level_width, self.total_level_height, self.volumeEffects,
                                           port=self.portShocker, shockerLvl=self.shockerLevel)
                        self.massBlock = self.massBlockTemp
                        self.pause = not self.pause
                    elif self.pauseMenuLevel == 2:  # END game
                        self.endLevel = True
                        self.endLevelOnPlayer = True


            self.pauseTextR = self.menuFont.render("Pause", False, self.colorRed)
            self.pauseTextR.set_alpha(150)
            self.pauseTextB = self.menuFont.render("Pause", False, self.colorBlue)
            self.pauseTextB.set_alpha(150)
            self.pauseText = self.menuFont.render("Pause", False, self.colorWhite)

            self.returnTextR = self.menuFont.render("Return", False, self.colorRed)
            self.returnTextR.set_alpha(150)
            self.returnTextB = self.menuFont.render("Return", False, self.colorBlue)
            self.returnTextB.set_alpha(150)
            self.returnText = self.menuFont.render("Return", False, self.colorWhite)

            self.replayTextR = self.menuFont.render("Replay", False, self.colorRed)
            self.replayTextR.set_alpha(150)
            self.replayTextB = self.menuFont.render("Replay", False, self.colorBlue)
            self.replayTextB.set_alpha(150)
            self.replayText = self.menuFont.render("Replay", False, self.colorWhite)

            self.mainMenuTextR = self.menuFont.render("Main Menu", False, self.colorRed)
            self.mainMenuTextR.set_alpha(150)
            self.mainMenuTextB = self.menuFont.render("Main Menu", False, self.colorBlue)
            self.mainMenuTextB.set_alpha(150)
            self.mainMenuText = self.menuFont.render("Main Menu", False, self.colorWhite)

            pauseX = WIN_WIDTH / 2 - self.pauseText.get_width() / 2
            textHeigt = self.returnTextR.get_height()
            allTextH = textHeigt * 3

            returnTextX = WIN_WIDTH / 2 - self.returnText.get_width() / 2
            returnTextY = WIN_HEIGHT / 2 - allTextH / 2 - textHeigt / 2 + 50

            replayTextX = WIN_WIDTH / 2 - self.replayText.get_width() / 2
            replayTextY = returnTextY + textHeigt   +50

            mainMenuTextX = WIN_WIDTH / 2 - self.mainMenuText.get_width() / 2
            mainMenuTextY = replayTextY + textHeigt

            if self.pauseMenuLevel == 0:
                self.menuGid.rect = (returnTextX, returnTextY, self.returnText.get_width(), textHeigt)
                self.menuGid.update()
                self.screen.blit(self.menuGid.image, self.menuGid.rect)

            elif self.pauseMenuLevel == 1:
                self.menuGid.rect = (replayTextX, replayTextY, self.replayText.get_width(), textHeigt)
                self.menuGid.update()
                self.screen.blit(self.menuGid.image, self.menuGid.rect)

            elif self.pauseMenuLevel == 2:
                self.menuGid.rect = (mainMenuTextX, mainMenuTextY, self.mainMenuText.get_width(), textHeigt)
                self.menuGid.update()
                self.screen.blit(self.menuGid.image, self.menuGid.rect)

            txtPosX = random.randint(2, 6)
            txtPosY = random.randint(2, 6)
            self.screen.blit(self.pauseTextR, (pauseX -txtPosX, 50 - txtPosY))
            self.screen.blit(self.pauseTextB, (pauseX + txtPosX, 50 + txtPosY))
            self.screen.blit(self.pauseText, (pauseX, 50))

            self.screen.blit(self.returnTextR, (returnTextX - txtPosX, returnTextY - txtPosY))
            self.screen.blit(self.returnTextB, (returnTextX + txtPosX, returnTextY + txtPosY))
            self.screen.blit(self.returnText, (returnTextX, returnTextY))

            self.screen.blit(self.replayTextR, (replayTextX - txtPosX, replayTextY - txtPosY))
            self.screen.blit(self.replayTextB, (replayTextX + txtPosX, replayTextY + txtPosY))
            self.screen.blit(self.replayText, (replayTextX, replayTextY))

            self.screen.blit(self.mainMenuTextR, (mainMenuTextX - txtPosX, mainMenuTextY - txtPosY))
            self.screen.blit(self.mainMenuTextB, (mainMenuTextX + txtPosX, mainMenuTextY + txtPosY))
            self.screen.blit(self.mainMenuText, (mainMenuTextX, mainMenuTextY))

        elif not self.pause:

            for e in pygame.event.get():  # Обрабатываем события
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    self.pause = not self.pause
                if e.type == QUIT:
                    raise SystemExit, "QUIT"
                if e.type == KEYDOWN and (e.key == K_UP or e.key == K_w):
                    self.up = True
                #if e.type == KEYDOWN and e.key == K_g:
                #    self.heroGod = True
                #    print "God mode " + str(self.heroGod)
                #    self.hero.setGod(self.heroGod)
                #if e.type == KEYDOWN and e.key == K_n:
                #    self.heroGod = False
                #    self.hero.setGod(self.heroGod)
                #    print "God mode " + str(self.heroGod)
                if e.type == KEYDOWN and (e.key == K_LEFT or e.key == K_a):
                    self.left = True
                if e.type == KEYDOWN and (e.key == K_RIGHT or e.key == K_d):
                    self.right = True
                if e.type == KEYUP and (e.key == K_UP or e.key == K_w):
                    self.up = False
                if e.type == KEYUP and (e.key == K_RIGHT or e.key == K_d):
                    self.right = False
                if e.type == KEYUP and (e.key == K_LEFT or e.key == K_a):
                    self.left = False
                if e.type == KEYDOWN and e.key == K_BACKQUOTE:
                    self.showStatistic = True

            heroX, heroY = self.hero.rect.x, self.hero.rect.y
            milliseconds = self.clock.tick(120)  # do not go faster than this frame rate

            if heroX < self.total_level_width:
                block = self.maping(heroX, 0, self.total_level_width, 1, self.xLen)

            self.screen.blit(self.background, (0, 0))  # Фон
            self.screen.blit(self.planetGif.image, self.planetGif.rect)
            self.planetGif.update()
            if not self.inRocket:
                self.timeLevel = timerGame.time() - self.preTimeLevel
                self.camera.update(self.hero)  # центризируем камеру относительно персонажа
            else:
                self.rocketSound0.play(0)
            #
            self.hero.update(self.left, self.right, self.up, self.massBlock[block])
            for e in self.massBlock[block]: #отрисовка платформ
                self.screen.blit(e.image, self.camera.apply(e))
                typeIs = e.getData()
                if typeIs == "kill_shock1":
                    e.update()
                elif typeIs == "kill_move1":
                    e.update()
                elif typeIs == "rocket":
                    e.update(self.hero)
                    self.inRocket = e.inRocket
                    self.endLevel = e.endLevel
            self.starPoint, self.pointLevel = self.hero.getPoint()
            textPoint = self.pointTextFont.render(str(self.pointLevel) + " :|: " + str(self.starPoint), False, (255, 255, 255))
            textPointR = self.pointTextFont.render(str(self.pointLevel) + " :|: " + str(self.starPoint), False, (202, 0, 42))
            textPointB = self.pointTextFont.render(str(self.pointLevel) + " :|: " + str(self.starPoint), False, (0, 43, 198))
            self.screen.blit(textPointR, (WIN_WIDTH - 500-5, WIN_HEIGHT - 70-3))
            self.screen.blit(textPointB, (WIN_WIDTH - 500+5, WIN_HEIGHT - 70+5))
            self.screen.blit(textPoint, (WIN_WIDTH - 500, WIN_HEIGHT - 70))

            if self.showStatistic:
                self.posX = self.defaultFont.render("block: " + str(block) +
                                                    " camX:" + str(self.camera.state.x) +
                                                    " FPS: " + str(round(self.clock.get_fps(), 1)), False, (255, 0, 0))
                self.screen.blit(self.posX, (0, 5))

                self.blockX = self.defaultFont.render("x:" + str(heroX) +
                                                      " y:" + str(heroY), False,(255, 0, 0))
                self.screen.blit(self.blockX, (0, 25))

            self.screen.blit(self.hero.image, self.camera.apply(self.hero))

        pygame.display.update()  # обновление и вывод всех изменений на экран

    def maping(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
