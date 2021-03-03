from copy import deepcopy
from os import system, name
from time import sleep

# 0 = Road, 1 = Wall, "O" = Starting Point, "X" = Finish/End Point
map_basic = [\
    ["O",1,0,1,0,1,0,1,0,0],\
    [0,1,0,0,0,0,0,0,0,1],\
    [0,0,1,0,0,1,1,0,1,1],\
    [0,0,1,0,1,1,1,"X",1,1],\
    [0,0,0,0,1],\
    [0,1,0,1,0,1],\
    [0,1,0,0,0,1],\
    [0,0,1,0],\
    [0,0,1,0],\
    [0,0,0,0]]

map = deepcopy(map_basic)

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def start_and_finish():
    point = 0
    for irow, row in enumerate(map_basic):
        for icol, col in enumerate(row):
            if col == "O":
                start = (irow,icol)
                point += 1
            if col == "X":
                finish = (irow,icol)
                point += 1
            if point == 2:
                break
    if point < 2:
        return (0,0), (0,0)
    return start, finish

def reward(x,y):
    try:
        if map[x-1][y] == 0 and x>0:
            map[x-1][y] = map[x][y]+2
    except:
        pass
    try:
        if map[x+1][y] == 0:
            map[x+1][y] = map[x][y]+2
    except:
        pass
    try:
        if map[x][y-1] == 0 and y>0:
            map[x][y-1] = map[x][y]+2
    except:
        pass
    try:
        if map[x][y+1] == 0:
            map[x][y+1] = map[x][y]+2
    except:
        pass

def next_step(x,y,stat):
    if stat == 0:
        next = map[x][y]+2
    else:
        next = map[x][y]-2
    steps = []
    try:
        if map[x-1][y] == next and x>0:
            steps.append((x-1,y))
    except:
        pass
    try:
        if map[x+1][y] == next:
            steps.append((x+1,y))
    except:
        pass
    try:
        if map[x][y-1] == next and y>0:
            steps.append((x,y-1))
    except:
        pass
    try:
        if map[x][y+1] == next:
            steps.append((x,y+1))
    except:
        pass
    if stat == 0:
        return steps
    else:
        if len(steps) != 0:
            return [steps[0]]
        return steps

def explore_route(x,y,finish):
    map[x][y] = 2
    steps = [(x,y)]
    while True:
        next_steps = steps
        steps = []
        if len(next_steps) == 0 or list(finish) in next_steps:
            break
        for step in next_steps:
            reward(step[0],step[1])
            steps.extend(next_step(step[0],step[1],0))

def get_track(x,y):
    steps = [(x,y)]
    next_steps = []
    while True:
        if len(steps)>0:
            next_steps.extend(steps)
        else:
            break
        steps = []
        steps.extend(next_step(next_steps[-1][0],next_steps[-1][1],1))
    return next_steps

def print_map():
    clear()
    for i in map_basic:
        print(i)
    print()

def draw_route(track):
    for i in track[::-1]:
        map_basic[i[0]][i[1]]=9
        sleep(0.3)
        print_map()

if __name__ == "__main__":
    start, finish = start_and_finish()
    map[start[0]][start[1]] = 0
    map[finish[0]][finish[1]] = 0
    print_map()
    print("\nSTART ('O') and FINISH ('X') location")
    sleep(3)
    explore_route(start[0],start[1],finish)
    track = get_track(finish[0],finish[1])
    if len(track) == 1:
        print("There is no route to the location")
    else:
        draw_route(track)
        print("Here is the shortest route :")
        print(track)
