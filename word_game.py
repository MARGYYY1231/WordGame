import tkinter as tk
from tkinter import messagebox
from tkinter import font
from wonderwords import RandomWord
import time
from spellchecker import SpellChecker

class MyGUI:
    def __init__(self):
        """Starts up the tkinter GUI window"""
        self.root = tk.Tk()
        self.root.geometry("360x640")
        self.root.resizable(0, 0)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0,weight=1)
        self.r = RandomWord()
        self.makeFrames(self.root)
        
        self.root.protocol("WM_DELETE_WINDOW",self.on_closing)
        
        self.root.mainloop()

    def makeFrames(self, root):
        """Creates the pages needed which are
        the four letter, five letter and homepage"""
        self.frame1 = tk.Frame(root)
        self.frame2 = tk.Frame(root, bg='#134565')
        self.frame3 = tk.Frame(root, bg='#134565')

        for frame in (self.frame1,self.frame2,self.frame3):
            frame.grid(row=0,column=0,sticky='nsew')
 
        self.start_page(self.frame1)
        self.four_letter(self.frame2)
        self.five_letter(self.frame3)
        self.show_frame(self.frame1)

    def show_frame(self, frame):
        """This shows the frame called"""
        frame.tkraise()

    def start_page(self, frame):
        """This is the start page"""
        self.bg = tk.PhotoImage(file="background2.png")
        self.four = tk.PhotoImage(file="4_letter.png")
        self.five = tk.PhotoImage(file="5_letter.png")
        self.frame1_title = tk.Label(frame, image=self.bg)
        self.frame1_title.place(x=0, y=0)
        self.help(frame)
        myFont = font.Font(family='Helvetica', size=12, weight='bold')
        frame1_btn = tk.Button(frame, image=self.four, command=lambda:self.show_frame(self.frame2), height=45, width=90, borderwidth=0)
        frame1_btn.place(x=140, y=380)
        frame1_btn2 = tk.Button(frame, image=self.five, command=lambda:self.show_frame(self.frame3), height=45, width=90, borderwidth=0)
        frame1_btn2.place(x=140, y=450)

    def makeGrid4(self):
        """Create the grid for the four letter"""
        self.GridFrame = tk.Frame(self.frame2, bg="white")        

        for x in range(4):
            self.GridFrame.columnconfigure(x, weight=1)
            
        for r in range(5):
            for c in range(4):
                self.write(self.GridFrame, "", '#134565', c, r, 8, 4)

        self.write(self.GridFrame, self.first_letter, '#134565', 0, 0, 8, 4)

        self.GridFrame.pack(pady=10)

    def makeGrid5(self):
        """Create the grid for the five letter"""
        self.GridFrame2 = tk.Frame(self.frame3, bg="white")        

        for x in range(5):
            self.GridFrame2.columnconfigure(x, weight=1)
            
        for r in range(5):
            for c in range(5):
                self.write(self.GridFrame2, "", '#134565', c, r,6, 3)

        self.write(self.GridFrame2, self.first_letter2, '#134565', 0, 0, 6, 3)

        self.GridFrame2.pack(pady=5)

    def updateboard4(self, e):
        """Updates the grid for the four letter"""
        emptyDict = {}
        for c in self.word:
            emptyDict.update({c: 0})
        for i in range(4):
            self.color4 = '#134565'
            self.get_color(e, self.word, i, emptyDict)
            self.write(self.GridFrame, e[i], self.color4, i, self.row_four, 8, 4)
        self.row_four += 1
        self.win(self.GridFrame, e, self.word, 4, self.row_four, 8, 4, self.list4)
        if self.row_four < 5:
            for x in range(4):
                self.write(self.GridFrame, self.list4[x], '#134565', x, self.row_four, 8, 4)

    def updateboard5(self, e):
        """updates te grid for the five letter"""
        emptyDict = {}
        for c in self.word2:
            emptyDict.update({c: 0})
        for i in range(5):
            self.color5 = '#134565'
            self.get_color(e, self.word2, i, emptyDict)
            self.write(self.GridFrame2, e[i], self.color5, i, self.row_five, 6, 3)
        self.row_five += 1
        self.win(self.GridFrame2, e, self.word2, 5, self.row_five, 6, 3, self.list5)
        if self.row_five < 5:
            for x in range(5):
                self.write(self.GridFrame2, self.list5[x], '#134565', x, self.row_five, 6, 3)

    def set_color(self, ans, color):
        """Sets the color of the letter"""
        if len(ans) == 4:
            self.color4 = color
        else:
            self.color5 = color

    def set_list(self, e, ans, i):
        if len(ans) == 4:
            self.list4[i] = e[i]
        else:
            self.list5[i] = e[i]

    def get_color(self, e, ans, i, emptyDict):
        """should set the color of the letter based on the answer
            if in correct place turns green, if it contains the letter in the answer
            then it sets it to yellow otherwise it is kept blue"""
        if e[i] == ans[i]:
            self.set_list(e, ans, i)
            self.set_color(ans, '#3cb03c')
            emptyDict[e[i]] += 1
        elif e[i] in ans:
            if ans.count(e[i]) >= e.count(e[i]):
                    emptyDict[e[i]] += 1
                    self.set_color(ans, '#fcba03')
            else:
                indexes = [index for index in range(len(e))
                               if e[index] == e[i]]
                rpos = False
                for x in indexes:
                    if e[x] == ans[x]:
                        rpos = True
                if emptyDict[e[i]] < ans.count(e[i]) and not rpos:
                    self.set_color(ans, '#fcba03')
                    emptyDict[e[i]] += 1
                else:
                    self.set_color(ans, '#134565')
        else:
            self.set_color(ans, '#134565')

    def win(self, frame, e, ans, word_len, row_num, w, h, l):
        """Checks if the player has won"""
        if(ans == e or l.count("") == 0):
            self.askyesno("Congratulations!! You Win :) Do you want to restart?", 4)
        elif row_num >= 5:
            self.extraline(frame, ans, word_len, row_num, w, h)

    def write(self, frame, t, c, col, r, w, h):
        """writes to the board"""
        square = tk.Label(frame, text=t, font=('Arial',12), fg="white", bg=c, width=w, height=h)
        square.grid(row=r, column=col, padx=2, pady=2)

    def play4(self, event):
        """Gets the entry and compares it to the answer"""
        if self.row_four < 5:
            e = self.myentry1.get().upper();
            print(len(e))
            self.correct_length(e, self.word, 4, self.first_letter, self.GridFrame, self.row_four, 8, 4)
            
        self.myentry1.delete(0, tk.END)

    def play5(self, event):
        """Gets the entry and compares it to the answer"""
        if self.row_five < 5:
            e = self.myentry2.get().upper();
            print(len(e))
            self.correct_length(e, self.word2, 5, self.first_letter2, self.GridFrame2, self.row_five, 6, 3)
            
        self.myentry2.delete(0, tk.END)

    def correct_length(self, e, ans, length, first_letter, frame, row_num, w, h):
        """Checks if the entry is the correct length and determines the next action
        if correct length then would update board otherwise will reveal answer"""
        spell = SpellChecker()
        if len(e) == length and e[0]==first_letter and spell.correction(e) == e:
            print(ans)
            print(e)
            if len(ans) == 4:
                self.updateboard4(e)
            else:
                print("5 letter")
                self.updateboard5(e)
        elif len(e) > length:
            print("Too long")
            #clear board
            self.incorrect(frame, e, ans, length, length, w, h, row_num)
        else:
            print("Too short")
            #clear board
            self.incorrect(frame, e, ans, len(e), length, w, h, row_num)

    def incorrect(self, frame, e, ans, r, word_len, w, h, row_num):
        """If run out of attempts or entry too long or too short then revels answer"""
        for x in range(r):
            self.write(frame, e[x], '#fc0352', x, row_num, w, h)
        self.extraline(frame, ans, word_len, row_num, w, h)

    def extraline(self, frame, ans, length, row_num, w, h):
        """Creates extraline to sjow the anser if incorrect"""
        for x in range(length):
            self.write(frame, ans[x], '#134565', x, row_num+1, w, h)
        self.askyesno("Do you want to restart?", 4 if (len(ans) == 4) else 5)

    def askyesno(self, msg, length):
        """asks the user if they would like to restart if they win or lose"""
        if messagebox.askyesno(title="Restart?", message=msg):
            self.reset(length)
        else:
            self.reset(length)
            self.show_frame(self.frame1)

    def reset(self, length):
        """clears evereything on the page and resets to make a new word to guess"""
        if length == 4:
            self.destroy(self.frame2)
            self.four_letter(self.frame2)
        else:
            self.destroy(self.frame3)
            self.five_letter(self.frame3)

    def destroy(self, frame):
        """clears everything on the page"""
        for widget in frame.winfo_children():
            widget.destroy()

    def help(self, frame):
        msg = "How to play: \nYou have five attempts to guess the five letter word by entering in the entry box.\nIf a letter turns green it is in the correct place.\nIf it is yellow then it is a correct letter but in the wrong place."
        self.qmark = tk.PhotoImage(file="question-mark.png")
        btn = tk.Button(frame, bg='#134565', activebackground='#134565', image=self.qmark, command=lambda:self.write_info("Help", msg), height=45, width=90, borderwidth=0)
        btn.place(x=280, y=5)

    def write_info(self, topic, msg):
        messagebox.showinfo(topic, msg)

    def four_letter(self, frame):
        """This is for the five letters page"""
        self.list4 = ["","","",""]
        self.row_four = 0
        self.word = self.r.word(include_parts_of_speech=["nouns", "adjectives"], word_min_length=4, word_max_length=4).upper()
        self.first_letter = self.word[0]
        self.list4[0] = self.first_letter
        
        self.frame2_title = tk.Label(frame, text='Enter Word:', fg='white',bg='#134565')
        self.frame2_title.pack(pady=5)
        self.myentry1 = tk.Entry(self.frame2)
        self.myentry1.bind("<Return>", self.play4)
        self.myentry1.pack();
        self.makeGrid4()
        
        frame2_btn1 = tk.Button(frame, text="<- Back",command=lambda:self.show_frame(self.frame1))
        frame2_btn1.pack()

    def five_letter(self, frame):
        """This is for the five letters page"""
        #have a list of letters that have already been found
        self.list5 = ["","","","",""]
        self.row_five = 0
        self.word2 = self.r.word(include_parts_of_speech=["nouns", "adjectives"], word_min_length=5, word_max_length=5).upper()
        #get first letter of word
        self.first_letter2 = self.word2[0]
        self.list5[0] = self.first_letter2
        
        self.frame3_title = tk.Label(self.frame3, text='Enter Word:', fg='white',bg='#134565')
        self.frame3_title.pack(pady=5)
        self.myentry2 = tk.Entry(self.frame3)
        self.myentry2.bind("<Return>", self.play5)
        self.myentry2.pack();
        self.makeGrid5()
        
        frame2_btn1 = tk.Button(frame, text="<- Back",command=lambda:self.show_frame(self.frame1))
        frame2_btn1.pack()
        
    def on_closing(self):
        """Asks the user if they want to exit if they press the x on the window"""
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
            self.root.destroy()
MyGUI()
