import random as r
import time as t
import unidecode as u
import pygame
from pygame.locals import *

WHITE = "#FFFFFF"
BLACK = "#000000"
RED = "#FF0000"
GREEN = "#00FF00"
DARKGREEN = "#228B22"
GOLD = "#EEC900"
BEIGE = "#FFF8DC"

POLICE = "resources/MVSansBold.ttf"

START = "start"
READY = "ready"
INGAME = "in game"
RESULTS = "results"
END = "end"
LAST = "last"
FIRST = "first"

# API Initialization

import sys
from tkinter import *
from ezyapi.UUID import UUID
import ezyapi.game_manager as manager
from ezyapi.game_manager import GameVersion
from ezyapi.sessions import UserNotFoundException
from ezyapi.mysql_connection import DatabaseConnexionError


GAME_UUID = UUID("6d5ee3d7-35e5-411e-38a1-0eab2b9ef338")
GAME_VERSION = GameVersion("v2.0")


class Error(Tk):
    def __init__(self, name: str, desc: str):
        super().__init__("err")
        self.app_bg = DARKGREEN
        self.app_fg = BEIGE
        self.app_circle_color = GOLD
        self.app_cross_color = RED

        self.title("Erreur")
        # self.resizable(False, False)
        self.geometry("300x300")
        self.configure(background=self.app_bg)

        self.name, self.desc = name, desc

        self.name_label = Label(self, bg=self.app_bg, fg=self.app_fg, font=("", 16, "bold"), wraplengt=300, text=name)
        self.name_label.pack(side=TOP, pady=10)

        self.desc_label = Label(self, bg=self.app_bg, fg=self.app_fg, wraplengt=300, text=desc)
        self.desc_label.pack(side=TOP, pady=10)

        self.opt_frame = Frame(self, bg=self.app_bg)
        self.cont_frame = Frame(self.opt_frame, bg=self.app_circle_color)
        self.cont_btn = Button(self.cont_frame, activebackground=self.app_bg, bg=self.app_bg, bd=0, relief=SOLID,
                               width=12, activeforeground=self.app_circle_color, fg=self.app_circle_color,
                               highlightcolor=self.app_circle_color, font=("", 12, "bold"), text="Continuer !",
                               command=self.cont_cmd)
        self.cont_btn.pack(padx=1, pady=1)
        self.cont_frame.pack(side=LEFT, padx=5)
        self.quit_frame = Frame(self.opt_frame, bg=self.app_cross_color)
        self.quit_btn = Button(self.quit_frame, activebackground=self.app_bg, bg=self.app_bg, bd=0, relief=SOLID,
                               width=12, activeforeground=self.app_cross_color, fg=self.app_cross_color,
                               highlightcolor=self.app_cross_color, font=("", 12, "bold"), text="Quitter.",
                               command=self.quit_cmd)
        self.quit_btn.pack(padx=1, pady=1)
        self.quit_frame.pack(side=RIGHT, padx=5)
        self.opt_frame.pack(side=BOTTOM, pady=5)

        self.protocol("WM_DELETE_WINDOW", self.quit_cmd)
        self.bind("<Configure>", self.event_handler)
        self.bind("<Return>", self.on_return)
        self.quit_btn.focus_set()

        self.mainloop()

    def on_return(self, event=None):
        if self.focus_get() == self.cont_btn:
            self.cont_cmd()
        elif self.focus_get() == self.quit_btn:
            self.quit_cmd()

    def cont_cmd(self, event=None):
        self.destroy()

    def quit_cmd(self, event=None):
        try:
            sys.exit(1)
        except NameError:
            quit(1)

    def event_handler(self, event=None):
        new_wrap = int(self.winfo_geometry().split("x")[0]) - 5
        self.name_label.config(wraplengt=new_wrap)
        self.desc_label.config(wraplengt=new_wrap)


CONTINUE = "\n\nIf you Continue, you will not be able to get rewards and update the ranking."
try:
    try:
        manager.setup(GAME_UUID, GAME_VERSION)
    except manager.UserParameterExpected as e:
        Error("UserParameterExpected", str(e) + "\nYou must run the game from the Launcher to avoid this error." + CONTINUE)
    except UserNotFoundException as e:
        Error("UserNotFoundException", str(e) + "\nThe user information given does not match with any user." + CONTINUE)
    except manager.GameNotFound as e:
        Error("GameNotFound", str(e) + CONTINUE)
except DatabaseConnexionError as e:
    Error("DatabaseConnexionError",
          str(e) + "\nThe SQL Serveur is potentially down for maintenance...\nWait and Retry Later." + CONTINUE)

# Force Refresh Word Data (.temp files) and Icon
_ = [r.save_by_erasing("resources", name="icon" if r.specification == "icon" else None) for r in manager.import_resources(GAME_UUID) if r.type == "temp" or r.specification == "icon"]

###

pygame.init()

pygame.display.set_caption('Word Typer')
icon = pygame.image.load('resources/icon.png')
pygame.display.set_icon(icon)
window = pygame.display.set_mode((800, 600))
window.fill(BEIGE)

def writeText(text, coordx, coordy, fontSize, color):
    font = pygame.font.Font(POLICE, fontSize)
    text = font.render(str(text).upper(), False, color)
    window.blit(text, (coordx, coordy))
    pygame.display.flip()

def writeTextTop(text, coordx, fontSize, color):
    font = pygame.font.Font(POLICE, fontSize)
    text = font.render(str(text).upper(), False, color)
    window.blit(text, (coordx, 50))
    pygame.display.flip()

def writeTextMid(text, coordx, fontSize, color):
    font = pygame.font.Font(POLICE, fontSize)
    text = font.render(str(text).upper(), False, color)
    window.blit(text, (coordx, 270))
    pygame.display.flip()

def writeLilText(text, coordx, coordy, color):
    font = pygame.font.Font(POLICE, 25)
    text = font.render(str(text).upper(), False, color)
    window.blit(text, (coordx, coordy))
    pygame.display.flip()

def writeWord(text):
    drawWordRect()
    font = pygame.font.Font(POLICE, 50)
    text = font.render(str(text).upper(), False, WHITE)
    window.blit(text, (250, 160))
    pygame.display.flip()

def writePoints(points):
    drawPointsdRect()
    font = pygame.font.Font(POLICE, 25)
    text = font.render(str("PTS :"), False, RED)
    window.blit(text, (650, 535))
    text1 = font.render(str(points), False, RED)
    window.blit(text1, (730, 535))
    pygame.display.flip()

def writeTime(time):
    drawTimeRect()
    font = pygame.font.Font(POLICE, 25)
    text = font.render(str(time), False, RED)
    window.blit(text, (45, 535))
    pygame.display.flip()

def drawTimeRect():
    pygame.draw.rect(window, BEIGE, (40, 530, 40, 35))
    pygame.display.flip()

def drawPointsdRect():
    pygame.draw.rect(window, BEIGE, (725, 530, 40, 35))
    pygame.display.flip()

def drawRectTop():
    pygame.draw.rect(window, GOLD, (30, 30, 740, 100))
    pygame.display.flip()

def drawRectMid():
    pygame.draw.rect(window, BLACK, (30, 250, 740, 100))
    pygame.display.flip()

def drawWordRect():
    pygame.draw.rect(window, BLACK, (30, 140, 740, 100))
    pygame.display.flip()

def drawRestartButton():
    pygame.draw.rect(window, BLACK, (300, 120, 200, 100))
    writeText("restart", 330, 150, 30, BEIGE)
    pygame.display.flip()

def drawStartButton():
    pygame.draw.rect(window, BLACK, (300, 270, 200, 100))
    writeText("start", 360, 300, 30, BEIGE)
    pygame.display.flip()

def startMenu():
    clearWindow()
    drawRectTop()
    writeTextTop("word typer", 230, 50, BLACK)
    drawStartButton()

def readyMenu():
    clearWindow()
    drawRectTop()
    drawRectMid()
    clearText()
    writeTextTop("ready?", 320, 40, BLACK)
    writeLilText("(press enter to start)", 240, 95, BLACK)

def getFile():
    fichier = open("resources/word_data.temp", "r")
    wordList = fichier.read().split(', ')
    fichier.close()
    return wordList
#
def isAnswerTrue(answer, word):
    if answer == word:
        return True
    else:
        return False

def start():
    t0 = t.time()
    return t0

def getTime(t0):
    t1 = t.time()
    time = round(t1 - t0)
    return time

def clearText():
    pygame.draw.rect(window, BEIGE, (50, 275, 700, 50))
    pygame.display.flip()

def getWordList2():
    wordList2 = []
    wordList = getFile()
    nbWord = 0
    while not 150 < nbWord < 160:
        while len(wordList2) != 25:
            randomNumberData = r.randint(0, len(wordList) - 1)
            randomWordData = u.unidecode(wordList[randomNumberData])
            if randomWordData not in wordList2 and randomWordData.isalpha():
                wordList2.append(randomWordData)
                nbWord += len(randomWordData)
        if not 150 < nbWord < 160:
            randomNumberList = r.randint(0, len(wordList2) - 1)
            randomWordList = wordList2[randomNumberList]
            wordList2.remove(randomWordList)


    return wordList2

def clearWindow():
    window.fill(BEIGE)
    pygame.draw.rect(window, DARKGREEN, (0, 0, 1000, 30))
    pygame.draw.rect(window, DARKGREEN, (0, 570, 1000, 30))
    pygame.draw.rect(window, DARKGREEN, (770, 0, 30, 1000))
    pygame.draw.rect(window, DARKGREEN, (0, 0, 30, 1000))
    pygame.display.flip()

def userClickStart(event):
    if (event.type == MOUSEBUTTONDOWN and event.button == 1 and 300 < event.pos[0] < 500 and 270 < event.pos[1] < 370) or (event.type == KEYDOWN and event.key != K_ESCAPE):
        return True
    else:
        return False

def userQuitGame(event):
    if event.type == KEYDOWN and event.key == K_ESCAPE:
        return True
    else:
        return False


def main():
    startMenu()
    step = START
    answer = ""
    numWord = 0
    word = ""
    nbrLettre = 0
    wordTyped = ""
    continuer = 1
    points = 0
    t0 = 0
    time = 0
    wordTurn = FIRST
    scoreTurn = FIRST
    timeTurn = FIRST
    turn = None
    score = 0
    wordList2 = []
    while continuer:
        for event in pygame.event.get():
            if step == START and userClickStart(event):
                step = READY
                readyMenu()
                print("start ok")

            elif step == READY and event.type == KEYDOWN and event.key == K_RETURN:
                drawRectTop()
                for i in range(3):
                    writeTextTop(str(i + 1), 380, 50, BLACK)
                    t.sleep(0.5)
                    drawRectTop()
                    pygame.display.flip()
                step = INGAME
                writeTextTop("Let's go!", 280, 50, BLACK)
                wordList2 = getWordList2()
                word = wordList2[numWord]
                t0 = start()
                print("ready ok")

            elif step == INGAME and event.type == KEYDOWN and event.key == K_BACKSPACE and nbrLettre > 0:
                clearText()
                wordTyped = wordTyped[:-1]
                writeTextMid(wordTyped, 100, 50, BLACK)
                nbrLettre -= 1
                print("supr ok")

            elif step == INGAME and event.type == KEYDOWN and event.key != K_ESCAPE:
                lettre = pygame.key.name(event.key)
                if len(lettre) == 1 and lettre.isalpha():
                    wordTyped += lettre
                    writeTextMid(wordTyped, 100, 50, BLACK)
                    nbrLettre += 1
                    answer = wordTyped
                    print("lettre =", lettre)
                    print("wordTyped =", wordTyped)
                    print("nbrLettre =", nbrLettre)
                    print()
                    print("lettre ok")

            elif step == END and event.type == MOUSEBUTTONDOWN and event.button == 1 and 270 < event.pos[0] < 470 and 120 < event.pos[1] < 220 or step == END and event.type == KEYDOWN and event.key == K_RETURN:
                step = READY
                answer = ""
                numWord = 0
                word = ""
                nbrLettre = 0
                wordTyped = ""
                points = 0
                t0 = 0
                time = 0
                wordTurn = FIRST
                scoreTurn = FIRST
                timeTurn = FIRST
                score = 0
                readyMenu()
                print("restart ok")

            elif userQuitGame(event):
                step = START
                answer = ""
                numWord = 0
                word = ""
                nbrLettre = 0
                wordTyped = ""
                points = 0
                t0 = 0
                time = 0
                wordTurn = FIRST
                scoreTurn = FIRST
                timeTurn = FIRST
                score = 0
                startMenu()
                print("quit ok")

            elif event.type == QUIT:
                continuer = 0
                exit()

            pygame.display.flip()


        if step == INGAME and isAnswerTrue(answer, word):
            answer = ""
            points += 1
            clearText()
            nbrLettre = 0
            wordTyped = ""
            numWord += 1
            print("answertrue ok")

        elif step == INGAME and time >= 30:
            step = RESULTS
            turn = LAST
            print(f"end ok {numWord=}")

            if manager.linked():
                manager.start_new_game()
                manager.commit_new_set(numWord >= 12, exp_earned=numWord * 8, gp_earned=0 if numWord < 15 else (numWord - 14), other=f"{numWord=}")

        elif step == INGAME:
            wordTest = word
            word = wordList2[numWord]
            if word != wordTest:
                writeWord(word)
            if wordTurn == FIRST:
                writeWord(word)
                wordTurn = None

            scoreTest = score
            score = points
            if score != scoreTest:
                writePoints(score)
            if scoreTurn == FIRST:
                writePoints(score)
                scoreTurn = None

            timeTest = time
            time = getTime(t0)
            if time != timeTest:
                writeTime(time)
            if timeTurn == FIRST:
                writeTime(time)
                timeTurn = None

            if 3.5 >= getTime(t0) >= 3:
                drawRectTop()

        elif step == RESULTS:
            clearWindow()
            if turn == LAST:
                if len(str(points)) == 2:
                    writeText(points, 125, 245, 60, RED)
                else:
                    writeText(points, 155, 245, 60, RED)
                writeTextMid("mots en 30 secondes", 225, 30, BLACK)
                turn = None
                drawRestartButton()
                step = END


        pygame.display.flip()

    return score


main()
