import random
import turtle
import time
def setup():
    size = 50
    screen = turtle.Screen()

    n = screen.textinput("Size","Board Size (e.g. 12x10): ")
    n = "12x10" if n == None else n
    size_x, size_y = list(int(i) for i in n.split("x"))
    bombs_left = size_x*size_y//6
    
    screen.setup(width=(size_x+0.8)*size, height=(size_y+1.8)*size)
    screen.title("Minesweeper")
    t = turtle.Turtle()
    return t, screen, size, size_x, size_y, bombs_left

t, screen, size, size_x, size_y, bombs_left = setup()
del setup

t.right(90)
screen.colormode(255)
t.hideturtle()

#generates number board and state board
def gen_board(width:int, height:int, amount:int) -> tuple[list[list[int]], list[list[str]], tuple[int, int]]:

    board_num = [[0]*width for _ in range(height)]
    board_state = [["closed"]*width for _ in range(height)] #closed, flagged, open

    available = []
    for y in range(height):
        for x in range(width):
            available.append((x, y))
            
    for _ in range(amount):
        selected = random.choice(available)
        board_num[selected[1]][selected[0]] = -1
        available.remove(selected)
        
        for j in range(-1, 2):
            for i in range(-1, 2):
                xx, yy = selected[0]+i, selected[1]+j
                if xx!=-1 and yy!=-1 and xx<size_x and yy<size_y:       
                    if board_num[yy][xx]!=-1:
                        board_num[yy][xx]+=1
    zero_cells = []
    for cell in available:
        if board_num[cell[1]][cell[0]] == 0:
            zero_cells.append(cell)
    starting_cell = random.choice(zero_cells)
    # board_state[starting_cell[1]][starting_cell[0]] = "open"
    # 
    return board_num, board_state, starting_cell


board_num, board_state, starting_cell = gen_board(size_x, size_y, bombs_left)


def win_detection(board_num=board_num, board_state=board_state) -> bool:
    for y in range(size_y):
        for x in range(size_x):
            if board_num[y][x]!=-1 and board_state[y][x] != "open":
                return False
    return True

mouse_pos = [0, 0]
def l_click(x, y) -> None:
    click_action(x, y, "l")
def r_click(x, y) -> None:
    click_action(x, y, "r")
    
    
def click_action(x:float, y:float, btn, cell=None) -> None:
    global mouse_pos
    global board_state
    global bombs_left
    mouse_pos = [x, y]
    if cell==None:
        cell = [int(x/size+size_x/2), int(size_y-((y-size/2)/size+size_y/2)-1)]

    match board_state[cell[1]][cell[0]]:
        case "closed":
            if btn == "r":
                board_state[cell[1]][cell[0]] = "flagged"
                bombs_left -= 1
            else:
                board_state[cell[1]][cell[0]] = "open"
                if board_num[cell[1]][cell[0]] == 0:
                    for j in range(-1, 2):
                        for i in range(-1, 2):
                            xx, yy = cell[0]+i, cell[1]+j
                            if xx!=-1 and yy!=-1 and xx<size_x and yy<size_y:
                                click_action(0, 0, "l", [xx, yy])
        case "flagged":
            if btn == "r":
                board_state[cell[1]][cell[0]] = "closed"
                bombs_left += 1

    draw_board_on_screen(bombs_left=bombs_left)
    if board_num[cell[1]][cell[0]] == -1 and btn == "l" and board_state[cell[1]][cell[0]]=="open":
        exit()
    if bombs_left == 0:
        if win_detection():
            print("YOU WON")
            screen.reset()
            t.write("You won!", align="center", font=("Courier New", (int(size/3)), "bold"))
            turtle.exitonclick()

COLORS = {
    "text":"#000000",
    "borders":"#000000",
    "F":"#FF0000", #flag
    "O":"#000000", #bomb
    "0":"#AEAEAE",
    "1":"#3032C4",
    "2":"#0A8110",
    "3":"#A11010",
    "4":"#180756",
    "5":"#611B1B",
    "6":"#207386",
    "7":"#151515",
    "8":"#494848"
}

def draw_board_on_screen(board_num=board_num, board_state=board_state, size_x=size_x, size_y=size_y, cell_size=size, bombs_left=bombs_left) -> None:
    t.clear()
    screen.tracer(False)
    for y in range(size_y):
        for x in range(size_x):
            t.penup()
            t.goto((x-(size_x/2))*cell_size, ((size_y-1)/2-y)*cell_size) #goto top left cell's corner
            t.color(COLORS["borders"])
            t.pendown() #draw borders
            for _ in range(4):
                t.forward(cell_size)
                t.left(90)
            t.penup()
            t.forward(cell_size)
            t.left(90) #go to bottom middle to write
            t.forward(cell_size/2) 
        
            match board_state[y][x]:
                case "open":
                    num = board_num[y][x]
                    num = "O" if num == -1 else num
                    t.color(COLORS[str(num)])
                    t.write(str(num), align="center", font=("Courier New", (int(cell_size/1.5)), "bold")) # write number for open cell
                case "closed":
                    ...
                case "flagged":
                    t.color(COLORS["F"])
                    t.write("X", align="center", font=("Courier New", (int(cell_size/1.5)), "bold")) # draw X as flag
            t.backward(cell_size)
            t.right(90)
            t.back(cell_size/2) #come back to top left corner
    t.color(COLORS["text"])
    t.goto(0, cell_size*size_y/2)
    t.write(f"Bombs left: {bombs_left}", align="center", font=("Courier New", (int(cell_size/3)), "bold"))

    screen.update()

draw_board_on_screen() #initial rendering
click_action(0, 0, "l", starting_cell)


turtle.onscreenclick(l_click, 1)
turtle.onscreenclick(r_click, 3)

turtle.listen()
turtle.mainloop() #just has to be at the end