

class SnakeHead:
    name = ""
    x = 0
    y = 0
    long = 0
    sign = 1
    score = 0

    def __init__(self, name="", long=1, sign=1, x=0, y=0, score=0):
        self.name = name
        self.x = x
        self.y = y
        self.long = long
        self.sign = sign
        self.score = score

    def step(self, direction):
        if direction == "up":
            self.x -= 1
        elif direction == "down":
            self.x += 1
        elif direction == "left":
            self.y -= 1
        elif direction == "right":
            self.y += 1


class LaxaderAss:
    x = 0
    y = 0
    nutritious = 1
    sign = 2

    def __init__(self, x=0, y=0, nutritious=1, sign=2):
        self.x = x
        self.y = y
        self.nutritious = nutritious
        self.sign = sign


class SnakeTale:
    x = 0
    y = 0
    sign = 1
    long = 0

    def __init__(self, x=0, y=0, long=0, sign=1):
        self.x = x
        self.y = y
        self.long = long
        self.sign = sign

