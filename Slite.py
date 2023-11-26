import telebot
import time
import sqlite3
from secret import Talker_API

bot = telebot.TeleBot(Talker_API)

print("hello")

@bot.message_handler(commands=['start'])
def main(message):
    conn = sqlite3.connect("ddb.sql")
    cur = conn.cursor()
    bot.send_message(message.chat.id, "Привет, 1")
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50), pass VARCHAR(50))')
    bot.send_message(message.chat.id, "Привет, 2")
    conn.commit()
    bot.send_message(message.chat.id, "Привет, 3")
    cur.close()
    bot.send_message(message.chat.id, "Привет, 4")
    conn.close()
    bot.send_message(message.chat.id, "Привет, 5")
    bot.register_next_step_handler(message, user_name)
    bot.send_message(message.chat.id, "Привет, 6")
    print('start')


def user_name(message):
     password = message.text.strip()

while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(5)