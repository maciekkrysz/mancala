import PySimpleGUI as sg
import tkinter as tk
from tkinter.font import Font

COLOR = '#AF6125'
MOVE_COLOR = '#e69a60'

class Circle():
    def __init__(self, x0, y0, x1, y1, r_rocks, n, canvas):
        self.canvas = canvas
        self.oval = canvas.TKCanvas.create_oval(x0, y0, x1, y1, fill=COLOR)
        self.rocks = []    # rows of rocks
        self.set_marbles(r_rocks, canvas)
        self.number = canvas.TKCanvas.create_text((x0 + x1)/2, (y0 + y1)/2, text='11', font=Font(weight='bold'), fill='#CCCCCC')
        self.show_number(n)

    def set_marbles(self, r_rocks, canvas):
        x0, y0, x1, y1 = canvas.TKCanvas.coords(self.oval)
        rx = (x1 - x0)# * 1.03
        ry = (y1 - y0) * 1.03
        # print(rx, ry)
        n = 5
        # canvas.TKCanvas.create_oval(x0 + rx/2 - n, y0 + rx/2 - n, x0 + rx/2 + n, y0 + rx/2 + n, fill="black")

        yc0 = y0
        spacex = rx/4
        spacey = ry/4

        for y in range(3):
            self.rocks.append(Rocks(x0 + rx/5, yc0 + ry/5, r_rocks, spacex, canvas=canvas))
            self.rocks[y].show(y+1)
            yc0 += spacey
    
    def show_number(self, number):
        for rock in self.rocks:
            rock.show(0)
            self.canvas.TKCanvas.itemconfig(self.number, state=tk.HIDDEN)

        if number == 0:
            return
        elif number < 10:
            if number == 1:
                self.rocks[1].show(1)
            elif number == 2:
                self.rocks[1].show(2)
            elif number == 3:
                self.rocks[1].show(3)
            elif number == 4:
                self.rocks[0].show(2)
                self.rocks[1].show(2)
            elif number == 5:
                self.rocks[0].show(2)
                self.rocks[1].show(1)
                self.rocks[2].show(2)
            elif number == 6:
                self.rocks[0].show(2)
                self.rocks[1].show(2)
                self.rocks[2].show(2)
            elif number == 7:
                self.rocks[0].show(2)
                self.rocks[1].show(3)
                self.rocks[2].show(2)
            elif number == 8:
                self.rocks[0].show(3)
                self.rocks[1].show(3)
                self.rocks[2].show(2)
            elif number == 9:
                self.rocks[0].show(3)
                self.rocks[1].show(3)
                self.rocks[2].show(3)
        else:
            self.rocks[0].show(3)
            if number > 99:
                self.rocks[1].show(0)
            else:
                self.rocks[1].show(10)
            self.rocks[2].show(3)
            self.canvas.TKCanvas.itemconfig(self.number, text=str(number), state=tk.NORMAL)

    def update_color(self, move):
        if move:
            self.canvas.TKCanvas.itemconfig(self.oval, fill=MOVE_COLOR)
        else:
            self.canvas.TKCanvas.itemconfig(self.oval, fill=COLOR)






class Rocks:
    def __init__(self, startx, starty, r, space, canvas, n=3):
        self.tripples = []
        self.doubles = []
        self.canvas = canvas

        for i in range(3):
            oval = canvas.TKCanvas.create_oval(startx, starty, startx + r, starty + r, fill="#222222", state=tk.HIDDEN)
            self.tripples.append(oval)
            startx += space

        startx -= space * 100/67
        for i in range(2):
            oval = canvas.TKCanvas.create_oval(startx, starty, startx + r, starty + r, fill="#222222", state=tk.HIDDEN)
            self.doubles.append(oval)
            startx -= space

    def show(self, n):
        if n==0:
            for r in self.tripples:
                hide_rock(r, self.canvas)
            for r in self.doubles:
                hide_rock(r, self.canvas)
        else:
            self.show(0)
            if n==1:
                show_rock(self.tripples[1], self.canvas)
            elif n==2:
                for r in self.doubles:
                    show_rock(r, self.canvas)
            elif n==3:
                for r in self.tripples:
                    show_rock(r, self.canvas)
            elif n==10:
                show_rock(self.tripples[2], self.canvas)
                show_rock(self.tripples[0], self.canvas)


def hide_rock(n, canvas):
    canvas.TKCanvas.itemconfig(n, state=tk.HIDDEN)

def show_rock(n, canvas):
    canvas.TKCanvas.itemconfig(n, state=tk.NORMAL)
