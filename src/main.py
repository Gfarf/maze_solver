from classes import Window
from maze import Maze


def main():
    win = Window(800, 600, "Maze Solver")
    m = Maze(10,10,20,20,25,25,win,0)
    m._break_walls_r(0,0)
    m.break_entrance_and_exit()

    win.wait_for_close()
    

if __name__ == "__main__":
    main()