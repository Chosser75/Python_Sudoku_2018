from tkinter import *
from tkinter import messagebox

import LayoutGenerator
import random
import time
import threading
import NewRecord
import os.path


sec = 1 # time in seconds
w = None
root = None
generator = None # instance of LayoutGenerator.py
combobox = None # difficulty level combobox
difficultyLevel = None # difficulty level
layout = None # generated layout
isSolutionShown = False # whether the correct solution is already shown
timer = None # Timer object
gameTime = False # is the game in progress
gameOver = False # is the game over
timeCount = "" # passed since the game was started time
checkRec = ""   # tuple report of the checkRecord() function
                # [[0]isNewRecord, [1]fileName, [2]operation]


''' Depending on the difficulty level, loads the best results from a 
related to the difficulty level file, and shows either window with the message
that there are no results yet or window with best results.'''
def showHOF():
    lines = []
    prompt = ""
    global difficultyLevel
    if difficultyLevel == "Beginner":
        fileName = "records_list_beginner.txt"
    elif difficultyLevel == "Advanced":
        fileName = "records_list_advanced.txt"
    elif difficultyLevel == "Master":
        fileName = "records_list_master.txt"
    if os.path.isfile(fileName):
        hof = open(fileName, 'r')
        if len(hof.readlines()) > 0:
            hof.seek(0, 0)
            lines = [line.split(";") for line in hof.readlines()]
            for line in lines:
                line[3] = int(line[3])
            sortedLines = sorted(lines, key = lambda player: player[3])  # sort by time
        else:
            prompt = "Oops, no records yet for " + difficultyLevel + " level..."
        hof.close()
    else:
        prompt = "Oops, no records yet for " + difficultyLevel + " level..."
    # if no records, just show "prompt" message
    if prompt != "":
        messagebox.showinfo("Best results", prompt)
    else:
        # show best results
        messageWindow("Best results", sortedLines)


'''Saves new record to the related to the current difficulty level file.
Creates new file if it does not exist, adds record if there are less than 5
records, deletes the worst result and adds new record 
if there are already 5 results in the file.'''
def processNewRecord(name):
    lines = []
    if name == "":
        name = "Anonymous"
    newRecordString = name + ";" + difficultyLevel + ";" + timeCount + ";" + str(sec - 1)
    if checkRec[2] == "new": # operation = new
        # just add new record
        try:
            hof = open(checkRec[1], "w")
            hof.write(newRecordString)
        except FileNotFoundError:
            # create file if it does not exist
            hof = open(checkRec[1], "w+")
            hof.write(newRecordString)
    elif checkRec[2] == "append": # operation = append
        # append new record to the file
        hof = open(checkRec[1], "a")
        hof.write("\n" + newRecordString)
    elif checkRec[2] == "rewrite": # operation = rewrite
        # replace the lowest result with the new record
        lines.append([name, difficultyLevel, timeCount, int(sec - 1)])
        hof = open(checkRec[1], "r")
        for line in hof.readlines():
            ls = line.split(";")
            ls[3] = int(ls[3])
            lines.append(ls)
            hof.close()
        sortedLines = sorted(lines, key=lambda player: player[3])  # sort by time
        sortedLines.pop()
        hof = open(checkRec[1], "w+")
        isFirst = True
        for line in sortedLines:
            if isFirst:
                hof.write(line[0]+";"+line[1]+";"+line[2]+";"+str(line[3]))
                isFirst = False
            else:
                hof.write("\n" + line[0] + ";" + line[1] + ";" + line[2] + ";" + str(line[3]))
    hof.close()


'''Opens related to the current difficulty level file and checks 
if the time of the current game is shorter than those saved in the file.
Returns report in a tuple of three parameters:
- Boolean isNewRecord
- String name of the related to the current difficulty level file
- String operation type (new, append, rewrite).'''
def checkRecord():
    global timeCount, sec, difficultyLevel
    isNewRecord = False
    fileName = ""
    operation = ""
    # Check if this is a new record
    if difficultyLevel == "Beginner":
        fileName = "records_list_beginner.txt"
    elif difficultyLevel == "Advanced":
        fileName = "records_list_advanced.txt"
    elif difficultyLevel == "Master":
        fileName = "records_list_master.txt"
    if os.path.isfile(fileName):
        hof = open(fileName, 'r')
        hofLen = len(hof.readlines())
        hof.seek(0, 0)
        # less than 5 records
        if 0 <= hofLen < 5:
            isNewRecord = True
            operation = "append"
        # 5+ records
        else:
            for line in hof.readlines():
                l = line.split(";")
                if int(l[3]) > sec:
                    isNewRecord = True
            operation = "rewrite"
    # new file
    else:
        isNewRecord = True
        operation = "new"
        hof = open(fileName, 'w+')
    hof.close()
    return isNewRecord, fileName, operation


'''Requests checkRecord() function to check if it is a new record.
Shows a window with congratulations and offering
user to enter his name when a new record is established.'''
def congratWinner():
    global timeCount, sec, checkRec
    isNewRecord = False
    checkRec = checkRecord()
    isNewRecord = checkRec[0]
    # it is a new record
    if isNewRecord:
        message = "Congratulations! \n\nYou have established a new record! \nYour time is " + timeCount + "\n\nEnter your name:"
        NewRecord.create_New_record(root, message)
    # not a record
    else:
        messagebox.showinfo("Winner", "Congratulations! \n" +
                              "Your solution is correct. \n" +
                               "Your time is " + timeCount)


'''Checks user's solution correctness.
If solution is correct, will call function congratWinner().
If is incorrect, will show error message.'''
def checkSolution():
    global gameTime, w, layout, isSolutionShown
    if isSolutionShown or not layout:
        return
    gameTime = False
    cells = w.getCells()
    n = 0
    isCorrect = True
    for l in layout:
        for i in l:
            if cells[n].get() == "" or int(cells[n].get()) != i:
                cells[n].configure({"foreground": "Red"})
                isCorrect = False
            cells[n].config(state="readonly")
            n += 1
    if isCorrect:
        congratWinner()
    else:
        messagebox.showerror("Error", "Sorry! \nYour solution is NOT correct. \nYour time is {0}".format(timeCount))


'''Stops game and fills in cells with correct numbers.'''
def showSolution():
    global isSolutionShown, w, layout, gameTime
    if not layout:
        return
    gameTime = False
    cells = w.getCells()
    n = 0
    for l in layout:
        for i in l:
            cells[n].config(state="NORMAL")
            cells[n].delete(0, END)
            cells[n].insert(0, i)
            cells[n].config(state="readonly")
            n += 1
    isSolutionShown = True


'''Starts and shows a timer, counting a time passed since the game was started.'''
def timerStart():
    global sec, gameTime, w, timeCount
    sec = 0
    while not gameOver:
        while gameTime:
            hours = sec // 3600
            minutes = (sec // 60) % 60
            seconds = sec % 60
            timeCount = ""
            if hours < 10:
                timeCount += "0"+str(hours)
            else:
                timeCount += str(hours)
            if minutes < 10:
                timeCount += ":0"+str(minutes)
            else:
                timeCount += ":"+str(minutes)
            if seconds < 10:
                timeCount += ":0"+str(seconds)
            else:
                timeCount += ":"+str(seconds)
            w.TLabel1.configure(text=timeCount)
            time.sleep(1)
            sec += 1


'''Starts a new game. Requests a new layout, fills in cells with these numbers,
 hiding some of the numbers depending of the current difficulty level.
 Starts a timer.'''
def startNewGame():
    global w, layout, isSolutionShown, timer, gameTime, sec, difficultyLevel
    isSolutionShown = False
    difficultyLevel = w.level.get()
    cells = w.getCells()
    layout = None
    while not layout:
        layout = generator.generateLayout()
    hn = 0
    if difficultyLevel == "Beginner":
        hn = 20
    elif difficultyLevel == "Advanced":
        hn = 30
    elif difficultyLevel == "Master":
        hn = 40
    hideNums = random.sample(range(1, 81), hn)
    n = 0
    for l in layout:
        for i in l:
            cells[n].config(state="NORMAL")
            cells[n].configure({"foreground": "Black"})
            if cells[n].get() != "":
                cells[n].delete(0, END)
            if n not in hideNums:
                cells[n].insert(0, i)
                cells[n].config(state="readonly")
            n += 1
    gameTime = True
    sec = 0
    if not timer:
        timer = threading.Timer(0, timerStart)
        timer.start()

'''Shows a window with the best results'''
def messageWindow(title, sortedLines):
    win = Toplevel()
    win.geometry("385x225+500+200")
    win.title(title)
    Label(win, text="Name").grid(row=0, column=0, ipady=5)
    Label(win, text="Difficulty").grid(row=0, column=1, ipady=5)
    Label(win, text="Time").grid(row=0, column=2, ipady=5)
    n = 1
    for line in sortedLines:
        Label(win, text=line[0]).grid(row=n, column=0, sticky=W, ipadx=40)
        Label(win, text=line[1]).grid(row=n, column=1, ipady=3)
        Label(win, text=line[2]).grid(row=n, column=2, ipadx=50)
        n += 1
    Label(win, text="    ").grid(row=n)
    Button(win, text='Thanks!', command=win.destroy).grid(row=7, columnspan=3, sticky=S)


def set_Tk_var():
    global combobox
    combobox = StringVar()


'''Initializer.'''
def init(top, gui, *args, **kwargs):
    global w, top_level, root, generator
    w = gui
    top_level = top
    root = top
    generator = LayoutGenerator.LayoutGenerator()
    set_Tk_var()
    return True


def destroy_window():
    # Function which closes the window.
    global gameTime
    print("bye bye")
    global top_level
    gameTime = False
    top_level.destroy()
    top_level = None


