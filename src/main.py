from classes import *


def main():
    win = Window(800, 600, "Maze Solver")
    m = Maze(10,10,20,20,25,25,win)

    win.wait_for_close()
    

if __name__ == "__main__":
    main()