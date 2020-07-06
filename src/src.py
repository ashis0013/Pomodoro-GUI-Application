import tkinter as tk
import math
import subprocess

info = open('../data/info.txt','r')
info_map = {}
line = info.readline()
while line:
    info_map[line.split('=')[0]] = int(line.split('=')[1])
    line = info.readline()

focus_time = info_map['FOCUS_TIME']
short_rest = info_map['SHORT_REST']
long_rest = info_map['LONG_REST']
cycle_lenght = info_map['CYCLE_LENGTH']

class Pomodoro(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('400x300+0+0')
        self.timer = 0
        self.running = False
        self.focus = True
        self.rounds = 0
        self.clock = tk.Label(self, text=self.pretty_time(self.timer))
        self.clock.pack()
        self.clock.place(relx=0.5,rely=0.4,anchor=tk.CENTER)
        self.clock.config(font=('DS-Digital',28))

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.filemenu = tk.Menu(self.menu)
        self.menu.add_cascade(label='Option', menu=self.filemenu) 
        self.filemenu.add_command(label='Reset',command=(lambda: self.reset()))
        self.filemenu.add_command(label='Stop',command=(lambda: self.stop()))

        self.b = tk.Button(self,text='START',command=(lambda: self.start()))
        self.b.pack()
        self.b.place(relx=0.5,rely=0.9,anchor=tk.CENTER)

    def tick_tock(self):
        if self.timer == 0:
            if self.focus:
                msg = 'You have focused for ' + str(focus_time/60) + ' minutes'
                subprocess.Popen(['notify-send',msg])
            if not self.focus:
                self.rounds = (self.rounds + 1)%cycle_lenght
                subprocess.Popen(['notify-send','Your break is over time for focus'])
            self.focus = not self.focus
            self.running = False
        if self.running:
            self.timer -= 1
            self.clock.configure(text=self.pretty_time(self.timer))
            self.after(1000,self.tick_tock)

    def start(self):
        if self.running: return
        self.running = True
        if self.timer == 0:
            if self.focus:
                self.timer = focus_time
            elif self.rounds+1 == cycle_lenght:
                self.timer = long_rest
            else: self.timer = short_rest
        self.tick_tock()
    
    def stop(self):
        self.running = False

    def reset(self):
        self.timer = 25*60
        self.clock.configure(text=self.pretty_time(self.timer))
    
    def pretty_time(self,sec):
        tym = ''
        if sec > 3600:
            hh = int(math.floor(sec/3600))
            sec = sec%3600
            if(hh < 10): tym += '0'
            tym += str(hh) + ':'
        
        mm = int(math.floor(sec/60))
        ss = sec%60
        if(mm < 10): tym += '0'
        tym += str(mm) + ':'
        if(ss < 10): tym += '0'
        tym += str(ss)
        return tym


window = Pomodoro()

window.mainloop()
