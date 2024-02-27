import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import time
from os.path import join, exists
from os import listdir
import cv2
from PyQt5 import QtWidgets, QtCore, uic, QtGui
import pyautogui as pg
from random import random

from gui.startup import Ui_MainWindow
from tools.player import playerClass
from tools import thread_

# TODO: Make sure all click actions are made with a random duration from currentCursorPos to FinalCursorPos. (0->1 sec)

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('gui/startup.ui', self)
        self.threadpool = QtCore.QThreadPool()
        self.threads = []
        self.connect_btns()

    def closeEvent(self, event):
        print("closing the window")
        try:
            if hasattr(self, 'players'):
                for pl in self.players:
                    pl.FLAGend = True
        except:
            raise Exception("couldnt set endFlag to True")
        event.accept()

    def connect_btns(self):
        self.refresh_btn.clicked.connect(self.refresh_table)
        self.start_btn.clicked.connect(self.start_noobz)
        self.stop_btn.clicked.connect(self.stop_all)
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)

    def stop_all(self):
        self.stop_btn.setEnabled(False)
        for plyr in self.players:
            plyr.FLAGend = True
            # TODO: also stop subsequent threads
        self.allQuests.clear()

    def start_noobz(self):
        self.refresh_btn.setEnabled(False)
        self.start_btn.setEnabled(False)

        self.allQuests = dict()
        for r, rowName in enumerate(self.names):
            quests = []
            for c, colName in enumerate(self.colNames):
                if c == 0:
                    continue
                if self.tableWidget.item(r, c).checkState() == 2:
                    quests.append(colName)
            self.allQuests[rowName] = quests
        print("all quests: ", self.allQuests)
        self.stop_btn.setEnabled(True)
        self.start()

    def start(self):
        if not self.allQuests:
            print("No quests checked")
            return
        self.players = []
        for playerName in self.allQuests.keys():
            if not self.allQuests[playerName]:
                continue
            self.players.append(playerClass(playerName))

        for player in self.players:
            questName = self.allQuests[player.name].pop(0)
            player.createThread(thread_.Worker(fn=player.qName2fnc[questName],  playerName=player.name))
            player.thread.signals.finished.connect(self.end_mission)
            player.thread.signals.result.connect(lambda x: print("Result: ", x))
            player.thread.signals.error.connect(lambda x: print(x))
            self.threadpool.start(player.thread)

    def end_mission(self, playerNameFromThread):
        if not self.allQuests:
            print(f"Stop {playerNameFromThread}")
            # Remove player from the self.players list
            idx2remove = []
            for i, plyr in enumerate(self.players):
                if plyr.name == playerNameFromThread:
                    idx2remove.append(i)
            idx2remove.sort(reverse=True)
            for i in idx2remove:
                self.players.pop(i)
            if not self.players:
                self.refresh_btn.setEnabled(True)

        elif not self.allQuests[playerNameFromThread]:
            print(f"{playerNameFromThread} completed all quests !")
            # Remove player from the self.players list
            idx2remove = []
            for i, plyr in enumerate(self.players):
                if plyr.name == playerNameFromThread:
                    idx2remove.append(i)
            idx2remove.sort(reverse=True)
            for i in idx2remove:
                self.players.pop(i)
            
            if (not any(self.allQuests.values())) and (len(self.players)==0):
                print("all Quests for all players have been completed")
                self.refresh_btn.setEnabled(True)

        else:
            # setup next mission and start it
            print(f"{playerNameFromThread} completed the quest succesfully !")
            questName = self.allQuests[playerNameFromThread].pop(0)
            print(f"{playerNameFromThread} now starting {questName} ...")
            for plyr in self.players:
                if (plyr.name == playerNameFromThread):
                    plyr.createThread(thread_.Worker(fn=plyr.qName2fnc[questName], playerName=plyr.name))
                    plyr.thread.signals.finished.connect(self.end_mission)
                    plyr.thread.signals.result.connect(lambda x: print("Result: ", x))
                    plyr.thread.signals.error.connect(lambda x: print(x))
                    self.threadpool.start(plyr.thread)
                    return

    def refresh_table(self):
        wins = [x for x in pg.getAllWindows() if "Dofus" in x.title]
        if not wins:
            print("no windows found")
            return
        self.start_btn.setEnabled(True)
        self.names = [x.title.split(" - ")[0] for x in wins]
        # self.names = ["hironoobs", "gaalnoobs"]   # for debugging
        print(self.names)

        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(len(self.names))
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.colNames = ['Player', 'Almanax', 'Dede', 'Captain Amakna', 'test']
        self.tableWidget.setHorizontalHeaderLabels(self.colNames)

        for col, string in enumerate(self.colNames):
            for row, name in enumerate(self.names):
                if col==0:
                    self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(name))
                else:
                    chkBoxItem = QtWidgets.QTableWidgetItem(string)
                    chkBoxItem.setText("Check Box")
                    chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    chkBoxItem.setCheckState(QtCore.Qt.Checked)
                    self.tableWidget.setItem(row, col, chkBoxItem)



def main():
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())


# TODO:
# Add "Stop_btn" to [stop all threads] + [prevent next thread from being executed], without exiting the program
# Add Checkbox State: "in progress", "Done", "Waiting" as the label
# Add unique start_btn and stop_btn for each player
# Handle errors (pause program? stop program? stop gui?)

if __name__ == "__main__" :
    main()
    # pg.mouseInfo()