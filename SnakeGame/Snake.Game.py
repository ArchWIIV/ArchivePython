import random
import keyboard
import time
import os
from Snake import *


def set_field(height, width):
    field = []
    for i in range(height):
        field.append([0 for _ in range(width)])
    return field


def print_field(field):
    os.system('cls')
    for row in field:
        row_string = ""
        for cell in row:
            if cell == 1:
                row_string += "#"
            elif cell == 2:
                row_string += "*"
            else:
                row_string += "0"
        print(row_string)


def step(count):
    print_field(m)
    purge(m, H, W)
    if count % 5 == 0:
        random_spawn(apple, m, H, W)
    if snake.x == apple.x and snake.y == apple.y:
        snake.score += apple.nutritious
        random_spawn(apple, m, H, W)
    next_step(snake, m)
    next_step(apple, m)
    print_field(m)
    return count


def game_lup():
    count = 0

    while True:
        time.sleep(0.1)
        if keyboard.is_pressed("up"):
            snake.step(direction="up")
            next_step(snake, m)
            count += 1
            step(count)
            print(snake.score)
            print(count)
            pp(m)
            print(str(snake.x) + " : X|Y : " + str(snake.y))
        elif keyboard.is_pressed("down"):
            snake.step(direction="down")
            next_step(snake, m)
            count += 1
            step(count)
            print(snake.score)
            print(count)
            pp(m)
            print(str(snake.x) + " : X|Y : " + str(snake.y))
        elif keyboard.is_pressed("left"):
            snake.step(direction="left")
            next_step(snake, m)
            count += 1
            step(count)
            print(snake.score)
            print(count)
            pp(m)
            print(str(snake.x) + " : X|Y : " + str(snake.y))
        elif keyboard.is_pressed("right"):
            snake.step(direction="right")
            next_step(snake, m)
            count += 1
            step(count)
            print(snake.score)
            print(count)
            pp(m)
            print(str(snake.x) + " : X|Y : " + str(snake.y))
        elif keyboard.is_pressed("escape"):
            print("You are close the game")
            break


def pp(field):
    for i in range(5):
        print(field[i])


def random_spawn(item, field, h, w):
    x = random.randint(0, h-1)
    y = random.randint(0, w-1)
    field[x][y] = item.sign
    item.x = x
    item.y = y


def purge(field, h, w):
    for i in range(h):
        field[i] = []
        for j in range(w):
            field[i].append(0)


def next_step(name, field):
    if name.long is False or name.score == 0:
        if name.x >= 0 and name.y >= 0:
            x = name.x
            y = name.y
            field[x][y] = name.sign
        elif name.x >= 0 > name.y:
            print("out of range")
        elif name.x < 0 >= name.y:
            print("out of range")
    else:
        if name.x >= 0 and name.y >= 0:
            x = name.x
            y = name.y
            field[x][y] = name.sign
            if name.score > 0:
                tale = SnakeTale
                tale.long = name.score
                tale.x = name.x
                tale.y = name.y
                field[tale.x][tale.y] = tale.sign
        elif name.x >= 0 > name.y:
            print("out of range")
        elif name.x < 0 >= name.y:
            print("out of range")


while True:

    p_choose = input("If u wont to play, print |p| - play, |s|- to see a scores, |exit| - exit: ")
    if p_choose == "p":
        snake = SnakeHead()
        apple = LaxaderAss()
        H = int(input("Choose height of the FIELD: "))
        W = int(input("Choose weight of the RICE FIELD MTHFUCKA: "))
        m = set_field(H, W)
        print_field(m)
        random_spawn(snake, m, H, W)
        random_spawn(apple, m, H, W)
        game_lup()
    elif p_choose == "s":
        pass
    elif p_choose == "exit":
        break
