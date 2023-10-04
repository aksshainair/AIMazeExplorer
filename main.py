import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import ml
import re

GRID_SIZE = 11
CELL_SIZE = 60
INP_PATTERN  = r'^\d+,\d+$'
GRID = ml.get_grid()
path = []
invalid_start_flag = False

def get_final_coordinates():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if GRID[row][col] == 2:
                return(row,col)
    return (0,0)

final_coordinates = get_final_coordinates()

def get_colors(row, col):
    color, line = " ", " "
    if (GRID[row][col]) == 0:   #path
        color = "white"
        line = "black"
    elif (GRID[row][col]) == 2: #goal
        color = "green"  
        line = "white"
    elif (GRID[row][col]) == 3: #current walking path
        color = "red"
        line = "white"
    else:                       #wall
        color = "black"
        line = "white"

    return line, color

# def on_cell_click(pos):
#     row = pos[1] // CELL_SIZE
#     col = pos[0] // CELL_SIZE
#     print(f"Cell clicked at row {row+1}, column {col+1}")


def input_validator(text):
    try:
        value = int(text)
        if 1 <= value <= GRID_SIZE:
            return True
        else:
            print("Only In Range 1 to 11 Inclusive")
            return False
    except (ValueError or TypeError):
        print("Only Integers")
        return False
    
def reset_grid():
    global path, GRID
    path = []
    GRID = [[0 if cell == 3 else cell for cell in row] for row in GRID]
    final_row, final_col = final_coordinates
    GRID[final_row][final_col] = 2

def input_handler(start_coordinates):
    reset_grid()    
    global path, invalid_start_flag, INP_PATTERN
    
    if re.match(INP_PATTERN, start_coordinates):
        pass
    else:
        print("ERROR : Invalid input format")
        return
    
    start_row, start_col = start_coordinates.split(",")

    if input_validator(start_row) and input_validator(start_col):
        start_row = int(start_row)
        start_col = int(start_col)
        if GRID[start_row-1][start_col-1]!=1:
            invalid_start_flag = False
            path_or_not  = ml.get_path(start_row-1, start_col-1)
            if path_or_not=="BOUNDED":
                invalid_start_flag = True
            else:
                path = path_or_not
                del path[-1]
        else:
            invalid_start_flag = True
    else:
        print("Invalid input. Please enter numbers between 1 and 11.")


def update_grid():

    if not path:
        return
    else:
        row, col = path[0]
        GRID[row][col] = 3  # Set cell color to red
        del path[0]

def draw_handler(canvas):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x0 = col * CELL_SIZE
            y0 = row * CELL_SIZE
            x1 = x0 + CELL_SIZE
            y1 = y0 + CELL_SIZE

            line, color = get_colors(row, col)

            if color=="black":
                canvas.draw_image(wall, (wall_w/2, wall_h/2), (wall_w, wall_h), (x0+20, y0+20), (60, 60))
            else:
                canvas.draw_polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], 1, line, color)
                canvas.draw_text(f"{(row+1)} {(col+1)}", (x0+20,y0+30), 15, "black")

ml.train()

timer_interval = 200
timer = simplegui.create_timer(timer_interval, update_grid)

frame = simplegui.create_frame("Maze Runner", GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
frame.add_input("Starting (a,b) : ", input_handler, 100)
wall = simplegui.load_image('https://raw.githubusercontent.com/aksshainair/AIMazeExplorer/main/wall.jpeg')
# wall = simplegui._load_local_image('/Users/aksshainair/Desktop/aksshaipy/SEM4IndividualProject/AIMazeRunner/wall.jpeg')
# goal = simplegui.load_image('/Users/aksshainair/Desktop/aksshaipy/SEM4IndividualProject/goal.png')
wall_w, wall_h = wall.get_width(), wall.get_height()
# goal_w, goal_h = goal.get_width(), goal.get_height()
frame.set_draw_handler(draw_handler)

# frame.set_mouseclick_handler(on_cell_click)

timer.start()
frame.start()
