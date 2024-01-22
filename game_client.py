class Connect4Client:
    def __init__(self):
        self.display_symbols = {
            " ": "⚪",
            "o": "🟡",
            "x": "🔴",
        }

    def start(self, game):
        status, board = game.start()

        message = "|:one:|:two:|:three:|:four:|:five:|:six:|:seven:|\n"

        for row in board:
            for item in row:
                message += "|" + str(self.display_symbols[item])
            message += "|\n"

        return status, message

    def play(self, game, x):
        status, board = game.play(x)

        message = "|:one:|:two:|:three:|:four:|:five:|:six:|:seven:|\n"

        for row in board:
            for item in row:
                message += "|" + str(self.display_symbols[item])
            message += "|\n"

        return status, message

class MinesweeperClient:
    def __init__(self):
        self.display_symbols = {
            "\u25A1": ":purple_square:",
            "-": ":blue_square:",
            "x": ":dragon:",
            "f": ":triangular_flag_on_post:",
            "1": ":one:",
            "2": ":two:",
            "3": ":three:",
            "4": ":four:",
            "5": ":five:",
            "6": ":six:",
            "7": ":seven:",
            "8": ":eight:"
        }

    def start(self, game):
        status, board = game.start()

        message = ""

        for row in board:
            for item in row:
                message += str(self.display_symbols[item])
            message += "\n"

        return status, message
    
    def play(self, game, x, y, mode):
        status, board = game.play(x, y , mode)

        message = ""

        for row in board:
            for item in row:
                message += str(self.display_symbols[str(item)])
            message += "\n"

        return status, message
