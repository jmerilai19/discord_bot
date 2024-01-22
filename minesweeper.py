import math
import random

class Game:
    """
    Minesweeper game

    Game starts with start() function
    Moves are made with play(x, y, mode) function where x and y are the coordinates and mode is open or flag
    Both functions return (status, board)
        status: -1 = error, 0 = success, 1 = win, 2 = lose
    """
    def __init__(self, size):
        self.size = size
        self.mine_amount = math.floor(0.15 * self.size**2)

        self.symbols = {
            "unopened": "\u25A1",
            "empty": "-",
            "mine": "x",
            "flag": "f"
        }

        self.board, self.grid = [], []

    def start(self):
        self.board, self.grid = self.init_board()
        self.place_mines()
        self.place_numbers()
        
        return 0, self.board_state()
        
    def init_board(self):
        board = []
        grid = []

        for i in range(self.size):
            board.append([])
            for _ in range(self.size):
                board[i].append(self.symbols["unopened"])

        for i in range(self.size):
            grid.append([])
            for _ in range(self.size):
                grid[i].append("")

        return board, grid
    
    def board_state(self):
        return self.board
    
    def play(self, x, y, mode):
        try:
            x, y = int(x) - 1, int(y) - 1
        except Exception as e:
            return -1, self.board_state()
        else:
            if x < 0 or y < 0 or x >= self.size or y >= self.size:
                return -1, self.board_state()
            elif not self.board[y][x] == self.symbols["unopened"] and mode == "open":
                return -1, self.board_state()
            else:
                if mode == "open":
                    return self.open_field(x, y)
                elif mode == "flag":
                    self.flag(x, y)

                return 0, self.board_state()

    def place_mines(self):
        empty_spaces = []

        for x in range(self.size):
            for y in range(self.size):
                empty_spaces.append((x, y))

        for _ in range(self.mine_amount):
            random_index = random.randint(0, len(empty_spaces) - 1)
            random_space = empty_spaces[random_index]
            empty_spaces.pop(random_index)
            self.grid[random_space[1]][random_space[0]] = self.symbols["mine"]

    def place_numbers(self):
        for y in range(0, self.size):
            for x in range(0, self.size):
                if not self.grid[y][x] == "x":
                    self.grid[y][x] = self.count_mines_in_neighbor_fields(x, y)

    def count_mines_in_neighbor_fields(self, x, y):
        mine_amount = 0
        for yy in range(y - 1, y + 2):
            for xx in range(x - 1, x + 2):
                if yy >= 0 and xx >= 0 and yy < self.size and xx < self.size and self.grid[yy][xx] == self.symbols["mine"]:
                    mine_amount += 1
        return mine_amount

    def open_field(self, x, y):
        if self.grid[y][x] == self.symbols["mine"]:
            self.board[y][x] = self.grid[y][x]
            return 2, self.board_state()
        else:
            field_list = []
            field_list.append((x, y))
            
            while len(field_list) > 0:
                field = field_list.pop()
                
                if not self.board[field[1]][field[0]] == self.symbols["flag"]:
                    if self.grid[field[1]][field[0]] == 0:
                        self.board[field[1]][field[0]] = self.symbols["empty"]
                        self.grid[field[1]][field[0]] = self.symbols["empty"] # mark the field as opened in grid as well
                        for yy in range(field[1] - 1, field[1] + 2):
                            for xx in range(field[0] - 1, field[0] + 2):
                                if yy >= 0 and xx >= 0 and yy < self.size and xx < self.size:
                                    field_list.append((xx, yy))
                    elif isinstance(self.grid[field[1]][field[0]], int):
                        self.board[field[1]][field[0]] = self.grid[field[1]][field[0]]
            
        if self.check_winner():
            return 1, self.board_state()

        return 0, self.board_state()

    def flag(self, x, y):
        if self.board[y][x] == self.symbols["unopened"]:
            self.board[y][x] = self.symbols["flag"]
        elif self.board[y][x] == self.symbols["flag"]:
            self.board[y][x] = self.symbols["unopened"]
        
    def check_winner(self):
        fields_left = 0

        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] == self.symbols["unopened"] or self.board[y][x] == self.symbols["flag"]:
                    fields_left += 1

        if fields_left == self.mine_amount:
            return True
