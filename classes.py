import pygame as pg, constants as c, math, random

class TownHall():
    def __init__(self, screen, position, images, level):
        self.screen         = screen
        self.position       = position
        self.images         = images
        self.level          = level
        self.maxMoney       = 250
        self.money          = self.maxMoney/2
        self.upgradeMoney   = 125
        self.moneyFactor    = 0.13
        self.maxLevel       = 11
        self.objects        = []
        self.image          = self.images[self.level]
        self.hpPerlvl       = [
            100,
            175,
            260,
            330,
            440,
            580,
            640,
            760,
            900,
           1330,
           1500,
           2000,
           3580,
        ]
        self.hitpoints      = self.hpPerlvl[self.level]
        self.maxHitpoints   = self.hpPerlvl[self.level]
    
    def aplyDamage(self, damage):
        self.hitpoints -= damage
    
    def healHitpoints(self, heal):
        self.hitpoints += heal
        if self.hitpoints > self.maxHitpoints:
            self.hitpoints = self.maxHitpoints
        
    def addMoney(self, money):
        self.money += money
        if self.money > self.maxMoney:
            self.money = self.maxMoney
    
    def levelUp(self):
        if self.level < self.maxLevel:
            self.level += 1
            self.maxMoney       = int(self.maxMoney*1.60)
            self.upgradeMoney   = int(self.upgradeMoney*1.48)
            self.moneyFactor    *= 1.28
            self.hitpoints      = self.hpPerlvl[self.level]*(self.level+1)
            self.maxHitpoints   = self.hpPerlvl[self.level]
            for object in self.objects:
                object.levelUp()
    
    def setObjects(self, objects):
        self.objects = objects
    
    def update(self):
        self.money += self.moneyFactor
        if self.money > self.maxMoney:
            self.money = self.maxMoney
        self.image = self.images[self.level]
        self.screen.blit(self.image, self.position)

class Barrack():
    def __init__(self, screen, position, images, level, worth):
        self.screen         = screen
        self.position       = position
        self.images         = images
        self.level          = level
        self.worth          = worth
        self.maxLevel       = 11
        self.image          = self.images[self.level]
        self.hpPerlvl       = [
            50,
            75,
            125,
            180,
            240,
            300,
            360,
            475,
            555,
            610,
            660,
            730,
        ]
        self.respawnLimit   = 0
        self.hitpoints      = self.hpPerlvl[self.level]
        self.maxHitpoints   = self.hpPerlvl[self.level]
        self.objects        = []
        self.units          = [
            
        ]
        self.troop          = [
            [1,],
            [1,],
            [1, 1],
            [1, 1],
            [1, 2],
            [1, 2],
            [1, 2, 2],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3, 4],
            [1, 2, 3, 4],
            [1, 2, 3, 4, 5],
        ]
        self.units.append(Unit(self.screen, self.position, c.buildingsAndUnits["units"][self.troop[self.level][0]-1], 0, self.troop[self.level][0]))
    
    def aplyDamage(self, damage):
        self.hitpoints -= damage
        
    def setObjects(self, objects):
        self.objects = objects
    
    def healHitpoints(self, heal):
        self.hitpoints += heal
        if self.hitpoints >= self.maxHitpoints:
            self.hitpoints = self.maxHitpoints
        for unit in self.units:
            unit.healHitpoints(unit.hitpoints/100)
        if self.respawnLimit >= 500:
            if len(self.units)  == 0:
                for i in range(len(self.troop[self.level])):
                    self.units.append(Unit(self.screen, self.position, c.buildingsAndUnits["units"][self.troop[self.level][i]-1], 0, self.troop[self.level][i]))
    
    def levelUp(self):
        if self.level < self.maxLevel:
            self.level += 1
            self.hitpoints      = self.hpPerlvl[self.level]
            self.maxHitpoints   = self.hpPerlvl[self.level]
            self.units          = []
            for i in range(len(self.troop[self.level])):
                self.units.append(Unit(self.screen, self.position, c.buildingsAndUnits["units"][self.troop[self.level][i]-1], 0, self.troop[self.level][i]))
    
    def update(self, enemies):
        self.respawnLimit += 1
        self.image = self.images[self.level]
        self.screen.blit(self.image, self.position)
        for i, unit in enumerate(self.units):
            unit.setEnemies(enemies)
            unit.update(self.level)
            if unit.hitpoints <= 0:
                self.units.pop(i)

class Unit():
    def __init__(self, screen, position, images, level, troop, typeTroop=1):
        self.screen         = screen
        self.position       = position
        self.positionBase   = position
        self.movePosition   = position
        self.images         = images
        self.level          = level
        self.troop          = troop # 1-5 Barb, Archer, Miner, Dragon, Pekka
        self.maxLevel       = 11
        self.target         = None
        self.image          = self.images[self.level]
        self.levelUpT       = (typeTroop == 1)
        self.damage         = [
            18,
            20,
            22,
            125,
            200,
        ] if self.levelUpT else [
            15,
            12,
            18,
            155,
            251,
        ]
        self.speed          = 0.60 if self.levelUpT else 0.45
        self.hpPerlvl       = [
            50*(self.troop+0.2)*1.5,
            75*(self.troop+0.2)*1.5,
            125*(self.troop+0.2)*1.4,
            258*(self.troop+0.2)*1.4,
            512*(self.troop+0.2)*1.3,
            789*(self.troop+0.2)*1.3,
            969*(self.troop+0.2)*1.2,
            1675*(self.troop+0.2)*1.2,
            1855*(self.troop+0.2)*1.2,
            2410*(self.troop+0.2)*1.2,
            2860*(self.troop+0.2)*1.2,
            3333*(self.troop+0.2)*1.2,
        ] if self.levelUpT and self.troop != 5 else [
            50*(self.troop+1)*1.5,
            75*(self.troop+1)*1.5,
            125*(self.troop+1)*1.5,
            258*(self.troop+1)*1.5,
            512*(self.troop+1)*1.5,
            789*(self.troop+1)*1.6,
            969*(self.troop+1)*1.6,
            1675*(self.troop+1)*1.7,
            1855*(self.troop+1)*1.7,
            2410*(self.troop+1)*1.7,
            2860*(self.troop+1)*1.7,
            3333*(self.troop+1)*1.7,
        ] if self.levelUpT and self.troop == 5 else [
            30,
            55,
            125,
            280,
            440,
            525,
            860,
            975,
            1255,
            1610,
            1960,
            2130,
        ] if self.troop == 2 else [
            50*(self.troop),
            75*(self.troop),
            125*(self.troop),
            258*(self.troop),
            512*(self.troop),
            789*(self.troop),
            969*(self.troop),
            1125*(self.troop),
            1522*(self.troop),
            1890*(self.troop),
            2254*(self.troop),
            2696*(self.troop),
        ] if self.troop == 3 else [
            50*(self.troop+0.01),
            75*(self.troop+0.01),
            125*(self.troop+0.01),
            258*(self.troop+0.01),
            512*(self.troop+0.01),
            789*(self.troop+0.01),
            969*(self.troop+0.01),
            1125*(self.troop+0.01),
            1522*(self.troop+0.01),
            1890*(self.troop+0.01),
            2254*(self.troop+0.01),
            2696*(self.troop+0.01),
        ]if self.troop == 4 else [
            50*(self.troop+0.1),
            75*(self.troop+1),
            125*(self.troop+1),
            258*(self.troop+1),
            512*(self.troop+1),
            789*(self.troop+1),
            969*(self.troop+1),
            1125*(self.troop+1),
            1522*(self.troop+1),
            1890*(self.troop+1),
            2254*(self.troop+1),
            2696*(self.troop+1),
        ]
        self.range          = ([45, 115, 35, 65, 55][self.troop-1])
        self.hitpoints      = self.hpPerlvl[self.level]
        self.maxHitpoints   = self.hpPerlvl[self.level]
        self.enemies        = []
        self.levelUpTick    = 0
        self.distTarget     = 9999
        self.supports       = []
    
    def aplyDamage(self, damage):
        self.hitpoints -= damage
        
    def setEnemies(self, enemies:list):
        self.enemies = enemies
    
    def healHitpoints(self, heal):
        self.hitpoints += heal
        if self.hitpoints >= self.maxHitpoints:
            self.hitpoints = self.maxHitpoints
    
    def levelUp(self):
        if self.level < self.maxLevel:
            self.level += 1
            self.damage         = self.damage.copy()*((self.level+1.1)*self.troop)
            self.hitpoints      = self.hpPerlvl[self.level].copy()*(self.troop*1.2)
            self.maxHitpoints   = self.hpPerlvl[self.level].copy()*(self.troop*1.2)
            
    def levelUpTroop(self):
        if self.troop < 5:
            self.troop += 1
            self.damage         = self.damage.copy()*((self.level+1.1)*self.troop)
            self.hitpoints      = self.hpPerlvl[self.level].copy()*(self.troop*1.2)
            self.maxHitpoints   = self.hpPerlvl[self.level].copy()*(self.troop*1.2)
    
    def setTarget(self):
        if self.levelUpT:
            closestEnemy = None
            closestDistance = float('inf')
            for enemy in self.enemies:
                distance = math.sqrt((enemy.position[0] - self.positionBase[0])**2 + (enemy.position[1] - self.positionBase[1])**2)
                if distance < closestDistance and distance <= 175:
                    closestEnemy = enemy
                    closestDistance = distance
            self.target = closestEnemy
        else:
            closestEnemy = None
            closestDistance = float('inf')
            for enemy in self.enemies:
                distance = math.sqrt((enemy.position[0] - self.position[0])**2 + (enemy.position[1] - self.position[1])**2)
                if distance < closestDistance:
                    closestEnemy = enemy
                    closestDistance = distance
                if type(enemy) == Barrack:
                    units = enemy.units
                    for unit in units:
                        distance = math.sqrt((unit.position[0] - self.position[0])**2 + (unit.position[1] - self.position[1])**2)
                        if distance < closestDistance:
                            closestEnemy = unit
                            closestDistance = distance
            self.target = closestEnemy
    
    def moveRandomly(self, maxDistance=100):
        random_x = random.randint(self.positionBase[0] - maxDistance, self.positionBase[0] + maxDistance)
        random_y = random.randint(self.positionBase[1] - maxDistance, self.positionBase[1] + maxDistance)

        self.position = (random_x, random_y)

    def update(self, maxLevel=11):
        try:
            if self.levelUpT:
                if self.levelUpTick >= 500 and self.level < self.maxLevel and self.level < maxLevel+1:
                    self.level += 1
                    self.levelUpTick = 0
                else:
                    self.levelUpTick += 1
            if self.target is None or self.target.hitpoints <= 0:
                self.setTarget()
                if self.target is None and (abs(self.movePosition[0] - self.position[0]) <= 2) and (abs(self.movePosition[1] - self.position[1]) <= 2):
                    self.movePosition = [
                        random.randint(self.positionBase[0] - 50, self.positionBase[0] + 50),
                        random.randint(self.positionBase[1] - 50, self.positionBase[1] + 50)
                    ]
                elif self.target == None:
                    dx = self.movePosition[0] - self.position[0]
                    dy = self.movePosition[1] - self.position[1]
                    dist = math.sqrt(dx**2 + dy**2)
                    if dist != 0:
                        dx /= dist
                        dy /= dist
                    self.position = (self.position[0] + dx * self.speed, self.position[1] + dy * self.speed)

            if self.target is not None and self.target.hitpoints > 0:
                distance = math.sqrt((self.target.position[0] - self.position[0])**2 + (self.target.position[1] - self.position[1])**2)
                if distance <= self.range:
                    if self.levelUpT:
                        self.target.aplyDamage((self.damage[self.troop-1]*(1+(0.1*self.level)))/10)
                    else:
                        self.target.aplyDamage((self.damage[self.troop-1]*(1+(0.1*self.level)))/10)
                else:
                    self.setTarget()
                    dx = self.target.position[0] - self.position[0]
                    dy = self.target.position[1] - self.position[1]
                    dist = math.sqrt(dx**2 + dy**2)
                    if dist != 0:
                        dx /= dist
                        dy /= dist
                    self.position = (self.position[0] + dx * self.speed, self.position[1] + dy * self.speed)
            else:
                self.setTarget()
        except:
            self.setTarget()
        
        if not self.levelUpT:
            x = random.randint(0, 50000)
            if x == 500 and len(self.supports) <= 2:
                self.supports.append(Unit(self.screen, [self.position[0]+random.randint(-15,15), self.position[1]+random.randint(-15,15)], self.images, self.level, self.troop, 999))
                self.supports[len(self.supports)-1].healHitpoints(9999)
            for support in self.supports:
                support.setEnemies(self.enemies)
                support.update()
        
        self.image = self.images[self.level]
        self.screen.blit(self.image, self.position)

class Mine():
    def __init__(self, screen, position, images, level, townHall, worth):
        self.screen         = screen
        self.position       = position
        self.images         = images
        self.level          = level
        self.worth          = worth
        self.townHall       = townHall
        self.maxLevel       = 11
        self.value          = 1
        self.imageCoin      = c.coinImage
        self.image          = self.images[self.level]
        self.hpPerlvl       = [
            20,
            45,
            75,
            90,
            140,
            220,
            310,
            385,
            455,
            565,
            590,
            640,
        ]
        self.hitpoints      = self.hpPerlvl[self.level]
        self.maxHitpoints   = self.hpPerlvl[self.level]
        self.objects        = []
        self.tick           = 0
        self.displayCoin    = 0
    
    def aplyDamage(self, damage):
        self.hitpoints -= damage
        
    def setObjects(self, objects):
        self.objects = objects
    
    def healHitpoints(self, heal):
        self.hitpoints += heal
        if self.hitpoints >= self.maxHitpoints:
            self.hitpoints = self.maxHitpoints
    
    def levelUp(self):
        if self.level < self.maxLevel:
            self.level += 1
            self.value *= (1.05 + self.level/10)
            self.hitpoints      = self.hpPerlvl[self.level]
            self.maxHitpoints   = self.hpPerlvl[self.level]
    
    def update(self):
        self.tick += 1
        self.image = self.images[self.level]
        self.screen.blit(self.image, self.position)
        if self.tick >= 120:
            self.townHall.addMoney(self.value)
            self.tick = 0
            self.displayCoin = 5
        if self.displayCoin > 0:
            self.screen.blit(self.imageCoin, self.position)
            self.displayCoin -= 0.1

class Wall():
    def __init__(self, screen, position, images, level, worth):
        self.screen         = screen
        self.position       = position
        self.images         = images
        self.level          = level
        self.worth          = worth
        self.maxLevel       = 11
        self.image          = self.images[self.level]
        self.hpPerlvl       = [
            125,
            175,
            280,
            540,
            820,
            1710,
            2800,
            3340,
            2580,
            5500,
            7300,
           7890,
        ]
        self.hitpoints      = self.hpPerlvl[self.level]
        self.maxHitpoints   = self.hpPerlvl[self.level]
        self.objects        = []
        self.neighbour      = [0,0,0,0,0,0,0,0] #*L, U, R, D, LU, UR, RD, DL
        self.imageDark = self.image.copy()
        dark = pg.Surface((self.imageDark.get_width(), self.imageDark.get_height()), flags=pg.SRCALPHA)
        dark.fill((50, 50, 50, 0))
        self.imageDark.blit(dark, (0, 0), special_flags=pg.BLEND_RGBA_SUB)
    
    def setObjects(self, objects):
        self.setImagesByNeighbour()
        self.objects = objects
        
    def setImagesByNeighbour(self):
        self.neighbour      = [0,0,0,0,0,0,0,0] #*L, U, R, D, LU, UR, RD, DL
        for object in self.objects:
            if type(object) != Wall:
                continue
            oPos = object.position
            sPos = self.position
            if sPos[0] == oPos[0]:
                if sPos[1]-32 == oPos[1]:
                    self.neighbour[1] = 1
                if sPos[1]+32 == oPos[1]:
                    self.neighbour[3] = 1
            if sPos[1] == oPos[1]:
                if sPos[0]-32 == oPos[0]:
                    self.neighbour[0] = 1
                if sPos[0]+32 == oPos[0]:
                    self.neighbour[2] = 1
            if sPos[0]-32 == oPos[0] and sPos[1]+32 == oPos[1]:
                self.neighbour[4] = 1
            if sPos[0]+32 == oPos[0] and sPos[1]-32 == oPos[1]:
                self.neighbour[5] = 1
            if sPos[0]+32 == oPos[0] and sPos[1]+32 == oPos[1]:
                self.neighbour[6] = 1
            if sPos[0]-32 == oPos[0] and sPos[1]-32 == oPos[1]:
                self.neighbour[7] = 1
                
    def aplyDamage(self, damage):
        self.hitpoints -= damage
    
    def healHitpoints(self, heal):
        self.hitpoints += heal
        if self.hitpoints >= self.maxHitpoints:
            self.hitpoints = self.maxHitpoints
    
    def levelUp(self):
        if self.level < self.maxLevel:
            self.level += 1
            self.hitpoints      = self.hpPerlvl[self.level]
            self.maxHitpoints   = self.hpPerlvl[self.level]
            self.image          = self.images[self.level]
            self.imageDark      = self.image.copy()
            dark = pg.Surface((self.imageDark.get_width(), self.imageDark.get_height()), flags=pg.SRCALPHA)
            dark.fill((50, 50, 50, 0))
            self.imageDark.blit(dark, (0, 0), special_flags=pg.BLEND_RGBA_SUB)
    
    def update(self):
        #*L, U, R, D, LU, UR, RD, DL
        if self.neighbour[0]:
            self.screen.blit(self.image, [self.position[0]-16, self.position[1]])
            if self.level <= 9:
                self.screen.blit(self.imageDark, [self.position[0]-8, self.position[1]])
        if self.neighbour[1]:
            self.screen.blit(self.image, [self.position[0], self.position[1]-16])
            if self.level <= 9:
                self.screen.blit(self.imageDark, [self.position[0], self.position[1]-8])
        if self.neighbour[2]:
            self.screen.blit(self.image, [self.position[0]+16, self.position[1]])
            if self.level <= 9:
                self.screen.blit(self.imageDark, [self.position[0]+8, self.position[1]])
        if self.neighbour[3]:
            self.screen.blit(self.image, [self.position[0], self.position[1]+16])
            if self.level <= 9:
                self.screen.blit(self.imageDark, [self.position[0], self.position[1]+8])
        if self.neighbour[4]:
            self.screen.blit(self.image, [self.position[0]-16, self.position[1]+16])
            if self.level <= 9:
                self.screen.blit(self.imageDark, [self.position[0]-8, self.position[1]+8])
        if self.neighbour[5]:
            self.screen.blit(self.image, [self.position[0]+16, self.position[1]-16])
            if self.level <= 9:
                self.screen.blit(self.imageDark, [self.position[0]+8, self.position[1]-8])
        if self.neighbour[6]:
            self.screen.blit(self.image, [self.position[0]+16, self.position[1]+16])
            if self.level <= 9:
                self.screen.blit(self.imageDark, [self.position[0]+8, self.position[1]+8])
        if self.neighbour[7]:
            self.screen.blit(self.image, [self.position[0]-16, self.position[1]-16])
            if self.level <= 9:
                self.screen.blit(self.imageDark, [self.position[0]-8, self.position[1]-8])
        
        self.screen.blit(self.image, self.position)

