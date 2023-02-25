import math
import random

class Game:
    def __init__(self, size):
        self.size = size
        self.dragon_amount = math.floor(0.15 * self.size**2)

        self.symbols = {
            "unopened": "-",
            "empty": " ",
            "dragon": "x",
            "flag": "f"
        }

        self.display_symbols = {
            "unopened": ":purple_square:",
            "empty": ":blue_square:",
            "dragon": ":dragon:",
            "flag": ":triangular_flag_on_post:",
            "1": ":one:",
            "2": ":two:",
            "3": ":three:",
            "4": ":four:",
            "5": ":five:",
            "6": ":six:",
            "7": ":seven:",
            "8": ":eight:"
        }

        self.board, self.grid = self.init_board()
        
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

    def place_dragons(self):
        empty_spaces = []
        for x in range(self.size):
            for y in range(self.size):
                empty_spaces.append((x, y))

        for _ in range(self.dragon_amount):
            random_index = random.randint(0, len(empty_spaces) - 1)
            random_space = empty_spaces[random_index]
            empty_spaces.pop(random_index)
            self.grid[random_space[1]][random_space[0]] = self.symbols["dragon"]

    def count_dragons_in_neighbor_fields(self, x, y):
        dragon_amount = 0
        for yy in range(y - 1, y + 2):
            for xx in range(x - 1, x + 2):
                if yy >= 0 and xx >= 0 and yy < self.size and xx < self.size and self.grid[yy][xx] == self.symbols["dragon"]:
                    dragon_amount += 1
        return dragon_amount

    def place_numbers(self):
        for y in range(0, self.size):
            for x in range(0, self.size):
                if not self.grid[y][x] == "x":
                    self.grid[y][x] = self.count_dragons_in_neighbor_fields(x, y)

    def board_message(self):
        message = ""

        for y in range(self.size):
            for x in range(self.size):
                if isinstance(self.board[y][x], int):
                    message += self.display_symbols[str(self.board[y][x])]
                else:
                    for symbol_key in self.symbols.keys():
                        if self.board[y][x] == self.symbols[symbol_key]:
                            message += self.display_symbols[symbol_key]
            message += "\n"

        return message

    def open_field(self, x, y):
        if self.grid[y][x] == self.symbols["dragon"]:
            self.board[y][x] = self.grid[y][x]
            return self.lose()
        else:
            field_list = []
            field_list.append((x, y))
            
            while len(field_list) > 0:
                field = field_list.pop()
                
                if self.grid[field[1]][field[0]] == 0:
                    self.board[field[1]][field[0]] = self.symbols["empty"]
                    self.grid[field[1]][field[0]] = self.symbols["empty"] # mark the field as opened in grid as well
                    for yy in range(field[1] - 1, field[1] + 2):
                        for xx in range(field[0] - 1, field[0] + 2):
                            if yy >= 0 and xx >= 0 and yy < self.size and xx < self.size:
                                field_list.append((xx, yy))
                elif isinstance(self.grid[field[1]][field[0]], int):
                    self.board[field[1]][field[0]] = self.grid[field[1]][field[0]]
            
        if self.check_win():
            return self.win_message()
        return self.board_message()

    def flag(self, x, y):
        if self.board[y][x] == self.symbols["unopened"]:
            self.board[y][x] = self.symbols["flag"]
        elif self.board[y][x] == self.symbols["flag"]:
            self.board[y][x] = self.symbols["unopened"]

    def win_message(self):
        board = self.board_message()
        return board

    def lose(self):
        board = self.board_message()
        return board
    
    def check_win(self):
        fields_left = 0
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] == self.symbols["unopened"] or self.board[y][x] == self.symbols["flag"]:
                    fields_left += 1

        if fields_left == self.dragon_amount:
            return True

    def start(self):
        self.init_board()
        self.place_dragons()
        self.place_numbers()
        
        board = self.board_message()

        return board

    def play(self, x, y, mode):
        try:
            x, y = int(x) - 1, int(y) - 1
        except Exception as e:
            if mode == "open":
                return "invalid !open command"
            elif mode == "flag":
                return "invalid !flag command"
        else:
            if x < 0 or y < 0 or x >= self.size or y >= self.size:
                return "Invalid coordinates"
            elif not self.board[y][x] == self.symbols["unopened"]:
                return "Field already opened"
            else:
                if mode == "open":
                    return self.open_field(x, y)
                elif mode == "flag":
                    self.flag(x, y)

                return self.board_message()
        