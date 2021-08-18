from lib import *
import random
import json

player = Player()


def load_monster():
    global m_l
    global loot_table
    monsterfile = open('monster.json')
    m_l = json.load(monsterfile)
    loot_table = LootTable(dict=m_l['loot_table'])
    monsterfile.close()


def adv():
    x = random.randint(0, 2)
    m = m_l['monsters'][x]
    monster = Monster(dict=m)
    print('=' * 10, 'Adventure', '=' * 10)
    print(player)
    while True:
        answ = input('You see a monster ' + str(monster.name) + ' what you wold to do? \'а-attack\', \'b-run\': ')
        if answ == "a":
            if monster.receive_dmg(player.get_dmg()):
                print(str(monster.name) + ' are откинул копыта')
                pr_loot = loot_table.drop_loot()
                for item in pr_loot:
                    print("And this your reward " + str(item))
                player.inventory.add_items(pr_loot)
                break
            print(monster)

            if player.receive_dmg(monster.dmg):
                print("You are проебали, сэр")
                player.health = player.max_health
                break
            print(player)
            continue
        elif answ == "b":
            print("Runin90's.mp3")
            break
        else:
            continue
    print('!' + '=' * 25 + '!')


def equip():
    print('=' * 10, 'Equipment', '=' * 10)
    x = int(input("Номер слота айтема: "))
    if x >= len(player.inventory.item_list):
        print("Ты лох и пиши нормально ")
        return
    if isinstance(player.inventory.item_list[x], Weapon):
        slot = input("Выбери слот для оружия: (r_weapon/l_weapon)")
        if slot != "r_weapon" and slot != "l_weapon":
            slot = "r_weapon"
            print("Крч, оно в правой руке, дрочила")
        player.inventory.item_list[x].slot = slot
    player.equip(x)
    print('!' + '=' * 42 + '!')


load_monster()


while True:
    player_ansv = input('What u wont to do? \'adv\' - avdenture. \'save\' - save. \'inv\'- see the inventory, '
                        '\'e\'- see equipment, \'exit\' - log out: ')
    if player_ansv == 'adv':
        pass
        adv()
    elif player_ansv == 'save':
        save_player("save", player)
    elif player_ansv == 'inv':
        print(player.inventory)
    elif player_ansv == 'e':
        p_a = input("What you wont to do this your Equipment(\'equip\' - for equip, \'look\' - for looking): ")
        if p_a == 'equip':
            equip()
            save_player("save", player)
        if p_a == 'look':
            print(player.equipment)
    elif player_ansv == "exit":
        save_player("save", player)
        exit(0)
