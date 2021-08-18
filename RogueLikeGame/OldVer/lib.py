class Item:
    name = ""
    amount = 1

    def __init__(self, name="", amount=1, dict=None):
        if dict in None:
            self.name = name
            self.amount = amount
        else:
            self.name = dict['name']
            self.amount = dict['amount']

    def __eq__(self, other):
        return other.name == self.name

    def __str__(self):
        return self.name + " x" + str(self.amount)


class Inventory:
    item_list = []
    label = "Inventory"

    def add_item(self, item):
        if item in self.item_list:
            needed_item = self.item_list[self.item_list.index(item)]
            needed_item.amount += item.amount
        else:
            self.item_list += [item]

    def __str__(self):
        string = "+" + "=" * 20 + ' ' + self.label + ' ' + "=" * 20 + '+\n'
        for item in self.item_list:
            string += "| " + str(item) + "\n"
        string += "+" + "=" * (42 + len(self.label)) + "+"
        return string


class Weapon:
    dmg = 0
    armor = 0


class Armor:
    armor = 0
    slot = ""


class Equipment:
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

class Monster:
    name = ""
    health = 0
    dmg = 0
    armor = 0

    def load_monster(self):
        


class Player:
    inventory = Inventory
    equipment = Equipment
    level = 1
    exp = 0
    health = 100
    dmg = 10
    armor = 5

    def equip(self, item_index):
        old_item = self.equipment.equip(self.inventory.item_list.pop(item_index))
        if old_item is not None:
            self.inventory.add_item(old_item)

