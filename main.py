import pygame as pg, os, constants as c, classes as cs, time, random

def font(size, pBold, pItalic):
    return pg.font.SysFont("verdana", int(size), bold=pBold, italic=pItalic)

def drawText(text, font, color, x, y):
    img = font.render(str(text), True, color)
    screenGame.blit(img, (x, y))

def drawQuitX():
    global screenGame
    def drawText(text, font, color, x, y):
        global screenGame
        img = font.render(str(text), True, color)
        screenGame.blit(img, (x, y))
    #* BORDER X
    displayX_font = pg.font.SysFont("comicsansms", 28, bold=True)
    drawText('X', displayX_font, (0, 0, 0), 1892, 0)
    
    
    #* CENTER X
    displayX_font = pg.font.SysFont("comicsansms", 16, bold=False)
    drawText('X', displayX_font, (255, 255, 255), 1896, 9)

def customSort(obj):
    return obj.position[1], obj.position[0]

print("If you don't want to play the progressiv mode type 'wave' and then press 'Enter', \nto play a wave like mode. \nElse press 'Enter'")
gameType = input(">")

# Initialisierung von pg und Game-Fenster
pg.init()
pg.font.init()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
pg.display.set_caption("Pygame")
clock = pg.time.Clock()
screenGame = pg.display.set_mode((0, 0))

textFont = font(16, True, False)
hpFont   = font(10, True, False)

selectedTerrain = c.terrains[c.terrainSelected]

enemies = []
objects = []
townHall= None

selected    = None
showHP      = False
game        = True
running     = True
tick        = 0
if gameType == "wave":
    minTimeEnemie = 1500
else:
    minTimeEnemie = 1900
doSpawn     = 800
minTimeMinus= 65
timeSpend   = 0
healTick    = 0
maxBuildings= 8
buildings   = 0
maxWalls    = 20
walls       = 0
max     	= 0

time.sleep(1)

while running:
    if townHall == None:
        screenGame.blit(selectedTerrain, (0, 0))
        screenGame.blit(c.selectedImage,                  (10, 1018))
        screenGame.blit(c.buildingsAndUnits["townHalls"][0], (20, 1028))
        screenGame.blit(c.buildingsAndUnits["townHalls"][0], list(pg.mouse.get_pos()))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                #* Quit when widow is closed
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                #* mouse presses
                if event.button == 1:
                    mousePos = list(pg.mouse.get_pos())
                    mousePos = [int(mousePos[0]*c.scale[0]), int(mousePos[1]*c.scale[1])]
                    if mousePos[0] >= 1884 and mousePos[1] <= 36:
                        pg.quit()
                        quit()
                    mousePosTemp = [(mousePos[0]//c.tileSize)*c.tileSize, (mousePos[1]//c.tileSize)*c.tileSize]
                    townHall = cs.TownHall(screenGame, mousePosTemp, c.buildingsAndUnits["townHalls"], 0)
                        
    
    elif townHall.hitpoints <= 0:
        bigAFont = font(78, True, True)
        drawText(f"GG, you survived {timeSpend} Frames!", bigAFont, (255,255,255), 200, 200)
        drawText(f"GG, you survived {timeSpend} Frames!", bigAFont, (0,0,0), 205, 205)
        drawText(f"Townhall Level: {townHall.level+1}/12!", bigAFont, (255,255,255), 200, 270)
        drawText(f"Townhall Level: {townHall.level+1}/12!", bigAFont, (0,0,0), 205, 275)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                #* Quit when widow is closed
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                #* mouse presses
                if event.button == 1:
                    mousePos = list(pg.mouse.get_pos())
                    mousePos = [int(mousePos[0]*c.scale[0]), int(mousePos[1]*c.scale[1])]
                    if mousePos[0] >= 1884 and mousePos[1] <= 36:
                        pg.quit()
                        quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DELETE:
                    running = False
    else:
        clock.tick(60)
        screenGame.fill((0,0,0))
    
        # Event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                #* Quit when widow is closed
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                #* mouse presses
                if event.button == 1:
                    mousePos = list(pg.mouse.get_pos())
                    mousePos = [int(mousePos[0]*c.scale[0]), int(mousePos[1]*c.scale[1])]
                    if mousePos[0] >= 1884 and mousePos[1] <= 36:
                        pg.quit()
                        quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    c.terrainSelected += 1
                    if c.terrainSelected >= 13:
                        c.terrainSelected = 0
                    selectedTerrain = c.terrains[c.terrainSelected]
                if event.key == pg.K_DOWN:
                    c.terrainSelected -= 1
                    if c.terrainSelected <= -1:
                        c.terrainSelected = 12
                    selectedTerrain = c.terrains[c.terrainSelected]
                if event.key == pg.K_F1:
                    showHP = not showHP
                if event.key == pg.K_BACKSPACE:
                    mousePos = list(pg.mouse.get_pos())
                    mousePos = [int(mousePos[0]*c.scale[0]), int(mousePos[1]*c.scale[1])]
                    mousePosTemp = [(mousePos[0]//c.tileSize)*c.tileSize, (mousePos[1]//c.tileSize)*c.tileSize]
                    for i, object in enumerate(objects):
                        if object.position == mousePosTemp:
                            objects.pop(i)
                            townHall.money += object.worth
                            if type(object) == cs.Wall:
                                walls     -= 1
                            else:
                                buildings -= 1
                            break
                if event.key == pg.K_SPACE and townHall.money >= townHall.upgradeMoney and townHall.level != townHall.upgradeMoney and townHall.level < townHall.maxLevel:
                    townHall.addMoney(-townHall.upgradeMoney)
                    townHall.levelUp()
                    maxBuildings += int(maxBuildings *0.40)
                    maxWalls += int(maxWalls*0.30)
                if event.key == pg.K_q:
                    selected = "barrack"
                elif event.key == pg.K_w:
                    selected = "wall"
                elif event.key == pg.K_e:
                    selected = "mine"
                # elif event.key == pg.K_r:
                #     selected = "bomb"
                # elif event.key == pg.K_t:
                #     selected = "giantBomb"
                # elif event.key == pg.K_z:
                #     selected = "cannon"
                # elif event.key == pg.K_u:
                #     selected = "archer"
                # elif event.key == pg.K_i:
                #     selected = "storage"
                # elif event.key == pg.K_o:
                #     selected = "tesla"
                # elif event.key == pg.K_p:
                #     selected = "multiCannon"
                # elif event.key == pg.K_a:
                #     selected = "altar" #* Barbking, ArcherQueen, Warden Fighting Mashine, Royal Campion etc.
                elif event.key == pg.K_0 or event.key == pg.K_d or event.key == pg.K_ESCAPE:
                    selected = None
                elif event.key == pg.K_DELETE:
                    running = False
            
            if event.type == pg.MOUSEBUTTONDOWN:
                #* mouse presses
                if event.button == 1:
                    mousePos = list(pg.mouse.get_pos())
                    mousePos = [int(mousePos[0]*c.scale[0]), int(mousePos[1]*c.scale[1])]
                    if mousePos[0] >= 1884 and mousePos[1] <= 36:
                        pg.quit()
                        quit()
                        print(mousePos)
                    if selected != None:
                        canBePlaced = True
                        for object in objects:
                            if object.position == [(mousePos[0]//c.tileSize)*c.tileSize, (mousePos[1]//c.tileSize)*c.tileSize]:
                                canBePlaced = False
                                break
                        if townHall.position == [(mousePos[0]//c.tileSize)*c.tileSize, (mousePos[1]//c.tileSize)*c.tileSize]:
                            canBePlaced = False
                        mousePosTemp = [(mousePos[0]//c.tileSize)*c.tileSize, (mousePos[1]//c.tileSize)*c.tileSize]
                        if canBePlaced and buildings < maxBuildings:
                            if selected == "barrack" and townHall.money >= round(c.infos["barrack"]["cost"] * (1+(townHall.level/6))):
                                townHall.addMoney(-round(c.infos["barrack"]["cost"] * (1+(townHall.level/6))))
                                objects.append(cs.Barrack(screenGame, mousePosTemp, c.buildingsAndUnits["barrack"], townHall.level, round(c.infos["barrack"]["cost"] * (1+(townHall.level/2.5))/1.25)))
                                buildings += 1
                            if selected == "mine" and townHall.money >= round(c.infos["mine"]["cost"] * (1+(townHall.level/6))):
                                townHall.addMoney(-round(c.infos["mine"]["cost"] * (1+(townHall.level/6))))
                                objects.append(cs.Mine(screenGame, mousePosTemp, c.buildingsAndUnits["mine"], townHall.level, townHall, round(c.infos["mine"]["cost"] * (1+(townHall.level/2.5))/1.25)))
                                buildings += 1
                        if canBePlaced and walls < maxWalls:
                            if selected == "wall" and townHall.money >= round(c.infos["wall"]["cost"] * (1+(townHall.level/6))):
                                townHall.addMoney(-round(c.infos["wall"]["cost"] * (1+(townHall.level/6))))
                                objects.append(cs.Wall(screenGame, mousePosTemp, c.buildingsAndUnits["wall"], townHall.level, round(c.infos["wall"]["cost"] * (1+(townHall.level/2.5))/1.25)))
                                walls += 1
                            objects = sorted(objects, key=customSort)
        
        screenGame.blit(selectedTerrain, (0, 0))
        
        townHall.setObjects(objects)
        townHall.update()
        if townHall.hitpoints <= 0:
            game    = False
        if showHP:
            pg.draw.rect(screenGame, (0  , 0, 0),(townHall.position[0]-2, townHall.position[1]-2, 28, 8))
            pg.draw.rect(screenGame, (255, 0, 0),(townHall.position[0],   townHall.position[1],   24, 3))
            pg.draw.rect(screenGame, (0, 255, 0),(townHall.position[0],   townHall.position[1],   int((townHall.hitpoints / townHall.maxHitpoints) * 24), 3))
        
        for i, object in enumerate(objects):
            object.setObjects(objects)
            if type(object) == cs.Barrack:
                object.update(enemies)
            else:
                object.update()
            if object.hitpoints <= 0:
                objects.pop(i)
                if type(object) == cs.Wall:
                    walls     -= 1
                else:
                    buildings -= 1
            if showHP:
                pg.draw.rect(screenGame, (0  , 0, 0),(object.position[0]-2, object.position[1]-2, 28, 8))
                pg.draw.rect(screenGame, (255, 0, 0),(object.position[0],   object.position[1],   24, 3))
                pg.draw.rect(screenGame, (0, 255, 0),(object.position[0],   object.position[1],   int((object.hitpoints/object.maxHitpoints)*24), 3))
                drawText(round(object.hitpoints), hpFont, (255,255,255), object.position[0]-2, object.position[1]-10)
                drawText(round(object.hitpoints), hpFont, (0,0,0), object.position[0], object.position[1]-12)
                if type(object) == cs.Barrack:
                    for unit in object.units:
                        pg.draw.rect(screenGame, (0  , 0, 0),(unit.position[0]-2, unit.position[1]-2, 28, 8))
                        pg.draw.rect(screenGame, (255, 0, 0),(unit.position[0],   unit.position[1],   24, 3))
                        pg.draw.rect(screenGame, (0, 255, 0),(unit.position[0],   unit.position[1],   int((unit.hitpoints/unit.maxHitpoints)*24), 3))
                        drawText(round(unit.hitpoints), hpFont, (255,255,255), unit.position[0]-2, unit.position[1]-10)
                        drawText(round(unit.hitpoints), hpFont, (0,0,0), unit.position[0], unit.position[1]-12)

        for i, enemie in enumerate(enemies):
            enemie.setEnemies(objects+[townHall])
            enemie.update()
            if showHP:
                pg.draw.rect(screenGame, (0  , 0, 0),(enemie.position[0]-2, enemie.position[1]-2, 28, 8))
                pg.draw.rect(screenGame, (255, 0, 0),(enemie.position[0],   enemie.position[1],   24, 3))
                pg.draw.rect(screenGame, (0, 255, 0),(enemie.position[0],   enemie.position[1],   int((enemie.hitpoints/enemie.maxHitpoints)*24), 3))
                drawText(round(enemie.hitpoints), hpFont, (255,255,255), enemie.position[0]-2, enemie.position[1]-12)
                drawText(round(enemie.hitpoints), hpFont, (0,0,0), enemie.position[0], enemie.position[1]-10)
            if enemie.hitpoints <= 0:
                enemies.pop(i)
        
        #* Money
        pg.draw.rect(screenGame, (0  ,   0, 0),(10, 10, 258, 31))
        pg.draw.rect(screenGame, (255,   0, 0),(15, 15, 250, 20))
        pg.draw.rect(screenGame, (255, 255, 0),(14,   14, int((townHall.money/townHall.maxMoney) * 250), 20))
        drawText(f"Money: {int(townHall.money)}/{townHall.maxMoney}|{int(townHall.upgradeMoney)}", textFont, (  0,   0,   0), 14, 14)
        
        #* Building/Walls Infos
        drawText(f"{buildings}/{maxBuildings} Buildings", textFont, (255,255,255), 10, 50)
        drawText(f"{buildings}/{maxBuildings} Buildings", textFont, (0,0,0), 12, 52)
        drawText(f"{walls}/{maxWalls} Walls", textFont, (255,255,255), 10, 70)
        drawText(f"{walls}/{maxWalls} Walls", textFont, (0,0,0), 12, 72)
        
        #* QUIT Button
        drawQuitX()
        
        #* Stats
        drawText(str(timeSpend), hpFont, (255,255,255), 11, 1063)
        drawText(str(timeSpend), hpFont, (0,0,0), 10, 1062)
        drawText(str(minTimeEnemie), hpFont, (255,255,255), 11, 1043)
        drawText(str(minTimeEnemie), hpFont, (0,0,0), 10, 1042)
        drawText(f"{int(doSpawn)}/{tick}", hpFont, (255,255,255), 11, 1023)
        drawText(f"{int(doSpawn)}/{tick}", hpFont, (0,0,0), 10, 1022)
        
        if selected:
            screenGame.blit(c.selectedImage,                  (10, 1018))
            screenGame.blit(c.buildingsAndUnits[selected][0], (20, 1028))
            drawText(str(round(c.infos[selected]["cost"]  * (1+(townHall.level/6)))), textFont, (0,0,0), 18, 1050)
        
        #* Hold
        keys = pg.key.get_pressed()
        mousePresses = pg.mouse.get_pressed()
        if keys[pg.K_END]:
            running = False
        if (mousePresses[0] or mousePresses[1] or mousePresses[2]) and selected is None:
            mousePos = pg.mouse.get_pos()
            mousePos = [int(mousePos[0]*c.scale[0]), int(mousePos[1]*c.scale[1])]
            mousePosTemp = [(mousePos[0]//c.tileSize)*c.tileSize, (mousePos[1]//c.tileSize)*c.tileSize]
            for object in objects:
                if object.position == mousePosTemp:
                    pg.draw.rect(screenGame, (0  , 0, 0),(object.position[0]-2, object.position[1]-2, 36, 10))
                    pg.draw.rect(screenGame, (255, 0, 0),(object.position[0],   object.position[1],   32, 5))
                    pg.draw.rect(screenGame, (0, 255, 0),(object.position[0],   object.position[1],   int((object.hitpoints/object.maxHitpoints)*32), 5))
                    drawText(f"Level:{object.level+1}", textFont, (255, 255, 255), object.position[0], object.position[1]-40)
                    drawText(f"Hitpoints{int(object.hitpoints)}/{object.maxHitpoints}", textFont, (255, 255, 255), object.position[0], object.position[1]-20)
                    drawText(f"Can be sold for: {int(object.worth)}", textFont, (255, 255, 255), object.position[0], object.position[1])
            if townHall.position == mousePosTemp:
                    pg.draw.rect(screenGame, (0  , 0, 0),(townHall.position[0]-2, townHall.position[1]-2, 36, 10))
                    pg.draw.rect(screenGame, (255, 0, 0),(townHall.position[0],   townHall.position[1],   32, 5))
                    pg.draw.rect(screenGame, (0, 255, 0),(townHall.position[0],   townHall.position[1],   int((townHall.hitpoints / townHall.maxHitpoints) * 32), 5))
                    drawText(townHall.level+1, textFont, (255, 255, 255), townHall.position[0], townHall.position[1]-40)
                    drawText(f"{townHall.hitpoints}/{townHall.maxHitpoints}", textFont, (255, 255, 255), townHall.position[0], townHall.position[1]-20)
        
        if tick >= doSpawn:
            if gameType == "wave":
                minTimeEnemie -= minTimeMinus//11
            try:
                doSpawn = random.randint(int(minTimeEnemie), int(minTimeEnemie*2))
            except ValueError:
                doSpawn = int(minTimeEnemie*1.25)
            if minTimeEnemie <= 0:
                minTimeEnemie = 750
            if gameType == "wave":
                minTimeEnemie //= 1.5
                if townHall.level == 3:
                    max = 1
                elif townHall.level == 4:
                    max = 2
                elif townHall.level == 5:
                    max = 3
                elif townHall.level == 9:
                    max = 4
                elif townHall.level == 11:
                    max = 5
                amount = random.randint(1, 2+townHall.level+5*(4*int(timeSpend//1000)))
                
                for i in range(amount if townHall.level < 2 else townHall.level+2):
                    for i in range(1 if minTimeEnemie > 0 else 2):
                        trp = random.randint(1,max) if max > 1 else max
                        x = random.randint(1, 4)
                        if townHall.level == 0:
                            min = townHall.level
                        else:
                            min = townHall.level-1
                        y = random.randint(min,townHall.level+int(townHall.level/3)+1)
                        if x == 1:
                            enemies.append(cs.Unit(screenGame, [random.randint(1, 1920), 0], c.buildingsAndUnits["units"][trp-1 if trp-1 != -1 else 1], y if y < 11 else random.randint(min,townHall.level), trp if trp-1!= -1 else 1, typeTroop=99))
                        elif x == 2:
                            enemies.append(cs.Unit(screenGame, [random.randint(1, 1920), 1080], c.buildingsAndUnits["units"][trp-1 if trp-1 != -1 else 1], y if y < 11 else random.randint(min,townHall.level), trp if trp-1!= -1 else 1, typeTroop=99))
                        elif x == 3:
                            enemies.append(cs.Unit(screenGame, [0, random.randint(1, 1080)], c.buildingsAndUnits["units"][trp-1 if trp-1 != -1 else 1], y if y < 11 else random.randint(min,townHall.level), trp if trp-1!= -1 else 1, typeTroop=99))
                        else:
                            enemies.append(cs.Unit(screenGame, [1920, random.randint(1, 1080)], c.buildingsAndUnits["units"][trp-1 if trp-1 != -1 else 1], y if y < 11 else random.randint(min,townHall.level), trp if trp-1!= -1 else 1, typeTroop=99))
                print(minTimeEnemie)
                tick = 0
            else:
                
                if minTimeEnemie >= 1000:
                    minTimeEnemie -= minTimeMinus
                    minTimeMinus = int(minTimeMinus/0.92)
                elif minTimeEnemie >= 750:
                    minTimeEnemie -= minTimeMinus
                    minTimeMinus = int(minTimeMinus/0.89)
                elif minTimeEnemie >= 500:
                    minTimeMinus = 10
                    minTimeEnemie -= minTimeMinus
                elif minTimeEnemie >= 250:
                    minTimeMinus = 7
                    minTimeEnemie -= minTimeMinus
                elif minTimeEnemie >= 175:
                    minTimeMinus = 5
                    minTimeEnemie -= minTimeMinus
                elif minTimeEnemie >= 150:
                    minTimeMinus = 4
                    minTimeEnemie -= minTimeMinus
                elif minTimeEnemie >= 125:
                    minTimeMinus = 2
                    minTimeEnemie -= minTimeMinus
                elif minTimeEnemie >= 50:
                    minTimeMinus = 1
                    minTimeEnemie -= minTimeMinus
                else:
                    minTimeMinus = 1
                    minTimeEnemie -= minTimeMinus
                try:
                    doSpawn = random.randint(int(minTimeEnemie), int(minTimeEnemie*2))
                except ValueError:
                    doSpawn = int(minTimeEnemie*1.25)
                if minTimeEnemie <= 0:
                    minTimeEnemie = 0
                    for i in range(2):
                        if townHall.level == 1:
                            max = 1
                        elif townHall.level == 2:
                            max = 2
                        elif townHall.level == 5:
                            max = 3
                        elif townHall.level == 8:
                            max = 4
                        elif townHall.level == 10:
                            max = 5
                        trp = random.randint(1,max) if max > 1 else max
                        x = random.randint(1, 4)
                        if townHall.level == 0:
                            min = townHall.level
                        else:
                            min = townHall.level-1
                        y = random.randint(min,townHall.level+int(townHall.level/3)+1)
                        if x == 1:
                            enemies.append(cs.Unit(screenGame, [random.randint(1, 1920), 0], c.buildingsAndUnits["units"][trp-1 if trp-1 != -1 else 1], y if y < 11 else random.randint(min,townHall.level), trp if trp-1!= -1 else 1, typeTroop=99))
                        elif x == 2:
                            enemies.append(cs.Unit(screenGame, [random.randint(1, 1920), 1080], c.buildingsAndUnits["units"][trp-1 if trp-1 != -1 else 1], y if y < 11 else random.randint(min,townHall.level), trp if trp-1!= -1 else 1, typeTroop=99))
                        elif x == 3:
                            enemies.append(cs.Unit(screenGame, [0, random.randint(1, 1080)], c.buildingsAndUnits["units"][trp-1 if trp-1 != -1 else 1], y if y < 11 else random.randint(min,townHall.level), trp if trp-1!= -1 else 1, typeTroop=99))
                        else:
                            enemies.append(cs.Unit(screenGame, [1920, random.randint(1, 1080)], c.buildingsAndUnits["units"][trp-1 if trp-1 != -1 else 1], y if y < 11 else random.randint(min,townHall.level), trp if trp-1!= -1 else 1, typeTroop=99))
                else:
                    if townHall.level == 0:
                        max = 2
                    elif townHall.level == 5:
                        max = 3
                    elif townHall.level == 8:
                        max = 4
                    elif townHall.level == 10:
                        max = 5
                    trp = random.randint(1,max) if max > 1 else max
                    x = random.randint(1, 4)
                    if townHall.level == 0:
                        min = townHall.level
                    else:
                        min = townHall.level-1
                    for i in range(townHall.level):
                        y = random.randint(min,townHall.level+int(townHall.level/3)+1)
                        if x == 1:
                            enemies.append(cs.Unit(screenGame, [random.randint(1, 1920), 0], c.buildingsAndUnits["units"][trp-1 if trp-1 != -1 else 1], y if y < 11 else random.randint(min,townHall.level), trp if trp-1!= -1 else 1, typeTroop=99))
                        elif x == 2:
                            enemies.append(cs.Unit(screenGame, [random.randint(1, 1920), 1080], c.buildingsAndUnits["units"][trp-1 if trp-1 != -1 else 1], y if y < 11 else random.randint(min,townHall.level), trp if trp-1!= -1 else 1, typeTroop=99))
                        elif x == 3:
                            enemies.append(cs.Unit(screenGame, [0, random.randint(1, 1080)], c.buildingsAndUnits["units"][trp-1 if trp-1 != -1 else 1], y if y < 11 else random.randint(min,townHall.level), trp if trp-1!= -1 else 1, typeTroop=99))
                        else:
                            enemies.append(cs.Unit(screenGame, [1920, random.randint(1, 1080)], c.buildingsAndUnits["units"][trp-1 if trp-1 != -1 else 1], y if y < 11 else random.randint(min,townHall.level), trp if trp-1!= -1 else 1, typeTroop=99))
            print(minTimeEnemie)
            tick = 0
        tick += 0.5
        timeSpend += 1

        if healTick >= 240:
            townHall.healHitpoints(townHall.hitpoints/100)
            for object in objects:
                object.healHitpoints(object.hitpoints/100)
            healTick = 0
        else:
            healTick += 1
        #! DEBUGING UND TESTING ONLY REMOVE AFTER!
        #townHall.money = townHall.maxMoney
    
    screen.blit(pg.transform.scale(screenGame, (c.screenSize[0], c.screenSize[1])), (0,0))
    
    # Fenster aktualisieren
    pg.display.flip()