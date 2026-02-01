import random
import turtle

def setup():
    size_x, size_y = 20, 16
    size = 70
    bombs_left = 50
    screen = turtle.Screen()
    screen.setup(width=size_x*size, height=(size_y+1)*size)
    t = turtle.Turtle()
    return t, screen, size, size_x, size_y, bombs_left
t, screen, size, size_x, size_y, bombs_left = setup()
del setup

t.right(90)
screen.colormode(255)
t.hideturtle()

#generates number board and state board
def gen_board(width:int, height:int, amount:int, start:tuple[int, int]=(0, 0)) :

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
                        
    return board_num, board_state


board_num, board_state = gen_board(size_x, size_y, bombs_left)
del gen_board


def win_detection(board_num=board_num, board_state=board_state) -> bool:
    for y in range(size_y):
        for x in range(size_x):
            if board_num[y][x]!=-1 and board_state[y][x] != "open":
                return False
    return True

mouse_pos = [0, 0]
def l_click(x, y):
    click_action(x, y, "l")
def r_click(x, y):
    click_action(x, y, "r")
    
    
def click_action(x:float, y:float, btn, cell=None):
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
            turtle.exitonclick()

COLORS = {
    "text":"#000000",
    "borders":"#000000",
    "F":"#FF0000",
    "B":"#FF00E1",
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

def draw_board_on_screen(board_num=board_num, board_state=board_state, size_x=size_x, size_y=size_y, cell_size=size, bombs_left=bombs_left):
    t.clear()
    screen.tracer(False)
    for y in range(size_y):
        for x in range(size_x):
            t.penup()
            t.goto((x-(size_x/2))*cell_size, ((size_y-1)/2-y)*cell_size)
            t.pendown()
            t.color(COLORS["borders"])
            for _ in range(4):
                t.forward(cell_size)
                t.left(90)
            t.penup()
            t.forward(cell_size)
            t.left(90)
            t.forward(cell_size/2)
        
            match board_state[y][x]:
                case "open":
                    num = board_num[y][x]
                    num = "B" if num == -1 else num
                    t.color(COLORS[str(num)])
                    t.write(str(num), align="center", font=("Courier New", (int(cell_size/1.5)), "bold"))
                case "closed":
                    ...
                case "flagged":
                    t.color(COLORS["F"])
                    t.write("X", align="center", font=("Courier New", (int(cell_size/1.5)), "bold"))
            t.backward(cell_size)
            t.right(90)
            t.back(cell_size/2)
    t.color(COLORS["text"])
    t.goto(0, cell_size*size_y/2)
    t.write(f"Bombs left: {bombs_left}", align="center", font=("Courier New", (int(cell_size/3)), "bold"))

    screen.update()

draw_board_on_screen()

turtle.onscreenclick(l_click, 1)
turtle.onscreenclick(r_click, 3)

turtle.listen()
turtle.mainloop()
turtle.done()