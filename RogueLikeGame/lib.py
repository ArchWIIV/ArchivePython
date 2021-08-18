import math, random, shelve


class Item:
    name = ""
    amount = 1

    def __init__(self, name="", amount=1, d=None):
        if d is None:
            self.name = name
            self.amount = amount
        else:
            self.name = d['name']
            self.amount = d['amount']

    def __eq__(self, other):
        return other.name == self.name

    def __str__(self):
        return self.name + " x" + str(self.amount)

    def clone(self):
        return Item(self.name, self.amount)


class Inventory:
    item_list = []
    label = "Inventory"

    def add_item(self, item):
        item_names = [item.name for item in self.item_list]
        if item.name in item_names:
            needed_item = self.item_list[item_names.index(item.name)]
            needed_item.amount += item.amount
        else:
            self.item_list += [item]

    def add_items(self, item_list):
        for item in item_list:
            self.add_item(item)

    def __str__(self):
        string = "+" + "=" * 20 + ' ' + self.label + ' ' + "=" * 20 + '+\n'
        for i in range(len(self.item_list)):
            string += str(i) + " | " + str(self.item_list[i]) + "\n"
        string += "+" + "=" * (42 + len(self.label)) + "+"
        return string


class Weapon:
    dmg = 0
    armor = 0
    slot = "r_weapon"

    def __init__(self, name="", amount=0, dmg=0, armor=0, slot="r_weapon", dict=None):
        if dict is None:
            self.name = name
            self.amount = amount
            self.dmg = dmg
            self.armor = armor
            self.slot = slot
        else:
            self.name = dict['name']
            self.amount = dict['amount']
            self.dmg = dict['dmg']
            self.armor = dict['armor']

    def clone(self):
        return Weapon(self.name, self.amount, self.dmg, self.armor, self.slot)

    def __str__(self):
        return self.name + " x" + str(self.amount) + " | Armor: " + str(self.armor) + " Dmg: " + str(self.dmg)


class Armor:
    armor = 0
    slot = ""

    def __init__(self, name="", amount=0, armor=0, slot="r_weapon", dict=None):
        if dict is None:
            self.name = name
            self.amount = amount
            self.armor = armor
            self.slot = slot
        else:
            self.name = dict['name']
            self.amount = dict['amount']
            self.armor = dict['armor']
            self.slot = dict['slot']

    def clone(self):
        return Armor(self.name, self.amount, self.armor, self.slot)

    def __str__(self):
        return self.name + " x" + str(self.amount) + " Armor: " + str(self.armor) + " |Slot: " + str(self.slot)


class LootTable:
    item_list = []
    chances = []

    def __init__(self, dict=None):
        for item in dict:
            self.item_list.append(item_from_dict(item))
            self.chances.append(item['chance'])

    def drop_loot(self):
        loot = []
        for i in range(len(self.item_list)):
            if self.chances[i] > (random.random() * 100):
                amount = random.randint(1, self.item_list[i].amount + 1)
                item = self.item_list[i].clone()
                item.amount = amount
                loot.append(item)
        return loot


class Equipment:
    label = "Equipment"
    r_weapon = None
    l_weapon = None
    head = None
    breast = None
    legs = None
    gloves = None

    def get_total_armor(self):
        total_armor = 0
        total_armor += self.r_weapon.armor if self.r_weapon is not None else 0
        total_armor += self.l_weapon.armor if self.l_weapon is not None else 0
        total_armor += self.head.armor if self.head is not None else 0
        total_armor += self.breast.armor if self.breast is not None else 0
        total_armor += self.legs.armor if self.legs is not None else 0
        total_armor += self.gloves.armor if self.gloves is not None else 0
        return total_armor

    def equip(self, item):
        if item.slot == "r_weapon":
            old_item = self.r_weapon
            self.r_weapon = item
            return old_item
        elif item.slot == "l_weapon":
            old_item = self.l_weapon
            self.l_weapon = item
            return old_item
        elif item.slot == "head":
            old_item = self.head
            self.head = item
            return old_item
        elif item.slot == "breast":
            old_item = self.breast
            self.breast = item
            return old_item
        elif item.slot == "legs":
            old_item = self.legs
            self.legs = item
            return old_item
        elif item.slot == "gloves":
            old_item = self.gloves
            self.gloves = item
            return old_item

    def get_total_dmg(self):
        total_dmg = 0
        total_dmg += self.r_weapon.dmg if self.r_weapon is not None else 0
        total_dmg += self.l_weapon.dmg if self.l_weapon is not None else 0
        return total_dmg

    def __str__(self):
        string = "+" + "=" * 20 + ' ' + self.label + ' ' + "=" * 20 + '+\n'
        string += "Right hand | " + str(self.r_weapon) + "\n"
        string += " Left hand | " + str(self.l_weapon) + "\n"
        string += "      Head | " + str(self.head) + "\n"
        string += "    Breast | " + str(self.breast) + "\n"
        string += "      Legs | " + str(self.legs) + "\n"
        string += "    Gloves | " + str(self.gloves) + "\n"
        string += "+" + "=" * (42 + len(self.label)) + "+"
        return string


class Monster:
    name = ""
    max_health = 0
    health = 0
    dmg = 0
    armor = 0

    def __init__(self, name="", max_health=0, dmg=0, armor=0, dict=None):
        if dict is None:
            self.name = name
            self.max_health = max_health
            self.health = max_health
            self.dmg = dmg
            self.armor = armor
        else:
            self.name = dict['monster_name']
            self.max_health = dict['monster_hp']
            self.health = self.max_health
            self.dmg = dict['monster_dmg']
            self.armor = dict['monster_def']

    def __str__(self):
        return self.name + " X " + str(self.max_health) + "/" + str(self.health) #+ "| |" + str(self.armor) + str(self.dmg) + "| |"

    def receive_dmg(self, att):
        dmg = int(att - math.atan(0.017 * self.armor) / (math.pi / 2))
        self.health -= dmg
        return self.health <= 0


class Player:
    inventory = Inventory()
    equipment = Equipment()
    level = 1
    exp = 0
    max_health = 100
    health = 100
    dmg = 100
    armor = 5

    def __str__(self):
        return "Твое здоровье " + str(self.health) + " \ " + str(self.max_health)# + " |Your state " + str(self.armor) + " armor|dmg " + str(self.dmg)

    def equip(self, item_index):
        item = self.inventory.item_list[item_index]
        if item.amount > 1:
            item.amount -= 1
            if isinstance(item, Weapon):
                old_item = self.equipment.equip(Weapon(item.name, 1, item.dmg, item.armor, item.slot))
            elif isinstance(item, Armor):
                old_item = self.equipment.equip(Armor(item.name, 1, item.armor, item.slot))
            else:
                item.amount += 1
                print("Вход только для Armor и Weapon")
                return
        else:
            old_item = self.equipment.equip(self.inventory.item_list.pop(item_index))
        if old_item is not None:
            self.inventory.add_item(old_item)

    def get_dmg(self):
        return self.dmg + self.equipment.get_total_dmg()

    def receive_dmg(self, att):
        dmg = int(att - math.atan(0.017 * self.armor) / (math.pi / 2))
        self.health -= dmg
        return self.health <= 0


def load_player(p):
    save_file = shelve.open(p)
    player = save_file['player']
    player.inventory = save_file['inventory']
    player.equipment = save_file['equipment']
    save_file.close()
    return player


def item_from_dict(d):
    print(d.keys())
    if 'class' in d.keys() and d['class'] == "weapon":
        return Weapon(dict=d)
    elif 'class' in d.keys() and d["class"] == "armor":
        return Armor(dict=d)
    else:
        return Item(d=d)


def save_player(p, player):
    save_file = shelve.open(p)
    save_file['inventory'] = player.inventory
    save_file['equipment'] = player.equipment
    save_file['player'] = player
    save_file.close()
