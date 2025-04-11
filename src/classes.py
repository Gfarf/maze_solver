from tkinter import Tk, BOTH, Canvas
import time

class Window():
    def __init__(self, height, width, title):
        self.__height = height
        self.__width = width
        self.__root = Tk()
        self.__root.title(title)
        self.__canvas = Canvas(self.__root, bg="white", height=self.__height, width=self.__width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed")

    def close(self):
        self.__running = False

    def draw_line(self, line, color):
        line.draw(self.__canvas, color)

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, p_one, p_two):
        self.point_one = p_one
        self.point_two = p_two

    def draw(self, canvas, color):
        canvas.create_line(
            self.point_one.x, self.point_one.y, self.point_two.x, self.point_two.y, fill=color, width=2
        )


class Cell():
    def __init__(self, window, p_one = Point(0,0), p_two = Point(20,20),  border="black", fill="white"):
        self.has_wall = {"bellow": True, "above": True, "left": True, "right": True, "invalid": True}
        self.position = [
            min(p_one.x, p_two.x), 
            max(p_one.x, p_two.x),
            min(p_one.y, p_two.y),
            max(p_one.y, p_two.y)
        ]
        self._win = window
        self.border = border
        self.fill = fill

    def draw(self):
        if self._win is None:
            return
        if self.has_wall["bellow"] == True:
            linha = Line(Point(self.position[0], self.position[3]), Point(self.position[1], self.position[3]))
            self._win.draw_line(linha, self.border)
        if self.has_wall["above"] == True:
            linha = Line(Point(self.position[0], self.position[2]), Point(self.position[1], self.position[2]))
            self._win.draw_line(linha, self.border)
        if self.has_wall["left"] == True:
            linha = Line(Point(self.position[0], self.position[2]), Point(self.position[0], self.position[3]))
            self._win.draw_line(linha, self.border)
        if self.has_wall["right"] == True:
            linha = Line(Point(self.position[1], self.position[2]), Point(self.position[1], self.position[3]))
            self._win.draw_line(linha, self.border)

    def draw_move(self, to_cell, undo=False):
        if self._win is None:
            return
        color = "red"
        if undo:
            color = "gray"
        relation = self.check_touching_side(to_cell)
        if self.has_wall[relation]:
            return "invalid move"
        self._win.draw_line(
             Line(
                 Point(
                    (self.position[0]+self.position[1]) / 2,
                    (self.position[2]+self.position[3]) / 2
                ),
                Point(
                    (to_cell.position[0]+to_cell.position[1]) / 2,
                    (to_cell.position[2]+to_cell.position[3]) / 2
                )),
                color
            )
       

    def check_touching_side(self, to_cell):
        if to_cell.position[0] == self.position[0]:
            if to_cell.position[2] == self.position[3]:
                return "bellow"
            if to_cell.position[3] == self.position[2]:
                return "above"
        if to_cell.position[2] == self.position[2]:
            if to_cell.position[0] == self.position[1]:
                return "right"
            if to_cell.position[1] == self.position[0]:
                return "left"
        return "invalid"


class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win,
    ):
        self.x1 = x1
        self.y1 = y1
        self.rows = num_rows
        self.cols = num_cols
        self.cellsize = [cell_size_x, cell_size_y]
        self._win = win
        self._create_cells()

    def _create_cells(self):
        self._cells = []
        start_y = self.y1
        for _ in range (self.cols):
            start = self.x1
            row = []
            for _ in range(self.rows):
                p_start = Point(start, start_y)
                p_end = Point(start + self.cellsize[0], start_y + self.cellsize[1])
                row.append(Cell(self._win, p_start, p_end))
                start += self.cellsize[0]
            self._cells.append(row)
            start_y += self.cellsize[1]
        for i in range (self.cols):
            for j in range(self.rows):
                self._draw_cells(i, j)
    
    def _draw_cells(self, i, j):
        self._cells[i][j].draw()
        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)
