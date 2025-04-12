from classes import *
import time
import random


class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
        seed = None
    ):
        self.x1 = x1
        self.y1 = y1
        self.rows = num_rows
        self.cols = num_cols
        self.cellsize = [cell_size_x, cell_size_y]
        self._win = win
        if seed is not None:
            self.seed = random.seed(seed)
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
    
    def _draw_cells(self, i, j, animate=True):
        if self._win is None:
            return
        self._cells[i][j].draw()
        if animate:
            self._animate(0.002)

    def _animate(self, tempo):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(tempo)

    def break_entrance_and_exit(self):
        self._cells[0][0].has_wall["above"] = False
        self._draw_cells(0,0,False)
        self._cells[-1][-1].has_wall["bellow"] = False
        self._draw_cells(-1,-1,False)
        self._reset_visited_cells()
        self._win.redraw()

    def _break_walls_r(self, i, j):
        if i == (len(self._cells)-1) and j == (len(self._cells[0])-1):
            return
        self._cells[i][j].visited = True
        b_cell = self._get_visit(i, j)
        to_break = random.randint(0,3)
        broken = True
        for _ in range(4):
            if b_cell[to_break]:
                to_break += 1
                if to_break == 4:
                    to_break = 0
            else:
                broken = False
                break
        if broken:
            return
        all_broken = True
        new_break = to_break
        while all_broken:
            b_cell = self._get_visit(i, j)        
            if b_cell[new_break]:
                new_break += 1
                if new_break == 4:
                    new_break = 0
                if new_break == to_break:
                    all_broken = False
                continue
            
            else:
                i2 = i
                j2 = j
                match new_break:
                    case 0:
                        dir = "above"
                        dir2 = "bellow"
                        i2 -= 1
                    case 1:
                        dir = "bellow"
                        dir2 = "above"
                        i2 += 1
                    case 2:
                        dir = "left"
                        dir2 = "right"
                        j2 -= 1
                    case 3: 
                        dir = "right"
                        dir2 = "left"
                        j2 += 1
                self._cells[i][j].has_wall[dir] = False
                self._cells[i2][j2].has_wall[dir2] = False
                self._draw_cells(i,j,False)
                self._draw_cells(i2,j2,False)
                self._break_walls_r(i2,j2)
                new_break += 1
                if new_break == 4:
                    new_break = 0
                if new_break == to_break:
                    all_broken = False
            

    def _get_visit(self, i, j):
        #mudar retorno para iteravel com 4 posições pegando a situação de cada vizinho
        visiteds = []
        if i - 1 < 0:
            visiteds.append(True)
        else:
            visiteds.append(self._cells[i-1][j].visited)
        if i + 1 >= len(self._cells):
            visiteds.append(True)
        else:
            visiteds.append(self._cells[i+1][j].visited)
        if j - 1 < 0:
            visiteds.append(True)
        else:
            visiteds.append(self._cells[i][j-1].visited)
        if j +1 >= len(self._cells[0]):
            visiteds.append(True)
        else:
            visiteds.append(self._cells[i][j+1].visited)
        return visiteds

    def _reset_visited_cells(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[0])):
                self._cells[i][j].visited = False
            
    def solve(self):
        return self._solver_r(0,0)

    def _solver_r(self, i, j):
        self._animate(0.1)
        self._cells[i][j].visited = True
        if i == self.rows - 1 and j == self.cols - 1:
            return True
        to_test = []
        for key, value in self._cells[i][j].has_wall.items():
            if not value:
                to_test.append(key)
        if i == j == 0:
            to_test.remove("above")
        if len(to_test) == 0:
            return False
        for side in to_test:
            a, b, c = self.cell_to_visit(i, j, side)
            if not c:
                self._cells[i][j].draw_move(self._cells[a][b])
                d = self._solver_r(a, b)
                if d:
                    return True
                self._cells[i][j].draw_move(self._cells[a][b], True)
                
        return False
        
    def cell_to_visit(self, i, j, side):
        match side:
            case "above":
                return i - 1, j, self._cells[i - 1][j].visited
            case "bellow":
                return i + 1, j, self._cells[i + 1][j].visited
            case "left":
                return i, j - 1, self._cells[i][j - 1].visited
            case "right":
                return i, j + 1, self._cells[i][j + 1].visited



    