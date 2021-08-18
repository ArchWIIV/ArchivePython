from p_pfile import *
import random
import json


def load_weather():
    global weather_preset
    kwk = open('weather.json')
    weather_preset = json.load(kwk)
    kwk.close()


def load_market():
    global itm_lst
    lwl = open('projectile_char.json')
    itm_lst = json.load(lwl)
    lwl.close()


def load_catapult():
    global catapult_list
    lwl = open('catapult.json')
    catapult_list = json.load(lwl)
    lwl.close()


def start_game():
    load_weather()
    feat = random.randint(0, 5)
    castle = Castle()
    weather = Weather(d=weather_preset[feat])
    level_of_difficulty = int(input("Введите урвень сложности: "))
    castle.chose_castle(level_of_difficulty)
    print(castle.info("d") + " | " + castle.info("name"))
    count = 0
    while castle.durability > 0:
        if count % 2 == 0:
            feat = random.randint(0, 6)
            weather = Weather(d=weather_preset[feat])
        ans = input("Стрелять в керчи - |x|, Смотреть сумку со взрывчаткой в метро - |inv|: ")
        if ans.lower() == "x":
            print(weather)
            x = int(input("Положи свой угол:"))
            y = int(input("Выбери че кидать будешь да?: "))
            if player.inventory.item_list[y].amount > 0:
                castle.receive_dmg(weather, player.catapult, player.inventory.item_list[y], int(x))
                print(castle.info("d"))
                count += 1
                player.inventory.item_list[y].amount -= 1
            else:
                print("А сам полететь не хочешь? Не суй то чего у тебя нету")
                player.inventory.item_list.pop(y)
        elif ans.lower() == "inv":
            print(player.inventory)
        else:
            break
    if castle.durability <= 0:
        player.value += castle.reward
    else:
        print("Ну ты сбежал... а дальше что?")


def barter():
    load_market()
    print("Эй ты, вид у тебя какой-то подозрительный... кишки наматывать 10 минут любишь? каво?!, бдя да я, "
          "\n *Сраный барыга шизик* - думаешь ты ")
    c_or_bar = input("Слушай, что я тебе скажу... 'Псс я обосрался', да шучу я так, бдя бда дая, Ууу у тебя "
                     "тележечка прикольная, уаА-А-А *отрыжка* хочешь сделаю ей пожилой тюненг?"
                     " \n *Мда, но предложение очень даже заманчивое* |go|, |no|")
    if c_or_bar.lower() == "no":
        mem = input("Не ну ты и фашист конечно... да...*удар лица об прилавок*, Смотри что есть, хочешь купить? "
                    "У меня даже катапульты естьб бда дяа я...\n пиши |catap| - чтобы купить новую катапульту, "
                    "|proj|- снаряды, для катапульты: ")
        if mem == "proj":
            ebuchiibariga = EbuchiiBariga(d=itm_lst)
            kek = ebuchiibariga.set_list(player)
            player.inventory.buy_items(kek)
        elif mem == "catap":
            load_catapult()
            player.bought_catapult(d=catapult_list)
    elif c_or_bar.lower() == "go":
        print("НЫА ОТЛЕТАЕШЬ, СОЛЯНОГО ЫЫЫЫЫ, каво?! э?! \n *...* - твои мысли "
              "\n готовО, да да*неразборчивое пожилое бормотание* ")
        print(player.catapult.cost)
        player.catapult.cpu(player)
    print("Надеюсь ты ничего не украл, а то знаю я вас таких любителей... "
          "ууусука, А-а-а-а*звук удара головы об ведро\n каво?!")


while True:
    n_or_l = input(
        "Хоти те ли загрузить персонажа или начать новую игру? ||'new' - Новая игра, 'load' - Загрузить персонажа: ")
    if n_or_l.lower() == "new":
        player = Player(input("Введите имя персонажа: "), 1000)
        save_player(player.name + "_save", player)
        break
    elif n_or_l.lower() == "load":
        player = load_player(input("Имя вашего персонажа: ").lower() + "_save")
        break
    else:
        print("Такой персонаж находиться в твои мечтах, бич")


while True:
    p_choose = input("What you wont to do? || 'p' - play, 'barter' - зайти к ЕбучемуБарыге чисто по рофлу,"
                     " \n 'exit' - to выйти отсюда вперед ногами, 'save' - сохраниться, 'inv' - инвентарь: ")
    if p_choose.lower() == "p":
        start_game()
    elif p_choose.lower() == "barter":
        barter()
        save_player(player.name.lower() + "_save", player)
    elif p_choose.lower() == "inv":
        print(player.inventory)
        print(str(player.value) + " | це твои гроши")
        print(player.catapult)
        print(player.catapult.info_get())
    elif p_choose.lower() == "exit":
        save_player(player.name.lower() + "_save", player)
        break
