import random, math, shelve, json

p_inventory = [
    {'name': 'none', 'amount': 0},
    {'name': 'none', 'amount': 0},
    {'name': 'none', 'amount': 0}

]
p_stat = [
    {'HP': 100},
    {'ATK': 10},
    {'XP': 0},
    {'DEF': 0},
    {'LVL': 1},
    {'Points': 0}
]

monsters = [
    {'monster_name': 'wolf', 'monster_hp': 100, 'monster_armor': 5},
    {'monster_name': 'boar', 'monster_hp': 200, 'monster_armor': 10},
    {'monster_name': 'rabbit', 'monster_hp': 50, 'monster_armor': 2}

]

loot_tables = [
    {'item_name': 'gold', 'chance': 100, 'max_amount': 300},
    {'item_name': 'skin', 'chance': 25, 'max_amount': 5},
    {'item_name': 'tusk', 'chance': 40, 'max_amount': 10},
    {'item_name': 'meat', 'chance': 50, 'max_amount': 30}
]


def inv():

    print("!" + '=' * 10, 'Inventory', '=' * 10 + "!")
    for item in p_inventory:
        if item['amount'] > 1:
            print('+', item['amount'], 'x', item['name'] + 's', "|", item['class'],)
        else:
            print('+', item['amount'], 'x', item['name'], "|",  item['class'])
    print('!' + '=' * 31 + '!')


def equipment():
    print('=' * 10, 'Equipment', '=' * 10)
    for i in range(6):
        print('+', p_equipment[i])
    print('!', '=' * 31, '!')


    print('!', '=' * 31, '!')
# def p_stats():
#   for i in range(6):
#        print('+', p_stat[i])
#   print('!', '=' * 30, '!')


# def take():
#    print('=' * 10, 'Inventory', '=' * 10)
#    a = input("How much do you wont to pick up? ")
#    b = 0
#    for i in range(int(inpnum(a))):
#        if i == 0 :
#            print('ass')
#    print('!', '=' * 30, '!')


# def inpnum(a):
#    while True:
#        a = input("Chose, which item you will take ")
#        if a.isdecimal() == True:
#            return a
#       else:
#            print("only numbers")


def drop_loot(loot_table):
    loot = []
    for possible_item in loot_table:
        if possible_item['chance'] > random.random():
            amount = random.randint(1, possible_item['max_amount'])
            item = {'name': possible_item['name'], 'amount': amount, 'class': possible_item['class']}
            loot.append(item)
    return loot


def load_items():
    global item_character
    item_file = open('item_characters.txt')
    item_character = json.load(item_file)
    item_file.close()


def load_monsters():
    global m_l
    monsterfile = open('monster.txt')
    m_l = json.load(monsterfile)
    monsterfile.close()


def save_state():
    save_file = shelve.open('save_p')
    save_file['inventory'] = p_inventory
    save_file['equipment'] = p_equipment
    save_file['current_health'] = p_currenthp
    save_file['level'] = p_level
    save_file['exp'] = p_exp
    save_file['dmg'] = p_dmg
    save_file['def'] = p_def
    save_file.close()


def load_state():
    global p_inventory, p_equipment, p_currenthp, p_level, p_exp, p_dmg, p_def

    save_file = shelve.open('save_p')
    p_inventory = save_file['inventory']
    p_equipment = save_file['equipment']
    p_currenthp = save_file['current_health']
    p_level = save_file['level']
    p_exp = save_file['exp']
    p_dmg = save_file['dmg']
    p_def = save_file['def']
    save_file.close()


def att(a, b):
    dmg = a - math.atan(10*b)//(math.pi/2)
    return dmg


def adv():
    load_state()
    global p_currenthp
    load_monsters()
    x = random.randint(0, 2)
    monster = m_l['monsters'][x]
    drop = m_l['loot_table']
    m_hp = monster['monster_hp']
    print('=' * 10, 'Adventure', '=' * 10)
    print(p_currenthp, '- Your health' "\n",  p_exp, 'Your exp' "\n", p_dmg, 'Your dmg' "\n", p_equipment, end="\n")
    print('You see a monster', monster['monster_name'], 'what you wold to do? \'а-attak\', \'b-run\'')

    if input() == "a":

        while m_hp > 0 and input() == "a" and p_currenthp > 0:
            d = att(int(p_dmg), int(monster['monster_def']))
            p_d = att(monster['monster_dmg'], p_def)
            m_hp -= d
            p_currenthp -= p_d
            print(m_hp, "/", monster['monster_hp'], '|', p_currenthp, '/', max_hp)

        if m_hp <= 0:
            print('you win, and this your reward')
            drop = drop_loot(drop)
            print('=' * 10, 'drop', '=' * 10)

            for i in range(len(drop)):
                print('+', drop[i]['name'], + drop[i]['amount'], "|", drop[i]['class'])
            print('!' + '=' * 25 + '!')

            if len(p_inventory) == 0:
                for item in drop:
                    p_inventory.append(item)
            else:
                for i in range(len(p_inventory)):
                    if drop[i]['name'] == p_inventory[i]['name']:
                        p_inventory[i]['amount'] += drop[i]['amount']
                    else:
                        p_inventory.append(drop[i])

            save_state()

        elif m_hp > 0 >= p_currenthp:
            print("You dead")
            save_state()

        else:
            print('You escaped')
            save_state()

    elif input() == 'b':
        print('You escaped')
        save_state()

    print('!' + '=' * 29 + '!')


p_inventory = []
p_equipment = [

    {'f_weapon': 'none'},
    {'s_weapon': 'none'},
    {'head': 'none'},
    {'breast': 'none'},
    {'legs': 'none'},
    {'hands': 'none'}

]
max_hp = 100
p_currenthp = 100
p_level = 1
p_exp = 0
p_dmg = 50
p_def = 4
save_state()
load_state()

while True:
    player_ansv = input('What u wont to do?\'adv\' - avdenture. \'save\' - save. \'inv\'- see the inventory, '
                        '\'e\'- see equipment, \'exit\' - log out: \n')
    if player_ansv == 'adv':
        adv()
    elif player_ansv == 'save':
        save_state()
    elif player_ansv == 'inv':
        inv()
    elif player_ansv == 'e':
        p_a = input("What you wont to do this your Equipment(\'equip\' - for equipment | \'look\' - for an overview \n")
        if p_a == 'equip':
            pass
        if p_a == 'look':
            equipment()
    elif player_ansv == "exit":
        save_state()
        exit(0)
    else:
        save_state()
