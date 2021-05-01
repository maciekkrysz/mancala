import PySimpleGUI as sg
from consts import *
from utils.board_utils import *
from utils.utilities import *
from classes.circle import Circle
from classes.side import Side
from AI.ai import *
import random
import time

layout = [
    [sg.Canvas(size=(sizex, sizey), background_color='#287840', key='canvas')],
    [sg.Text('Player:    ', key='-PLAYER-')],
    [sg.Button(n-1-i) for i in range(n)]
]


# #7C2F2F
window = sg.Window('Canvas test', layout, finalize=True)

canvas = window['canvas']
tablex = sizex * 0.9
tabley = sizey * 0.8
table_cornerx = sizex * 0.1
table_cornery = sizey * 0.2

print(tablex, tabley)
print(table_cornerx, table_cornery)

table = canvas.TKCanvas.create_rectangle(
    tablex, tabley, table_cornerx, table_cornery, fill='#854A1B')


# CREATING ARROWS


cups = []
p1_cups = []
p2_cups = []

# CREATING CUPS
c_startx = table_cornerx + sizex * 0.15
c_starty = table_cornery + sizey * 0.1
c_size = sizex * 0.07 * 6/n

r_rocks = c_size/9

arrows = []

for i in range(2):
    arrows.append(create_arrow(canvas, 20, c_starty, c_size, '#CC5801'))
    for j in range(n):
        c = Circle(c_startx, c_starty, c_startx + c_size,
                   c_starty + c_size, r_rocks, k, canvas)
        c_startx += sizex * 0.0875 * 6 / n
        cups.append(c)

    c_startx = c_startx - (sizex * 0.0875 * 6)
    c_starty = sizey - c_starty - c_size


home_cirx = sizex * 0.13
home_ciry = tabley * 0.2
home_bound = sizex * 0.02

# CREATING HOME CUP

x0 = table_cornerx+home_bound
y0 = table_cornery+home_ciry
x1 = table_cornerx+home_cirx
y1 = tabley-home_ciry
cir1 = Circle(x0, y0, x1, y1, r_rocks, 0, canvas)

x0 = tablex-home_bound
y0 = table_cornery+home_ciry
x1 = tablex-home_cirx
y1 = tabley-home_ciry
cir2 = Circle(x0, y0, x1, y1, r_rocks, 0, canvas)

# CREATING PLAYERS CUPS LIST

p1_cups.append(cir1)
p2_cups.append(cir2)

for cup in cups[0:int(len(cups)/2)]:
    p1_cups.append(cup)

for cup in cups[-1:int(len(cups)/2)-1:-1]:
    p2_cups.append(cup)

# print(p1_cups) # for n=6 [2, 4, 5, 6, 7, 8, 9]
# print(p2_cups) # for n=6 [3, 15, 14, 13, 12, 11, 10]

# CREATE PLAYERS
p1 = Side(is_AI=True)
p2 = Side(is_AI=False)
players = [p1, p2]
cups = [p1_cups, p2_cups]
current_player = random.randint(0, 1)  # p1 = players[0], p2 = players[-1]
current_player = 1

# MAIN LOOP
prev_move = p1_cups[0]

canvas.TKCanvas.itemconfig(arrows[current_player], state='normal')
while True:
    print(f'Player: p{current_player + 1}')
    window['-PLAYER-'].Update(f'Player: p{current_player + 1}')

    # waiting for move
    print(AI.movgen(players[current_player]))
    print('lacznie kamieni:', players[0].count() + players[1].count())
    
    minmax_result = AI.minmax(players[current_player], players[current_player-1])

    print(players[0].get_cups())
    print(players[1].get_cups()[::-1])
    

    print(minmax_result)

    if not players[current_player].AI:
        event, values = window.read()
    else:
        _, _ = window.read(timeout=500)

        event = minmax_result[1].split(' ')[0]

    print(event)
    if is_int(event):
        event = int(event)

    if event == sg.WIN_CLOSED:
        breaks
    elif event >= 0 and event < n:
        if players[current_player].cups[event] > 0:

            # move
            result = players[current_player].move(
                event, players[current_player - 1])
            print(result)

            # coloring current move
            prev_move.update_color(move=False)
            prev_move = cups[current_player][event+1]
            prev_move.update_color(move=True)

            # end game if any players's cups are clear
            if not p1.possible_move() or not p2.possible_move():
                p1_points = p1.count()
                p2_points = p2.count()

                print('KONIEC! STATUS GRY:')
                print(f'p1: {p1_points}')
                print(f'p2: {p2_points}')

                # popup with score and end program
                breaks

            # changing side
            if result != 'again':
                current_player = other_player(current_player)

            # changing side visualise
            canvas.TKCanvas.itemconfig(
                arrows[other_player(current_player)], state='hidden')
            canvas.TKCanvas.itemconfig(
                arrows[current_player], state='normal')
                
            # updating board
            update_cups(p1_cups, players[0].get_cups())
            update_cups(p2_cups, players[1].get_cups())

    elif event == 2:
        print(event)

    # update values

    # if game ends
