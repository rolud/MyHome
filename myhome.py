import telepot
import time
import pickle
from house import House
from house import ToBuyList
from house import Home
from rounds import Round

#  TOKEN = "456087597:AAFovjaINg0aqR_rwL_qFQ0dvCYERCo6fik"  # testing bot token
TOKEN = "389923145:AAFKDIOoGD08DYbVFUCw6k-2ySAfC3zQo1s" # myhome bot token


def handle(msg):
    chat_id = msg["chat"]["id"]
    sender_name = msg["from"]["first_name"]
    sender_id = msg["from"]["id"]
    command, *text = msg["text"].split()
    if "@" in command:
        command = command.split("@")[0]
    # the first string in the message is the command
    # text is a list that contains remaining strings of the message
    print("--- Got command %-10s in chat %d sent by %s - %d" % (command, chat_id, sender_name, sender_id))
    # logfile = open("logfile.data", "a")
    # log = "--- " + time.strftime("%d/%m/%Y %H.%M.%S", time.gmtime()) + ": Got command " + command + " in chat "\
    #       + str(chat_id) + " sent by " + sender_name + " - " + str(sender_id) + ".\n"
    # print(log.rstrip())
    # logfile.write(log)
    if not house.is_hsm(sender_id):
        bot.sendMessage(chat_id, "Hey, you're new!")
        house.add_hsm(sender_id, sender_name)
        bot.sendMessage(chat_id, "Can you tell me your username?")
        bot.sendMessage(chat_id, "Write me: /myusr <USERNAME>")
    if command.lower() == "/start":
        message = "Benvenuto, digita /help per vedere tutti i comandi utilizzabili"
        bot.sendMessage(chat_id, message)
    elif command.lower() == "/myusr":
        house.get_hsm_by_id(sender_id).update_username(text[0])
        bot.sendMessage(chat_id, "You are now registered!")
    elif command.lower() == "/help":
        message = "Comandi disponibili:\n- /today: per controllare il turno di oggi\n"\
                  + "- /week: per vedere i turni della settimana\n"
        bot.sendMessage(chat_id, message)
    elif command.lower() == "/today":
        message = rounds.today_round(house)
        bot.sendMessage(chat_id, message)
    elif command.lower() == "/week":
        message = rounds.week_round(house)
        bot.sendMessage(chat_id, message)
    elif command.lower() == "/nextweek":
        message = rounds.next_week_round(house)
        bot.sendMessage(chat_id, message)
    elif command.lower() == "/add":  # adds an object to the list of things to buy
        obj = " "
        obj = obj.join(text)
        if to_buy_list.add(obj):
            message = obj.capitalize() + " è stato aggiunto."
        else:
            if obj == "":
                message = "Usa il comando /add seguito da ciò che vuoi aggiungere alla lista"
            else:
                message = "Elemento già presente."
        bot.sendMessage(chat_id, message)
    elif command.lower() == "/list":    # shows the list of things to buy
        lst = to_buy_list.get_list()
        if lst == "":
            message = "La lista è vuota."
        else:
            message = "Cose da comprare:\n\n" + lst
        bot.sendMessage(chat_id, message)
    elif command.lower() == "/removeall":  # clears the list of things to buy
        to_buy_list.remove_all()
        message = "Ho svuotato la lista.\nNon c'è nulla da comprare."
        bot.sendMessage(chat_id, message)
    elif command.lower() == "/remove":  # removes an object from the list of things to buy
        obj = " "              # the parameter passed could be the name of the object
        obj = obj.join(text)   # or the index of the obj (index starts from 1)
        if not to_buy_list.empty_list():
            dlt = to_buy_list.remove(obj)  # dlt is the name of the object removed
            message = dlt.capitalize() + " è stato rimosso."
        else:
            message = "La lista è vuota."
        bot.sendMessage(chat_id, message)
    elif command.lower() == "/addgarbage":
        house.set_garbage(True)
        message = "Hai aggiunto un sacco.\nOra ci sono " + str(house.there_is_garbage()) + " sacchi da buttare."
        bot.sendMessage(chat_id, message)
    elif command.lower() == "/remgarbage":
        house.set_garbage(False)
        message = "Avete buttato tutta la spazzatura. Bravi."
        bot.sendMessage(chat_id, message)
    elif command.lower() == "/garbage":
        message = "Ci sono " + str(house.there_is_garbage()) + " sacchi da buttare."
        bot.sendMessage(chat_id, message)
    # elif command.lower() == "/garbagealarm":
    #     message = "Ci sono " + str(house.there_is_garbage()) + " sacchi da buttare.\nButtateli."
    #    notify_all(house.get_hsm_all(), message)
    elif command.lower() == "/save":
        save(home)
        message = "Data saved."
        bot.sendMessage(chat_id, message)
    elif command.lower() == "/allhsm":
        hsm = house.get_hsm_all()
        message = "\n"
        message = message.join(hsm)
        bot.sendMessage(chat_id, message)
    elif command.lower() == "/allhsmuser":
        hsm_user = []
        for hsm in house.get_hsm_all():
            hsm_user.append(house.get_hsm_by_name(hsm).get_username())
        message = "\n"
        message = message.join(hsm_user)
        bot.sendMessage(chat_id, message)
    elif command.lower() == "/setusr":
        name = ""
        new_user = ""
        if len(text) > 2:
            name = " "
            name = name.join((text[0], text[1]))
            new_user = text[2]
        elif len(text) == 2:
            name = text[0]
            new_user = text[1]
        try:
            user = house.get_hsm_by_name(name).get_username()
            house.get_hsm_by_name(name).update_username(new_user)
            message = "Lo username di " + name + " è stato modificato da " + user + " a " + new_user
        except KeyError:
            message = name + " non è un coinquilino."
        bot.sendMessage(chat_id, message)
    # logfile.close()


def save(hm):  # saves data in a file
    pickle.dump(hm, open("save_load.data", "wb"))


def load():
    return pickle.load(open("save_load.data", "rb"))


def notify_round(hsm):  # notifies
    if hsm.get_username() is None:
        message = "Ehi " + hsm.get_name() + "! Oggi tocca a te!"
    else:
        message = "Ehi " + hsm.get_username() + "! Oggi tocca a te!"
    bot.sendMessage(hsm.get_id(), message)
    message = rounds.today_round(house)
    bot.sendMessage(hsm.get_id(), message)


def notify_all(hsm_list, msg):

    for hsm in hsm_list:
        try:
            bot.sendMessage(house.get_hsm_by_name(hsm).get_id(), msg)
        except KeyError:
            #pass
            print(hsm)


print("========== STARTED ==========")
# START BOT
bot = telepot.Bot(TOKEN)
# LOAD HOME DATA
print("Loading home data......", end=" ")
try:
    home = load()
    house = home.get_house()
    to_buy_list = home.get_lst()
except FileNotFoundError:
    home = Home()
    house = home.get_house()
    to_buy_list = home.get_lst()
print("Done!")
# LOAD ROUNDS DATA
print("Loading rounds data....", end=" ")
rounds = Round()
rounds.load()
print("Done!")

bot.message_loop(handle)
print("Listening..............\n")

# alarm flag = True --> alarm is activated
alarm_9am = True
alarm_2pm = True
alarm_7pm = True
# save flag = False --> data have to be saved
save_data = False
# garbage alarm flag = True --> there is garbage
alarm_garbage = False

while True:
    time.sleep(1)
    tma = int(time.strftime("%H", time.gmtime())) + 1
    # ROUND ALARM
    try:
        # gmtime() returns UTC times  --> UTC+1 is local time
        if rounds.is_round_day() and alarm_9am and tma == 9:
            notify_round(house.get_hsm_by_name(rounds.today()))
            alarm_9am = False
            alarm_7pm = True
        elif rounds.is_round_day() and alarm_2pm and tma == 14:
            notify_round(house.get_hsm_by_name(rounds.today()))
            alarm_2pm = False
            alarm_9am = True
        elif rounds.is_round_day() and alarm_7pm and tma == 19:
            notify_round(house.get_hsm_by_name(rounds.today()))
            alarm_7pm = False
            alarm_2pm = True
    except KeyError:
        pass
    # SAVE DATA
    if tma == 12 and not save_data:
        save(home)
        save_data = True
    elif tma == 13 and save_data:
        save_data = False
    elif tma == 22 and not save_data:
        save(home)
        save_data = True
    elif tma == 23 and save_data:
        save_data = False

    # GARBAGE ALARM
    if tma >= 10 and tma % 2 == 0 and alarm_garbage:
        message = "Ci sono " + house.there_is_garbage() + " sacchi da buttare.\nButtateli."
        notify_all(house.get_hsm_all(), message)
        alarm_garbage = False
    elif not alarm_garbage and house.there_is_garbage() > 0:
        alarm_garbage = False
