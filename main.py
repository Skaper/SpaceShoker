#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import sys
import glob
import pygame

#from pygame import *
from game import Game
from blocks import *
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами
pygame.font.init()

try:
    import serial
    LibSerial = True
except:
    LibSerial = False

WIN_WIDTH = 1280#1280  # Ширина создаваемого окна
WIN_HEIGHT = 720#720  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#000000"

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

class Menu():
        def __init__(self):
            self.fps = 60.0
            self.showStatistic = False
            self.heroGod = False


            pygame.init()
            pygame.display.set_caption("Space Shocker!")
            self.screen = pygame.display.set_mode(DISPLAY)
            self.pointFont = font.Font('%s/fonts/3X5.TTF' % ICON_DIR, 65)
            self.menuFont = font.Font('%s/fonts/spaceAge.TTF' % ICON_DIR, 65)
            self.menuFont2 = font.Font('%s/fonts/electrox.TTF' % ICON_DIR, 65)

            self.menuLevelSet = 0
            self.menuGid = MenuRECT((0,1,10,5))
            self.clock = pygame.time.Clock()

            #Очки уровня
            self.pointLevel = 0
            self.starPoint = 0
            self.timeLevel = 0
            self.totalPoit = 0
            self.pointLevelTemp = 0
            self.starPointTemp = 0
            self.timeLevelTemp = 0

            #Рандомный уровень
            self.RandomxBox = 0
            self.RandomyBox = 0
            self.RandomlvlBlocks = 0
            self.Randomcomplexity = 0
            self.menuLevelSetings = 0

            #Настройки
            self.soundValume = 0.5
            self.effectsValume = 0.3
            self.resolution = 1280#1920
            self.graphics = "Higt"

            #Shoker
            self.portId = 0
            self.shockLevel = 'low'
            self.portName = ""
        def main(self):
            self.planetGif = Planet(WIN_WIDTH-500, 0)
            self.background = Surface((WIN_WIDTH, WIN_HEIGHT))
            self.background.fill(Color(BACKGROUND_COLOR))  # Фон
            if WIN_WIDTH == 1920:
                self.background = image.load("%s/texture/backFullHD.jpg" % ICON_DIR)
            elif WIN_WIDTH == 1280:
                self.background = image.load("%s/texture/back1.jpg" % ICON_DIR)

            self.colorWhite = Color("#d6d7e1")#(255, 255, 255)
            self.colorRed = (202, 0, 42)
            self.colorBlue = (0, 43, 198)

            pygame.mixer.pre_init(44100, 16, 2, 4096)
            self.backSound = pygame.mixer.music
            self.backSound.load("%s/sound/assimilator.mp3" % ICON_DIR)
            self.backSound.set_volume(self.soundValume)
            self.backSound.play(-1)

            #a = pygame.mixer.pre_init(44100, 16, 2, 4096)
            self.menuSound0 = pygame.mixer.Sound("%s/sound/menu0.wav" % ICON_DIR)
            self.menuSound0.set_volume(self.effectsValume)
            self.enterSound0 = pygame.mixer.Sound("%s/sound/enter0.wav" % ICON_DIR)
            self.enterSound0.set_volume(self.effectsValume)
            self.loadSound0 = pygame.mixer.Sound("%s/sound/load0.wav" % ICON_DIR)
            self.loadSound0.set_volume(self.effectsValume)
            self.negativeSound0 = pygame.mixer.Sound("%s/sound/negative0.wav" % ICON_DIR)
            self.negativeSound0.set_volume(self.effectsValume)
            self.screenLevel = 0
            #self.USBports = serial_ports()
            self.USBports = []
            self.USBports.append("OFF")
            #self.USBports.append("OFF")
            while 1:
                self.loop()

        def setValume(self):
            self.menuSound0.set_volume(self.effectsValume)
            self.enterSound0.set_volume(self.effectsValume)
            self.loadSound0.set_volume(self.effectsValume)
            self.negativeSound0.set_volume(self.effectsValume)
            self.backSound.set_volume(self.soundValume)
        def loop(self):
            self.clock.tick(30)
            #Главное менб
            if self.screenLevel ==0:
                self.gameLogo1 = self.menuFont.render("SPACE ", False, (255, 255, 255))
                self.gameLogo2 = self.menuFont2.render("SHOCK!", False, (255, 255, 255))
                logoWidth1 = WIN_WIDTH / 2 - self.gameLogo1.get_width()/ 2  -self.gameLogo2.get_width()/2
                logoWidth2 = WIN_WIDTH / 2 - self.gameLogo2.get_width() / 2 +self.gameLogo1.get_width()/2

                self.connectShockerR = self.menuFont.render("CONNECT SHOCKER", False, self.colorRed)
                self.connectShockerR.set_alpha(150)
                self.connectShockerB = self.menuFont.render("CONNECT SHOCKER", False, self.colorBlue)
                self.connectShockerB.set_alpha(150)
                self.connectShocker = self.menuFont.render("CONNECT SHOCKER", False, self.colorWhite)

                self.startRandomR = self.menuFont.render("START RANDOM", False, self.colorRed)
                self.startRandomR.set_alpha(150)
                self.startRandomB = self.menuFont.render("START RANDOM", False, self.colorBlue)
                self.startRandomB.set_alpha(150)
                self.startRandom    = self.menuFont.render("START RANDOM", False, self.colorWhite)

                self.startMissionsR = self.menuFont.render("MISSIONS", False, self.colorRed)
                self.startMissionsR.set_alpha(150)
                self.startMissionsB = self.menuFont.render("MISSIONS", False, self.colorBlue)
                self.startMissionsB.set_alpha(150)
                self.startMissions  = self.menuFont.render("MISSIONS", False, self.colorWhite)

                self.settingsR  = self.menuFont.render("SETTINGS", False, self.colorRed)
                self.settingsR.set_alpha(150)
                self.settingsB  = self.menuFont.render("SETTINGS", False, self.colorBlue)
                self.settingsB.set_alpha(150)
                self.settings   = self.menuFont.render("SETTINGS", False, self.colorWhite)

                self.exitButtonR = self.menuFont.render("EXIT", False, self.colorRed)
                self.exitButtonR.set_alpha(150)
                self.exitButtonB = self.menuFont.render("EXIT", False, self.colorBlue)
                self.exitButtonB.set_alpha(150)
                self.exitButton = self.menuFont.render("EXIT", False, self.colorWhite)

                textHeigt = self.startRandom.get_height()
                allTextH = textHeigt*4
                conShoX = WIN_WIDTH / 2 - self.connectShocker.get_width() / 2
                conShoY = WIN_HEIGHT / 2 - allTextH / 2 - textHeigt / 2
                strRndX = WIN_WIDTH / 2 - self.startRandom.get_width() / 2
                strRndY = conShoY + textHeigt
                strMsnX = WIN_WIDTH / 2 - self.startMissions.get_width() / 2
                strMsnY = strRndY + textHeigt
                stngX = WIN_WIDTH / 2 - self.settings.get_width() / 2
                stngY = strMsnY + textHeigt

                exitX = WIN_WIDTH / 2 - self.exitButton.get_width() / 2
                exitY = WIN_HEIGHT - textHeigt - 10

                #self.startMissions.get_height()  + self.startSettings.get_height()
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.planetGif.image, self.planetGif.rect)
                self.planetGif.update()

                if self.menuLevelSet == 0:
                    self.menuGid.rect = (conShoX, conShoY, self.connectShocker.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)

                elif self.menuLevelSet == 1:
                    self.menuGid.rect =(strRndX, strRndY, self.startRandom.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)

                elif self.menuLevelSet == 2:
                    self.menuGid.rect =(strMsnX, strMsnY, self.startMissions.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)

                elif self.menuLevelSet == 3:
                    self.menuGid.rect =(stngX, stngY, self.settings.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)
                elif self.menuLevelSet == 4:
                    self.menuGid.rect = (exitX, exitY, self.exitButton.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)

                txtPosX = random.randint(2, 6)
                txtPosY = random.randint(2, 6)

                self.screen.blit(self.connectShockerR, (conShoX-txtPosX, conShoY-txtPosY))
                self.screen.blit(self.connectShockerB, (conShoX+txtPosX, conShoY+txtPosY))
                self.screen.blit(self.connectShocker, (conShoX, conShoY))

                self.screen.blit(self.startRandomR, (strRndX-txtPosX, strRndY-txtPosY))
                self.screen.blit(self.startRandomB, (strRndX+txtPosX, strRndY+txtPosY))
                self.screen.blit(self.startRandom, (strRndX, strRndY))#self.connectShocker.get_rect().centerx + textHeigt/4))

                self.screen.blit(self.startMissionsR, (strMsnX-txtPosX, strMsnY-txtPosY))
                self.screen.blit(self.startMissionsB, (strMsnX+txtPosX, strMsnY+txtPosY))
                self.screen.blit(self.startMissions, (strMsnX, strMsnY))

                self.screen.blit(self.settingsR, (stngX-txtPosX, stngY-txtPosY))
                self.screen.blit(self.settingsB, (stngX+txtPosX, stngY+txtPosY))
                self.screen.blit(self.settings, (stngX, stngY))

                self.screen.blit(self.exitButtonR, (exitX - txtPosX, exitY - txtPosY))
                self.screen.blit(self.exitButtonB, (exitX + txtPosX, exitY + txtPosY))
                self.screen.blit(self.exitButton, (exitX, exitY))

                self.screen.blit(self.gameLogo1, (logoWidth1, 50))
                self.screen.blit(self.gameLogo2, (logoWidth2, 52))

                for e in pygame.event.get():  # Обрабатываем события
                    if e.type == QUIT:
                        raise SystemExit, "QUIT"
                    if e.type == KEYDOWN and e.key == K_m:
                        self.backSound.stop()
                    if e.type == KEYDOWN and (e.key == K_DOWN or e.key == K_s):
                        self.menuLevelSet += 1
                        self.menuSound0.play(0)
                        if self.menuLevelSet >4:
                            self.menuLevelSet = 0

                    if e.type == KEYDOWN and (e.key == K_UP or e.key == K_w):
                        self.menuLevelSet -= 1
                        self.menuSound0.play(0)
                        if self.menuLevelSet <0:
                            self.menuLevelSet = 4

                    if e.type == KEYDOWN and e.key == K_RETURN:
                        self.enterSound0.play(0)
                        if self.menuLevelSet == 0:
                            self.screenLevel = 4
                        if self.menuLevelSet == 1:
                            self.RandomxBox = random.randint(20, 61)
                            self.RandomyBox = random.randint(15, 45)
                            self.RandomlvlBlocks  = random.randint(3, 11)
                            self.Randomcomplexity = 0 #TODO Сделать разную сложность
                            self.screenLevel = 1

                        if self.menuLevelSet == 2: #Missions
                            game1 = Game(10, 20, 3, 0)
                            self.RandomxBox = 10
                            self.RandomyBox = 20
                            self.RandomlvlBlocks =3
                            self.pointLevel, self.starPoint, self.timeLevel = game1.main()
                            self.screenLevel = 2
                        if self.menuLevelSet == 3:
                            self.screenLevel = 3
                        if self.menuLevelSet == 4:
                            raise SystemExit, "QUIT"
            #Настройка рандомного уровня
            elif self.screenLevel == 1:#Настройка уровня
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.planetGif.image, self.planetGif.rect)
                self.planetGif.update()

                for e in pygame.event.get():  # Обрабатываем события
                    if e.type == QUIT:
                        raise SystemExit, "QUIT"
                    if e.type == KEYDOWN and e.key == K_m:
                        self.backSound.stop()
                    if e.type == KEYDOWN and (e.key == K_DOWN or e.key == K_s):
                        self.menuSound0.play(0)
                        self.menuLevelSetings += 1
                        if self.menuLevelSetings > 5:
                            self.menuLevelSetings = 0
                    if e.type == KEYDOWN and (e.key == K_UP or e.key == K_w):
                        self.menuSound0.play(0)
                        self.menuLevelSetings -= 1
                        if self.menuLevelSetings < 0:
                            self.menuLevelSetings = 5
                    if e.type == KEYDOWN and (e.key == K_RIGHT or e.key == K_d):

                        if self.menuLevelSetings == 0:
                            if self.RandomxBox <  120:
                                self.RandomxBox +=5
                            else:
                                self.negativeSound0.play(0)

                        elif self.menuLevelSetings == 1:
                            if self.RandomyBox < 120:
                                self.RandomyBox +=5
                            else:
                                self.negativeSound0.play(0)

                        elif self.menuLevelSetings == 2:
                            if self.RandomlvlBlocks < 40:
                                self.RandomlvlBlocks +=1
                            else:
                                self.negativeSound0.play(0)

                        elif self.menuLevelSetings == 3:
                            if self.Randomcomplexity < 2:
                                self.Randomcomplexity +=1
                            else: self.negativeSound0.play(0)

                    if e.type == KEYDOWN and (e.key == K_LEFT or e.key == K_a):
                        if self.menuLevelSetings == 0:
                            if self.RandomxBox>15:
                                self.RandomxBox -=5
                            else:
                                self.negativeSound0.play(0)
                        elif self.menuLevelSetings == 1:
                            if self.RandomyBox>15:
                                self.RandomyBox -=5
                            else:
                                self.negativeSound0.play(0)
                        elif self.menuLevelSetings == 2:
                            if self.RandomlvlBlocks >3:
                                self.RandomlvlBlocks -=1
                            else: self.negativeSound0.play(0)
                        elif self.menuLevelSetings == 3:
                            if self.Randomcomplexity >0:
                                self.Randomcomplexity -=1
                            else: self.negativeSound0.play(0)
                    if e.type == KEYDOWN and e.key == K_RETURN:
                        if self.menuLevelSetings ==4: #Retum to main menu
                            self.enterSound0.play(0)
                            self.screenLevel = 0
                        elif self.menuLevelSetings == 5:
                            self.loadSound0.play(0)
                            game1 = Game(self.RandomxBox, self.RandomyBox, self.RandomlvlBlocks,
                                         self.Randomcomplexity, portName=self.portName, shockLevel=self.shockLevel)
                            self.pointLevel, self.starPoint, self.timeLevel = game1.main()  # self.pointLevel, self.starPoint, self.timeLevel
                            if self.timeLevel == 0: #Если игра прервана возвращаемся в главное меню
                                self.screenLevel = 0
                            else:
                                self.screenLevel = 2

                self.gameLogo1 = self.menuFont.render("Random Level", False, (255, 255, 255))
                #self.gameLogo2 = self.menuFont2.render("SHOCK!", False, (255, 255, 255))
                logoWidth1 = WIN_WIDTH / 2 - self.gameLogo1.get_width() / 2


                #self.menuLevelSetings == 0
                self.lenSetXR = self.menuFont.render("Length block: " + str(self.RandomxBox), False, self.colorRed)
                self.lenSetXR.set_alpha(150)
                self.lenSetXB = self.menuFont.render("Length block: "+ str(self.RandomxBox), False, self.colorBlue)
                self.lenSetXB.set_alpha(150)
                self.lenSetXi = self.menuFont.render("Length block: "+ str(self.RandomxBox), False, self.colorWhite)

                #self.menuLevelSetings == 1
                self.lenSetYR = self.menuFont.render("Height block: "+ str(self.RandomyBox), False, self.colorRed)
                self.lenSetYR.set_alpha(150)
                self.lenSetYB = self.menuFont.render("Height block: "+ str(self.RandomyBox), False, self.colorBlue)
                self.lenSetYB.set_alpha(150)
                self.lenSetYi = self.menuFont.render("Height block: "+ str(self.RandomyBox), False, self.colorWhite)

                #self.menuLevelSetings == 2
                self.lenSetBlockR = self.menuFont.render("Quantity of block: " + str(self.RandomlvlBlocks), False, self.colorRed)
                self.lenSetBlockR.set_alpha(150)
                self.lenSetBlockB = self.menuFont.render("Quantity of block: " + str(self.RandomlvlBlocks), False, self.colorBlue)
                self.lenSetBlockB.set_alpha(150)
                self.lenSetBlocki = self.menuFont.render("Quantity of block: " + str(self.RandomlvlBlocks), False, self.colorWhite)
                #self.menuLevelSetings == 3:
                self.complexitySetR = self.menuFont.render("Complexity level: " + str(self.Randomcomplexity), False, self.colorRed)
                self.complexitySetR.set_alpha(150)
                self.complexitySetB = self.menuFont.render("Complexity level: "  + str(self.Randomcomplexity), False, self.colorBlue)
                self.complexitySetB.set_alpha(150)
                self.complexitySeti = self.menuFont.render("Complexity level: "  + str(self.Randomcomplexity), False, self.colorWhite)
                # self.menuLevelSetings == 4
                self.backButtonR = self.menuFont.render("< BACK", False, self.colorRed)
                self.backButtonR.set_alpha(150)
                self.backButtonB = self.menuFont.render("< BACK", False, self.colorBlue)
                self.backButtonB.set_alpha(150)
                self.backButton = self.menuFont.render("< BACK", False, self.colorWhite)
                #self.menuLevelSetings == 5
                self.okButtonR = self.menuFont.render("GO! >", False, self.colorRed)
                self.okButtonR.set_alpha(150)
                self.okButtonB = self.menuFont.render("GO! >", False, self.colorBlue)
                self.okButtonB.set_alpha(150)
                self.okButton = self.menuFont.render("GO! >", False, self.colorWhite)


                textHeigt = self.lenSetXi.get_height()
                allTextH = textHeigt * 4
                conShoX = WIN_WIDTH / 2 - self.lenSetXi.get_width() / 2
                conShoY = WIN_HEIGHT / 2 - allTextH / 2 - textHeigt / 2

                strRndX = WIN_WIDTH / 2 - self.lenSetYi.get_width() / 2
                strRndY = conShoY + textHeigt
                strMsnX = WIN_WIDTH / 2 - self.lenSetBlocki.get_width() / 2
                strMsnY = strRndY + textHeigt
                stngX = WIN_WIDTH / 2 - self.complexitySeti.get_width() / 2
                stngY = strMsnY + textHeigt

                okButtonX = WIN_WIDTH - self.okButton.get_width() - 10
                okButtonY = WIN_HEIGHT - textHeigt - 10

                backButtonX = 10
                backButtonY = WIN_HEIGHT - textHeigt - 10

                # self.startMissions.get_height()  + self.startSettings.get_height()
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.planetGif.image, self.planetGif.rect)
                self.planetGif.update()

                if self.menuLevelSetings == 0:
                    self.menuGid.rect = (conShoX, conShoY, self.lenSetXi.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)

                elif self.menuLevelSetings == 1:
                    self.menuGid.rect = (strRndX, strRndY, self.lenSetYi.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)

                elif self.menuLevelSetings == 2:
                    self.menuGid.rect = (strMsnX, strMsnY, self.lenSetBlocki.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)

                elif self.menuLevelSetings == 3:
                    self.menuGid.rect = (stngX, stngY, self.complexitySeti.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)

                elif self.menuLevelSetings == 4:
                    self.menuGid.rect = (backButtonX, backButtonY, self.backButton.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)

                elif self.menuLevelSetings == 5:
                    self.menuGid.rect = (okButtonX, okButtonY, self.okButton.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)

                txtPosX = random.randint(2, 6)
                txtPosY = random.randint(2, 6)

                self.screen.blit(self.lenSetXR, (conShoX - txtPosX, conShoY - txtPosY))
                self.screen.blit(self.lenSetXB, (conShoX + txtPosX, conShoY + txtPosY))
                self.screen.blit(self.lenSetXi, (conShoX, conShoY))

                self.screen.blit(self.lenSetYR, (strRndX - txtPosX, strRndY - txtPosY))
                self.screen.blit(self.lenSetYB, (strRndX + txtPosX, strRndY + txtPosY))
                self.screen.blit(self.lenSetYi, (strRndX, strRndY))

                self.screen.blit(self.lenSetBlockR, (strMsnX - txtPosX, strMsnY - txtPosY))
                self.screen.blit(self.lenSetBlockB, (strMsnX + txtPosX, strMsnY + txtPosY))
                self.screen.blit(self.lenSetBlocki, (strMsnX, strMsnY))

                self.screen.blit(self.complexitySetR, (stngX - txtPosX, stngY - txtPosY))
                self.screen.blit(self.complexitySetB, (stngX + txtPosX, stngY + txtPosY))
                self.screen.blit(self.complexitySeti, (stngX, stngY))

                self.screen.blit(self.okButtonR, (okButtonX - txtPosX, okButtonY - txtPosY))
                self.screen.blit(self.okButtonB, (okButtonX + txtPosX, okButtonY + txtPosY))
                self.screen.blit(self.okButton,  (okButtonX, okButtonY))

                self.screen.blit(self.backButtonR, (backButtonX - txtPosX, backButtonY - txtPosY))
                self.screen.blit(self.backButtonB, (backButtonX + txtPosX, backButtonY + txtPosY))
                self.screen.blit(self.backButton, (backButtonX, backButtonY))

                self.screen.blit(self.gameLogo1, (logoWidth1, 50))
            #Результат уровня
            elif self.screenLevel ==2: #Подсчет очков

                if self.pointLevelTemp <= self.pointLevel:
                    self.screen.blit(self.background, (0, 0))
                    self.screen.blit(self.planetGif.image, self.planetGif.rect)
                    self.planetGif.update()

                    self.pointCalck = self.pointFont.render("POINTS: " + str(self.pointLevelTemp), False, self.colorWhite)
                    self.starCalck = self.pointFont.render("SHOCK STARS: " + str(self.starPoint), False, self.colorRed)
                    self.totalTimeLevel = self.pointFont.render("TOTAL TIME: " + str(round(self.timeLevel, 2)) +"", False, self.colorBlue)
                    self.screen.blit(self.pointCalck, (WIN_WIDTH/2 - self.pointCalck.get_width() /2, 100))
                    self.screen.blit(self.starCalck, (WIN_WIDTH / 2 - self.starCalck.get_width()/2, 200))
                    self.screen.blit(self.totalTimeLevel, (WIN_WIDTH / 2 - self.totalTimeLevel.get_width() /2, 300))
                    pygame.display.update()
                    for e in pygame.event.get():  # Обрабатываем события
                        if e.type == QUIT:
                            raise SystemExit, "QUIT"
                        if e.type == KEYDOWN and e.key == K_RETURN:
                            self.pointLevelTemp = self.pointLevel
                    self.pointLevelTemp +=5
                else:
                    self.screen.blit(self.background, (0, 0))
                    self.screen.blit(self.planetGif.image, self.planetGif.rect)
                    self.planetGif.update()
                    self.pointCalck = self.pointFont.render("POINTS: " + str(self.pointLevel), False,
                                                            self.colorWhite)
                    self.starCalck = self.pointFont.render("SHOCK STARS: " + str(self.starPoint), False, self.colorRed)
                    self.totalTimeLevel = self.pointFont.render("TOTAL TIME: " + str(round(self.timeLevel, 3)) + "",
                                                                False, self.colorBlue)

                            #game1 = Game(self.RandomxBox, self.RandomyBox, self.RandomlvlBlocks, self.Randomcomplexity)
                    self.totalPoit = self.pointLevel*(self.Randomcomplexity+1) / (self.timeLevel/self.RandomlvlBlocks) * \
                                     (self.RandomxBox * self.RandomyBox/(self.starPoint+1))
                    self.totalPoit = round(self.totalPoit , 0)
                    self.totalPoitCalc = self.pointFont.render("TOTAL POINT: " + str(self.totalPoit) + "",
                                                                False, self.colorBlue)
                    self.screen.blit(self.pointCalck, (WIN_WIDTH / 2 - self.pointCalck.get_width() / 2, 100))
                    self.screen.blit(self.starCalck, (WIN_WIDTH / 2 - self.starCalck.get_width() / 2, 200))
                    self.screen.blit(self.totalTimeLevel, (WIN_WIDTH / 2 - self.totalTimeLevel.get_width() / 2, 300))
                    self.screen.blit(self.totalPoitCalc, (WIN_WIDTH / 2 - self.totalPoitCalc.get_width() / 2, 450))
                    pygame.display.update()
                    for e in pygame.event.get():  # Обрабатываем события
                        if e.type == QUIT:
                            raise SystemExit, "QUIT"
                        if e.type == KEYDOWN and e.key == K_RETURN:
                            self.screenLevel = 0
            #Настройки
            elif self.screenLevel == 3:  # Настройки
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.planetGif.image, self.planetGif.rect)
                self.planetGif.update()

                for e in pygame.event.get():  # Обрабатываем события
                    if e.type == QUIT:
                        raise SystemExit, "QUIT"
                    if e.type == KEYDOWN and e.key == K_m:
                        self.backSound.stop()
                    if e.type == KEYDOWN and (e.key == K_DOWN or e.key == K_s):
                        self.menuSound0.play(0)
                        self.menuLevelSetings += 1
                        if self.menuLevelSetings > 5:
                            self.menuLevelSetings = 0
                    if e.type == KEYDOWN and (e.key == K_UP or e.key == K_w):
                        self.menuSound0.play(0)
                        self.menuLevelSetings -= 1
                        if self.menuLevelSetings < 0:
                            self.menuLevelSetings = 5
                    if e.type == KEYDOWN and (e.key == K_RIGHT or e.key == K_d):

                        if self.menuLevelSetings == 0:
                            if self.soundValume <= 0.9:
                                self.soundValume += 0.1
                            else:
                                self.negativeSound0.play(0)

                        elif self.menuLevelSetings == 1:
                            if self.effectsValume < 0.9:
                                self.effectsValume += 0.1
                            else:
                                self.negativeSound0.play(0)

                        elif self.menuLevelSetings == 2:
                            self.resolution = 1920
                            self.negativeSound0.play(0)

                        elif self.menuLevelSetings == 3:
                            self.negativeSound0.play(0)

                    if e.type == KEYDOWN and (e.key == K_LEFT or e.key == K_a):
                        if self.menuLevelSetings == 0:

                            if self.soundValume > 0.09:
                                self.soundValume -= 0.1
                                if self.soundValume<0.09:
                                    self.soundValume =0.0
                                print  self.soundValume
                            else:
                                self.negativeSound0.play(0)
                            print self.soundValume
                        elif self.menuLevelSetings == 1:
                            if self.effectsValume > 0.09:
                                self.effectsValume -= 0.1
                                if self.effectsValume<0.09:
                                    self.effectsValume = 0.0
                            else:
                                self.negativeSound0.play(0)
                        elif self.menuLevelSetings == 2:
                            self.negativeSound0.play(0)
                            self.resolution = 1280
                        elif self.menuLevelSetings == 3:
                            self.negativeSound0.play(0)
                    if e.type == KEYDOWN and e.key == K_RETURN:
                        if self.menuLevelSetings == 4:  # Retum to main menu
                            self.enterSound0.play(0)
                            self.screenLevel = 0

                        elif self.menuLevelSetings == 5: #OK BUTTON
                            self.loadSound0.play(0)
                            self.screenLevel = 0
                            #TODO save as file settings

                self.setValume()
                self.gameLogo1 = self.menuFont.render("Settings", False, (255, 255, 255))
                # self.gameLogo2 = self.menuFont2.render("SHOCK!", False, (255, 255, 255))
                logoWidth1 = WIN_WIDTH / 2 - self.gameLogo1.get_width() / 2

                # self.menuLevelSetings == 0
                self.lenSetXR = self.menuFont.render("Sound Valume:   " + str(self.soundValume*100), False, self.colorRed)
                self.lenSetXR.set_alpha(150)
                self.lenSetXB = self.menuFont.render("Sound Valume:   " + str(self.soundValume*100), False, self.colorBlue)
                self.lenSetXB.set_alpha(150)
                self.lenSetXi = self.menuFont.render("Sound Valume:   " + str(self.soundValume*100), False, self.colorWhite)

                # self.menuLevelSetings == 1
                self.lenSetYR = self.menuFont.render("Effects Valume: " + str(self.effectsValume*100), False, self.colorRed)
                self.lenSetYR.set_alpha(150)
                self.lenSetYB = self.menuFont.render("Effects Valume: " + str(self.effectsValume*100), False, self.colorBlue)
                self.lenSetYB.set_alpha(150)
                self.lenSetYi = self.menuFont.render("Effects Valume: " + str(self.effectsValume*100), False, self.colorWhite)

                # self.menuLevelSetings == 2
                self.lenSetBlockR = self.menuFont.render("Screen resolution: " + str(self.resolution), False,
                                                         self.colorRed)
                self.lenSetBlockR.set_alpha(150)
                self.lenSetBlockB = self.menuFont.render("Screen resolution: " + str(self.resolution), False,
                                                         self.colorBlue)
                self.lenSetBlockB.set_alpha(150)
                self.lenSetBlocki = self.menuFont.render("Screen resolution: " + str(self.resolution), False,
                                                         self.colorWhite)
                # self.menuLevelSetings == 3:
                self.complexitySetR = self.menuFont.render("Graphics: " + str(self.graphics), False,
                                                           self.colorRed)
                self.complexitySetR.set_alpha(150)
                self.complexitySetB = self.menuFont.render("Graphics: " + str(self.graphics), False,
                                                           self.colorBlue)
                self.complexitySetB.set_alpha(150)
                self.complexitySeti = self.menuFont.render("Graphics: " + str(self.graphics), False,
                                                           self.colorWhite)
                # self.menuLevelSetings == 4
                self.backButtonR = self.menuFont.render("< BACK", False, self.colorRed)
                self.backButtonR.set_alpha(150)
                self.backButtonB = self.menuFont.render("< BACK", False, self.colorBlue)
                self.backButtonB.set_alpha(150)
                self.backButton = self.menuFont.render("< BACK", False, self.colorWhite)
                # self.menuLevelSetings == 5
                self.okButtonR = self.menuFont.render("OK! >", False, self.colorRed)
                self.okButtonR.set_alpha(150)
                self.okButtonB = self.menuFont.render("OK! >", False, self.colorBlue)
                self.okButtonB.set_alpha(150)
                self.okButton = self.menuFont.render("OK! >", False, self.colorWhite)

                textHeigt = self.lenSetXi.get_height()
                allTextH = textHeigt * 4
                conShoX = WIN_WIDTH / 2 - self.lenSetXi.get_width() / 2
                conShoY = WIN_HEIGHT / 2 - allTextH / 2 - textHeigt / 2

                strRndX = WIN_WIDTH / 2 - self.lenSetYi.get_width() / 2
                strRndY = conShoY + textHeigt
                strMsnX = WIN_WIDTH / 2 - self.lenSetBlocki.get_width() / 2
                strMsnY = strRndY + textHeigt
                stngX = WIN_WIDTH / 2 - self.complexitySeti.get_width() / 2
                stngY = strMsnY + textHeigt

                okButtonX = WIN_WIDTH - self.okButton.get_width() - 10
                okButtonY = WIN_HEIGHT - textHeigt - 10

                backButtonX = 10
                backButtonY = WIN_HEIGHT - textHeigt - 10

                # self.startMissions.get_height()  + self.startSettings.get_height()
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.planetGif.image, self.planetGif.rect)
                self.planetGif.update()

                if self.menuLevelSetings == 0:
                    self.menuGid.rect = (conShoX, conShoY, self.lenSetXi.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)

                elif self.menuLevelSetings == 1:
                    self.menuGid.rect = (strRndX, strRndY, self.lenSetYi.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)

                elif self.menuLevelSetings == 2:
                    self.menuGid.rect = (strMsnX, strMsnY, self.lenSetBlocki.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)

                elif self.menuLevelSetings == 3:
                    self.menuGid.rect = (stngX, stngY, self.complexitySeti.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)

                elif self.menuLevelSetings == 4:
                    self.menuGid.rect = (backButtonX, backButtonY, self.backButton.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)

                elif self.menuLevelSetings == 5:
                    self.menuGid.rect = (okButtonX, okButtonY, self.okButton.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)

                txtPosX = random.randint(2, 6)
                txtPosY = random.randint(2, 6)

                self.screen.blit(self.lenSetXR, (conShoX - txtPosX, conShoY - txtPosY))
                self.screen.blit(self.lenSetXB, (conShoX + txtPosX, conShoY + txtPosY))
                self.screen.blit(self.lenSetXi, (conShoX, conShoY))

                self.screen.blit(self.lenSetYR, (strRndX - txtPosX, strRndY - txtPosY))
                self.screen.blit(self.lenSetYB, (strRndX + txtPosX, strRndY + txtPosY))
                self.screen.blit(self.lenSetYi, (strRndX, strRndY))

                self.screen.blit(self.lenSetBlockR, (strMsnX - txtPosX, strMsnY - txtPosY))
                self.screen.blit(self.lenSetBlockB, (strMsnX + txtPosX, strMsnY + txtPosY))
                self.screen.blit(self.lenSetBlocki, (strMsnX, strMsnY))

                self.screen.blit(self.complexitySetR, (stngX - txtPosX, stngY - txtPosY))
                self.screen.blit(self.complexitySetB, (stngX + txtPosX, stngY + txtPosY))
                self.screen.blit(self.complexitySeti, (stngX, stngY))

                self.screen.blit(self.okButtonR, (okButtonX - txtPosX, okButtonY - txtPosY))
                self.screen.blit(self.okButtonB, (okButtonX + txtPosX, okButtonY + txtPosY))
                self.screen.blit(self.okButton, (okButtonX, okButtonY))

                self.screen.blit(self.backButtonR, (backButtonX - txtPosX, backButtonY - txtPosY))
                self.screen.blit(self.backButtonB, (backButtonX + txtPosX, backButtonY + txtPosY))
                self.screen.blit(self.backButton, (backButtonX, backButtonY))

                self.screen.blit(self.gameLogo1, (logoWidth1, 50))
            #Настройка шокера
            elif self.screenLevel == 4:  # Настройки шокера
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.planetGif.image, self.planetGif.rect)
                self.planetGif.update()

                for e in pygame.event.get():  # Обрабатываем события
                    if e.type == QUIT:
                        raise SystemExit, "QUIT"
                    if e.type == KEYDOWN and e.key == K_m:
                        self.backSound.stop()
                    if e.type == KEYDOWN and (e.key == K_DOWN or e.key == K_s):

                        self.menuSound0.play(0)
                        self.menuLevelSetings += 1
                        if self.menuLevelSetings > 5:
                            self.menuLevelSetings = 0
                    if e.type == KEYDOWN and (e.key == K_UP or e.key == K_w):

                        self.menuSound0.play(0)
                        self.menuLevelSetings -= 1
                        if self.menuLevelSetings < 0:
                            self.menuLevelSetings = 5
                    if e.type == KEYDOWN and (e.key == K_RIGHT or e.key == K_d):

                        if self.menuLevelSetings == 0:
                            self.USBports = []
                            self.USBports.append("OFF")
                            portsFound = serial_ports()
                            #self.USBports[0] = "OFF"
                            for port in portsFound:
                                self.USBports.append(port)

                            if self.portId < len(self.USBports)-1:
                                    self.portId +=1
                            else:
                                self.negativeSound0.play(0)
                            if self.USBports[self.portId] != "OFF":
                                self.portTest = serial.Serial(self.USBports[self.portId], baudrate=115200, timeout=0.0)
                        if self.menuLevelSetings == 1:
                            self.shockLevel = 'high'
                    if e.type == KEYDOWN and (e.key == K_LEFT or e.key == K_a):

                        if self.menuLevelSetings == 0:
                            self.USBports = []
                            self.USBports.append("OFF")
                            portsFound = serial_ports()
                            # self.USBports[0] = "OFF"
                            for port in portsFound:
                                self.USBports.append(port)
                            if self.portId > 0:
                                    self.portId -=1
                            else:
                                self.negativeSound0.play(0)
                            if self.USBports[self.portId] != "OFF":
                                self.portTest = serial.Serial(self.USBports[self.portId], baudrate=115200, timeout=0.0)
                        if self.menuLevelSetings == 1:
                            self.shockLevel = 'low'

                    if e.type == KEYDOWN and e.key == K_RETURN:
                        if self.menuLevelSetings == 2:
                            if self.USBports[self.portId] != "OFF":
                                #port = serial.Serial(self.USBports[self.portId], baudrate=115200, timeout=0.0)
                                try:
                                    if self.shockLevel == 'high':
                                        self.portTest.write("T1>1\n")
                                    elif self.shockLevel == 'low':
                                        self.portTest.write("T2>1\n")
                                except:
                                    pass
                                #port.close()
                        elif self.menuLevelSetings == 3:  # Retum to main menu
                            self.enterSound0.play(0)
                            self.screenLevel = 0
                            self.portId = 0
                            if self.USBports[self.portId] != "OFF":
                                self.portTest.close()
                            else:
                                self.portName = ""

                        elif self.menuLevelSetings == 4: #OK BUTTON
                            self.loadSound0.play(0)
                            self.screenLevel = 0
                            if self.USBports[self.portId] != "OFF":
                                self.portTest.close()
                                self.portName = self.USBports[self.portId]
                            else:
                                self.portName = ""


                self.gameLogo1 = self.menuFont.render("CONNECT SHOCKER", False, (255, 255, 255))
                # self.gameLogo2 = self.menuFont2.render("SHOCK!", False, (255, 255, 255))
                logoWidth1 = WIN_WIDTH / 2 - self.gameLogo1.get_width() / 2

                # self.menuLevelSetings == 0


                self.lenSetXR = self.menuFont.render("USB Port: " + self.USBports[self.portId], False, self.colorRed)
                self.lenSetXR.set_alpha(150)
                self.lenSetXB = self.menuFont.render("USB Port: " + self.USBports[self.portId], False, self.colorBlue)
                self.lenSetXB.set_alpha(150)
                self.lenSetXi = self.menuFont.render("USB Port: " + self.USBports[self.portId], False, self.colorWhite)

                # self.menuLevelSetings == 1
                self.lenSetYR = self.menuFont.render("Shock level: " + self.shockLevel, False, self.colorRed)
                self.lenSetYR.set_alpha(150)
                self.lenSetYB = self.menuFont.render("Shock level: " + self.shockLevel, False, self.colorBlue)
                self.lenSetYB.set_alpha(150)
                self.lenSetYi = self.menuFont.render("Shock level: " + self.shockLevel, False, self.colorWhite)

                # self.menuLevelSetings == 2
                self.lenSetBlockR = self.menuFont.render("Test shock!", False, self.colorWhite)
                self.lenSetBlockR.set_alpha(150)
                self.lenSetBlockB = self.menuFont.render("Test shock! ", False, self.colorBlue)
                self.lenSetBlockB.set_alpha(150)
                self.lenSetBlocki = self.menuFont.render("Test shock! ", False, self.colorRed)
                # self.menuLevelSetings == 3:


                # self.menuLevelSetings == 4
                self.backButtonR = self.menuFont.render("< BACK", False, self.colorRed)
                self.backButtonR.set_alpha(150)
                self.backButtonB = self.menuFont.render("< BACK", False, self.colorBlue)
                self.backButtonB.set_alpha(150)
                self.backButton = self.menuFont.render("< BACK", False, self.colorWhite)
                # self.menuLevelSetings == 5
                self.okButtonR = self.menuFont.render("Connect! >", False, self.colorRed)
                self.okButtonR.set_alpha(150)
                self.okButtonB = self.menuFont.render("Connect! >", False, self.colorBlue)
                self.okButtonB.set_alpha(150)
                self.okButton = self.menuFont.render("Connect! >", False, self.colorWhite)

                textHeigt = self.lenSetXi.get_height()
                allTextH = textHeigt * 4
                conShoX = WIN_WIDTH / 2 - self.lenSetXi.get_width() / 2
                conShoY = WIN_HEIGHT / 2 - allTextH / 2 - textHeigt / 2

                strRndX = WIN_WIDTH / 2 - self.lenSetYi.get_width() / 2
                strRndY = conShoY + textHeigt
                strMsnX = WIN_WIDTH / 2 - self.lenSetBlocki.get_width() / 2
                strMsnY = strRndY + textHeigt


                okButtonX = WIN_WIDTH - self.okButton.get_width() - 10
                okButtonY = WIN_HEIGHT - textHeigt - 10

                backButtonX = 10
                backButtonY = WIN_HEIGHT - textHeigt - 10

                # self.startMissions.get_height()  + self.startSettings.get_height()
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.planetGif.image, self.planetGif.rect)
                self.planetGif.update()

                if self.menuLevelSetings == 0:
                    self.menuGid.rect = (conShoX, conShoY, self.lenSetXi.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)

                elif self.menuLevelSetings == 1:
                    self.menuGid.rect = (strRndX, strRndY, self.lenSetYi.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)

                elif self.menuLevelSetings == 2:
                    self.menuGid.rect = (strMsnX, strMsnY, self.lenSetBlocki.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)



                elif self.menuLevelSetings == 3:
                    self.menuGid.rect = (backButtonX, backButtonY, self.backButton.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)

                elif self.menuLevelSetings == 4:
                    self.menuGid.rect = (okButtonX, okButtonY, self.okButton.get_width(), textHeigt)
                    self.menuGid.update()
                    self.screen.blit(self.menuGid.image, self.menuGid.rect)

                txtPosX = random.randint(2, 6)
                txtPosY = random.randint(2, 6)

                self.screen.blit(self.lenSetXR, (conShoX - txtPosX, conShoY - txtPosY))
                self.screen.blit(self.lenSetXB, (conShoX + txtPosX, conShoY + txtPosY))
                self.screen.blit(self.lenSetXi, (conShoX, conShoY))

                self.screen.blit(self.lenSetYR, (strRndX - txtPosX, strRndY - txtPosY))
                self.screen.blit(self.lenSetYB, (strRndX + txtPosX, strRndY + txtPosY))
                self.screen.blit(self.lenSetYi, (strRndX, strRndY))

                self.screen.blit(self.lenSetBlockR, (strMsnX - txtPosX, strMsnY - txtPosY))
                self.screen.blit(self.lenSetBlockB, (strMsnX + txtPosX, strMsnY + txtPosY))
                self.screen.blit(self.lenSetBlocki, (strMsnX, strMsnY))



                self.screen.blit(self.okButtonR, (okButtonX - txtPosX, okButtonY - txtPosY))
                self.screen.blit(self.okButtonB, (okButtonX + txtPosX, okButtonY + txtPosY))
                self.screen.blit(self.okButton, (okButtonX, okButtonY))

                self.screen.blit(self.backButtonR, (backButtonX - txtPosX, backButtonY - txtPosY))
                self.screen.blit(self.backButtonB, (backButtonX + txtPosX, backButtonY + txtPosY))
                self.screen.blit(self.backButton, (backButtonX, backButtonY))

                self.screen.blit(self.gameLogo1, (logoWidth1, 50))

            pygame.display.update()





menuGame = Menu()
menuGame.main()