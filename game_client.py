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

