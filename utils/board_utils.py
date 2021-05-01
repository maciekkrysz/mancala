import PySimpleGUI as sg
from classes.circle import Circle

def create_arrow(canvas, startx, starty, size, color):
    points = [
        startx, starty,
        startx + size, starty + size/2,
        startx, starty + size
    ]
    return canvas.TKCanvas.create_polygon(points, fill=color, width=1, outline='black', state='hidden')

def update_cups(cups, values):
    for i, cup in enumerate(cups):
        cup.show_number(values[i])
