from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo

bot = Bot('')
dp = Dispatcher(bot)

print("hello")
link1 = "https://xd.adobe.com/view/58fface2-d5a1-4572-af02-5fac362d3fa4-0dac/"

persona = None

@dp.message_handler(commands=['start'])
async def start(message: types.Message): 
    await message.answer("Привет, здесь ты можешь выбрать персонажа и пообщаться с ним")

@dp.message_handler(commands=['menu'])
async def start(message: types.Message): 
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(types.KeyboardButton("Доступные персонажи", web_app=WebAppInfo(url=link1)))
    await message.answer("Нажми на кнопку - получишь результат", reply_markup=markup)

executor.start_polling(dp)
