from tkinter import *
import tkinter.ttk as ttk
import SudokuController


w = None


def create_New_record(root, prompt, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel(root)
    top = New_record(w, prompt)
    return (w, top)


def destroy_New_record():
    global w
    w.destroy()
    w = None

'''Defines new record window UI.'''
class New_record:
    def __init__(self, top, prompt):
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85'
        font13 = "-family {Segoe UI} -size 13 -weight normal -slant " \
                 "roman -underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("600x450+415+150")
        top.title("New record")
        top.configure(background="#d9d9d9")

        self.TLabel1 = ttk.Label(top)
        self.TLabel1.place(relx=0.13, rely=0.18, height=150, width=435)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(font=font13)
        self.TLabel1.configure(relief=FLAT)
        self.TLabel1.configure(anchor=CENTER)
        self.TLabel1.configure(justify=LEFT)
        self.TLabel1.configure(text=prompt)
        self.TLabel1.configure(width=435)

        self.TEntry1 = ttk.Entry(top)
        self.TEntry1.place(relx=0.15, rely=0.62, relheight=0.08, relwidth=0.73)
        self.TEntry1.configure(width=436)
        self.TEntry1.configure(takefocus="")
        self.TEntry1.configure(cursor="ibeam")

        self.newRecordWinBtn = ttk.Button(top)
        self.newRecordWinBtn.place(relx=0.35, rely=0.82, height=40, width=178)
        self.newRecordWinBtn.configure(command=self.processNewRec)
        self.newRecordWinBtn.configure(takefocus="")
        self.newRecordWinBtn.configure(text='''Ok''')
        self.newRecordWinBtn.configure(width=178)


    '''Sends winner's name to SudokuController.processNewRecord() 
    and disables the window.'''
    def processNewRec(self):
        SudokuController.processNewRecord(self.TEntry1.get())
        destroy_New_record()
