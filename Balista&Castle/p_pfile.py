import shelve
import random
from epic_calculator import *


class Castle:
    name = ""
    coord = []
    reward = 0
    durability = 0
    max_durability = 0

    def info(self, a):
        if a == "d":
            return str(self.durability) + " - Durability | Coordinates - " + str(self.coord)
        elif a == "name":
            return self.name + "'s_fort " + " - Name | Reward - " + str(self.reward)
        else:
            return a

    def __init__(self, name="", coord=None, reward=0, max_durability=0, d=None):
        if d is None:
            self.name = name
            self.coord = coord
            self.reward = reward
            self.max_durability = max_durability
            self.durability = max_durability
        else:
            self.name = d['name']
            self.coord = d['coord']
            self.reward = d['reward']
            self.max_durability = d['durability']
            self.durability = d['durability']

    def receive_dmg(self, weather, catapult, projectile, angle=0):
        result = calculate(hg_to_p(weather.air_pressure), c_to_k(weather.temperature), weather.humidity,
                           projectile.mass, projectile.radius, catapult.power, angle, weather.wind)
        print(result)
        result.draw_castle(self.coord[0], self.coord[1])
        result.save_image('kek.png')
        if (self.coord[0] - projectile.radius) <= result.x <= (self.coord[1] + projectile.radius):
            self.durability -= (result.calculate_damage(1) + projectile.damage)
        else:
            print("Miss, try again")

    def chose_castle(self, a=1):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.durability = random.randint(800, 2000) * a
        self.reward = random.randint(50, 1000) * a
        for i in range(6):
            self.name += alphabet[random.randint(0, len(alphabet)-1)]
            self.name = self.name.capitalize()
        x1 = clamp(random.randint(20, 150*a), 924, 20)
        x2 = clamp(x1 + random.randint(2, 200/a), 1023, 21)
        self.coord = [x1, x2]


class Catapult:
    name = ""
    level = 0
    cost = 0
    cost_up = 0
    power = 0

    def __init__(self, name="", cost_up=50, cost=0, power=100, d=None):
        if d is None:
            self.name = name
            self.cost = cost
            self.power = power
            self.cost_up = cost_up
        else:
            self.name = d['name']
            self.cost = d['cost']
            self.power = d['power']
            self.cost_up = d['cost_up']

    def cpu(self, player):
        if input('Введи ||up|| если хочешь улучшить катапульту:') == "up" and (player.value - self.cost_up) > 0:
            self.power *= 1.1
            self.cost_up *= 1.5
            self.level += 1
            player.value -= self.cost_up

    def __str__(self):
        return str(self.power) + " - Power| Level - " + str(self.level)

    def info_get(self):
        return self.name + " |Цена - " + str(self.cost) + "| Сила - " + str(self.power) + "| Цена за улучшение"\
               + str(self.cost_up) + "| Левел - " + str(self.level)


class Inventory:
    item_list = []
    label = "Inventory"

    def buy_item(self, item):
        item_names = [item.name for item in self.item_list]
        if item.name in item_names:
            needed_item = self.item_list[item_names.index(item.name)]
            needed_item.amount += item.amount
        else:
            self.item_list += [item]
            print(item)

    def buy_items(self, items):
        for item in items:
            self.buy_item(item)

    def __str__(self):
        string = "+" + "=" * 20 + ' ' + self.label + ' ' + "=" * 20 + '+\n'
        for i in range(len(self.item_list)):
            string += str(i) + " | " + str(self.item_list[i]) + "\n"
        string += "+" + "=" * (42 + len(self.label)) + "+"
        return string


class EbuchiiBariga:
    item_list = []
    cost = []
    label = "EbuchiBariga"

    def __init__(self, d=None):
        for item in d:
            self.item_list.append(Projectile(d=item))
            self.cost.append(item['cost'])

    def __str__(self):
        string = "+" + "=" * 20 + ' ' + self.label + ' ' + "=" * 20 + '+\n'
        for i in range(len(self.item_list)):
            string += str(i) + " | " + self.item_list[i].info_get() + "\n"
        string += "+" + "=" * (42 + len(self.label)) + "+"
        return string

    def set_list(self, player):
        buying_list = []
        print(self)
        while True:
            x = input("Введи ||yes|| что бы покупать, ||exit|| для того чтобы выйти: ")
            if x.lower() == "yes" and player.value != 0:
                y = int(input('Введи номер, предмета который хочешь купить: '))
                z = int(input('Введи количество, предмета который хочешь купить: '))
                for i in range(z+1):
                    if player.value - self.cost[y] < 0:
                        print("У вас кончились деньги, Ты успел купить только " + str(i))
                        break
                    buying_list += [self.item_list[y].clone()]
                    player.value -= self.cost[y]
            elif x.lower() == "exit":
                break
        return buying_list


class Projectile:
    name = ""
    amount = 1
    damage = 0
    mass = 0
    radius = 0
    cost = 0

    def __init__(self, name="", damage=0, mass=0, cost=0, amount=1, radius=0, d=None):
        if d is None:
            self.name = name
            self.damage = damage
            self.mass = mass
            self.cost = cost
            self.amount = amount
            self.radius = radius
        else:
            self.name = d['name']
            self.damage = d['damage']
            self.mass = d['mass']
            self.cost = d['cost']
            self.amount = d["amount"]
            self.radius = d['radius']

    def __str__(self):
        return self.name + " |Кол-во " + str(self.amount)

    def info_get(self):
        return self.name + " |Цена " + str(self.cost) + "|Масса " + str(self.mass) + "|Damage " \
               + str(self.damage) + "|Radius " + str(self.radius)

    def clone(self):
        return Projectile(self.name, self.damage, self.mass, self.cost, self.amount, self.radius)


class Weather:
    air_pressure = 762
    temperature = 27
    humidity = 0.8
    wind = 0

    def __init__(self, air_pressure=762, temperature=27, humidity=0.8, wind=0, d=None):
        if d is None:
            self.air_pressure = air_pressure
            self.temperature = temperature
            self.humidity = humidity
            self.wind = wind
        else:
            self.air_pressure = d['air_pressure']
            self.temperature = d['temperature']
            self.humidity = d['humidity']
            self.wind = d['wind']

    def __str__(self):
        return "Давление: " + str(self.air_pressure) + "|Температура: " + str(self.temperature) \
               + "|Влажность воздуха: " + str(self.humidity) + "|Сила и направление воздуха: " + str(self.wind)


class Player:
    catapult = Catapult()
    inventory = Inventory()
    name = ""
    value = 1000

    def __init__(self, name="", value=1000):
        self.name = name
        self.value = value

    def bought_catapult(self, d=None):
        for i in range(len(d)):
            print(str(i) + " -| " + d[i]['name'] + " |Power " + str(d[i]['power']) + " |Cost " + str(d[i][
                "cost"]) + " |Деньги за улучшение " + str(d[i]['cost_up']))
        print(self.value)
        x = int(input("Введи номер, катапульты которую хочешь купить: "))
        self.catapult = Catapult(d=d[x])
        self.value -= self.catapult.cost


def load_player(p):
    save_file = shelve.open(p)
    player = save_file['player']
    player.inventory = save_file['inventory']
    player.catapult = save_file['catapult']
    save_file.close()
    return player


def save_player(p, player):
    save_file = shelve.open(p)
    save_file['inventory'] = player.inventory
    save_file['player'] = player
    save_file['catapult'] = player.catapult
    save_file.close()
