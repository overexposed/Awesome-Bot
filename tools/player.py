import numpy as np
import tools.thread_
import time
import pyautogui as pg
import pygetwindow as pw
import random
from os.path import join
from PyQt5.QtCore import QMutex
import win32gui


randomVal = random.random
mutex = QMutex()
class playerClass:
    def __init__(self, playerName) -> None:
        self.FLAGend = False
        self.pathTemplate = "data/template/"
        self.name = playerName
        self.movement = self.movementClass()
        self.qName2fnc = {
            'Almanax': self.dq_almanax, 
            'Dede': self.dq_dede, 
            'Captain Amakna': self.dq_captainAmakna,
            'test': self.test_fnc}
    
    class movementClass:
        def __init__(self) -> None:
            # self.map = self.getCurrentMap()
            self.map = np.array([-23, 8])
        
        def lock(self):
            mutex.lock()
        
        def unlock(self):
            mutex.unlock()

        def isMapReached(self, vect):
            targetMap = self.map + vect
            print("targetmap: ", targetMap)

            if pg.locateOnScreen(f"data/template/almanax/map{targetMap[0]}{targetMap[1]}.png", confidence=0.8):
                return True
            else:
                if np.all(targetMap == np.array([-5,-24])):
                    if pg.locateOnScreen(f"data/template/almanax/map{targetMap[0]}{targetMap[1]}_v2.png", confidence=0.8):
                        return True
                else:
                    return False


        def movePlayer(self, moveCmd):
            """
            moveCmd = Top, Bot, Right, Left
            """
            height, width = pg.size()
            secs = 1
            if moveCmd == "T":
                # pg.click(1023, 37, duration=secs*randomVal())
                imgPos = np.random.uniform([450, 31], [1450, 42]).astype(int)
                vect = np.array([0, -1])
            elif moveCmd == "B":
                # pg.click(1025, 898, duration=secs*randomVal())
                imgPos = np.random.uniform([450, 890], [1450, 905]).astype(int)
                vect = np.array([0, 1])
            elif moveCmd == "R":
                # pg.click(1672, 505, duration=secs*randomVal())
                imgPos = np.random.uniform([1600, 80], [1880, 850]).astype(int)
                vect = np.array([1, 0])
            elif moveCmd == "L":
                # TODO: add the ranges for going left
                # imgPos = np.random.uniform([31, 450], [42, 1450]).astype(int)
                imgPos = np.array([246, 361])
                vect = np.array([-1, 0])

                # pg.click(np.random.uniform([low1, low2], [high1, high2]).astype(int), duration=secs*randomVal())
            else:
                raise Exception("Wrong move Command given: Send either 'T', 'B', 'R', 'L'")
            pg.click(imgPos[0], imgPos[1], duration=secs*randomVal())
        
            return vect

        def go2target(self, playerName, path2target):
            """
            Run this function on a thread.
            Every 2sec do
            - check if window is the correct player
            - if no change the window to correct player
            - check if map has changed
            - if no wait and recheck
            - check if current map is the one wanted
            - if no, find next move, apply move, go back to start loop (every 2 sec do)
            - if yes, map is reached end functionn
            """
            idx = 0
            failed_attempt = 0
            nextMove = path2target[0]
            skipSleep = True

            while (idx < len(path2target)) and (failed_attempt<5):
                if not skipSleep:
                    print("sleeping")
                    time.sleep(4*randomVal())
                print("mok")
                self.lock()
                self.focusWindow(playerName)
                if failed_attempt<2:
                    vect = self.movePlayer(nextMove)
                isSameMap = not self.isMapReached(vect)
                print("isSameMap: ", isSameMap)
                self.unlock()

                if isSameMap:
                    failed_attempt += 1
                    skipSleep = False
                    print("failed Attempt: ", failed_attempt)
                else:
                    failed_attempt = 0
                    idx += 1
                    if idx < len(path2target):                        
                        nextMove = path2target[idx]
                    self.map += vect
                    skipSleep = True

            return idx==len(path2target)

        def getCurrentPlayer():
            return "gaalhiro"

        def getCurrentMap():
            return np.array([-2, 24])

        def focusWindow(self, playerName):
            winlist = []
            def enum_callback(hwnd, results):
                winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

            win32gui.EnumWindows(enum_callback, [])
            playerWin = [hwnd for hwnd, title in winlist if playerName in title]
            win32gui.SetForegroundWindow(playerWin[0])

            # wins = [x for x in pg.getAllWindows() if "Dofus" in x.title]
            # print("wins: ", wins)
            # if not wins:
            #     print("wins is empty")
            # win2focus = [x for x in wins if (playerName in x.title)]
            # win2focus[0].minimize()
            # time.sleep(.1)
            # win2focus[0].restore()
            # # self.unlock()

            
    def createThread(self, thread):
        self.thread = thread

    def dq_almanax(self):
        sleepTime = 0.8
        """
        Assumptions/Preparation:
        - Ressources already bought
        - money for transport

        Strategy:
        - Tp to zaap
        - go to map
        - enter door
        - talk to maj ax
        - Click at fixed pos + Check if worked |or| Click at template pos
        - move 2 maps
        - look for "?" and click under it --> if issue, pause program and display pop-up for help
        - Multiple different talk --> develop a way to make it reliable
        - go back 2 maps 
        - talk to maj ax
        - End
        """
        if self.FLAGend:
            return False    
        print("ALMANAX SCRIPT START")
        pathAlma = join(self.pathTemplate, "almanax")
        # TODO: 
        # use confidence or gray scale?
        # Setup the dialog pop-up for issue (with sound?)
        # safeguard when quest already completed
        self.movement.lock()
        self.movement.focusWindow(self.name)
        pg.write("h")
        time.sleep(0.8)
        pg.click(529, 425, duration=randomVal())
        time.sleep(0.4)
        pg.typewrite("pork", 0.15)
        time.sleep(0.18)
        if self.FLAGend:
            return False 
        pg.press("enter")
        self.movement.unlock()
        self.movement.map = np.array([-5, -23])
        self.movement.go2target(self.name, ["T", "R"])
        while not pg.locateOnScreen(join(pathAlma,"almanaxDoor.png"), confidence=0.8):
            if self.FLAGend:
                return False
            time.sleep(1)
        pg.click(pg.locateOnScreen(join(pathAlma,"almanaxDoor.png"), confidence=0.8), duration=randomVal())
        while not pg.locateOnScreen(join(pathAlma, "majax.png"), confidence=0.8):
            if self.FLAGend:
                return False
            time.sleep(1)
        pg.click(pg.locateOnScreen(join(pathAlma, "majax.png"), confidence=0.8), duration=randomVal())
        time.sleep(sleepTime)
        pg.click(pg.locateOnScreen(join(pathAlma, "majaxDial1.png"), confidence=0.8), duration=randomVal())
        time.sleep(sleepTime)
        if self.FLAGend:
            return False 
        pg.click(pg.locateOnScreen(join(pathAlma, "majaxDial2.png"), confidence=0.8), duration=randomVal())
        time.sleep(sleepTime)
        pg.click(pg.locateOnScreen(join(pathAlma, "majaxDial3.png"), confidence=0.8), duration=randomVal())
        time.sleep(sleepTime)
        pg.click(pg.locateOnScreen(join(pathAlma, "majaxDial4.png"), confidence=0.8), duration=randomVal())
        time.sleep(sleepTime)

        pg.click(pg.locateOnScreen(join(pathAlma, "majax.png"), confidence=0.8), duration=randomVal())
        time.sleep(sleepTime)
        pg.click(pg.locateOnScreen(join(pathAlma, "majaxOffrande1.png"), confidence=0.8), duration=randomVal())
        time.sleep(sleepTime)
        pg.click(pg.locateOnScreen(join(pathAlma, "majaxOffrande2.png"), confidence=0.8), duration=randomVal())
        time.sleep(sleepTime)
        # TODO: Here if discussion is not yet finished click on 1st answer until end of disc
        #       OR pop-up
        if self.FLAGend:
            return False 
        
        pg.click(pg.locateOnScreen(join(pathAlma, "majaxEscalier.png"), confidence=0.8), duration=randomVal())
        while not pg.locateOnScreen(join(pathAlma, "grosseDameSaison.png"), confidence=0.8):
            if self.FLAGend:
                return False
            time.sleep(1)
        isDoorFound = False
        for _ in range(4):
            if pg.locateOnScreen(join(pathAlma, "porteSaison1.png"), confidence=0.8):
                pg.click(pg.locateOnScreen(join(pathAlma, "porteSaison1.png"), confidence=0.8), duration=randomVal())
                isDoorFound = True
                break
            elif pg.locateOnScreen(join(pathAlma, "porteSaison2.png"), confidence=0.8):
                pg.click(pg.locateOnScreen(join(pathAlma, "porteSaison2.png"), confidence=0.8), duration=randomVal())
                isDoorFound = True
                break
            elif pg.locateOnScreen(join(pathAlma, "porteSaison3.png"), confidence=0.8):
                pg.click(pg.locateOnScreen(join(pathAlma, "porteSaison3.png"), confidence=0.8), duration=randomVal())
                isDoorFound = True
                break
            elif pg.locateOnScreen(join(pathAlma, "porteSaison4.png"), confidence=0.8):
                pg.click(pg.locateOnScreen(join(pathAlma, "porteSaison4.png"), confidence=0.8), duration=randomVal())
                isDoorFound = True
                break
            time.sleep(sleepTime)
        if not isDoorFound:
            raise Exception("No template match for Season Doors")
        
        while not pg.locateOnScreen(join(pathAlma, "autel.png"), confidence=0.8):
            if self.FLAGend:
                return False
            time.sleep(1)
        pg.click(pg.locateOnScreen(join(pathAlma, "autel.png"), confidence=0.8), duration=randomVal())
        time.sleep(sleepTime)

        isPnjFound = False
        for _ in range(4):
            if pg.locateOnScreen(join(pathAlma, "dailyQ.png"), confidence=0.7):
                pg.click(pg.locateOnScreen(join(pathAlma, "dailyQ.png"), confidence=0.7), duration=randomVal())
                isPnjFound = True
                break
            elif pg.locateOnScreen(join(pathAlma, "dailyQv2.png"), confidence=0.7):
                pg.click(pg.locateOnScreen(join(pathAlma, "dailyQv2.png"), confidence=0.7), duration=randomVal())
                isPnjFound = True
                break
            else:
                pg.keyDown("z")
                if pg.locateOnScreen(join(pathAlma, "makssName.png"), confidence=0.8):
                    pg.click(pg.locateOnScreen(join(pathAlma, "makssName.png"), confidence=0.8), duration=randomVal())
                    pg.keyUp("z") 
                    isPnjFound = True
                    break
                elif pg.locateOnScreen(join(pathAlma, "laturb.png"), confidence=0.8):
                    pg.click(pg.locateOnScreen(join(pathAlma, "laturb.png"), confidence=0.8), duration=randomVal())
                    pg.keyUp("z") 
                    isPnjFound = True
                    break
                elif pg.locateOnScreen(join(pathAlma, "nosruo.png"), confidence=0.8):
                    pg.click(pg.locateOnScreen(join(pathAlma, "nosruo.png"), confidence=0.8), duration=randomVal())
                    pg.keyUp("z") 
                    isPnjFound = True
                    break
                else:
                    pg.keyUp("z") 
            time.sleep(1.3)   
        if not isPnjFound:
            raise Exception("No Pnj match in autel map")
        
        time.sleep(sleepTime)
        while pg.locateOnScreen(join(pathAlma, "answer.png"), confidence=0.9):
            highest = 100000
            for i in pg.locateAllOnScreen(join(pathAlma, "answer.png"), confidence=0.9):
                if i.top < highest:
                    highest = i.top
                    ans = i
            pg.click(ans, duration=randomVal())
            time.sleep(sleepTime)
        
        pg.click(682, 731, duration=randomVal())
        while not pg.locateOnScreen(join(pathAlma, "grosseDameSaison.png"), confidence=0.8):
            if self.FLAGend:
                return False
            time.sleep(1)
        pg.click(759, 771, duration=randomVal())
        while not pg.locateOnScreen(join(pathAlma, "majax.png"), confidence=0.8):
            if self.FLAGend:
                return False
            time.sleep(1)
        pg.click(pg.locateOnScreen(join(pathAlma, "majax.png"), confidence=0.8), duration=randomVal())
        time.sleep(sleepTime)
        pg.click(pg.locateOnScreen(join(pathAlma, "majaxEnd1.png"), confidence=0.8), duration=randomVal())
        time.sleep(sleepTime)
        pg.press("enter")
        time.sleep(sleepTime)
        pg.click(pg.locateOnScreen(join(pathAlma, "majaxEnd2.png"), confidence=0.8), duration=randomVal())
        time.sleep(sleepTime)
        pg.click(634, 752, duration=randomVal())
        while not pg.locateOnScreen(join(pathAlma, "almanaxDoor.png"), confidence=0.8):
            if self.FLAGend:
                return False
            time.sleep(1)
        print("ALMANAX SCRIPT DONE !")
        return True

    def dq_dede(self):
        """
        Iron available
        - Tp zaap
        - Go to map
        - Talk with pnj
        - Start fight
        - Depending on champ, select appropriate fight script
        - Close fight summary (click or "enter")
        - Get out
        - End
        """
        if self.FLAGend:
            return False
        
        print("hello I am currently running the dede script")
        for i in range(5):
            if self.FLAGend:
                return False
            print(i)
            time.sleep(1)
        print("dede script completed !")
        return True

    def dq_captainAmakna(self):
        """
        - Tp Zaap
        - Go to map
        - Talk to pnj
        
        x3
        - Go to map
        - Talk to Pnj
        - Fight

        - Go to map
        - Talk to captain pnj
        - End
        """
        if self.FLAGend:
            return False    
        print("Mok?")
        for i in range(5):
            if self.FLAGend:
                return False
            print(i)
            time.sleep(1)
        print("MokMok !")
        return True
    
    def test_fnc(self):
        if self.FLAGend:
            return False
        
        print("starting the test function ...")
        self.movement.go2target(self.name, ["L", "L", "B"])

        # self.movement.movePlayer("T")
        # time.sleep(3)
        # self.movement.movePlayer("B")
        # time.sleep(3)
        # self.movement.movePlayer("R")
        # time.sleep(3)
        # self.movement.movePlayer("L")
    # TODO: Later, add quest collecting bottles sufokia, ...