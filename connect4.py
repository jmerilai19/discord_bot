class Game:
    """
    Connect 4 game

    Game starts with start() function
    Moves are made with play(x) function where x is the column to drop the piece in
    Both functions return (status, board)
        status: -1 = error, 0 = player 0 turn, 1 = player 1 turn, 2 = player 0 won, 3 = player 1 won, 4 = draw
    """
    def __init__(self, _sixeX = 7, _sizeY = 6):
        self.symbols = {
            "empty": ' ',
            "0": 'o',
            "1": 'x'
        }

        self.board = []
        self.sizeX, self.sizeY = _sixeX, _sizeY

        self.turn = 0 # 0 or 1

    def start(self):
        self.board = self.init_board()
        return self.turn, self.board_state()
    
    def init_board(self):
        board = []

        for i in range(self.sizeY):
            board.append([])
            for _ in range(self.sizeX):
                board[i].append(self.symbols["empty"])

        return board
    
    def board_state(self):
        return self.board
    
    def play(self, x):
        if x < 0 or x >= self.sizeX:
            return self.turn, self.board_state()
        
        found = False
        # loop from bottom to top
        for y in range(self.sizeY - 1, -1, -1):
            if self.board[y][x] == self.symbols["empty"]:
                self.board[y][x] = self.symbols[str(self.turn)]
                found = True
                break

        if not found:
            return self.turn, self.board_state()

        if self.check_winner():
            if self.turn == 0:
                return 2, self.board_state() # player 0 won
            return 3, self.board_state() # player 1 won
        elif self.check_if_board_is_full():
            return 4, self.board_state() # draw

        # next turn
        self.turn = 0 if self.turn == 1 else 1

        return self.turn, self.board_state()
    
    def check_winner(self):
        # horizontal
        for y in range(self.sizeY):
            for x in range(self.sizeX - 3):
                if self.board[y][x] != self.symbols["empty"]:
                    if self.board[y][x] == self.board[y][x+1] and self.board[y][x+1] == self.board[y][x+2] and self.board[y][x+2] == self.board[y][x+3]:
                        return True
        
        # vertical
        for x in range(self.sizeX):
            for y in range(self.sizeY - 3):
                if self.board[y][x] != self.symbols["empty"]:
                    if self.board[y][x] == self.board[y+1][x] and self.board[y+1][x] == self.board[y+2][x] and self.board[y+2][x] == self.board[y+3][x]:
                        return True
        
        # anti diagonal
        for y in range(self.sizeY - 3):
            for x in range(self.sizeX - 3):
                if self.board[y][x] != self.symbols["empty"]:
                    if self.board[y][x] == self.board[y+1][x+1] and self.board[y+1][x+1] == self.board[y+2][x+2] and self.board[y+2][x+2] == self.board[y+3][x+3]:
                        return True
        
        # diagonal
        for y in range(3, self.sizeY):
            for x in range(self.sizeX - 3):
                if self.board[y][x] != self.symbols["empty"]:
                    if self.board[y][x] == self.board[y-1][x+1] and self.board[y-1][x+1] == self.board[y-2][x+2] and self.board[y-2][x+2] == self.board[y-3][x+3]:
                        return True
                    
        return False
    
    def check_if_board_is_full(self):
        for y in range(self.sizeY):
            for x in range(self.sizeX):
                if self.board[y][x] == self.symbols["empty"]:
                    return False
        return True
