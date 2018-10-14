from tkinter import *
import tkinter.ttk as ttk
import SudokuController


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", onClose)
    top = SudokuBrainteaser(root)
    SudokuController.init(root, top)
    SudokuController.startNewGame()
    root.mainloop()


def onClose():
    SudokuController.gameTime = False
    SudokuController.gameOver = True
    root.destroy()


w = None
def create_Sudoku_brainteaser(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    top = SudokuBrainteaser(w)
    SudokuController.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_Sudoku_brainteaser():
    print("bye bye")
    global w
    SudokuController.gameTime = False
    w.destroy()
    w = None


def testVal(inStr,i,acttyp):
    ind=int(i)
    if ind > 0:
        return False
    if acttyp == '1': #insert
        if not inStr[ind].isdigit():
            return False
        else:
            if int(inStr[ind]) == 0:
                return False
    return True


''' Defines application UI '''
class SudokuBrainteaser:

    cells = []
    x = 0
    y = 0.11
            
    def __init__(self, top=None):
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85'
        font13 = "-family {Segoe UI} -size 13 -weight normal -slant " \
                 "roman -underline 0 -overstrike 0"
        font16 = "-family {Segoe UI} -size 20 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"
        font18 = "-family {Segoe UI} -size 18 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("629x740+400+6")
        top.title("Sudoku brainteaser")
        top.configure(relief="sunken")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        def buildCell():
            self.c = ttk.Entry(top)
            self.c.place(relx=self.x, rely=self.y, relheight=0.06, relwidth=0.07)
            self.c.configure(font=font16)
            self.c.configure(justify=CENTER)
            self.c.configure(validate="key")
            self.c.configure(validatecommand=(self.c.register(testVal), '%P', '%i', '%d'))
            self.c.configure(width=46)
            self.c.configure(background="#000000")
            self.c.configure(takefocus="")
            self.c.configure(cursor="ibeam")
            self.cells.append(self.c)

        def buildRow():
            self.x = 0.06
            for n in range(3):
                for i in range(3):
                    buildCell()
                    self.x += 0.09
                self.x += 0.04

        for n in range(3):
            for i in range(3):
                buildRow()
                self.y += 0.07
            self.y += 0.04

        self.level = ttk.Combobox(top)
        self.level.place(relx=0.35, rely=0.85, relheight=0.04, relwidth=0.3)
        self.value_list = ["Beginner", "Advanced", "Master"]
        self.level.configure(font=font13)
        self.level.configure(values=self.value_list)
        self.level.configure(justify=CENTER)
        self.level.configure(textvariable=SudokuController.combobox)
        self.level.set("Beginner")
        self.level.configure()
        self.level.configure(takefocus="")
        self.level.config(state="readonly")
        self.level.bind("<<ComboboxSelected>>", lambda _: SudokuController.startNewGame())

        self.TLabel1 = ttk.Label(top)
        self.TLabel1.place(relx=0.4, rely=0.03, relheight=0.05, relwidth=0.2)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(font=font18)
        self.TLabel1.configure(relief=SUNKEN)
        self.TLabel1.configure(anchor=CENTER)
        self.TLabel1.configure(justify=CENTER)
        self.TLabel1.configure(text='''00:00:00''')
        #self.TLabel1.configure(width=125)

        self.menubar = Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.game = Menu(top,tearoff=0)
        self.menubar.add_cascade(menu=self.game,
                activebackground="#d9d9d9",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkMenuFont",
                foreground="#000000",
                label="Game")
        self.game.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=SudokuController.startNewGame,
                font="TkMenuFont",
                foreground="#000000",
                label="New game")
        self.game.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=SudokuController.checkSolution,
                font="TkMenuFont",
                foreground="#000000",
                label="Check my solution")
        self.game.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=SudokuController.showSolution,
                font="TkMenuFont",
                foreground="#000000",
                label="Show correct solution")
        self.menubar.add_command(
            activebackground="#d8d8d8",
            activeforeground="#000000",
            background="#d9d9d9",
            command=SudokuController.showHOF,
            font="TkMenuFont",
            foreground="#000000",
            label="Best results")

        self.startBtn = ttk.Button(top)
        self.startBtn.place(relx=0.1, rely=0.91, relheight=0.07, relwidth=0.3)
        self.startBtn.configure(command=SudokuController.startNewGame)
        self.startBtn.configure(takefocus="")
        self.startBtn.configure(text='''Start new game''')

        self.TButton2 = ttk.Button(top)
        self.TButton2.place(relx=0.56, rely=0.91, relheight=0.07, relwidth=0.3)
        self.TButton2.configure(command=SudokuController.checkSolution)
        self.TButton2.configure(takefocus="")
        self.TButton2.configure(text='''Check my solution''')

    '''Returns list of cell objects'''
    def getCells(self):
        return self.cells

    '''Returns current difficulty level'''
    def getDifficultyLevel(self):
        return self.level.get()


if __name__ == '__main__':
    vp_start_gui()



