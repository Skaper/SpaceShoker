#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

class GenerationBlocks():
    def __init__(self, x, y, blocksLen, complexity):
        self.xSize = x
        self.ySize = y
        self.blocksLen = blocksLen
        self.complexity = complexity
        print " > Level settings:"
        print "     x: %s" % self.xSize,
        print " y: %s" % self.ySize,
        print " Blocks in level: %s" % self.blocksLen,
        print " Complexity: %s" % self.complexity
        if complexity == 0:
            self.levelLen = x*blocksLen
            self.fire = x*y/100
            self.blocks = x*y/20
            self.platformMove = x*y/250
            print " > In 1 block of level:"
            print "     Stars: %s" %self.fire,
            print " Platforms: %s" %self.blocks,
            print " Portals: %s" %self.platformMove


    def getLevelBlocks(self):
        level = []
        for x in range(self.blocksLen):
            if x == self.blocksLen-1:
                lvl = self.getLevelBl1(x, end=1)
                level.append(lvl)
            else:
                lvl = self.getLevelBl1(x)
                level.append(lvl)
            #print x
        return level

    def getLevelBl1(self, block, end=0):
        #Генерация обычных блоков
        self.levelMap = [[' '] * self.xSize for i in range(self.ySize)]
        for x in range(self.xSize):  # вся строка
            #self.levelMap[0][x] = '-'
            self.levelMap[self.ySize-1][x] = '-'
        if block == 0: #Если это первый блок создаем стену слева
            for y in range(self.ySize):  # вся строка
                self.levelMap[y][0] = '-'
        elif end == 1: #Если это последний блок создаем стену справа
            for y in range(self.ySize-1):
                self.levelMap[y][self.xSize-1] = '-'

        blocks = self.blocks
        while blocks >0:
            x = random.randint(0, self.xSize-1)
            y = random.randint(0, self.ySize-1)
            while self.levelMap[y][x] == "-":
                x = random.randint(0, self.xSize-1)
                y = random.randint(0, self.ySize-1)
            lenPlathorm = random.randint(1, 5)
            if x+lenPlathorm<self.xSize:
                #self.levelMap[y][x] = '-'
                for i in range(lenPlathorm):
                    self.levelMap[y][x+i] = '-'
                #self.levelMap[y][x + 2] = '-'
                #self.levelMap[y][x] = '-'
                blocks -=1
        platformMove = self.platformMove
        while platformMove >0:
            x = random.randint(4, self.xSize-1)
            y = random.randint(0, self.ySize-1)
            while self.levelMap[y][x] == "=" or self.levelMap[y][x] == "-" :
                x = random.randint(4, self.xSize-1)
                y = random.randint(0, self.ySize-1)
            lenPlathormMove = random.randint(2, 4)

            if x+lenPlathormMove<self.xSize:
                if self.levelMap[y][x + 2] == '=' or self.levelMap[y][x - 2] == '=':
                    x += 1
                #self.levelMap[y][x] = '-'
                for i in range(lenPlathormMove):
                    for j in range(self.ySize - 2):
                        self.levelMap[j+1][x + i] = ' '

                    self.levelMap[y][x+i] = '='


                #self.levelMap[y][x + 2] = '-'
                #self.levelMap[y][x] = '-'
                platformMove -=1 #>>>
        conX = 0
        #for x in range((self.xSize-1)/5):  # вся строка
        #    for y in range((self.ySize-1)/5:  # каждый символ
        #        if self.levelMap[y][x] == "-":
        #            conX
        fire = self.fire
        while fire >0:
            x = random.randint(0, self.xSize-1)
            y = random.randint(0, self.ySize-1)
            while (self.levelMap[y][x] == "-" or self.levelMap[y][x] == "*"):
                x = random.randint(0, self.xSize-1)
                y = random.randint(0, self.ySize-1)
            self.levelMap[y][x] = '*'
            fire -=1
        if block == 0:
            self.levelMap[3][1] = "-"
            self.levelMap[3][2] = "-"
            self.levelMap[3][3] = "-"
            self.levelMap[2][1] = " "
            self.levelMap[2][2] = " "
            self.levelMap[2][3] = " "
            self.levelMap[1][1] = " "
            self.levelMap[1][2] = " "
            self.levelMap[1][3] = " "

        #for y in range(self.ySize - 10):
        #    self.levelMap[y][self.xSize - 1] = '-'
        for x in range(self.xSize):  # вся строка
            self.levelMap[0][x] = ' '
        self.levelMap[2][1] = block

        if end==1:
            y = self.ySize - 5
            self.levelMap[-y][-2] = " "
            self.levelMap[-y][-3] = " "
            self.levelMap[-y][-4] = "R"
            self.levelMap[-y+1][-2] = " "
            self.levelMap[-y+1][-3] = " "
            self.levelMap[-y+1][-4] = " "
            self.levelMap[-y+2][-2] = " "
            self.levelMap[-y+2][-3] = " "
            self.levelMap[-y+2][-4] = " "
            self.levelMap[-y+3][-2] = " "
            self.levelMap[-y+3][-3] = " "
            self.levelMap[-y+3][-4] = " "
            self.levelMap[-y+4][-2] = "-"
            self.levelMap[-y+4][-3] = "-"
            self.levelMap[-y+4][-4] = "-"
            self.levelMap[-y+4][-5] = "-"

        return self.levelMap