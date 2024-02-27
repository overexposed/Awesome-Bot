import pyautogui as pg
import pygetwindow as pw
import time
from tools.player import playerClass
from random import random as randomVal
import numpy as np
from os.path import join

pathAlma = "data/template/almanax"
# pg.click("data/template/icon_google.png", duration=2*random.random())


medems = pg.getWindowsWithTitle(title="Ad-renalyn")[0]
medems.minimize()
medems.maximize()
time.sleep(0.5)
print(pg.locateOnScreen(join(pathAlma, "map-5-24.png"), confidence=0.6))
#  pg.locateOnScreen(f"data/template/almanax/map{targetMap[0]}{targetMap[1]}_v2.png", confidence=0.8):
# pg.click(pg.locateOnScreen(join(pathAlma, "answer.png"), confidence=0.8))

# player = playerClass("gr")
# player.movement.map = np.array([-5, -23])
# player.movement.go2target(player.name, ["T", "R"])
# while not pg.locateOnScreen(join(pathAlma,"almanaxDoor.png")):
#     time.sleep(1)
# pg.click(join(pathAlma,"almanaxDoor.png"), duration=randomVal())


# print(pg.locateAllOnScreen("data/template/almanax/dailyQ.png", confidence=0.8))
# pg.click(pg.locateOnScreen("data/template/almanax/dailyQ1.png", confidence=0.8))

