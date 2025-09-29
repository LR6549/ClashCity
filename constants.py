import os, pygame as pg

#* Screen-Center : 959 539
FULLSCREEN = True
screenSize  = [1920, 1080] #[int(input("Width in Pixel: ")), int(input("Height in Pixel: "))]
screenSizeBase  = [1920, 1080]
tileSize        = 32
scale           = [screenSizeBase[0]/screenSize[0], screenSizeBase[1]/screenSize[1]]

#*Paths
PATH            = os.path.dirname(os.path.abspath(__file__))
PATHIMG         = PATH          + r"\images"
PATHIMGTER      = PATHIMG       + r"\terrain"
PATHIMGBAU      = PATHIMG       + r"\buildingsAndUnits"
PATHIMGTWN      = PATHIMGBAU    + r"\townHalls"
PATHIMGBRK      = PATHIMGBAU    + r"\barracks"
PATHIMGMNS      = PATHIMGBAU    + r"\mines"
PATHIMGWLS      = PATHIMGBAU    + r"\walls"

PATHIMGBAR      = PATHIMGBAU    + r"\barbarian"
PATHIMGARC      = PATHIMGBAU    + r"\archer"
PATHIMGMIN      = PATHIMGBAU    + r"\miner"
PATHIMGDRA      = PATHIMGBAU    + r"\dragon"
PATHIMGPEK      = PATHIMGBAU    + r"\pekka"

PATHIMGGUI      = PATHIMG       + r"\gui"
PATHIMGSUR      = PATHIMG       + r"\surrounding"

position = [-959, -539]

#* Zoom, Frame etc
frameRate       = 60

terrainNumb = 13
terrainSelected = 0
terrains    = [
    pg.image.load(PATHIMGTER+fr"\terrain{i}.png") for i in range(terrainNumb)
]

selectedImage = pg.image.load(fr"{PATHIMGGUI}\selectedBG.png")
coinImage     = pg.image.load(fr"{PATHIMGMNS}\coin.png")

buildingsAndUnits = {
    "units":[ # 1-5 Barb, Archer, Miner, Dragon, Pekka
        [
            pg.image.load(fr"{PATHIMGBAR}\bb1.png"),
            pg.image.load(fr"{PATHIMGBAR}\bb2.png"),
            pg.image.load(fr"{PATHIMGBAR}\bb3.png"),
            pg.image.load(fr"{PATHIMGBAR}\bb4.png"),
            pg.image.load(fr"{PATHIMGBAR}\bb5.png"),
            pg.image.load(fr"{PATHIMGBAR}\bb6.png"),
            pg.image.load(fr"{PATHIMGBAR}\bb7.png"),
            pg.image.load(fr"{PATHIMGBAR}\bb8.png"),
            pg.image.load(fr"{PATHIMGBAR}\bb9.png"),
            pg.image.load(fr"{PATHIMGBAR}\bb10.png"),
            pg.image.load(fr"{PATHIMGBAR}\bb11.png"),
            pg.image.load(fr"{PATHIMGBAR}\bb12.png"),
        ],
        [
            pg.image.load(fr"{PATHIMGARC}\ac1.png"),
            pg.image.load(fr"{PATHIMGARC}\ac2.png"),
            pg.image.load(fr"{PATHIMGARC}\ac3.png"),
            pg.image.load(fr"{PATHIMGARC}\ac4.png"),
            pg.image.load(fr"{PATHIMGARC}\ac5.png"),
            pg.image.load(fr"{PATHIMGARC}\ac6.png"),
            pg.image.load(fr"{PATHIMGARC}\ac7.png"),
            pg.image.load(fr"{PATHIMGARC}\ac8.png"),
            pg.image.load(fr"{PATHIMGARC}\ac9.png"),
            pg.image.load(fr"{PATHIMGARC}\ac10.png"),
            pg.image.load(fr"{PATHIMGARC}\ac11.png"),
            pg.image.load(fr"{PATHIMGARC}\ac12.png"),
        ],
        [
            pg.image.load(fr"{PATHIMGMIN}\mr1.png"),
            pg.image.load(fr"{PATHIMGMIN}\mr2.png"),
            pg.image.load(fr"{PATHIMGMIN}\mr3.png"),
            pg.image.load(fr"{PATHIMGMIN}\mr4.png"),
            pg.image.load(fr"{PATHIMGMIN}\mr5.png"),
            pg.image.load(fr"{PATHIMGMIN}\mr6.png"),
            pg.image.load(fr"{PATHIMGMIN}\mr7.png"),
            pg.image.load(fr"{PATHIMGMIN}\mr8.png"),
            pg.image.load(fr"{PATHIMGMIN}\mr9.png"),
            pg.image.load(fr"{PATHIMGMIN}\mr10.png"),
            pg.image.load(fr"{PATHIMGMIN}\mr11.png"),
            pg.image.load(fr"{PATHIMGMIN}\mr12.png"),
        ],
        [
            pg.image.load(fr"{PATHIMGDRA}\dg1.png"),
            pg.image.load(fr"{PATHIMGDRA}\dg2.png"),
            pg.image.load(fr"{PATHIMGDRA}\dg3.png"),
            pg.image.load(fr"{PATHIMGDRA}\dg4.png"),
            pg.image.load(fr"{PATHIMGDRA}\dg5.png"),
            pg.image.load(fr"{PATHIMGDRA}\dg6.png"),
            pg.image.load(fr"{PATHIMGDRA}\dg7.png"),
            pg.image.load(fr"{PATHIMGDRA}\dg8.png"),
            pg.image.load(fr"{PATHIMGDRA}\dg9.png"),
            pg.image.load(fr"{PATHIMGDRA}\dg10.png"),
            pg.image.load(fr"{PATHIMGDRA}\dg11.png"),
            pg.image.load(fr"{PATHIMGDRA}\dg12.png"),
        ],
        [
            pg.image.load(fr"{PATHIMGPEK}\pk1.png"),
            pg.image.load(fr"{PATHIMGPEK}\pk2.png"),
            pg.image.load(fr"{PATHIMGPEK}\pk3.png"),
            pg.image.load(fr"{PATHIMGPEK}\pk4.png"),
            pg.image.load(fr"{PATHIMGPEK}\pk5.png"),
            pg.image.load(fr"{PATHIMGPEK}\pk6.png"),
            pg.image.load(fr"{PATHIMGPEK}\pk7.png"),
            pg.image.load(fr"{PATHIMGPEK}\pk8.png"),
            pg.image.load(fr"{PATHIMGPEK}\pk9.png"),
            pg.image.load(fr"{PATHIMGPEK}\pk10.png"),
            pg.image.load(fr"{PATHIMGPEK}\pk11.png"),
            pg.image.load(fr"{PATHIMGPEK}\pk12.png"),
        ],
    ],
    "townHalls":[
        pg.image.load(fr"{PATHIMGTWN}\th1.png"),
        pg.image.load(fr"{PATHIMGTWN}\th2.png"),
        pg.image.load(fr"{PATHIMGTWN}\th3.png"),
        pg.image.load(fr"{PATHIMGTWN}\th4.png"),
        pg.image.load(fr"{PATHIMGTWN}\th5.png"),
        pg.image.load(fr"{PATHIMGTWN}\th6.png"),
        pg.image.load(fr"{PATHIMGTWN}\th7.png"),
        pg.image.load(fr"{PATHIMGTWN}\th8.png"),
        pg.image.load(fr"{PATHIMGTWN}\th9.png"),
        pg.image.load(fr"{PATHIMGTWN}\th10.png"),
        pg.image.load(fr"{PATHIMGTWN}\th11.png"),
        pg.image.load(fr"{PATHIMGTWN}\th12.png"),
    ],
    "barrack":[
        pg.image.load(fr"{PATHIMGBRK}\br1.png"),
        pg.image.load(fr"{PATHIMGBRK}\br2.png"),
        pg.image.load(fr"{PATHIMGBRK}\br3.png"),
        pg.image.load(fr"{PATHIMGBRK}\br4.png"),
        pg.image.load(fr"{PATHIMGBRK}\br5.png"),
        pg.image.load(fr"{PATHIMGBRK}\br6.png"),
        pg.image.load(fr"{PATHIMGBRK}\br7.png"),
        pg.image.load(fr"{PATHIMGBRK}\br8.png"),
        pg.image.load(fr"{PATHIMGBRK}\br9.png"),
        pg.image.load(fr"{PATHIMGBRK}\br10.png"),
        pg.image.load(fr"{PATHIMGBRK}\br11.png"),
        pg.image.load(fr"{PATHIMGBRK}\br12.png"),
    ],
    "mine":[
        pg.image.load(fr"{PATHIMGMNS}\mn1.png"),
        pg.image.load(fr"{PATHIMGMNS}\mn2.png"),
        pg.image.load(fr"{PATHIMGMNS}\mn3.png"),
        pg.image.load(fr"{PATHIMGMNS}\mn4.png"),
        pg.image.load(fr"{PATHIMGMNS}\mn5.png"),
        pg.image.load(fr"{PATHIMGMNS}\mn6.png"),
        pg.image.load(fr"{PATHIMGMNS}\mn7.png"),
        pg.image.load(fr"{PATHIMGMNS}\mn8.png"),
        pg.image.load(fr"{PATHIMGMNS}\mn9.png"),
        pg.image.load(fr"{PATHIMGMNS}\mn10.png"),
        pg.image.load(fr"{PATHIMGMNS}\mn11.png"),
        pg.image.load(fr"{PATHIMGMNS}\mn12.png"),
    ],
    "wall":[
        pg.image.load(fr"{PATHIMGWLS}\wl1.png"),
        pg.image.load(fr"{PATHIMGWLS}\wl2.png"),
        pg.image.load(fr"{PATHIMGWLS}\wl3.png"),
        pg.image.load(fr"{PATHIMGWLS}\wl4.png"),
        pg.image.load(fr"{PATHIMGWLS}\wl5.png"),
        pg.image.load(fr"{PATHIMGWLS}\wl6.png"),
        pg.image.load(fr"{PATHIMGWLS}\wl7.png"),
        pg.image.load(fr"{PATHIMGWLS}\wl8.png"),
        pg.image.load(fr"{PATHIMGWLS}\wl9.png"),
        pg.image.load(fr"{PATHIMGWLS}\wl10.png"),
        pg.image.load(fr"{PATHIMGWLS}\wl11.png"),
        pg.image.load(fr"{PATHIMGWLS}\wl12.png"),
    ],
}

# for key in buildingsAndUnits.keys():
#     for i in range(len(buildingsAndUnits[key])):
#         if isinstance(buildingsAndUnits[key][i], list):
#             for j in range(len(buildingsAndUnits[key][i])):
#                 buildingsAndUnits[key][i][j] = pg.transform.scale(buildingsAndUnits[key][i][j], (int(buildingsAndUnits[key][i][j].get_width()*scale[0]), int(buildingsAndUnits[key][i][j].get_height()*scale[1])))
#         else:
#             buildingsAndUnits[key][i] = pg.transform.scale(buildingsAndUnits[key][i], (int(buildingsAndUnits[key][i].get_width()*scale[0]), int(buildingsAndUnits[key][i].get_height()*scale[1])))

# for image in terrains:
#     pg.transform.scale(image, (image.get_width()*scale[0], image.get_height()*scale[1]))

infos = {
    "barrack":{
        "cost":55
    },
    "mine":{
        "cost":35
    },
    "wall":{
        "cost":15
    },
}