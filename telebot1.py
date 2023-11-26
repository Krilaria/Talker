import g4f
from g4f.Provider import GeekGpt, Bing
import telebot
from telebot import types, TeleBot
import time
import datetime
from telebot.types import WebAppInfo
from secret import Talker_API

bot = TeleBot(Talker_API)
link1 = "https://xd.adobe.com/view/58fface2-d5a1-4572-af02-5fac362d3fa4-0dac/"
persona = None
before = ""

print("hello")

@bot.message_handler(commands=['start'])
def main(message):
    # Получаем текущее время
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Сообщение для сохранения в db.txt
    log_message = f"user id: {message.from_user.id}; username: {message.from_user.username}; name: {message.from_user.first_name}; surname: {message.from_user.last_name}; time: {current_time}"
    # Записываем сообщение в db.txt
    with open("db.txt", "a") as file:
        file.write(log_message + "\n")
    bot.send_message(message.chat.id, "Привет, здесь ты можешь выбрать персонажа и пообщаться с ним")

@bot.message_handler(commands=['menu'])
def main(message):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text="Альберт Эйнштейн", callback_data="einstein")
    btn2 = types.InlineKeyboardButton(text="Марио", callback_data="mario")
    kb.add(btn1, btn2)
    bot.send_message(message.chat.id, "Доступные персонажи", reply_markup=kb)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(types.KeyboardButton("Доступные персонажи", web_app=WebAppInfo(url=link1)))
    bot.send_message(message.chat.id, "Нажми на кнопку - получишь результат", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    global persona
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Сообщение для сохранения в db.txt
    log_message = f"Comand menu was used in {current_time} by user with id {call.from_user.id}. Choose {call.data}"
    # Записываем сообщение в db.txt
    with open("db.txt", "a") as file:
        file.write(log_message + "\n")

    if call.data == "einstein":
        # Обработка нажатия на кнопку "Альберт Эйнштейн"
        persona = "Альберт Эйнштейн"
        bot.send_message(call.message.chat.id, f"Приветствую вас, я - {persona}, пытаюсь понять природу времени!")
    elif call.data == "mario":
        # Обработка нажатия на кнопку "Марио"
        persona = "Марио из игры Super Mario"
        bot.send_message(call.message.chat.id, f"Привет-привет! Меня зовут Марио!")
    return(persona)

def chat(ask):
    global persona
    global before
    prep = before +  "Отвечай как будто ты" + persona + "и мы просто беседуем. Очень старайся не выходить из роли" + persona
    try:
        response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        provider=g4f.Provider.GeekGpt,
        messages=[{"role": "user", "content": prep + ask}])
        return(response)
    except:
        response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        provider=g4f.Provider.Bing,
        messages=[{"role": "user", "content": prep + ask}]) 
        return(response)
    
@bot.message_handler()
def gpt(message):
    start = time.time()
    global before
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Пред вопрос: ", before)
    print("Вопрос: ", message.text)
    answer = "Мне нечего сказать..."
    try:
        answer = chat(message.text)
    except:
        answer = "Мне нечего сказать..."
    bot.send_message(message.chat.id, answer)
    before = "В прошлый раз я сказал " + message.text
    log_message = f"Comand gpt was used in {current_time} by user with id {message.from_user.id}. Question: {message.text}. Answer: {answer}"
    with open("db.txt", "a") as file:
        file.write(log_message + "\n")
    finish = time.time()
    print(f"Ответ: {answer} Потрачено {round((float(finish) - float(start)), 1)} секунд")

while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            # logger.error(e)
            time.sleep(5)
