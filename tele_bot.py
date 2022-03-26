import telebot
import psycopg2

import tele_bot_config as bot_config

TELETOKEN = bot_config.tele_token_!nameAngelBot #!nameAngelBot
bot = telebot.TeleBot(TELETOKEN, parse_mode='MARKDOWN') # You can set parse_mode by default. HTML or MARKDOWN)

conndb = bot_config.db_creds
CONTROL_GROUP_ID = !groupchatid

target_id = None


# cursor.execute('INSERT INTO info VALUES(%s,%s,%s)', (name, username, id))

def initialise_db():
    db = psycopg2.connect(conndb)
    cursor = db.cursor()
    # cursor.execute('DROP TABLE IF EXISTS info')
    cursor.execute('''CREATE TABLE IF NOT EXISTS info(
    name TEXT,
    username TEXT,
    id BIGINT
    )''')
    db.commit()
    cursor.close()
    db.close()

def get_user_from_db():
    global target_id
    db = psycopg2.connect(conndb)
    cursor = db.cursor()
    cursor.execute('SELECT * FROM info')
    data = cursor.fetchall()
    db.commit()
    cursor.close()
    db.close()
    for user in data:
        if user[1] == '!username':
            target_id = user[2]
            # print('target from db', target_id)
            break

def user_to_db(message):
    db = psycopg2.connect(conndb)
    cursor = db.cursor()
    name = f'{message.chat.first_name}{message.chat.last_name}'
    username = f'{message.chat.username}'
    id = str(message.chat.id)
    cursor.execute('INSERT INTO info VALUES(%s,%s,%s)', (name, username, id))
    db.commit()
    cursor.close()
    db.close()


# @bot.message_handler(commands=['a'])
# def a(message):
#     print(message.text)
#     bot.reply_to(message, f'1')
#     # bot.reply_to(message, "Hey! Hows it going?")
#     bot.send_message(CONTROL_GROUP_ID, 'text1')
#     bot.send_message(!mychatid, 'text1')

@bot.message_handler(commands=['start'])
def start(message):
    # print(message.text)
    if message.text != '/start hello_!name':
        if target_id and message.chat.username == '!username':
            bot.reply_to(message, f'Hello !name! Setup is already complete, you dont need to use the link anymore. You can just send messages here normally like any other chat.')
        else:
            bot.reply_to(message, f'Sorry I dont know you! Use the link if you received one. :)')
    elif message.chat.username != '!usename':
        bot.reply_to(message, f'Sorry this wasnt meant for you!')
    elif target_id is None:
        user_to_db(message)
        get_user_from_db()
        bot.reply_to(message, f'Hello !name! This is your angel for !clubname !eventname planning committee! Hope you are doing well!')
        bot.send_message(CONTROL_GROUP_ID, f'bot reg: {message.chat.username}: {message.chat.id}')
        # print(message.chat.id)
    else:
        bot.reply_to(message, f'Hello !name! Setup is already complete, you dont need to use the link anymore. You can just send messages here normally like any other chat.')


@bot.message_handler(content_types=['text'])
def all(message):
    print('all text')
    if message.chat.id == CONTROL_GROUP_ID:
        if target_id:
            bot.send_message(target_id, f'{message.text}')
        else:
            bot.reply_to(message, f'not setup yet')
    elif message.chat.id == target_id:
        bot.send_message(CONTROL_GROUP_ID, f'{message.text}')
    # print(message.text)
    # print(message.chat.id)




print('=====START=====')
initialise_db()
print('db ready')
get_user_from_db()
print('started polling')
bot.polling()


# https://t.me/!nameAngelBot?start=hello_!name
